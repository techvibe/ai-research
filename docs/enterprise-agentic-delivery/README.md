# Enterprise Agentic Delivery — research and architecture package

6 October 2026 · Version 1.0

The proposal tests whether a separate enterprise control-plane product is necessary. It recommends starting with an approved harness and existing controls, then adding shared contracts and durable coordination only for demonstrated gaps.

## Contents

- [White paper (PDF)](Enterprise_Agentic_Delivery_White_Paper.pdf): complete first-person, standalone paper.
- [Read online / editable paper](Enterprise_Agentic_Delivery_White_Paper.md): primary-source ledger and Mermaid diagrams.
- [Editable presentation](Enterprise_Agentic_Delivery_Slides.pptx): presentation with speaker notes.
- [Presentation preview (PDF)](Enterprise_Agentic_Delivery_Slides.pdf): rendered presentation for easy viewing.
- [C1–C4 diagrams](diagrams/): PNG and editable SVG; Mermaid source is in the paper.
- [Portable research prompt](Portable_Research_Architecture_Prompt.md): provider-neutral research/design loop to adapt or extend the work.
- [Validation report](VALIDATION.md): completed artifact checks and limitations.
- [Complete download](Enterprise_Agentic_Delivery_Package.zip): publication and editable sources.

Open the paper for detailed contracts, failure behavior, roadmap gates and disconfirmation experiments. The deck follows the same argument and terminology. Use the portable prompt with your chosen environment and provide its actual constraints.

This is a documentation-grounded proposal, not a built or production-validated platform. Product claims are a dated snapshot. Resolve deployment-specific procurement, policy, operational requirements and benchmark results before production adoption.

## Reproduction

Use Python 3.12 with the versions in `requirements.txt`, the DejaVu Sans/Mono fonts under `/usr/share/fonts/truetype/dejavu/`, and LibreOffice for slide PDF export.

```bash
python -m pip install -r requirements.txt
python render_deliverables.py
libreoffice --headless --convert-to pdf --outdir . Enterprise_Agentic_Delivery_Slides.pptx
```

The renderer generates the white paper PDF, native editable PowerPoint diagrams, publication diagrams and speaker-note manifest. The source Markdown contains the complete narrative and reference ledger. Refresh product evidence before adapting the architecture for an implementation decision.
