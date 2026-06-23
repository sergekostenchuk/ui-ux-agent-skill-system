---
name: serp-keyword-harvester
description: Collect and normalize search-demand inputs for public site projects before semantic-core work. Use when a UI/UX or SEO project needs seed keywords, SERP snapshots, autocomplete ideas, People Also Ask, related searches, or a dry-run keyword harvest with approval-gated external search APIs.
---

# SERP Keyword Harvester

This skill prepares raw search-demand evidence for the pre-design pipeline. It does not decide final site architecture or source/proxy policy; `serp-source-configurator` owns setup gates and this skill hands structured inputs to `semantic-core-builder`.

## Operating Modes

- `plan`: define seed keywords, locales, sources, approvals, and fallback.
- `harvest-local`: normalize user-provided keywords, exported CSVs, existing site text, or local reports.
- `harvest-external`: use approved SERP/autocomplete APIs or tools; approval required before network calls.
- `audit`: review an existing `reports/keyword-harvest.json`.

## Required Workflow

1. Read [references/keyword-harvest-contract.md](references/keyword-harvest-contract.md).
2. If OpenSERP, AKE, proxy, API keys, engine checkboxes, source settings, or paid-proxy limits are mentioned, route setup to `serp-source-configurator` first and consume its redacted `reports/serp-source-config.json` handoff.
3. If OpenSERP is already approved/configured, read [references/openserp-setup.md](references/openserp-setup.md) and use [assets/openserp-settings.example.json](assets/openserp-settings.example.json) only as a redacted contract, not as a credential store.
4. Confirm privacy and approval mode:
   - local inputs and user-provided public facts: allowed;
   - external SERP/API/crawling: explicit approval required;
   - private/authenticated sources: explicit approval plus data-handling note.
5. Collect or normalize seed keywords, market/locale, project type, and source provenance.
6. Write or update `reports/keyword-harvest.json` using [assets/keyword-harvest.schema.json](assets/keyword-harvest.schema.json) as the field contract.
7. Label every data group as `Ran`, `Skipped`, `Planned`, or `Manual`.
8. Hand off to `semantic-core-builder`; do not invent missing SERP evidence.

## Safety Rules

- Do not scrape or call external services without approval.
- Do not store API keys, cookies, private URLs, recovery codes, or `.env` values in reports.
- Treat OpenSERP as `optional-cloud` / `external-network`: no call without explicit approval, configured credentials, query scope, source config, and a data-transfer note.
- Do not decide proxy provider, paid budget, or engine selection inside this skill when it is not already explicit; use `serp-source-configurator`.
- If search APIs return 429/503 or are unavailable, mark the source `Skipped` and continue with local/user-provided inputs.

## Handoff Shape

```text
Mode:
Locale/market:
Seed keywords:
Sources used:
Sources skipped:
Source config:
Output path:
Privacy/approval note:
Next skill: semantic-core-builder
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/serp-keyword-harvester
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/serp-keyword-harvester
```
