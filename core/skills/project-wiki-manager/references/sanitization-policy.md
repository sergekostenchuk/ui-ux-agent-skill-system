# Sanitization Policy

## Never Store

- API keys, npm tokens, cloud tokens, private keys, passwords, recovery codes, cookies, session data, OAuth refresh tokens, `.env` values.
- Private screenshots, private URLs, personal data, or customer data unless the user explicitly approves the exact storage target.
- Raw logs that may contain credentials or private identifiers.

## Allowed References

Use redacted references:

- environment variable names without values;
- secret-store names without values;
- local artifact paths when the path itself is not sensitive;
- validation status without secret output.

## Fact Labels

Label uncertain information:

- `User-provided`: stated by user.
- `Source-backed`: supported by a local artifact or external source.
- `Inference`: derived by the agent and must not be stored as fact without context.
- `Manual`: expert judgment without machine verification.

## Pre-Capture Check

Before writing wiki content:

1. Scan for token-like strings and `.env` snippets.
2. Remove or redact secret values.
3. Keep exact artifact paths only when safe.
4. Record what was excluded.
