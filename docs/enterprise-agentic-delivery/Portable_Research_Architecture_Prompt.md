# Portable research and architecture loop

Copy the block below into an approved coding or research environment. Supply the outcome and constraints. The loop works with one agent; use additional agents only when the environment and user authorize them. File paths and tool availability are host-specific.

---

Act as my research architect and technical author. Build a first-person, standalone white paper and a matching presentation for the outcome below. Complete the work and validate the deliverables; do not stop at a proposed outline. Use first principles, critical thinking and active disconfirmation. Treat the reference architecture as a hypothesis rather than a required answer.

OUTCOME: [Describe the enterprise outcome and question to resolve.]
AUDIENCE: [Default: engineering leaders, architects and implementation teams.]
KNOWN CONTEXT: [Only facts supplied or independently verified.]
CONSTRAINTS: [Data locality, approved vendors, existing tools, authority, budget and deadlines. Mark unknowns explicitly.]
DELIVERABLES: white paper PDF and editable source; presentation with speaker notes; C1–C4 diagrams and editable diagram source; evidence/decision ledger; practical value-gated roadmap; final unresolved questions.

Start with a short progress update and a work plan. Ask for missing information only if it changes the decision materially; proceed with reversible research and document conditional assumptions. Never invent employer facts, current product capabilities, measurements or approvals.

Maintain six compact registers in files: assumptions, sources/claims, requirements/owners, alternatives/decisions, experiments/results, and unresolved questions. Give decisions and requirements stable identifiers. Update the existing records after each iteration instead of recreating the project from chat memory.

Run the following bounded loop:

1. **Frame.** Define the intended outcome, audience, terms, acceptance criteria, scope, exclusions, consequences and missing facts. Explain the context so a new reader can understand it without earlier conversations. Put every necessary assumption in the register with the effect if false.
2. **Research.** Verify time-sensitive claims using primary documentation and maintained repositories. Distinguish documented capability, vendor marketing, measured result, inference and your proposal. Open supporting sources; do not rely on snippets alone. Record URL, access date, source date/version when known, supported claim and uncertainty. Reconcile contradictory sources rather than silently choose the convenient one.
3. **Derive.** Remove product names and derive needed functions from outcomes, authority, evidence, external effects, interruption, observation and recovery. Identify what existing systems already supply. Include a conventional-script or single-agent alternative when plausible.
4. **Compare.** Build at least three alternatives, including reuse of existing infrastructure, a thin federated integration, and fuller orchestration only if justified. Compare simplicity, cost, operating burden, recoverability, trust boundaries, coupling, locality and enterprise fit. Do not award a universal “best” title without representative evidence.
5. **Disconfirm.** For every major recommendation, give its strongest objection, a realistic counterexample, and observations that would change it. Test whether multi-agent coordination adds value; whether an extra control-plane product adds value; whether native vendor state already covers recovery; whether memory or incumbent replacement is needed. Do not count model agreement as independent verification.
6. **Specify.** Define stable outcome, evidence and action contracts where appropriate. Map authority and state ownership. Bind evidence to exact revisions/artifacts and environments. Bind privileged actions to scope, identity, policy, preconditions, operation identity, expiry and reconciliation. Do not claim universal exactly-once effects across arbitrary external systems.
7. **Model.** Produce C1 system context, C2 containers, C3 components inside one named C2 container, and C4 types/interfaces inside one named C3 component. Use one consistent glossary and interface map. C4 means code-level structure, not a fourth infrastructure plane. Distinguish conversation context isolation from filesystem, network and credential isolation.
8. **Exercise.** Walk through successful delivery and failures: duplicate events, lost responses after successful writes, stale workers, expired approvals, missing telemetry, policy outages, cancellation with in-flight effects, evidence invalidation, prompt injection and memory contamination. State what is prevented, detected, reconciled, escalated or unrecoverable.
9. **Stage.** Define stages that each deliver useful outcomes and may stand alone. For each stage give what changes, what is reused, ownership, dependencies, acceptance evidence, proposed metrics, stopping criteria and reversal route. Label illustrative targets; do not fabricate schedules or ROI.
10. **Write.** Write in first person as the architectural author. Separate sourced facts from judgment. Explain acronyms, mechanisms, examples, limits and tradeoffs in ordinary language. Tell a cohesive story from problem and challenged assumptions through alternatives, selected design, implementation and evidence. Do not assume the reader saw this prompt.
11. **Present.** Derive the deck from the paper. Keep conclusion, component names, diagrams, stage numbers, metrics and caveats identical. Use claim-led titles, readable diagrams, restrained slide density and useful speaker notes. Cite product claims and provide a full source ledger.
12. **Review and repair.** Review source support, contradictions, architectural nesting, authority bypasses, state ownership, recovery, economics, narrative and file readability. Verify that every proposed component has a demonstrated role. Remove unjustified components. Validate PDF text/layout and slide rendering. Record remaining uncertainties honestly.

Use no more than three full design/review iterations unless a material failure requires another within the agreed budget. A repair must state what evidence changed the design. Stop when acceptance passes, a hard budget is reached, or an unresolved fact prevents a trustworthy answer. Deliver completed artifacts and identify the exact blocker if one remains. Never fabricate a test run or production readiness.

Keep progress updates concise and regular. Preserve work in the environment's authorized durable storage and provide accessible artifact links. Do not publish, deploy, merge, message people, or perform privileged production changes unless the user has authorized that action. Research and artifact creation do not imply operational authorization.

FINAL RESPONSE: state the architectural conclusion in a few sentences, link the paper and presentation, list the most consequential limitation, and provide the editable package. Include no implementation chronology.

---

This prompt is provider-neutral. Its loop is a specification for research and design behavior, not a guarantee of tool access, enterprise authority, native session portability, or reliable external action execution.
