# Architecture Loop

A portable research and architecture workflow that produces a first-person paper and an aligned slide deck from shared evidence, decisions, and C4 views.

Start with **START_HERE.md**. The fastest path is to give that file and this folder to your coding agent. The host agent supplies intelligence and tools; this kit supplies the process, durable records, structural checks, and rendering utilities. It has no model-vendor dependency or API key requirement of its own.

## What is included

| File | Purpose |
|---|---|
| START_HERE.md | Copyable master prompt and resume prompt |
| PROTOCOL.md | First-principles method, evidence rules, disconfirmation, C4 and writing requirements |
| STAGE_CARDS.md | Exact task and exit requirements for each stage |
| templates/ | Brief, structured records, paper, slides, review and export templates |
| DATA_CONTRACT.md | Field-level record contract and diagram layout instructions |
| adapters/ | Thin Claude Code, GitHub Copilot and generic integration instructions |
| loop.py + gates.py | Resumable coordinator and cumulative structural checks; Python 3.10+ |
| diagrams.py | Generate editable Mermaid and rendered SVG from the architecture registry |
| render.py | Optional PDF/PPTX renderer; requires reportlab and python-pptx |
| example/ | Worked example about this loop, including its C1–C4 architecture, paper, and slides |
| test_loop.py | Regression tests for consequential gate and state-machine failures |
| SOURCES.md | Primary sources used to inform this kit |
| VALIDATION.md | What was verified and what remains unverified |

## Run it

Run commands from the extracted kit folder. On Windows, `py` may replace `python3`.

1. Copy `templates/brief.json` to `my-brief.json`; fill in the topic and decision. The master prompt can have the host do this.
2. Initialize a new run:

```bash
python3 loop.py init runs/my-topic --brief my-brief.json
python3 loop.py prompt runs/my-topic
```

3. Give the emitted prompt to the host agent. It reads and updates the run files. With shell access, the host can operate the loop itself. After each stage:

```bash
python3 loop.py check runs/my-topic
python3 loop.py advance runs/my-topic
python3 loop.py prompt runs/my-topic
```

4. At design, generate views from the shared registry:

```bash
python3 diagrams.py runs/my-topic
```

5. At review, obtain the current fingerprint and record it **after** performing the review:

```bash
python3 loop.py fingerprint runs/my-topic
```

6. At export, either use the host's document/presentation tools or the optional renderer:

```bash
python3 render.py runs/my-topic
```

The renderer creates PDF, PPTX, a deck preview PDF, and an export manifest with `inspected: false`. Inspect the actual outputs, write accurate inspection notes, and set the flags only when warranted. Then check and advance. The optional renderer is deliberately simple; the host may use a richer renderer without changing the artifact contract.

Install the optional renderer dependencies into your usual isolated Python environment if absent:

```bash
python3 -m pip install reportlab python-pptx
```

The coordinator and SVG/Mermaid generation do not require those packages.

## Change, resume, and stop

Before editing an already-reviewed upstream artifact:

```bash
python3 loop.py revise runs/my-topic --to research --reason "The vendor source no longer supports claim CL3"
```

This saves a snapshot, increments the revision count, and reopens research. Downstream files remain for editing and comparison; they are not silently regenerated. The host must update them before proceeding. The final fingerprint prevents an unchanged review stamp from approving changed canonical files.

```bash
python3 loop.py status runs/my-topic
python3 loop.py block runs/my-topic --reason "Primary evidence unavailable for the decisive latency claim"
python3 loop.py resume runs/my-topic --reason "Primary measurement now supplied"
```

Default budgets: 3 revision cycles and 24 issued stage prompts. These are tunable operating limits, not research-backed optimums. Rejected checks do not consume prompt budget; the host must also stop repeated local retries after two unsuccessful repairs and record a blocker. Time, token, and monetary limits belong to the host, because a vendor-neutral file coordinator cannot enforce invisible API usage. Do not edit state to evade a limit. Start a new scoped run after agreeing a revised budget.

## Operating modes

| Host capability | Mode | Honest completion claim |
|---|---|---|
| Agent + research + files + shell + renderer | Host runs all stages | Ready for user review when all gates and inspections pass |
| Agent + files, limited research | Research supplied through approved documents | Conditional draft if pivotal current facts remain unverified |
| Chat only | Paste the master prompt; exchange named artifact blocks | Text workflow only; checks and binary exports are unverified |
| Different host mid-run | Open the same run folder and use the resume prompt | Continue from current files and recheck the last checkpoint |

“Any environment” means the workflow and records are portable. It does not imply every host can browse, execute Python, render PowerPoint, or invoke a separate reviewer. Adapters are instruction conventions, not tested vendor integrations. “Barcode copilot” was interpreted as GitHub Copilot; the generic instructions cover other tools.

## What the checks establish

The runner checks IDs, references, stage prerequisites, required alternatives, declared falsification work, C4 nesting, diagram presence, traceability, basic first-person wording, review freshness, and export signatures/hashes. It rejects absent or malformed records. It does **not** determine whether research is true, whether a source actually entails a claim, whether a reviewer is honest, whether slides are persuasive, or whether a system will succeed in production. Those require substantive review and, where relevant, experiments.

The files and coordinator are a local collaboration mechanism. An agent with unrestricted filesystem access could change the checks, records, or state. They are not a tamper-proof governance boundary. Use separate permissions and a protected approval service if you need independently enforced release authority.

Run one writer per run directory. Atomic replacement protects individual state writes, but this version has no cross-process locking or transactional multi-file edits. Do not run concurrent coordinators against the same folder.

## Example

The example explains **this loop itself**, so you can inspect a complete paper/slide/diagram relationship before applying it to your own topic. It uses first-person authorial language without attributing invented work experience to you. Its prototype tests validate local mechanics, not end-to-end model quality or real Claude Code/Copilot sessions. Read VALIDATION.md for the exact boundary.
