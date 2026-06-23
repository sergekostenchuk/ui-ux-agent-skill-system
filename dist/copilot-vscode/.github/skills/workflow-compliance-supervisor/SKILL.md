---
name: workflow-compliance-supervisor
description: Use when a UI/UX project must verify that the promised user journey, TASK-PLAN.md, progress-state.json, rendered progress HTML, evidence artifacts, and skipped stages are consistent. Detects lazy skips, fake Ran/Done claims, missing evidence, approval-gated external steps, and user-data blockers; recommends continue, pause_for_user, return_to_rework, skip_with_reason, or block without replacing senior-ui-ux-orchestrator as chair.
---

# Workflow Compliance Supervisor

This skill is the governance layer for journey-driven UI/UX projects. It checks whether the system did what it promised, whether skipped stages are justified, and whether the user sees honest reasons and next actions.

It does not execute design/build tasks and does not override `senior-ui-ux-orchestrator`.

## Operating Modes

- `gate`: check the current project before continuing or closing a phase.
- `review`: audit an existing task plan, progress state, progress screen, and evidence set.
- `log`: append or validate `workflow-log.jsonl` events.
- `fixture-test`: run lazy-skip and fake-evidence fixtures.
- `explain`: explain to the user why a stage is paused, skipped, returned to rework, or blocked.

## Required Workflow

1. Read [references/decision-framework.md](references/decision-framework.md).
2. Read [references/evidence-and-log-rules.md](references/evidence-and-log-rules.md).
3. Read [references/user-messaging.md](references/user-messaging.md) if the output will be shown to a non-technical user.
4. Locate the canonical project `TASK-PLAN.md`.
5. Locate the declared journey registry. Default local registry: `$UIUX_SKILL_SYSTEM_ROOT/data/journey-registry.json`.
6. Compare declared journey stages with task-plan claims, progress state, reports, screenshots, and logs.
7. Produce one decision per affected stage: `continue`, `pause_for_user`, `return_to_rework`, `skip_with_reason`, or `block`.
8. For every skip, require an acceptable reason code, impact, and next action.
9. For every `done`/`Ran` claim, require real evidence.
10. Write or update a sanitized report/log only when the user asked for execution or validation.

## Decision States

- `continue`: evidence is sufficient or deviation has no material impact.
- `pause_for_user`: missing user data, approval, budget, credentials, or production confirmation.
- `return_to_rework`: claimed completion lacks evidence or violates the journey contract.
- `skip_with_reason`: stage is intentionally skipped with accepted reason and visible impact.
- `block`: continuing would compromise quality, privacy, legality, production safety, or journey integrity.

## Hard Rules

- Do not accept `model_convenience`, `implicit_assumption`, `planned_counted_as_ran`, or `tool_not_called_but_marked_done`.
- Do not mark planned commands as executed.
- Do not claim that a full journey is complete when only a demo slice ran.
- Do not store secrets, tokens, cookies, `.env`, recovery codes, private screenshots, or raw provider payloads.
- Optional external tools, crawls, uploads, paid APIs, production deploys, analytics, ads, and account mutations require explicit approval.

## Local Validation Commands

```bash
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/validate_workflow_compliance.py" --fixtures
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/validate_workflow_log.py" --fixtures
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/validate_workflow_compliance.py" --project "$PROJECT_ROOT" --journey new-premium-site --out "$PROJECT_ROOT/reports/workflow-compliance-report.md" --log "$PROJECT_ROOT/workflow-log.jsonl"
```

Skill package checks:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/workflow-compliance-supervisor
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/workflow-compliance-supervisor
```

## Handoff Shape

```text
Declared journey:
Checked artifacts:
Decision:
Reason code:
Evidence:
User-visible message:
Next action:
Can continue:
Must rework:
Skipped with accepted reason:
Blocked:
```

