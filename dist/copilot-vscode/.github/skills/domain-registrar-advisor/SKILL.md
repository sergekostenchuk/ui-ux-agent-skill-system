---
name: domain-registrar-advisor
description: "Use when comparing domain registrars, TLD costs, renewal risks, privacy, DNS features, transfer lock, and purchase steps. Advisory/dry-run only; do not buy domains or log into registrar accounts without explicit approval."
---

# Domain Registrar Advisor

Compare registrar options and prepare purchase checklists without executing purchases.

## Workflow

1. Compare registrar criteria: price, renewal, privacy, DNS, support, transfer, region, payment.
2. Label current pricing as `Manual` unless verified from a current source.
3. Prepare purchase checklist and approval point.
4. Hand off DNS planning to `domain-dns-configurator`.

## Safety Rules

- Do not buy, transfer, renew, or change registrar settings without explicit approval.
- Do not store registrar credentials, payment data, or account screenshots.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/domain-registrar-advisor
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/domain-registrar-advisor
python3 -m json.tool $CODEX_HOME/skills/domain-registrar-advisor/evals/evals.json >/dev/null
```
