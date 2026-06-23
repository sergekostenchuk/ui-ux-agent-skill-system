---
name: omnichannel-comms-builder
description: "Use when a site needs communication workflow planning: forms, inboxes, chat, booking, email/SMS/Telegram/CRM handoffs, operator queues, routing, templates, consent, and escalation. Workflow design only; never send real messages or mutate CRM channels without explicit approval."
---

# Omnichannel Comms Builder

This skill designs communication flows between site users and operators. It does not send real messages by default.

## Operating Modes

- `workflow-plan`: define channels, routing, ownership, SLA, and escalation.
- `message-template`: draft safe templates without sending.
- `operator-ui-handoff`: specify inbox/queue UI needs.
- `consent-risk`: define consent, logging, retention, and opt-out requirements.

## Required Workflow

1. Read [references/comms-safety-contract.md](references/comms-safety-contract.md).
2. Use [assets/comms-workflow.template.md](assets/comms-workflow.template.md).
3. Confirm channels, personal-data handling, and approval status.
4. Mark all real sends and CRM mutations as `Planned` until explicit approval.

## Safety Rules

- Do not send email, SMS, Telegram, chat, webhook, or CRM messages without approval.
- Do not store private customer data, tokens, message exports, or cookies.
- Templates must avoid false claims and must support opt-out and escalation when needed.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/omnichannel-comms-builder
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/omnichannel-comms-builder
python3 -m json.tool $CODEX_HOME/skills/omnichannel-comms-builder/evals/evals.json >/dev/null
```
