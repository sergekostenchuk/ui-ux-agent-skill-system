# Feedback Status Contract

## Statuses

| Status | Meaning | UI Color |
| --- | --- | --- |
| `empty` | No comment exists yet. | blue |
| `open` | Comment exists and needs review. | red |
| `accepted` | Decision accepts the comment but work may not be applied yet. | red |
| `partially_applied` | Some action was taken, but the feedback is not fully resolved. | orange |
| `applied` | Accepted feedback is implemented and artifact is referenced. | green |
| `rejected` | Chair or owner rejected the feedback with rationale. | neutral |

## Resolution Rules

- User checkbox can mark an accepted item as applied only when an artifact or decision record exists.
- Agent critiques require evidence labels: `Ran`, `Skipped`, `Planned`, or `Manual`.
- Partial acceptance must state what was accepted and what was rejected.
- Critical feedback must name a next owner and validation gate.
