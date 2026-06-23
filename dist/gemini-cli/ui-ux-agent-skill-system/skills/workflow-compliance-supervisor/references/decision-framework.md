# Decision Framework

## First Question

What did the system promise the user?

Use the declared journey, usually from `data/journey-registry.json`, not a loose recollection of the conversation.

## Second Question

What did the system actually do?

Use:
- `TASK-PLAN.md`;
- `progress-state.json`;
- `agent-progress-screen.html`;
- reports and screenshots;
- `workflow-log.jsonl`;
- accepted manual checks.

## Decision Order

1. If continuing risks privacy, legality, production safety, or core journey integrity, choose `block`.
2. If user facts, approval, credentials, budget, or production confirmation are missing, choose `pause_for_user`.
3. If a stage is claimed done without evidence, choose `return_to_rework`.
4. If a stage is intentionally outside scope, choose `skip_with_reason`.
5. If evidence is sufficient, choose `continue`.

## Accepted Skip Reasons

- `out_of_scope_demo`
- `user_not_approved_external`
- `missing_user_data`
- `tool_unavailable`
- `service_bug`
- `not_required_for_selected_mode`
- `user_accepted_skip`

## Rejected Skip Reasons

- `model_convenience`
- `time_saving_without_user_notice`
- `implicit_assumption`
- `tool_not_called_but_marked_done`
- `planned_counted_as_ran`

