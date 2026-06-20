# TASK-PLAN v2 Field Layers

Use English field names for consistency. Narrative text can be English or Russian.

## 1. Pre-Implementation Layer

This layer exists before task decomposition. Its job is to prove the feature is ready to be turned into tasks.

Store it in `FEATURE-PREPARATION.md` or in a dedicated top section of `TASK-PLAN.md`.

Use [`../assets/FEATURE-PREPARATION-CHECKLIST.md`](../assets/FEATURE-PREPARATION-CHECKLIST.md) as the default scaffold.

Hard rule:
- if the pre-implementation layer is incomplete, implementation tasks stay `draft` or `blocked`
- do not mark them `ready` only because there is a rough idea or a UI mock

## 2. Feature-Level Fields

These fields describe the whole feature or initiative.

| Field | Purpose | Notes |
| --- | --- | --- |
| `feature_id` | Stable feature identifier | Add if the plan spans many tasks |
| `feature_title` | Canonical feature name | Prefer a short, stable name |
| `rationale` | Why the feature exists | Product-level why |
| `priority` | Global priority | `P0-P3` or project equivalent |
| `status` | Feature status | Separate from per-task status |
| `goal` | End-state to achieve | Measurable if possible |
| `scope_in` | Included surface | Keep concrete |
| `scope_out` | Explicit non-goals | Prevent drift |
| `changed_subsystems` | High-level impacted subsystems | Broad list |
| `constraints` | Global constraints | Technical, product, compliance |
| `assumptions` | Working assumptions | Mark shaky ones explicitly |
| `open_questions` | Unknowns needing resolution | Keep finite and actionable |
| `risks` | Delivery or design risks | Broad risks |
| `regression_risks` | Known regression vectors | Call out user-visible breakage |
| `security_privacy_notes` | Security/privacy framing | Data handling, auth, secrets |
| `non_functional_requirements` | Reliability/perf/UX constraints | Keep testable where possible |
| `milestones` | Feature milestones | Milestone list, not task list |
| `timebox` | Overall time window | Use dates or iteration names |
| `wiki_pages_to_read_before` | Required knowledge inputs | Read before planning |
| `wiki_pages_to_update_after` | Pages to sync after delivery | Update after completion |
| `wiki_facts_to_capture` | Facts that must be written back | Decisions, caveats, exact paths |
| `wiki_do_not_store` | Facts excluded from wiki | Secrets, personal data, ephemeral noise |

## 3. Execution Governance Layer

This layer defines what is forbidden during execution and what must be true before a task can progress.

Keep it near `Execution Policy` in `TASK-PLAN.md`.

| Field | Purpose | Notes |
| --- | --- | --- |
| `mode` | Execution stance | Recommended: `CODE-FIRST, NO-FICTION, ONE-TASK-ONLY` |
| `no_fiction_policy` | Prevent invented facts | Missing critical input returns `INVALID_INPUT` |
| `placeholder_policy` | Control `TBD` and placeholders | `TBD` allowed only while task is `draft` |
| `prompt_policy` | Enforce one-task prompt discipline | Prompt must include `RESUME_FROM` and `verification_strategy` |
| `code_first_policy` | Prevent docs-only closure for implementation work | Docs-only closure only for docs-governance tasks |
| `done_policy` | Closure contract | Dependencies, approvals, tests, evidence, rollback, sync |
| `commit_policy` | Commit/hash discipline | Verify hashes and keep implementation/docs evidence distinct |
| `sync_audit_policy` | Register/block consistency | Task Register and Task Block must agree |
| `boundary_audit_policy` | Scope and forbidden area enforcement | Scope violations block or reopen |
| `rollback_policy` | Revert/forward-fix/reopen rules | Failed checks cannot jump directly to done |
| `timeout_escalation_policy` | Timebox and stuck-loop handling | Escalate stale `in_progress` or exhausted review loops |
| `mock_policy` | Forbid silent mocks and fake integrations | Temporary mocks require alarms |
| `placeholder_policy` | Forbid silent placeholders in execution-ready work | Temporary placeholders require alarms |
| `alarm_propagation_policy` | Force unresolved alarms into every downstream context | Prompt, projection, handoff, dashboard |

Recommended hard rules:
- `ready`, `in_progress`, `approved`, and `done` are forbidden if critical fields are `TBD`.
- Placeholder evidence, placeholder tests, and placeholder artifact paths are forbidden.
- `done` is invalid if required tests were not run or if required artifacts are missing.
- `Task Register` and detailed task block must stay synchronized.
- Mocks, stubs, fake backends, dummy outputs, or placeholder integrations are forbidden by default.
- If a mock or placeholder is temporarily unavoidable, it must be recorded as an active alarm with an explicit replacement path.

## 4. Task-Level Fields

These fields live inside each normalized task block.

| Field | Purpose | Notes |
| --- | --- | --- |
| `task_id` | Stable task identifier | Required |
| `title` | Task title | Local title, not feature title |
| `rationale` | Why this task exists | Must support feature rationale |
| `priority` | Task priority | Can differ from feature priority |
| `status` | Task status | Keep enum finite |
| `dependencies` | Tasks this task waits on | Direct dependencies only |
| `blocked_by` | Active blockers | Dependencies or external blockers |
| `unblocks` | Tasks enabled by this task | Downstream tasks |
| `task_size` | Relative size | `XS/S/M/L/XL` or equivalent |
| `decomposition_rule` | How far to split | Example: "split if touches 3+ subsystems" |
| `milestones` | Local milestones | For large tasks only |
| `timebox` | Task-level window | Can be tighter than feature timebox |
| `goal` | Concrete task outcome | What must be true when done |
| `scope_in` | Files or behavior included | Keep operational |
| `scope_out` | Explicit exclusions | Prevent accidental expansion |
| `changed_subsystems` | Impacted subsystems | Narrower than feature-level list |
| `candidate_files` | Likely edit targets | Not a hard limit by itself |
| `forbidden_areas` | Areas that must not be changed | Hard boundary |
| `constraints` | Task-local constraints | Runtime, tooling, policy |
| `assumptions` | Task-local assumptions | Inputs you are betting on |
| `open_questions` | Open issues for this task | If unresolved, keep task not-ready |
| `risks` | Local delivery risks | Narrow to this task |
| `regression_risks` | User-visible regression risk | Specific to touched surface |
| `security_privacy_notes` | Local security or privacy notes | Especially for data-moving tasks |
| `non_functional_requirements` | Task-level NFRs | Example: latency, offline safety |
| `acceptance_criteria` | Human-readable success conditions | Must be testable |
| `acceptance_checks` | Concrete acceptance checks | Higher-level than raw test commands |
| `exit_criteria` | Gate to leave the task | Stronger than "code written" |
| `rollback_plan` | Backout path | Must be explicit for risky work |
| `active_alarm_ids` | Alarm ids still unresolved for this task | Keep empty when none exist |
| `resolved_alarm_ids` | Alarm ids resolved during this task | Useful for audit/history |

Recommended task status enum:
- `draft`
- `ready`
- `in_progress`
- `blocked`
- `needs_review`
- `approved`
- `done`
- `dropped`

## 5. Agent-Level Fields

Use these fields per task. Default orchestration is sequential.

| Field | Purpose | Notes |
| --- | --- | --- |
| `owner_role` | Current task owner | Exactly one active owner |
| `agent_sequence` | Ordered execution roles | Example: planner -> implementer -> reviewer -> tester -> docs-sync |
| `agent_contracts` | Per-agent handoff contracts | Keep explicit blocks |
| `required_approvals` | Named approvals or gate owners | Role-based, not person-only |
| `max_review_loops` | Maximum review correction cycles | Must be finite |
| `escalation_rule` | What happens if stuck | Include who decides and when |

Recommended default sequence:
1. `planner`
2. `implementer`
3. `reviewer`
4. `tester`
5. `docs_sync`

### Agent Contract Shape

Use one contract block per agent:

```md
##### A1
agent_id: A1
role: planner
entry_criteria:
- feature prep complete
- dependencies resolved
input_artifacts:
- FEATURE-PREPARATION.md
- TASK-PLAN.md
steps:
- refine task scope
- freeze candidate files
output_artifacts:
- updated task block
- handoff notes
handoff_to: A2
approval_gate:
- design-review
stop_conditions:
- missing dependency
- unresolved open question
```

## 6. Verification Strategy Fields

These fields are planned before implementation. The planner owns them first, the reviewer validates them, and the tester executes them.

| Field | Purpose | Notes |
| --- | --- | --- |
| `tests_required` | Whether tests are mandatory | `yes`, `no`, or `manual-check-needed` with rationale |
| `test_levels` | Test level list | `unit`, `integration`, `e2e`, `smoke`, `manual-check-needed` |
| `test_targets` | Exact targets to test | Modules, APIs, UI flows, media outputs, contracts |
| `test_data_origin` | Source of test data | Synthetic, fixture, recorded, user sample, generated |
| `fixtures` | Fixture paths or generators | Must be stable and allowed to modify or read |
| `oracle` | How success is judged | Snapshot, numeric threshold, status code, DOM assertion, waveform metric, invariant |
| `negative_tests` | Failure-path tests | Required for risky user-visible flows |
| `determinism_notes` | Determinism constraints | Seeds, clock mocking, stable order, network stubs |
| `flakiness_risk` | Known instability vector | Async UI, sidecar startup, network APIs, model output variability |
| `stop_on_failure` | Pipeline policy | If `true`, red required tests block handoff to docs_sync |
| `commands_planned` | Commands planned before coding | Filled by planner/reviewer before implementer starts |
| `commands_run` | Commands actually executed | Filled only after real execution |

Hard rules:
- Do not copy `commands_planned` into `commands_run` unless the command was actually executed.
- `oracle` must be concrete. "Works" or "looks okay" is not an oracle.
- If a critical verification field is unknown, keep the task `draft` or `blocked`.
- If `tests_required: no`, explain why in `oracle` or `acceptance_checks`.

## 7. Execution And Reporting Fields

These fields capture executed evidence and reporting after work is performed.

| Field | Purpose | Notes |
| --- | --- | --- |
| `commands_run` | Commands actually executed | Record facts, not intentions |
| `expected_artifacts` | All expected outputs | Code, tests, reports, docs |
| `code_artifacts` | Code outputs | Commits, files, PRs |
| `test_artifacts` | Test outputs | Logs, reports, screenshots |
| `review_artifacts` | Review outputs | Findings, approvals, notes |
| `artifact_locations` | Exact paths or links | Make discovery easy |
| `observability` | Logs, metrics, tracing hooks | What to inspect post-change |
| `decision_log` | Important decisions with dates | Append concise entries |
| `summary_format` | Expected final summary structure | Keep stable for handoffs |
| `wiki_pages_to_read_before` | Knowledge inputs | Can be repeated from feature level if task-specific |
| `wiki_pages_to_update_after` | Knowledge outputs | Same rule |
| `wiki_facts_to_capture` | Facts to preserve | Exact facts only |
| `wiki_do_not_store` | Facts excluded from wiki | Secrets and noise |

## 8. Alarm Fields

Use alarms when a plan cannot yet avoid a mock or placeholder. Do not hide them in paragraphs.

| Field | Purpose | Notes |
| --- | --- | --- |
| `alarm_id` | Stable alarm identifier | Example: `A-MOCK-001`, `A-PH-003` |
| `alarm_type` | Alarm type | `mock` or `placeholder` |
| `severity` | Alarm severity | `warning`, `blocking`, `critical` |
| `status` | Alarm state | `active`, `resolved`, `accepted-risk` |
| `scope` | Where the alarm applies | `feature`, `task`, `prompt`, `runtime` |
| `applies_to` | Feature id or task id | Keep explicit |
| `location` | File, field, subsystem, or dependency surface | What exactly contains the mock or placeholder |
| `summary` | Short human-readable statement | One sentence |
| `current_value` | The current mocked or placeholder value | Example: `MockLLMBackend`, `TBD telegraph token env name` |
| `why_present` | Why it currently exists | Must be factual, not vague |
| `missing_to_replace` | Exact missing fact or dependency | The key field the user asked for |
| `replacement_target` | What should exist after replacement | Real backend, real artifact, real value |
| `replacement_plan` | Concrete replacement approach | How the team intends to remove it |
| `owner_role` | Who owns the replacement | `planner`, `implementer`, `reviewer`, etc. |
| `blocks` | Which transitions it blocks | Example: `ready`, `in_progress`, `done` |
| `must_propagate` | Whether it must be copied forward | Recommended `true` for every active alarm |

Recommended hard rules:
- Active alarms must be copied into every task prompt and runtime projection that touches the same feature or task.
- `missing_to_replace` must be concrete. "Need more work" is not concrete enough.
- `replacement_plan` must say what exactly will remove the mock or placeholder.
- Critical active alarms block `ready`, `in_progress`, `approved`, or `done` according to their `blocks` field.

## 9. Overlap Rules

Some fields can appear at both feature and task level.

- `rationale`: keep the global why at feature level; keep the local why at task level.
- `timebox`: feature timebox defines the outer boundary; task timebox defines the local slice.
- `changed_subsystems`: feature level is broad; task level is the narrow delta.
- `risks`: feature level is broad; task level is action-specific.
- `wiki_*`: keep at feature level if shared, repeat at task level only when a task has special sync rules.

## 10. Normalization Rules

- Prefer stable `key: value` lines under Markdown headings over loose prose.
- Keep lists flat.
- Do not hide blockers inside paragraphs.
- Use `TBD` or `open_question` when data is missing.
- If a field is unknown and non-critical, keep the field and mark it unknown.
- If a field is unknown and critical for safe execution, keep the task not-ready.
- `Verification Strategy` headings are allowed, but fields should remain normal `key: value` lines for dashboard parsing.
- If a mock or placeholder exists, create a structured alarm block instead of hiding it in `assumptions` or `open_questions`.
