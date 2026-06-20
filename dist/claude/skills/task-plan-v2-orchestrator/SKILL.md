---
name: task-plan-v2-orchestrator
description: Create, refactor, audit, and maintain a multi-agent TASK-PLAN v2 as a canonical Markdown control document with a pre-implementation feature gate, sequential per-task agent orchestration, explicit test/review/rollback fields, wiki sync rules, and a derived HTML dashboard contract. Use when Codex needs to turn loose plans or checklists into structured planning docs, add agent handoff contracts, prepare plans for Codex, Claude Code, Gemini, or Antigravity, or keep Markdown as the source of truth and HTML as a generated dashboard.
---

# Task Plan V2 Orchestrator

Use this skill for planning and orchestration artifacts, not for feature implementation itself.

## Canonical Model

- `FEATURE-PREPARATION.md` is the pre-implementation gate.
- `TASK-PLAN.md` is the canonical, editable control document.
- `TASK-DASHBOARD.html` is derived from Markdown and never the source of truth.

If the user asks for only one file, preserve the same logical separation inside that file.

## Workflow

1. Classify the request:
   - create a new plan
   - refactor an existing plan
   - audit a plan
   - prepare runtime-specific projections
2. Read [`references/field-layers.md`](references/field-layers.md).
3. If the user mentioned `Codex`, `Claude Code`, `Gemini`, or `Antigravity`, also read [`references/runtime-adapters.md`](references/runtime-adapters.md).
4. If the user wants HTML, dashboard, graph, kanban, or observability views, also read [`references/dashboard-contract.md`](references/dashboard-contract.md).
5. Start with the pre-implementation layer. If it is incomplete, do not mark implementation tasks as ready.
6. Normalize every task into a stable task block with explicit fields instead of freeform prose.
7. Model multi-agent execution as sequential by default.
8. Add `Execution Governance` and `Verification Policy` before task execution.
9. Keep missing facts explicit as `TBD`, `unknown`, or `open_question`; do not invent them.
10. Treat critical `TBD` fields as blockers for `ready`, `in_progress`, `approved`, and `done`.
11. Default to `NO-MOCKS` and `NO-PLACEHOLDERS`.
12. If a mock or placeholder is temporarily unavoidable, convert it into an explicit alarm with replacement requirements and carry that alarm into every downstream prompt or runtime projection.

## Multi-Agent Rules

- A task may have many agents, but only one current `owner_role`.
- `agent_sequence` is ordered and sequential unless the user explicitly asks for parallel lanes.
- `agent_contracts` must define:
  - entry criteria
  - expected outputs
  - handoff target
  - stop conditions
- `required_approvals` must name roles or gates, not vague "review".
- `max_review_loops` must be finite.
- `escalation_rule` must say what happens when review loops are exhausted or a blocker cannot be resolved locally.

## Governance Rules

- `NO-FICTION`: do not invent files, commits, checks, approvals, blockers, or artifact paths.
- `NO-MOCKS`: do not plan or accept mocks, fake integrations, stubbed results, fake evidence, or pretend backends as a quiet default.
- `NO-PLACEHOLDERS`: do not leave placeholders in execution-ready work except as explicit unresolved alarms.
- `INVALID_INPUT`: if required input is missing, return the missing fields and do not execute.
- `prompt-first`: one task needs one prompt before `in_progress`.
- `code-first`: implementation tasks cannot close with docs-only progress.
- `strict DONE`: `done` requires dependencies, approvals, executed verification, evidence, rollback, and sync.
- `verification-first`: tests are planned by `planner`, reviewed by `reviewer`, and executed by `tester`.
- `commands_planned` is not the same as `commands_run`.
- Placeholder evidence, placeholder tests, and placeholder artifact paths are invalid.
- Unresolved mocks and placeholders must become `alarms`, not silent notes.
- Every unresolved alarm must state:
  - what is mocked or placeholder
  - why it exists
  - what exact fact, system, credential, artifact, or dependency is missing to replace it
  - the replacement target and proposed replacement path
  - whether it blocks `ready`, `in_progress`, `approved`, or `done`
- Every unresolved alarm must be copied into:
  - the task block
  - the task prompt
  - the runtime projection
  - the handoff summary

## What To Read

- Always read [`references/field-layers.md`](references/field-layers.md).
- Read [`references/runtime-adapters.md`](references/runtime-adapters.md) when runtime-specific outputs are needed.
- Read [`references/dashboard-contract.md`](references/dashboard-contract.md) when the user wants `.html` or a visual board.
- Copy from:
  - [`assets/FEATURE-PREPARATION-CHECKLIST.md`](assets/FEATURE-PREPARATION-CHECKLIST.md)
  - [`assets/TASK-PLAN-v2.template.md`](assets/TASK-PLAN-v2.template.md)
  - [`assets/CLAUDE-CODE.tasks-projection.md`](assets/CLAUDE-CODE.tasks-projection.md) when a Claude-style condensed tasks view is needed
  - [`assets/IMPLEMENTATION-PLAN.runtime.md`](assets/IMPLEMENTATION-PLAN.runtime.md) when Gemini or Antigravity needs a projection

## Output Rules

- Preserve Markdown as the source of truth.
- Make task blocks stable enough for deterministic parsing.
- Keep a compact register near the top only if it helps navigation or dashboard generation.
- Do not collapse agent-level data into one sentence; keep handoffs explicit.
- When adapting for another runtime, keep field semantics unchanged and only adjust layout or headings.
- If the plan still contains unresolved mocks or placeholders, surface them as top-level warnings and per-task alarms instead of burying them in prose.
- Do not mark a task `ready`, `in_progress`, `approved`, or `done` while a critical unresolved mock/placeholder alarm is active.

## Runtime Projections

- `Codex`: edit the canonical Markdown directly.
- `Claude Code`: keep the canonical Markdown and emit a condensed tasks projection only when useful.
- `Gemini` and `Antigravity`: keep the canonical Markdown and emit `implementation_plan.md` only as a projection, not a replacement.

## Completion Bar

A good TASK-PLAN v2 has:
1. an explicit feature-prep gate
2. normalized task blocks
3. sequential agent contracts
4. an `Execution Governance` section
5. a planned-before-coding `Verification Strategy`
6. test, review, artifact, and rollback fields
7. wiki read and write rules
8. a dashboard-ready structure
9. explicit unresolved-alarm tracking for any temporary mock or placeholder
