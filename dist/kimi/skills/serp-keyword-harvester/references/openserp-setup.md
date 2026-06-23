# OpenSERP Setup Contract

OpenSERP is an optional external-network source for search-demand evidence. It is not required for local keyword harvests and must not run without explicit user approval.

## Inventory Contract

- tool id: `openserp-api`
- class: `optional-cloud`
- status: `not-configured-approval-gated`
- privacy class: `external-network`
- approval required: `true`
- setup owner: `serp-source-configurator`
- evidence owner: `serp-keyword-harvester`
- downstream consumers: `semantic-core-builder`, `seo-llm-site-architect`

## Setup Inputs

- `OPENSERP_API_KEY`: stored only in local environment, never in Markdown, reports, wiki, task plans, screenshots, or shell transcripts.
- `OPENSERP_BASE_URL`: provider endpoint, stored locally if needed.
- locale/market.
- approved query set.
- allowed result types, for example organic SERP, autocomplete, People Also Ask, related searches, if the provider supports them.
- rate/quota limits.

Use `serp-source-configurator` and its source-config template for source selection, proxy/provider gates, budget, and preflight. Use `assets/openserp-settings.example.json` only as a redacted compatibility template. Do not replace placeholders with real credentials inside repository files.

## Approval Gate

Before any OpenSERP call, record:

- user approval;
- exact public queries to send;
- locale/market;
- purpose;
- expected output path;
- fallback if the provider is unavailable.

If any item is missing, do not call OpenSERP. Mark the source `Planned` or `Skipped`.

If source selection, proxy provider, API-key UI, paid-proxy limits, or engine checkboxes are missing, route to `serp-source-configurator` before harvesting.

## Reporting

OpenSERP evidence must be written into `reports/keyword-harvest.json` under source provenance and `source_status`.

Valid statuses:

- `Ran`: only after an actual approved call and saved output.
- `Skipped`: provider not configured, unavailable, quota-limited, or approval missing.
- `Planned`: intended for future setup.
- `Manual`: manually transcribed public SERP notes.

## Failure Behavior

If approval, credentials, quota, provider support, or network availability is missing:

- do not retry aggressively;
- do not invent SERP evidence;
- continue with local/user-provided inputs;
- hand off limitations to `semantic-core-builder`.
