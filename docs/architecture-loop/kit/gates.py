"""Structural gates for Architecture Loop. They do not establish factual truth."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

STAGES = ("frame", "research", "challenge", "design", "story", "draft", "review", "export")
CANONICAL = ("brief.json", "framing.json", "evidence.json", "decisions.json",
             "architecture.json", "story.json", "paper.md", "slides.json")


@dataclass
class Finding:
    code: str
    path: str
    message: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ReviewStamp:
    source_fingerprint: str
    reviewer: str
    mode: str

    def matches(self, store: "ArtifactStore") -> bool:
        return self.source_fingerprint == store.fingerprint()


class ArtifactStore:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def path(self, relative):
        p = (self.root / relative).resolve()
        if not p.is_relative_to(self.root):
            raise ValueError("Artifact paths must remain inside the run directory")
        return p

    def read(self, relative):
        return json.loads(self.path(relative).read_text(encoding="utf-8"))

    def text(self, relative):
        return self.path(relative).read_text(encoding="utf-8")

    def fingerprint(self):
        paths = list(CANONICAL)
        paths += sorted(str(p.relative_to(self.root)) for p in self.root.glob("diagrams/*")
                        if p.suffix in (".mmd", ".svg"))
        digest = hashlib.sha256()
        for name in paths:
            p = self.path(name)
            digest.update(name.encode() + b"\0")
            digest.update(p.read_bytes() if p.exists() else b"MISSING")
            digest.update(b"\0")
        return digest.hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class GateEngine:
    """Cumulative validation, returning findings instead of silently passing."""
    def __init__(self, root):
        self.store = ArtifactStore(root)
        self.findings = []

    def require(self, condition, code, path, message):
        if not condition:
            self.findings.append(Finding(code, path, message))

    def load(self, name):
        return self.store.read(name)

    def ids(self, rows, path):
        ids = [r.get("id") for r in rows]
        self.require(all(ids) and len(ids) == len(set(ids)), "unique_ids", path,
                     "Every record needs a unique, nonempty id")
        return set(ids)

    def fields(self, obj, fields, path):
        for key in fields:
            self.require(bool(obj.get(key)), "required", path, f"Missing or empty: {key}")

    def references(self, values, ids, path):
        self.require(set(values).issubset(ids), "unknown_reference", path,
                     f"Unknown references: {sorted(set(values) - ids)}")

    def check(self, stage):
        self.findings = []
        if stage == "ready":
            stage = "export"
        if stage not in STAGES:
            return [Finding("stage", "state.json", "Unknown stage")]
        for item in STAGES[:STAGES.index(stage) + 1]:
            try:
                getattr(self, "_" + item)()
            except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
                self.findings.append(Finding("invalid_artifact", item, str(exc)))
        return self.findings

    def _frame(self):
        b, f = self.load("brief.json"), self.load("framing.json")
        self.fields(b, ("topic", "decision", "audiences", "author", "as_of", "success_criteria"), "brief.json")
        date.fromisoformat(b["as_of"])
        self.fields(f, ("context", "problem", "stakeholders", "in_scope", "out_of_scope",
                        "invariants", "terms", "questions", "capabilities"), "framing.json")
        self.require(f.get("reader_context_explained") is True, "context", "framing.json",
                     "Explicitly explain reader context")
        self.require(f.get("assumptions_explicit") is True, "assumptions", "framing.json",
                     "Record unknowns and conditional assumptions")

    def _research(self):
        b, e = self.load("brief.json"), self.load("evidence.json")
        sources, claims = e["sources"], e["claims"]
        source_ids = self.ids(sources, "evidence.sources")
        self.ids(claims, "evidence.claims")
        self.require(bool(claims), "claims", "evidence.json", "At least one claim is required")
        source_map = {s["id"]: s for s in sources}
        for s in sources:
            self.fields(s, ("title", "url", "publisher", "accessed", "locator", "summary", "kind"), s["id"])
            date.fromisoformat(s["accessed"])
        for c in claims:
            self.fields(c, ("text", "kind", "confidence", "reason", "verification"), c["id"])
            self.references(c.get("source_ids", []), source_ids, c["id"])
            self.require(c["kind"] in ("fact", "inference", "proposal", "assumption"),
                         "claim_kind", c["id"], "Use fact, inference, proposal, or assumption")
            if c["kind"] == "fact":
                self.require(bool(c.get("source_ids")), "unsupported_fact", c["id"], "Facts need sources")
                self.require(c["verification"] == "verified", "unverified_fact", c["id"],
                             "Unverified facts must be qualified or removed")
                for sid in c.get("source_ids", []):
                    if sid in source_map:
                        self.require(source_map[sid].get("retrieved") is True,
                                     "unread_source", c["id"], f"Source {sid} was not retrieved")
            if c.get("time_sensitive") and c["kind"] == "fact":
                ages = [(date.fromisoformat(b["as_of"]) - date.fromisoformat(source_map[s]["accessed"])).days
                        for s in c.get("source_ids", []) if s in source_map]
                self.require(bool(ages) and all(0 <= n <= b.get("freshness_days", 30) for n in ages),
                             "freshness", c["id"], "Recheck time-sensitive evidence against the as-of date")
            if c["kind"] in ("inference", "assumption"):
                self.fields(c, ("could_change_if",), c["id"])
        self.require(bool(e.get("searches")), "search_log", "evidence.json", "Record actual search activity, including failures")
        self.require(any(s.get("purpose") == "disconfirm" for s in e.get("searches", [])),
                     "countersearch", "evidence.json", "Record at least one contrary-evidence search")
        self.require(bool(e.get("coverage")), "coverage", "evidence.json", "Define research coverage")
        for row in e.get("coverage", []):
            self.fields(row, ("question", "answer", "status"), "evidence.coverage")
            self.require(not(row.get("critical") and row["status"] == "open"),
                         "coverage_gap", "evidence.coverage", "Critical unknown must be resolved or explicitly constrain the recommendation")
        self.fields(e, ("stop_reason",), "evidence.json")

    def _challenge(self):
        d, e = self.load("decisions.json"), self.load("evidence.json")
        cid = {c["id"] for c in e["claims"]}
        opts = d["options"]
        oid = self.ids(opts, "decisions.options")
        self.require(len(opts) >= 3, "alternatives", "decisions.json", "Compare baseline, simple option, and proposed option")
        self.require(any(o.get("baseline") for o in opts), "baseline", "decisions.json", "Include a baseline")
        self.fields(d, ("criteria", "records", "challenges"), "decisions.json")
        did = self.ids(d["records"], "decisions.records")
        for rec in d["records"]:
            self.fields(rec, ("question", "selected_option", "rationale", "tradeoffs", "claim_ids",
                              "strongest_objection", "reversal_trigger", "validation_plan"), rec["id"])
            self.references([rec["selected_option"]], oid, rec["id"])
            self.references(rec["claim_ids"], cid, rec["id"])
        for challenge in d["challenges"]:
            self.fields(challenge, ("decision_id", "attack", "falsifier", "method", "status", "result", "consequence"), "challenge")
            self.references([challenge["decision_id"]], did, "challenge")
            self.require(challenge["status"] in ("executed", "planned", "not_feasible"),
                         "test_status", "challenge", "Distinguish performed tests from plans")
            self.require(not (challenge.get("blocks_decision") and challenge.get("unresolved")),
                         "unresolved_challenge", "challenge", "A decision-blocking challenge remains open")
        covered = {x["decision_id"] for x in d["challenges"]}
        self.require(did.issubset(covered), "challenge_coverage", "decisions.json", "Challenge every pivotal decision")
        for a in d.get("assumptions", []):
            self.fields(a, ("statement", "impact", "validation", "owner"), "assumption")

    def _design(self):
        a = self.load("architecture.json")
        elems, rels, views = a["elements"], a["relationships"], a["views"]
        eid = self.ids(elems, "architecture.elements")
        rid = self.ids(rels, "architecture.relationships")
        self.ids(views, "architecture.views")
        emap = {el["id"]: el for el in elems}
        valid_parents = {"container": "system", "component": "container", "code": "component"}
        for el in elems:
            self.fields(el, ("name", "type", "description", "status"), el["id"])
            if el["type"] in valid_parents:
                self.require(emap.get(el.get("parent"), {}).get("type") == valid_parents[el["type"]],
                             "c4_parent", el["id"], "Invalid C4 parent hierarchy")
            if el["type"] in ("container", "component"):
                self.fields(el, ("technology",), el["id"])
            if el["type"] == "code":
                self.fields(el, ("code_ref", "members"), el["id"])
                self.require(el["status"] in ("implemented", "proposed"), "code_status", el["id"], "Label code as implemented or proposed")
        for rel in rels:
            self.fields(rel, ("label", "protocol"), rel["id"])
            self.references([rel["source"], rel["target"]], eid, rel["id"])
        rmap = {r["id"]: r for r in rels}
        levels = {v["level"] for v in views}
        self.require({1, 2, 3, 4}.issubset(levels), "c4_levels", "architecture.views", "C1, C2, C3 and C4 are required")
        for v in views:
            self.fields(v, ("title", "scope", "nodes", "legend", "caption"), v["id"])
            self.references(v["nodes"], eid, v["id"])
            self.references(v.get("edges", []), rid, v["id"])
            scope_type = {1: "system", 2: "system", 3: "container", 4: "component"}.get(v["level"])
            self.require(emap.get(v["scope"], {}).get("type") == scope_type, "c4_scope", v["id"], "Wrong abstraction for the selected scope")
            if v["level"] > 1:
                self.require(any(v["scope"] in parent_view["nodes"] for parent_view in views if parent_view["level"] == v["level"] - 1),
                             "c4_continuity", v["id"], "Selected scope must be visible in the preceding C4 level")
            permitted = {1: {"person", "system", "external"}, 2: {"person", "container", "external"},
                         3: {"person", "component", "container", "external"}, 4: {"code"}}.get(v["level"], set())
            for node in v["nodes"]:
                el = emap.get(node, {})
                self.require(el.get("type") in permitted, "c4_mixed_level", v["id"], f"Wrong abstraction: {node}")
                primary = {2: "container", 3: "component", 4: "code"}.get(v["level"])
                if el.get("type") == primary:
                    self.require(el.get("parent") == v["scope"], "c4_zoom", v["id"], f"{node} is outside the selected parent")
            for edge in v.get("edges", []):
                rel = rmap.get(edge, {})
                self.require({rel.get("source"), rel.get("target")}.issubset(set(v["nodes"])),
                             "diagram_endpoint", v["id"], "Diagram edge has a missing endpoint")
            for suffix in (".mmd", ".svg"):
                diagram_path = self.store.path("diagrams/" + v["id"] + suffix)
                self.require(diagram_path.is_file(),
                             "diagram_file", v["id"], f"Missing generated {suffix}")
                if diagram_path.is_file():
                    self.require(file_hash(self.store.path("architecture.json")) in diagram_path.read_text(encoding="utf-8"),
                                 "stale_diagram", v["id"], "Regenerate views after architecture model changes")
        self.fields(a, ("contracts", "scenarios", "operations", "implementation", "sizing"), "architecture.json")
        for row in a["contracts"]:
            self.fields(row, ("id", "producer", "consumer", "payload", "errors", "idempotency", "authorization"), "contract")
            self.references([row["producer"], row["consumer"]], eid, row["id"])
        self.require(any(s.get("kind") == "failure" for s in a["scenarios"]),
                     "failure_path", "architecture.scenarios", "Include a failure and recovery sequence")

    def _story(self):
        s, e, d, a = (self.load(p) for p in ("story.json", "evidence.json", "decisions.json", "architecture.json"))
        self.fields(s, ("thesis", "tension", "recommendation", "decision_ask", "beats", "glossary"), "story.json")
        self.ids(s["beats"], "story.beats")
        for beat in s["beats"]:
            self.fields(beat, ("takeaway", "paper_section", "slide_ids", "claim_ids"), beat["id"])
            self.references(beat["claim_ids"], {x["id"] for x in e["claims"]}, beat["id"])
            self.references(beat.get("decision_ids", []), {x["id"] for x in d["records"]}, beat["id"])
            self.references(beat.get("view_ids", []), {x["id"] for x in a["views"]}, beat["id"])

    def _draft(self):
        paper = self.store.text("paper.md")
        slides = self.load("slides.json")["slides"]
        story, arch, ev = (self.load(p) for p in ("story.json", "architecture.json", "evidence.json"))
        slide_ids = self.ids(slides, "slides.json")
        self.require(bool(re.search(r"\bI (?:propose|recommend|argue|define|use|choose|conclude)\b", paper)),
                     "first_person", "paper.md", "Use first-person authorial voice")
        self.require(not re.search(r"\b(?:TODO|TBD|FIXME)\b|\[INSERT", paper, re.I),
                     "placeholder", "paper.md", "Remove unresolved placeholders")
        sections = set(re.findall(r"<!-- section:([A-Za-z0-9_-]+) -->", paper))
        chunks = re.split(r"<!-- section:([A-Za-z0-9_-]+) -->", paper)
        section_text = {chunks[i]: chunks[i+1] for i in range(1, len(chunks)-1, 2)}
        vids = {v["id"] for v in arch["views"]}
        cids = {c["id"] for c in ev["claims"]}
        sids = {s["id"] for s in ev["sources"]}
        self.references(re.findall(r"\[(CL\d+)\]", paper), cids, "paper.md")
        self.references(re.findall(r"\[(S\d+)\]", paper), sids, "paper.md")
        for beat in story["beats"]:
            self.require(beat["paper_section"] in sections, "section_map", beat["id"], "Mapped paper section missing")
            self.references(beat["slide_ids"], slide_ids, beat["id"])
        shown = set()
        for slide in slides:
            self.fields(slide, ("id", "title", "takeaway", "paper_section", "speaker_notes", "claim_ids"), slide["id"])
            self.require(slide["paper_section"] in sections, "slide_section", slide["id"], "Slide references missing paper section")
            self.references(slide["claim_ids"], cids, slide["id"])
            mappings = [b for b in story["beats"] if slide["id"] in b["slide_ids"]]
            self.require(bool(mappings), "unmapped_slide", slide["id"], "Every slide must belong to a story beat")
            self.require(any(b["paper_section"] == slide["paper_section"] and set(slide["claim_ids"]).issubset(set(b["claim_ids"])) for b in mappings),
                         "story_slide_mismatch", slide["id"], "Story beat and slide disagree on section or claim coverage")
            for cid in slide["claim_ids"]:
                self.require(f"[{cid}]" in section_text.get(slide["paper_section"], ""),
                             "slide_claim_section", slide["id"], f"{cid} is not traceable in the mapped paper section")
            self.references(slide.get("view_ids", []), vids, slide["id"])
            shown.update(slide.get("view_ids", []))
        for view in arch["views"]:
            self.require(f"[Figure:{view['id']}]" in paper and view["id"] in shown,
                         "diagram_coverage", view["id"], "Every C4 view must appear in paper and slides")
        for claim in ev["claims"]:
            if claim.get("pivotal"):
                self.require(f"[{claim['id']}]" in paper, "pivotal_claim", claim["id"], "Pivotal claim is not traceable in the paper")

    def _review(self):
        r = self.load("review.json")
        stamp = ReviewStamp(r["source_fingerprint"], r["reviewer"], r["mode"])
        self.require(stamp.matches(self.store), "stale_review", "review.json", "Artifacts changed after review; review current bytes")
        self.require(r["mode"] in ("single_model", "isolated_session", "separate_model", "human"),
                     "review_mode", "review.json", "Declare reviewer independence accurately")
        brief = self.load("brief.json")
        if brief.get("require_independent_review"):
            self.require(r["mode"] != "single_model", "independence", "review.json", "Independent review required by brief")
        self.fields(r, ("limitations", "checks", "scores"), "review.json")
        required = ("source_entailment", "first_person_integrity", "standalone_reader", "alternatives_fair",
                    "disconfirmation_substantive", "architecture_feasible", "paper_slide_consistency", "diagrams_readable")
        for check in required:
            row = r["checks"].get(check, {})
            self.require(row.get("pass") is True and bool(row.get("evidence")), "semantic_review", check,
                         "Record result and artifact-specific evidence")
        for score in ("evidence", "reasoning", "architecture", "clarity", "cohesion"):
            row = r["scores"].get(score, {})
            self.require(isinstance(row.get("score"), int) and 3 <= row["score"] <= 4 and bool(row.get("evidence")),
                         "quality_score", score, "Require at least 3/4 with evidence; scores are reviewer judgments")
        for f in r.get("findings", []):
            self.require(not(f.get("severity") in ("critical", "high") and f.get("status") != "resolved"),
                         "review_blocker", f.get("id", "finding"), "High/critical findings must be resolved")

    def _export(self):
        out = self.load("export.json")
        self.require(out["source_fingerprint"] == self.store.fingerprint(), "stale_export", "export.json", "Re-export after source changes")
        types = set()
        for f in out["files"]:
            p = self.store.path(f["path"])
            self.require(p.is_file() and p.stat().st_size > 0, "output_missing", f["path"], "Missing export")
            if not p.is_file():
                continue
            self.require(file_hash(p) == f["sha256"], "output_hash", f["path"], "Export changed after inspection")
            if f["format"] == "pdf":
                self.require(p.read_bytes().startswith(b"%PDF-"), "pdf_format", f["path"], "Not a PDF")
            elif f["format"] == "pptx":
                try:
                    with zipfile.ZipFile(p) as z:
                        self.require("ppt/presentation.xml" in z.namelist(), "pptx_format", f["path"], "Not a PowerPoint presentation")
                except zipfile.BadZipFile:
                    self.require(False, "pptx_format", f["path"], "Not a PowerPoint presentation")
            self.require(f.get("inspected") is True and bool(f.get("inspection_notes")),
                         "visual_inspection", f["path"], "Inspect actual rendered output; record limitations")
            types.add(f["format"])
        required = self.load("brief.json").get("required_outputs", ["pdf", "pptx"])
        self.require(set(required).issubset(types), "required_outputs", "export.json", "Required export format is missing")
