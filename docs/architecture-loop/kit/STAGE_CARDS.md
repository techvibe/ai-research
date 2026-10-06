# Stage task cards

These cards define roles as passes. Follow PROTOCOL.md and the current brief.

## FRAME
Role: problem framer. Read brief.json; create framing.json. Define decision, context, readers, outcomes, invariants, constraints by type, boundaries, terms, questions, assumptions and tool capabilities. Explain all context explicitly. Fix vague success criteria. Ask only questions that block a useful decision. Check the frame gate; then advance.

## RESEARCH
Role: researcher. Read framing.json. Create evidence.json from sources actually retrieved. Use primary evidence, precise locators, support scope, dates and versions. Search both for and against the initial hypothesis. Decompose pivotal statements into claim IDs; distinguish facts, inferences, proposals and assumptions. Record coverage and a defensible stopping reason. Unavailable research is a limitation, not permission to invent it. Check research; then advance.

## CHALLENGE
Role: skeptical decision analyst. Read the brief and evidence before reading any favored recommendation. Create decisions.json. Compare baseline, simplest viable option and a materially different option using declared criteria. State strongest objections and reversal triggers. Attempt to disprove every pivotal recommendation; record actual tests separately from plans. Revise research when necessary. Check challenge; then advance.

## DESIGN
Role: architect. Derive components from capabilities and invariants. Create architecture.json using the template and the example. Establish IDs and parent scopes before drawing. Include C1/C2/C3/C4, concrete contracts, state ownership, failure recovery, operations, sizing assumptions and implementation increments. Code views must reference real symbols or be labeled proposed. Run diagrams.py; inspect all views. Add runtime success/failure sequences if they clarify the design. Check design; then advance.

## STORY
Role: narrative architect. Create story.json. State one defensible thesis, the causal tension, the recommendation and decision ask. Map each beat to paper section, slide IDs, claims, decisions and diagrams. Define a running example and glossary. Test whether the strongest limitation changes the opening recommendation. Check story; then advance.

## DRAFT
Role: first-person author and presentation designer. Write paper.md and slides.json from the shared records. Use section anchors and [CL1]/[S1] evidence references; note that CL-prefixed evidence IDs are claim IDs, while diagram levels are named C1–C4 in captions. Embed figures using [Figure:V1]. Every slide maps to a section and claims, with speaker notes; all C4 views appear in both artifacts. Explain unfamiliar concepts before depending on them. Keep conditions and uncertainty visible. Check draft; then advance.

## REVIEW
Role: critic, source checker and newcomer reader. Review actual artifacts against the eight semantic checks in review.json and the rubric in PROTOCOL.md. Do not treat your own generated citations or mappings as proof. Inspect cited source passages. Try to reverse the recommendation. Trace one running example through every level. Audit the deck against the paper and figures. Resolve critical/high issues through revise; only then record the current fingerprint, reviewer mode, evidence-specific checks, scores and limitations. Check review; then advance.

## EXPORT
Role: publication producer. Render paper PDF and editable PowerPoint with notes using render.py or host tools. Inspect real files for clipping, diagram labels, citations, notes and contradictory simplification. If no PowerPoint-compatible renderer is available, state exactly which structural checks and layout proxy were used. Keep required unavailable inspection incomplete if it is a condition of the brief. Populate export.json with source fingerprint, each exact file hash and honest inspection notes. Run check and advance. Return files and outstanding limitations; ready_for_user_review is not publishing authority.
