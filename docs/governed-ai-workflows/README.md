# Governed AI Workflows and the Future of Software Delivery

A reference architecture and implementation blueprint. Version 2.0, 3 October 2026.

- [Read the publication (PDF)](Agent_Orchestration_Architecture_White_Paper.pdf)
- [Read online (Markdown)](whitepaper.md)
- [Editable Word document](Agent_Orchestration_Architecture_White_Paper.docx)

The 52-page paper contains 42 design sections, nine diagrams and 36 references. It explains component responsibilities, contracts and wiring, durable execution, selective delegation, governed memory, authorization, recovery, independent evaluation and controlled improvement. It includes implementation contracts, a staged roadmap, the path beyond dedicated CI/CD tools, and a fair two-week replication challenge with explicit rules for retiring custom components. Research findings, engineering proposals and unproven hypotheses are distinguished throughout.

This is a proposed architecture supported by reviewed public evidence. It is not a deployed reference implementation or proof of a universally best architecture. Product capabilities and proposed integration responsibilities are distinguished throughout.

## Source and reproduction

`whitepaper.md` is the manuscript. `figures/` contains PNG and SVG diagrams. `build_publication.py` regenerates the figures and Word document using the packages in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
python build_publication.py
```

Export the Word document to PDF using Word or LibreOffice and inspect all pages. Layout depends on fonts and the rendering application. The checked-in PDF is the reviewed publication artifact. HTML page-break comments in the manuscript control Word pagination.

The JSON contracts are illustrative interface examples, not vendor SDK schemas. Source references and research limitations are included in the manuscript.
