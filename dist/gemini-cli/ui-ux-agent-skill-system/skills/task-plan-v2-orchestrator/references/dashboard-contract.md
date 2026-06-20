# Dashboard Contract

Keep HTML as a visual layer over Markdown.

## Source Of Truth

- `TASK-PLAN.md` is canonical
- `TASK-DASHBOARD.html` is derived
- if both exist and disagree, Markdown wins

## Minimum Fields Needed For Reliable Dashboard Rendering

Every task block should expose at least:
- `task_id`
- `title`
- `status`
- `priority`
- `owner_role`
- `agent_sequence`
- `dependencies`
- `blocked_by`
- `required_approvals`
- `tests_required`
- `test_levels`
- `test_targets`
- `test_data_origin`
- `oracle`
- `commands_planned`
- `acceptance_checks`
- `commands_run`
- `artifact_locations`
- `timebox`
- `active_alarm_ids` or equivalent unresolved alarm field

These minimum fields unlock:
- kanban by status
- dependency graph
- critical path view
- owner or role view
- test gate view
- review gate view
- verification/governance warning view
- unresolved mock/placeholder alarm view

## Good Dashboard Views

### 1. Task Board

Columns:
- `draft`
- `ready`
- `in_progress`
- `blocked`
- `needs_review`
- `approved`
- `done`

### 2. Dependency Graph

Nodes:
- task id
- short title
- status

Edges:
- `dependencies`

### 3. Critical Path View

Highlight:
- tasks with no slack
- blockers that gate multiple downstream tasks

### 4. Agent Occupancy View

Show:
- current `owner_role`
- next role in `agent_sequence`
- tasks waiting on approval

### 5. Verification View

Show:
- tasks with `tests_required: yes`
- required test levels
- planned commands
- executed commands
- test targets
- oracle
- flakiness risk
- missing artifacts
- stop-on-failure status

### 6. Governance Warning View

Show warnings for:
- `ready`, `in_progress`, `approved`, or `done` tasks with critical `TBD` fields
- `done` tasks with `tests_required: yes` but no `commands_run`
- `done` tasks with `tests_required: yes` but no `test_artifacts`
- tasks with `commands_planned` populated but `commands_run` empty after tester phase
- `blocked` tasks without explicit `blocked_by`
- Task Register and Task Block status mismatch
- owner_role mismatch between Task Register, Task Block, and execution state
- active mock alarms
- active placeholder alarms
- alarms that do not explain `missing_to_replace`
- alarms present in the task block but missing from runtime projection metadata

## Regeneration Rule

Preferred flow:
1. edit Markdown
2. parse normalized task blocks
3. regenerate HTML

Avoid:
- patching HTML by hand while leaving Markdown stale
- extracting meaning from loose prose paragraphs

## Parsing Guidance

Prefer these structures:
- stable Markdown headings per task
- `key: value` lines
- flat bullet lists

Avoid:
- deeply nested prose
- inconsistent task headings
- changing field names across tasks

## Optional Dashboard Metadata

If you need richer visual output, add these optional fields:
- `current_gate`
- `last_updated`
- `last_decision`
- `latest_review_artifact`
- `latest_test_artifact`
- `health`
- `governance_issues`
- `verification_state`
- `active_alarms`
- `resolved_alarms`

## Safe Fallback

If no generator exists yet:
- keep the dashboard optional
- first normalize `TASK-PLAN.md`
- add a small "dashboard-ready" note rather than inventing a brittle HTML layer
