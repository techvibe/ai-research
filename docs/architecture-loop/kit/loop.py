#!/usr/bin/env python3
"""Model-neutral, file-based coordinator. Python 3.10+; standard library only."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from gates import GateEngine, ArtifactStore, STAGES

KIT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_state(root):
    return json.loads((root / "state.json").read_text(encoding="utf-8"))


def emit_prompt(root, state):
    stage = state["stage"]
    card = (KIT / "STAGE_CARDS.md").read_text(encoding="utf-8")
    marker = "## " + stage.upper() + "\n"
    selected = card.split(marker, 1)[1].split("\n## ", 1)[0]
    print(f"ARCHITECTURE LOOP | stage={stage} | run={root}\n")
    print("Read START_HERE.md and PROTOCOL.md in the kit. Follow host permissions.\n")
    print(selected)
    print("\nState:\n" + json.dumps(state, indent=2))
    print("\nRead current run artifacts from disk. Do not rely on earlier chat memory.")
    print("When the stage is complete, run check, then advance. Correct reported gaps;")
    print("if an earlier decision changes, use revise BEFORE editing it. Never edit state.json.")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init", help="Create a new run without overwriting files")
    init.add_argument("run")
    init.add_argument("--brief", required=True)
    for name in ("status", "prompt", "check", "advance", "fingerprint"):
        s = sub.add_parser(name)
        s.add_argument("run")
    r = sub.add_parser("revise", help="Snapshot current work and reopen an earlier stage")
    r.add_argument("run")
    r.add_argument("--to", required=True, choices=STAGES)
    r.add_argument("--reason", required=True)
    b = sub.add_parser("block", help="Record an unresolved blocker honestly")
    b.add_argument("run")
    b.add_argument("--reason", required=True)
    u = sub.add_parser("resume", help="Resume a blocked run after the cause is addressed")
    u.add_argument("run")
    u.add_argument("--reason", required=True)
    args = p.parse_args(argv)
    root = Path(args.run).resolve()
    try:
        if args.cmd == "init":
            brief_path = Path(args.brief).resolve()
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            if root.exists():
                raise ValueError("Run directory already exists; choose a new path")
            root.mkdir(parents=True)
            for src in (KIT / "templates").iterdir():
                if src.name != "brief.json" and src.is_file():
                    shutil.copy2(src, root / src.name)
            write_json(root / "brief.json", brief)
            for name in ("diagrams", "output", "snapshots"):
                (root / name).mkdir()
            state = {"version": 1, "stage": "frame", "status": "running", "created": now(),
                     "revision": 0, "prompts_issued": 0, "max_revisions": brief.get("max_revisions", 3),
                     "max_prompts": brief.get("max_prompts", 24), "history": [], "reason": ""}
            write_json(root / "state.json", state)
            print(json.dumps(state, indent=2))
            return 0
        state = load_state(root)
        if args.cmd == "status":
            print(json.dumps(state, indent=2)); return 0
        if args.cmd == "fingerprint":
            print(ArtifactStore(root).fingerprint()); return 0
        if args.cmd == "check":
            issues = GateEngine(root).check(state["stage"])
            print(json.dumps({"stage": state["stage"], "pass": not issues,
                              "findings": [f.to_dict() for f in issues]}, indent=2))
            return int(bool(issues))
        if args.cmd == "block":
            state.update(status="blocked", reason=args.reason)
        elif args.cmd == "resume":
            if state["status"] != "blocked":
                raise ValueError("Only a blocked run can be resumed")
            if state["prompts_issued"] >= state["max_prompts"]:
                raise ValueError("Prompt budget exhausted; close the run and agree a new scoped run")
            state.update(status="running", reason=args.reason)
        elif args.cmd == "revise":
            current = len(STAGES) if state["stage"] == "ready" else STAGES.index(state["stage"])
            if STAGES.index(args.to) > current:
                raise ValueError("Revision cannot skip forward")
            if state["revision"] >= state["max_revisions"]:
                state.update(status="blocked", reason="Revision budget exhausted: " + args.reason)
                write_json(root / "state.json", state)
                print(json.dumps(state, indent=2)); return 2
            dest = root / "snapshots" / f"revision-{state['revision']:02d}"
            if dest.exists():
                raise ValueError("Snapshot already exists; refusing to overwrite history")
            shutil.copytree(root, dest, ignore=shutil.ignore_patterns("snapshots", "__pycache__"))
            state["revision"] += 1
            state.update(stage=args.to, status="running", reason=args.reason)
            state["history"].append({"event": "revise", "to": args.to, "reason": args.reason, "at": now()})
        else:
            if state["status"] != "running":
                raise ValueError("Run is not running; inspect status or revise/resume with a reason")
            if args.cmd == "prompt":
                if state["prompts_issued"] >= state["max_prompts"]:
                    state.update(status="blocked", reason="Prompt budget exhausted")
                    write_json(root / "state.json", state)
                    print(json.dumps(state, indent=2)); return 2
                state["prompts_issued"] += 1
                write_json(root / "state.json", state)
                emit_prompt(root, state); return 0
            if args.cmd == "advance":
                issues = GateEngine(root).check(state["stage"])
                if issues:
                    print(json.dumps({"pass": False, "findings": [f.to_dict() for f in issues]}, indent=2))
                    return 1
                state["history"].append({"event": "pass", "stage": state["stage"], "at": now(),
                                         "fingerprint": ArtifactStore(root).fingerprint()})
                i = STAGES.index(state["stage"]) + 1
                state["stage"] = STAGES[i] if i < len(STAGES) else "ready"
                if state["stage"] == "ready":
                    state["status"] = "ready_for_user_review"
        write_json(root / "state.json", state)
        print(json.dumps(state, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
