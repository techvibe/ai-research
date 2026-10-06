# Primary sources informing the kit

Accessed 6 October 2026. These sources support the stated conventions and design
patterns; the specific workflow, gates, scripts and defaults are this kit's design.
Documentation may change. Recheck adapters when the host changes.

1. C4 model, [Diagrams](https://c4model.com/diagrams): the four static structure levels. The model does not require all levels for every system; this kit includes them because the user requested them.
2. C4 model, [System context](https://c4model.com/diagrams/system-context): people, the system in scope and external systems.
3. C4 model, [Containers](https://c4model.com/diagrams/container): applications and data stores within a system; deployment is a separate concern.
4. C4 model, [Components](https://c4model.com/diagrams/component): decomposition within one selected container.
5. C4 model, [Code](https://c4model.com/diagrams/code): implementation elements within a selected component; real code references are preferred for existing implementations.
6. C4 model, [Notation](https://c4model.com/diagrams/notation): notation independence, scope, titles, element types, legends and directed relationships.
7. Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 19 December 2024: composable workflow patterns, including evaluation followed by revision. This is a conceptual influence, not evidence that this kit improves outcomes.
8. Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 9 January 2026: using different kinds of graders and assessing actual outcomes. This informs the separation of structural checks and semantic review.
9. Anthropic, [How Claude remembers your project](https://code.claude.com/docs/en/memory): project instruction files. The adapter uses CLAUDE.md and explicit prompt fallback.
10. GitHub, [Adding repository custom instructions in your IDE](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/configure-custom-instructions/add-repository-instructions-in-your-ide): repository instruction conventions, including .github/copilot-instructions.md. Verify support in the selected host.

No claim is made that the workflow is universally accepted, the most advanced
available, or independently benchmarked. Its effectiveness should be tested
against a simpler baseline on the user's own briefs.
