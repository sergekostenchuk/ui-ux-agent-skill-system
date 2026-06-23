---
name: existing-site-analyzer
description: Analyze an existing website before improve, redesign, rebuild, or migration decisions. Use when a project has a current URL, local HTML/codebase, screenshots, sitemap, robots, analytics export, asset folder, or legacy site materials and needs a local-first audit with approval-gated crawling or authenticated access.
---

# Existing Site Analyzer

This skill creates the evidence base for existing-site work. It does not decide rebuild strategy by itself and does not mutate the live site.

## Operating Modes

- `local-inventory`: inspect local HTML, source files, assets, sitemap, robots, and reports.
- `public-url-review`: review public URLs or fetched HTML only after network/crawling approval.
- `screenshot-review`: analyze screenshots when URL or source is unavailable.
- `asset-inventory`: inventory images, videos, docs, icons, maps, and brand assets.
- `handoff`: produce evidence for `rebuild-or-improve-advisor` and `migration-planner`.

## Required Workflow

1. Read [references/existing-site-analysis-contract.md](references/existing-site-analysis-contract.md).
2. Confirm source type and privacy:
   - local files and user-provided public screenshots: allowed;
   - public URL crawling/fetching: approval required if not already requested;
   - authenticated/private pages, analytics, CRM, or CMS: explicit approval and data-handling note required.
3. Use [assets/existing-site-audit.template.md](assets/existing-site-audit.template.md) for the report.
4. Record evidence status for every source: `Ran`, `Skipped`, `Planned`, or `Manual`.
5. Capture:
   - page inventory;
   - content and IA;
   - SEO/LLM surface;
   - UX and conversion issues;
   - technical constraints;
   - asset inventory;
   - migration risks.
6. Hand off to `rebuild-or-improve-advisor`; involve `migration-planner` if URL structure, redirects, sitemap, robots, schema, or launch risk may change.

## Safety Rules

- Do not crawl private/authenticated pages without explicit approval.
- Do not store private analytics exports, cookies, tokens, private URLs, or `.env` values in reports.
- Do not claim Lighthouse, browser, crawler, or DOM evidence unless it was actually run.
- Do not change production content, redirects, robots, sitemap, DNS, CMS, or deployment settings.

## Handoff Shape

```text
Mode:
Sources:
Evidence status:
Major findings:
SEO/LLM risks:
UX risks:
Technical constraints:
Asset inventory:
Migration risk:
Next owner:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/existing-site-analyzer
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/existing-site-analyzer
python3 -m json.tool $CODEX_HOME/skills/existing-site-analyzer/evals/evals.json >/dev/null
```
