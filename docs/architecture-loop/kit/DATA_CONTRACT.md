# Artifact contract — version 1

The templates give top-level fields; `example/run/` gives populated records. Use
stable IDs and JSON types. The coordinator validates required structures and
references, not every possible field. Extra fields are permitted. This is a
human-readable contract, not a claim of full JSON Schema validation.

| Artifact | Record shape and meaning |
|---|---|
| brief.json | topic, decision, author, audiences[], as_of (YYYY-MM-DD), success_criteria[], constraints[], budgets, required_outputs[]; optional output_stem uses letters, numbers, underscores or hyphens |
| framing.json | context, problem, stakeholders[], in_scope[], out_of_scope[], invariants[], constraints[], terms{}, questions[], capabilities{}, explicit-context declarations |
| evidence.json | sources[], claims[], searches[], coverage[], stop_reason |
| decisions.json | criteria[], options[], records[], challenges[], assumptions[] |
| architecture.json | elements[], relationships[], views[], contracts[], scenarios[], operations{}, implementation[], sizing{} |
| story.json | thesis, tension, recommendation, decision_ask, running_example, glossary{}, beats[] |
| paper.md | First-person narrative; section anchors; claim/source markers; figure directives |
| slides.json | title, subtitle, slides[] with visible text, references and speaker notes |
| review.json | source_fingerprint, reviewer, mode, limitations[], checks{}, scores{}, findings[] |
| export.json | source_fingerprint and files[] containing path, format, sha256, inspected and inspection_notes |
| state.json | Coordinator-owned stage, status, budget counters and history; never edit to bypass the loop |

## Evidence

Each **source** has id (S1), title, url or local reference, publisher, accessed,
locator, summary, kind and retrieved (boolean). Add published/version and
limitations. `retrieved: true` is a report of actual retrieval, not permission
to assume a source exists.

Each **claim** has id (CL1), text, kind (fact/inference/proposal/assumption),
source_ids[], confidence, reason, verification, pivotal (boolean), and
time_sensitive (boolean). Facts require verified support from retrieved
sources. Inferences and assumptions also have could_change_if. A proposal does
not become a fact merely because it has citations.

Each **search** has the actual query or navigation, date, purpose (support or
disconfirm), and result. **Coverage** records question, answer, status
(answered/conditional/open), critical (boolean), and relevant claim_ids. A
critical open question blocks research; conditional answers must explicitly
limit the recommendation.

## Decisions

An **option** has id, name, baseline (boolean), benefit and cost. Compare at
least three. A **decision record** has id, question, selected_option, rationale,
tradeoffs[], claim_ids[], strongest_objection, reversal_trigger and
validation_plan. Each **challenge** references decision_id and contains attack,
falsifier, method, status (executed/planned/not_feasible), result, consequence,
blocks_decision and unresolved. An **assumption** contains statement, impact,
validation and owner. Prefer testable triggers over generic risk language.

## Architecture and diagrams

An **element** has id (safe identifier), name, type, description and status.
Types: person, external, system, container, component, code. Containers have a
system parent; components have a container parent; code has a component parent.
Containers/components include technology. Code includes code_ref and members[];
status must be implemented or proposed. Other status values are descriptive.

A **relationship** has id, source, target, label and protocol. A **view** has id
(V1), level (1–4), title, scope, nodes[], edges[], legend and caption. The
selected parent must be visible at the preceding level. C3 describes one
container and C4 one component. Use multiple views for additional selected
scopes. Display IDs as stable identifiers, not changing titles.

Layout is optional: size [width,height]; positions maps each node to
[x,y,width,height]; routes maps an edge to a list of [x,y] polyline points;
label_positions maps an edge to [x,y]. Coordinates use SVG pixels with origin
at top left. Avoid node or label overlap. The default grid is a starting point,
not a substitute for inspection. `diagrams.py` writes a model hash into each
SVG/Mermaid file, so registry changes require regeneration.

Contracts have id, producer, consumer, payload, errors, idempotency and
authorization; add schema/version, timeout and examples when material.
Scenarios have id, kind (success/failure) and steps[]. Operational fields
explain ownership, state, recovery, security and lifecycle rather than merely
naming desirable qualities.

## Paper, story and slides

Use `<!-- section:context -->` before a paper section. Cite `[CL1]` for a claim
and `[S1]` for a source. These markers support traceability; full source
references must also be present in the paper. CL avoids confusion with C1,
the first diagram level. Insert a figure on its own line as `[Figure:V1]`.

A **story beat** has id, takeaway, paper_section, slide_ids[], claim_ids[],
decision_ids[] and view_ids[]. Every slide belongs to a beat whose section and
claims agree. Every slide claim appears in its mapped paper section. The
semantic reviewer still checks whether the wording preserves the meaning.

A **slide** has id (P1), title, takeaway, paper_section, claim_ids[],
speaker_notes and view_ids[]. The supplied renderer accepts either one view,
up to three cards ({heading,body}), or bullets[]. It uses native editable
PowerPoint shapes for both text and diagrams. Keep card bodies to six short
wrapped lines. Use one diagram per slide. The core gate permits richer host
renderers, but the same reference and inspection requirements still apply.

## Review and export

Review modes: single_model, isolated_session, separate_model or human. These
describe how review was performed; none automatically guarantees independence
or correctness. If the brief requires independent review, single_model cannot
pass. Do not invent reviewer identities.

Every semantic check contains pass (boolean) and evidence (an artifact-specific
explanation). Every score contains score (0–4) and evidence. Findings should
include id, severity (critical/high/medium/low), location, evidence, remediation
and status (open/resolved/accepted). High and critical findings must be resolved.

The fingerprint comes from `loop.py fingerprint RUN`. Record it after reviewing
those exact bytes. Exports list relative paths confined to the run directory.
Set inspected only after actual inspection and record its limits. A proxy PDF
does not prove PowerPoint-engine rendering. Ready means ready for user review,
not published, approved for deployment or independently validated.
