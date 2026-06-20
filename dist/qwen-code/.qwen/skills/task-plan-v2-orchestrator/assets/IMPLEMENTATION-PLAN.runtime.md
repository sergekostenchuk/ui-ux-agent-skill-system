# Implementation Plan

This file is a runtime projection derived from the canonical `TASK-PLAN.md`.

## Goal

- Mirror the feature-level `goal` from `TASK-PLAN.md`

## Current State / Problems

- Summarize the active blockers, open questions, and risks from the canonical plan

## Active Alarms / Replacement Requirements

- Copy every unresolved mock or placeholder alarm relevant to the current slice
- For each alarm include:
  - what is mocked or placeholder now
  - why it still exists
  - what is missing to replace it
  - the proposed replacement target
  - whether it blocks `ready`, `in_progress`, or `done`

## Proposed Changes

- Summarize the current ready or in-progress task slices
- Keep task ids intact

## Verification Plan

- Pull from `tests_required`
- Pull from `test_levels`
- Pull from `test_targets`
- Pull from `test_data_origin`
- Pull from `oracle`
- Pull from `negative_tests`
- Pull from `flakiness_risk`
- Pull from `stop_on_failure`
- Pull from `commands_planned`
- Pull from `acceptance_checks`
- Pull from `rollback_plan`
- Do not copy `commands_planned` into `commands_run` until the checks actually execute
- Do not hide unresolved mock or placeholder alarms inside the verification plan; keep them visible above

## User Review Required

- List any task or feature change that materially affects UX, data handling, security, or rollout

## Implementation Tasks

- `T-001` - short task summary
- `T-002` - short task summary

## Alarm Carry Forward Rule

- Every new model call using this projection must still see the unresolved alarms from the canonical task or feature.
- If an alarm becomes resolved, update the canonical `TASK-PLAN.md` first, then regenerate this projection.

## Canonical Links

- `FEATURE-PREPARATION.md`
- `TASK-PLAN.md`
