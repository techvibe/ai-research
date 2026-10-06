# Validation record

Version 1.0 · 6 October 2026

## Verified in this environment

- Python compilation succeeded for the supplied modules.
- **17 regression tests passed.** TEST_RESULTS.txt contains the actual unittest output. They cover unread or unsupported facts, malformed JSON, absent code views, invalid C4 parents and zoom continuity, stale diagrams/reviews, unmapped or inconsistent slides, missing exports, confined artifact paths, blocked transitions, snapshots and prompt/revision limits.
- The worked example passes cumulative structural gates from framing through export. It is a populated demonstration run, not a transcript of a live Claude Code or Copilot session.
- The renderer produced an **11-page paper PDF**, **15-slide PowerPoint** and **15-page slide preview PDF**. The PowerPoint contains native editable text and diagram shapes, plus speaker notes on every slide.
- Every C4 view appears in both publications. Diagram scopes trace from the Loop system to the Runner container, Gates component and four actual Python classes in gates.py.
- The paper/deck claim and section mappings were checked. An early unmatched slide claim was found by the gate and corrected before release.
- All pages were inspected through rendered contact sheets, with detailed inspection of all four architecture views. Text and shape bounds were checked for page/slide overflow. A diagram boundary and overly long node text were corrected.
- Source definitions and instruction-file conventions were checked against the primary references listed in SOURCES.md. The example distinguishes proposals and inferences from verified documentation facts.

## Scope of inspection

The PDF was inspected as an actual rendered PDF. The PowerPoint was inspected
structurally, including slide count, editable shapes, bounds, notes and its ZIP/XML
package. Its visual layout was inspected through a PDF generated from the same
layout operations. **No PowerPoint or LibreOffice rendering engine was available.**
That PDF is a layout proxy, not proof that every presentation viewer will render
identically. DejaVu Sans is used; a viewer may substitute a font if it is absent.
Mermaid text sources were generated, but a Mermaid engine was not available to
parse them. The SVGs were rendered directly by the supplied publication renderer.

## Not yet established

- End-to-end operation in actual Claude Code and selected GitHub Copilot sessions.
- Quantified improvement in architecture decisions, publication quality or total effort.
- Independent human or separate-model review of the worked example. Review mode is single_model.
- Enterprise security enforcement, concurrent writer safety, hostile-agent resistance or production service levels.

The test suite checks local mechanics. It cannot establish source truth,
substantive architectural correctness, or honest review declarations. A useful
next evaluation is a matched comparison against a human checklist on several
representative briefs, using separate readers and predefined acceptance criteria.

## Reproduce

From the extracted kit folder:

```bash
python3 -m unittest -v test_loop.py
python3 loop.py check example/run
```

Rendering requires the optional dependencies. requirements-render.txt records
the exact versions used here. Rerendering rewrites the export manifest with
inspection flags cleared; inspect the new files before declaring them ready.
