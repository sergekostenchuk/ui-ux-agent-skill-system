---
name: pencil-design-bridge
description: Bridge approved UI/UX direction briefs into Pencil design workflows without treating `.pen` files as plain text. Use when a project needs Pencil MCP/tool handoff, editable design exploration, design-system-aware canvas work, or review of Pencil outputs after senior-ui-ux-orchestrator, ui-ux-pro-max, Stitch, or Figma constraints are known.
---

# Pencil Design Bridge

This skill is the Pencil layer in the UI/UX Agent Skill System. Pencil is a design-tool bridge and editable design workspace, not the central architect and not a plain-file parser.

## Operating Modes

- `brief`: turn an approved direction brief into a Pencil-ready design brief.
- `canvas-handoff`: prepare instructions for Pencil MCP/tools or a Pencil-capable agent.
- `review-output`: review Pencil output against UX, SEO/LLM, accessibility, brand, and implementation constraints.
- `figma-code-handoff`: prepare Pencil results for Figma or code implementation.
- `config-check`: check whether Pencil tools are available in the current runtime without reading `.pen` files directly.

## Required Workflow

1. Read [references/pencil-bridge-contract.md](references/pencil-bridge-contract.md).
2. Confirm the source brief was approved by `senior-ui-ux-orchestrator` or came from an explicit user decision.
3. Confirm inputs:
   - product/UX journey;
   - SEO/LLM constraints for public pages;
   - `ui-ux-pro-max` design intelligence;
   - optional Stitch output or Figma constraints;
   - required assets and forbidden claims.
4. Use [assets/pencil-handoff.template.md](assets/pencil-handoff.template.md) for handoff packets.
5. Access `.pen` documents only through Pencil MCP/tools. Do not use shell reads, grep, cat, or ad hoc JSON parsing on `.pen` files.
6. Treat Pencil output as a candidate design artifact. It still needs review before Figma, code, or production use.

## Safety Rules

- Do not store API keys, tokens, cookies, private URLs, private screenshots, or `.env` values in Pencil handoffs.
- Do not claim a Pencil tool ran unless a callable Pencil tool was used and an artifact path or tool response exists.
- If Pencil tooling is unavailable, produce a manual handoff and mark execution as `Skipped` or `Planned`.
- If Pencil output conflicts with accessibility, visible facts, SEO/LLM structure, or implementation feasibility, route to council.

## Handoff Shape

```text
Mode:
Approved direction:
Pencil tool availability:
Input artifacts:
Data excluded:
Prompt or canvas instructions:
Design-system constraints:
Review criteria:
Next owner:
Checks:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/pencil-design-bridge
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/pencil-design-bridge
python3 -m json.tool $CODEX_HOME/skills/pencil-design-bridge/evals/evals.json >/dev/null
```
