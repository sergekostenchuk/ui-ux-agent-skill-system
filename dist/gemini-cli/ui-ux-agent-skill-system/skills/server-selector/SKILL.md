---
name: server-selector
description: "Use when choosing hosting/server architecture for a site or app: static hosting, VPS, PaaS, CDN, region, cost assumptions, scaling, security, and ops tradeoffs. Advisory only; do not provision servers or create paid resources without explicit approval."
---

# Server Selector

Choose hosting options and tradeoffs without provisioning resources.

## Workflow

1. Gather stack, traffic, geography, budget, compliance, and maintenance needs.
2. Compare static hosting, VPS, managed platform, CDN, object storage, and database needs.
3. Mark pricing/freshness assumptions clearly.
4. Hand off provisioning plan to `server-provisioner`.

## Safety Rules

- Do not create paid resources, servers, databases, buckets, or CDN zones without approval.
- Do not store provider credentials.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/server-selector
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/server-selector
python3 -m json.tool $CODEX_HOME/skills/server-selector/evals/evals.json >/dev/null
```
