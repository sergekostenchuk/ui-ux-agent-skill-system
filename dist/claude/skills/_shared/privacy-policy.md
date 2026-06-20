# UI/UX Skills Privacy Policy

Default mode is `local-first`.

## Allowed Without Extra Approval

- Reading local project source files needed for the requested UI/UX task.
- Running local validators, linters, browser checks, and scripts that do not upload data externally.
- Opening user-provided public URLs or local URLs for visual verification.
- Using connected MCP context when the user explicitly provided the file, URL, or frame.

## Approval Required

Explicit user approval is required before sending any of the following to external services:

- private source code;
- screenshots of private products;
- Figma frames from private workspaces;
- product data, customer data, analytics exports, or internal URLs;
- cookies, Playwright storage state, session files, tokens, API keys, or `.env` contents.

For every approved external service, record:

- service name;
- exact data sent;
- purpose;
- local fallback;
- result status.

## Forbidden Defaults

- Do not store secrets in skill assets, reports, examples, or wiki pages.
- Do not treat cloud drafts as validation evidence.
- Do not hide destructive file operations inside scripts.
- Do not claim browser, Lighthouse, axe, or screenshot evidence unless the command ran and artifacts exist.
