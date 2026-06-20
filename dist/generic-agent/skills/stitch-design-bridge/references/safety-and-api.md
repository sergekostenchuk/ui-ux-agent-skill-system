# Stitch Safety And API Boundary

## Credential Handling

Do not store Stitch credentials in:

- `SKILL.md`;
- references;
- assets;
- evals;
- wiki pages;
- task plans;
- reports;
- screenshots;
- shell history examples with real values.

Use environment variables such as `STITCH_API_KEY`.

If a real API key appears in a chat, file, task plan, commit, report, or wiki page, treat it as exposed and recommend rotation.

## External Upload Policy

Stitch may be an external service. Before sending private project material, record:

- service name;
- exact data to send;
- purpose;
- local fallback;
- whether the user explicitly approved the transfer.

Public marketing copy or already-public URLs can be used with less friction, but still do not include secrets or credentials.

## Data To Avoid Sending

- private Figma files unless explicitly approved;
- internal screenshots;
- private client documents;
- `.env` files;
- tokens or API keys;
- customer data;
- private analytics;
- unreleased legal/financial material;
- private source code unless explicitly approved.

## Freshness

Stitch capabilities, API surface, MCP support, export behavior, and Figma integration may change. Verify current primary sources or local MCP tool availability before claiming:

- API endpoint names;
- supported export formats;
- pricing;
- availability by region/account;
- whether Figma export/import is supported;
- whether a MCP tool is installed in the current session.

## Failure Handling

If Stitch API/MCP is unavailable:

- produce a Stitch-ready prompt and manual workflow;
- keep the design exploration local when possible;
- route to Figma or code fallback only after the user accepts the limitation;
- label all unavailable checks as `Skipped` or `Blocked`, not `Ran`.
