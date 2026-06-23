# Runtime Enforcement Gap Checkpoint

Date: 2026-06-23
Context: UI/UX Skill System audit after yacht school workflow test.

## Remembered Decision

The current missing layer is not another expert skill. The missing layer is runtime enforcement that makes the system follow its promised user journeys.

Required additions:

1. Add `serp-source-configurator` into the active task plan, dashboard, routing, and projections.
2. Add a hard stage runner / gate runner so orchestration cannot skip required stages without a recorded reason.
3. Add a skill execution ledger that records which skill ran, why it ran, what it produced, and what evidence proves it.
4. Add a feedback bridge so user choices and comments from `agent-progress-screen.html` are written back to machine-readable state and read before the next stage.
5. Strengthen `workflow-compliance-supervisor` so it validates expected journey outputs as real files/artifacts, not only as text claims in `TASK-PLAN.md`.
6. Expand `TASK-DASHBOARD.html` into a matrix: phase, skill, required/optional status, installed status, evaluation coverage, script coverage, runtime gate, and latest evidence.

## Why

The yacht school run exposed that a progress page and a task plan are not enough. The system can still move forward while important promised stages are missing: SERP, Stitch exploration, three design variants, prototype, admin workflow, user feedback loop, and live progress updates.

The fix is to treat the user journey as an executable contract:

- every promised stage has required outputs;
- every skipped stage has a blocker or explicit approval;
- every user-facing choice is persisted;
- the progress screen reads real state rather than post-factum narration;
- the supervisor can stop, return, skip with reason, or ask the user for missing input.

## Next Architecture Step

Before adding more domain skills, implement the runtime control layer:

`journey-registry -> stage-runner -> skill-execution-ledger -> progress-feedback-bridge -> compliance-supervisor -> dashboard/progress screen`

