---
name: domain-name-generator
description: "Use when a project needs domain name ideas, naming constraints, availability-check planning, brand/SEO fit, and shortlists. Advisory only; do not purchase domains, call paid APIs, or claim live availability unless checked with evidence."
---

# Domain Name Generator

Generate and score domain ideas without purchasing or claiming availability without evidence.

## Workflow

1. Gather brand, geography, language, product category, forbidden words, and TLD preferences.
2. Produce candidate names with rationale and risks.
3. Mark availability as `Unknown`, `Manual`, `Planned`, or `Ran`.
4. Hand off registrar/pricing decisions to `domain-registrar-advisor`.

## Safety Rules

- Do not purchase domains or use paid availability APIs without approval.
- Do not imply a domain is available unless a check ran and the source is recorded.
- Avoid trademark, misleading, or legally risky names.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/domain-name-generator
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/domain-name-generator
python3 -m json.tool $CODEX_HOME/skills/domain-name-generator/evals/evals.json >/dev/null
```
