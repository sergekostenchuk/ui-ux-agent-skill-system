---
name: launch-readiness-auditor
description: "Use before launch to audit SEO, schema, accessibility, performance, security, analytics, redirects, sitemap, robots, SSL, monitoring, rollback, and approval gates. Evidence-first; do not mark launch ready unless required checks ran or are explicitly skipped with rationale."
---

# Launch Readiness Auditor

This skill is the final launch gate. It checks whether evidence exists before production launch.

## Operating Modes

- `pre-launch-audit`: compile required launch checks and evidence.
- `blocker-register`: list blockers, owners, and required approvals.
- `go-no-go`: produce launch decision with rollback and monitoring.

## Required Checks

- SEO metadata, canonical, sitemap, robots, schema, llms.txt when relevant.
- Accessibility and responsive UI smoke.
- Performance and asset loading.
- SSL/TLS, security headers, cookies, backups, monitoring.
- Redirects and migration checks when existing site is involved.
- Analytics and webmaster verification plan.
- Explicit production approval for deploy, DNS, registrar, server, and account mutations.

## Safety Rules

- Do not mark `Ready` without evidence or explicit skipped rationale.
- Do not perform production actions; route execution back to specialists after approval.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/launch-readiness-auditor
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/launch-readiness-auditor
python3 -m json.tool $CODEX_HOME/skills/launch-readiness-auditor/evals/evals.json >/dev/null
```
