# Generic adapter

No native integration is required. Open the kit in your agent's workspace and
paste START_HERE.md. Ask it to read the protocol and run files directly. If it
cannot read files, attach the protocol and exchange one named artifact at a time.

Expose only capabilities already permitted by your host: retrieve sources,
read/write scoped files, execute approved local tools, and render documents.
The adapter contract is files and commands, not a proprietary API. If switching
hosts, transfer the run folder including evidence, diagrams, reviews and state.

The host implements the agent loop: read current stage → plan its work → use
tools → inspect actual results → write records → check/advance or revise → repeat.
The local runner is a coordinator, not an autonomous model service.
