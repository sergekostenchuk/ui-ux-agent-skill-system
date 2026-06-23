---
name: webmaster-registrar
description: "Use when planning Google Search Console, Yandex Webmaster, Bing Webmaster, sitemap submission, verification records, ownership checks, and post-launch indexing monitoring. Planning only; do not submit, verify, or mutate webmaster accounts without explicit approval."
---

# Webmaster Registrar

Plan webmaster registration and verification without account mutations by default.

## Workflow

1. Identify search engines, domain/property type, sitemap, robots, and approval status.
2. Prepare verification options and records without exposing values.
3. Plan sitemap submission and post-launch indexing checks.
4. Mark account actions `Planned` until explicit approval exists.

## Safety Rules

- Do not log in, verify properties, submit sitemaps, add users, or store verification tokens without approval.
- Do not print private verification codes in reports.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/webmaster-registrar
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/webmaster-registrar
python3 -m json.tool $CODEX_HOME/skills/webmaster-registrar/evals/evals.json >/dev/null
```
