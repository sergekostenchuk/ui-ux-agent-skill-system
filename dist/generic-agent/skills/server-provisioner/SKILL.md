---
name: server-provisioner
description: "Use when preparing server provisioning plans, IaC drafts, SSH hardening, users, firewalls, backups, monitoring, and rollback. Dry-run by default; do not create, mutate, or destroy production servers without explicit approval."
---

# Server Provisioner

Prepare provisioning plans and dry-run commands without mutating real infrastructure.

## Workflow

1. Confirm provider, region, OS, stack, and approval status.
2. Produce dry-run provisioning checklist or IaC draft.
3. Include SSH, firewall, updates, backups, monitoring, secrets, and rollback.
4. Mark execution as blocked until explicit approval.

## Safety Rules

- Do not create, destroy, reboot, resize, open firewall, or SSH into production servers without approval.
- Do not print SSH keys, tokens, passwords, or `.env`.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/server-provisioner
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/server-provisioner
python3 -m json.tool $CODEX_HOME/skills/server-provisioner/evals/evals.json >/dev/null
```
