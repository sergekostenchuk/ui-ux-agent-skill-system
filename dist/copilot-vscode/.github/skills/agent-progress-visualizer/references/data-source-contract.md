# Data Source Contract

`agent-progress-visualizer` renders a view over other artifacts. It must not create a competing source of truth.

## Canonical Inputs

- `project-request.json`: bootstrap source before `TASK-PLAN.md` exists; stores the accepted user request, project root, declared journey, and privacy mode.
- `workflow-log.jsonl`: append-only event log for request acceptance, reasons, evidence, and next actions; exists from bootstrap onward.
- `TASK-PLAN.md`: task ids, titles, status, dependencies, owner roles, approval gates, verification state, artifact paths.
- `progress-state.json`: derived machine-readable state for HTML rendering.
- `reports/`: validation evidence, generated summaries, screenshots, audit outputs.
- `feedback/`: user choices, user comments, agent critique status, accepted/applied decisions.
- `wiki/`: sanitized durable decisions and project context.

## Output Artifacts

- `project-request.json`: immediate request acceptance record, only for bootstrap.
- `progress-state.json`: derived state.
- `agent-progress-screen.html`: customer-facing HTML view.
- `reports/progress-validation-summary.txt`: consistency and privacy validation.

## Update Events

Regenerate progress artifacts when any of these changes:

- bootstrap request is accepted and project folder is created;
- `TASK-PLAN.md` is created after bootstrap;
- task status, owner, dependency, or approval field changes;
- a user gate opens, closes, or changes status;
- a design variant, preview, report, screenshot, or validation artifact is created;
- feedback is accepted, partially accepted, rejected, or applied;
- wiki capture records a new accepted decision.

## Status Mapping

| Task-plan status | Progress status | Customer meaning |
| --- | --- | --- |
| `draft`, `ready` | `planned` | Впереди |
| `in_progress` | `running` | Идет прямо сейчас |
| `needs_review` | `waiting_user` | Нужно посмотреть или подтвердить |
| `blocked` | `blocked` | Есть блокер |
| `approved`, `done` | `done` | Готово |
| `dropped` | `skipped` | Пропущено |

## Drift Rule

Before `TASK-PLAN.md` exists, `project-request.json` and `workflow-log.jsonl` define only the bootstrap state.

If `TASK-PLAN.md`, `progress-state.json`, and `agent-progress-screen.html` disagree, Markdown wins. Fix the parser/generator or task-plan metadata, then regenerate JSON and HTML.
