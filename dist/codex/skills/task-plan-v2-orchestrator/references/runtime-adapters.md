# Runtime Adapters

Use one canonical planning model across runtimes. Adapt file layout, not field semantics.

## Core Rule

- `FEATURE-PREPARATION.md` and `TASK-PLAN.md` are the canonical sources.
- Runtime-specific files are projections.
- If a projection is edited, backport the change to the canonical file.
- Unresolved mock or placeholder alarms must be copied into every projection, not silently dropped.

## Codex

Best fit:
- keep `FEATURE-PREPARATION.md`
- keep `TASK-PLAN.md`
- optionally generate `TASK-DASHBOARD.html`

Notes:
- Codex works well with normalized Markdown and explicit task blocks.
- Keep `agent_sequence` and `agent_contracts` in the canonical file.
- Use the canonical plan directly instead of flattening it into a checklist too early.
- Keep active alarms visible near the top of the current task context so the model cannot ignore them.

## Claude Code

Best fit:
- keep the canonical files
- optionally emit a condensed projection for `.claude/specs/<feature>/tasks.md`

Projection rule:
- the Claude-facing tasks file should be derived from implementation-ready task blocks only
- keep it as a numbered checkbox list if the local Claude workflow expects that format
- keep links or references back to the canonical `TASK-PLAN.md`

Suggested mapping:
- canonical task `status=ready|in_progress` -> included in Claude projection
- `agent_sequence` -> turned into handoff notes or sub-bullets
- `acceptance_checks` and `test_targets` -> turned into explicit checklist notes
- `commands_planned` -> planned task checks
- `commands_run` -> only actual execution evidence, never copied from planned commands
- active alarms -> explicit warning bullets at the top of the Claude-facing projection

Use [`../assets/CLAUDE-CODE.tasks-projection.md`](../assets/CLAUDE-CODE.tasks-projection.md) as the starting projection.

## Gemini

Best fit:
- keep the canonical files
- optionally emit `implementation_plan.md`

Projection rule:
- keep the canonical fields intact in `TASK-PLAN.md`
- project them into the more narrative `implementation_plan.md` shape only if the runtime or local workflow expects it

Suggested section mapping:
- feature `goal` -> `Goal`
- global `risks` and open questions -> `Current State` or `Problems`
- task slices -> `Implementation Tasks`
- `acceptance_checks` and `tests_required` -> `Verification Plan`
- `test_levels`, `test_targets`, `test_data_origin`, `oracle`, and `commands_planned` -> `Verification Plan`
- `commands_run` -> executed checks only after work is performed
- active alarms -> dedicated `Active Alarms / Replacement Requirements` section

Use [`../assets/IMPLEMENTATION-PLAN.runtime.md`](../assets/IMPLEMENTATION-PLAN.runtime.md) as the starting projection.

## Antigravity

Best fit:
- treat it like a Gemini-adjacent runtime projection layer
- keep the canonical files outside the runtime cache or brain folder when possible
- project to `implementation_plan.md` or equivalent runtime-local plan files only when needed

Working rule for local Antigravity-style folders:
- `implementation_plan.md` is a projection
- `implementation_plan.md.resolved` is a further runtime artifact, not the source of truth
- do not update only the resolved artifact and forget the canonical plan

When a change affects UX or review risk, keep a visible review gate in the projection:
- `User Review Required`
- `Critical Changes`
- `Verification Plan`
- `Active Alarms / Replacement Requirements`

## What Must Stay Stable Across All Runtimes

These semantics should not change:
- task ids
- dependency direction
- status meaning
- agent order
- approval gates
- acceptance criteria
- rollback plan
- wiki sync obligations
- unresolved alarm meaning and blocking effect

## Projection Strategy

Use this order:
1. update canonical Markdown
2. regenerate runtime projection
3. verify that task ids, statuses, and unresolved alarms still match
4. if HTML exists, regenerate dashboard from canonical Markdown
