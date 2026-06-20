# App State Model

Every material app surface should account for:

- `loading`: initial and refetch.
- `empty`: no data, filtered empty, permission empty.
- `error`: network, validation, authorization, unknown.
- `disabled`: unavailable actions with reason.
- `focus`: keyboard-visible focus.
- `hover`: non-layout-shifting affordance.
- `selected`: table row, tab, segment, menu item.
- `submitting`: in-flight mutation.
- `success`: confirmation or optimistic resolution.

## Review Rule

If a state is not implemented, report it as `Skipped` or `Manual` with rationale. Do not infer state coverage from static happy-path code.
