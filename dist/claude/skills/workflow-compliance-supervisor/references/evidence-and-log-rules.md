# Evidence And Log Rules

## Evidence Labels

- `Ran`: command or check really ran and artifact exists.
- `Skipped`: intentionally skipped with accepted reason and visible impact.
- `Planned`: planned but not executed.
- `Manual`: human inspection or external action was explicitly accepted.

## Minimum Event Shape

Every workflow log event should include:

- timestamp;
- project;
- declared_journey;
- expected_stage;
- actual_state;
- decision;
- reason_code;
- evidence;
- user_options;
- owner_role;
- message;
- next_action.

## Secret Boundary

Never log:

- API keys or tokens;
- recovery codes;
- cookies or `.env` values;
- private screenshots or private URLs;
- raw external provider payloads.

Use redacted placeholders only when an example needs a credential-like value.

