# Safety Boundaries

## Privacy

Default to local-first. The progress screen may contain project brief text and local artifact paths, so treat it as a local project artifact unless the user approves publication.

Never include:

- API keys, tokens, passwords, recovery codes;
- cookies, storage state, `.env` values;
- private screenshots or private URLs without explicit approval;
- raw provider payloads from Stitch, Figma, SERP tools, analytics, ads, CRM, or hosting panels.

## Honesty

Bootstrap mode may only claim that the request was accepted, the project folder was created, and planning started. It must not imply that research, design, validation, Stitch, Figma, launch, or implementation has run.

Do not show a step as complete unless canonical status and evidence support it.

Use honest labels:

- `Ran`: command or check really ran and artifact exists.
- `Skipped`: intentionally skipped with reason.
- `Planned`: planned but not executed.
- `Manual`: requires human inspection or external action.

## Mutation Boundary

The progress screen must not silently mutate project state. It can collect or copy feedback, but durable changes must go through:

- `design-feedback-collector` for comments and decision status;
- `task-plan-v2-orchestrator` for task status changes;
- `project-wiki-manager` for sanitized project memory.

## Publication Boundary

Do not publish progress pages by default. They may reveal local paths, project assumptions, or draft work. If publication is requested, create a sanitized export first.
