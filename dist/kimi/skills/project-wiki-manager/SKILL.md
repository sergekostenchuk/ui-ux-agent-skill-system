---
name: project-wiki-manager
description: Manage sanitized project memory and Obsidian/LLM wiki gates for large UI/UX, SEO, Figma, Stitch, progress-screen, skill-system, migration, launch, or multi-session agent projects. Use when a project needs durable context, llms-context packs, decision capture, handoff notes, or wiki sync without storing secrets.
---

# Project Wiki Manager

This skill is the project-memory coordinator for the UI/UX Agent Skill System. It decides what should be captured, what must stay out, which wiki backend skill to call, and how downstream agents should consume the resulting context.

## Operating Modes

- `init`: create the project memory plan and required wiki artifact map before a large project starts.
- `capture`: capture sanitized decisions, artifacts, constraints, and blockers after a major decision or delivery step.
- `context-pack`: prepare a compact context pack for the next agent or future session.
- `sync`: update existing wiki pages after task-plan, design, SEO, Figma, or launch changes.
- `audit`: check whether project memory is stale, secret-bearing, duplicated, or missing important decisions.
- `handoff`: produce a final sanitized handoff with exact artifact paths and next owners.

## Required Workflow

1. Classify project scale:
   - `small`: one localized task; wiki capture optional.
   - `medium`: several files, one workflow, or one design direction; capture only major decisions.
   - `large`: multi-session, multi-skill, SEO/UI/Figma/Stitch/infra, migration, or launch work; wiki gate required.
2. Read [references/wiki-gate-contract.md](references/wiki-gate-contract.md).
3. Read [references/sanitization-policy.md](references/sanitization-policy.md) before writing or ingesting any artifact.
4. If creating a new project memory map, use [assets/project-memory-map.template.md](assets/project-memory-map.template.md).
5. Choose backend:
   - `wiki-capture` for current conversation decisions.
   - `obsidian-wiki-ingest` / `wiki-ingest` for existing documents and reports.
   - `wiki-context-pack` for a compact context slice for the next agent.
   - `wiki-query` for answering from stored project knowledge.
6. Record exact source artifact paths, decision date, owner role, evidence status, and excluded sensitive data.
7. Never store secrets, tokens, cookies, `.env` values, recovery codes, private screenshots, or private URLs unless the user explicitly approves that exact storage.

## Capture Triggers

Require a wiki gate when any trigger is true:

- The project uses `senior-ui-ux-orchestrator` plus two or more specialist skills.
- A three-variant design, council decision, migration, Figma handoff, Stitch output review, launch plan, or publication release is accepted.
- A progress-screen user gate records an accepted design choice, approval, blocker resolution, or launch confirmation that future agents must remember.
- The project spans multiple sessions or has a TASK-PLAN with open tasks.
- A future agent will need context that is not obvious from the current file tree.
- The user explicitly says not to lose context.

Skip or defer capture for tiny one-off edits, throwaway experiments, or artifacts containing unsanitized secrets.

## Artifact Contract

Capture only durable facts:

- project goal and audience;
- accepted and rejected decisions;
- source documents and exact artifact paths;
- UX/SEO/Figma/Stitch/implementation constraints;
- progress-screen decisions, user gates, and accepted comments after sanitization;
- validation evidence and skipped checks;
- open blockers and next owners;
- approved context packs for downstream agents.

Do not capture:

- raw tokens, passwords, recovery codes, session cookies, private keys, `.env` values;
- private URLs or screenshots without explicit storage approval;
- unverified claims as facts;
- large duplicate source text that should stay in the original artifact.

## Reporting Shape

```text
Wiki mode:
Project scale:
Source artifacts:
Backend skill/tool:
Captured facts:
Excluded sensitive data:
Context pack path:
Updated wiki pages:
Checks run:
Next owner:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/project-wiki-manager
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/project-wiki-manager
```
