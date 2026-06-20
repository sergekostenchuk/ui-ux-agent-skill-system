# UI/UX Agent Skill System for GLM / Z.ai

Primary entrypoint: `senior-ui-ux-orchestrator`.

Role rule: the orchestrator is the chair. Specialist skills provide input or execute bounded stages. They do not override the orchestrator's final decision.

Safety rule: local-first by default. Do not store or print secrets. External services require explicit approval.

Use `skills-index.md` to choose relevant skill files.
