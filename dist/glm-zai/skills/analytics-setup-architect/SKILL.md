---
name: analytics-setup-architect
description: "Use when a website or web app needs privacy-aware analytics architecture: GA4, Yandex Metrica, self-hosted analytics, consent, UTM, event taxonomy, funnels, dashboards, and launch verification. Do not mutate real analytics accounts or store credentials without explicit approval."
---

# Analytics Setup Architect

This skill designs analytics measurement plans. It is planning-first and does not change live analytics accounts by default.

## Operating Modes

- `measurement-plan`: define goals, events, conversions, UTM, and dashboards.
- `consent-plan`: define cookie/consent, privacy, retention, and no-track paths.
- `implementation-handoff`: prepare event specs for developers.
- `verification`: define checks for tags, events, and reporting.

## Required Workflow

1. Read [references/analytics-safety-contract.md](references/analytics-safety-contract.md).
2. Use [assets/analytics-plan.template.md](assets/analytics-plan.template.md).
3. Confirm data sensitivity, geography, consent needs, and analytics provider.
4. Define only needed events; avoid collecting personal data by default.
5. Mark real account changes as `Planned` until explicit approval exists.

## Safety Rules

- Do not store analytics tokens, cookies, measurement secrets, or private exports.
- Do not mutate GA4, Metrica, Tag Manager, dashboards, or production tags without approval.
- Do not collect personal data unless the user explicitly approves a legal/privacy plan.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/analytics-setup-architect
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/analytics-setup-architect
python3 -m json.tool $CODEX_HOME/skills/analytics-setup-architect/evals/evals.json >/dev/null
```
