# Architecture Loop

Version 1.0 · 6 October 2026

A portable research and architecture workflow for producing a defensible first-person paper and a cohesive slide deck from shared evidence, decisions, and C4 views.

## Downloads

| File | Purpose |
|---|---|
| [Architecture_Loop_Kit.zip](Architecture_Loop_Kit.zip) | Complete portable kit, templates, source, tests and worked example |
| [Architecture_Loop_Start_Here.md](Architecture_Loop_Start_Here.md) | Copyable master prompt and resume prompt |
| [Architecture_Loop_Example_Paper.pdf](Architecture_Loop_Example_Paper.pdf) | 11-page example explaining the loop and its C1–C4 architecture |
| [Architecture_Loop_Example_Slides.pptx](Architecture_Loop_Example_Slides.pptx) | 15 editable slides with speaker notes |
| [Architecture_Loop_Example_Slides_Preview.pdf](Architecture_Loop_Example_Slides_Preview.pdf) | PDF layout preview of the deck |

## Use from this repository

Open [kit/](kit/README.md) in your agent environment, read [START_HERE.md](kit/START_HERE.md), and supply your architecture topic and decision. The host supplies the model, research and authoring tools; the kit supplies durable records, stage tasks, checks and rendering utilities.

For the supplied completed example, run from the repository root:

```bash
cd docs/architecture-loop/kit
python3 loop.py check example/run
python3 -m unittest -v test_loop.py
```

For a new topic, follow the [quick start](kit/README.md) and use a new run directory. The core coordinator needs Python 3.10+; optional publication rendering dependencies are listed in [requirements-render.txt](kit/requirements-render.txt).

## What the loop requires

First-principles problem framing; explicit assumptions; primary-source research; credible alternatives; decision-specific attempts at disconfirmation; C1 context, C2 containers, C3 components and C4 code views; one story map linking the paper and slides; first-person authorial voice without invented experience; substantive review; bounded revision; and honest output inspection.

## Sources and validation

- [Operating protocol](kit/PROTOCOL.md)
- [Artifact contract](kit/DATA_CONTRACT.md)
- [Primary sources](kit/SOURCES.md)
- [Validation record and limitations](kit/VALIDATION.md)
- [Readable example paper source](kit/example/run/paper.md)
- [Evidence ledger](kit/example/run/evidence.json)
- [Diagram sources and SVG views](kit/example/run/diagrams/)

Seventeen local regression tests passed. Real Claude Code/Copilot sessions and comparative improvements in publication quality have not been established. The paper was rendered and inspected as PDF. The PowerPoint was checked structurally and through the shared-layout PDF preview; a native PowerPoint rendering engine was unavailable. The full limitations are retained in the validation record.

