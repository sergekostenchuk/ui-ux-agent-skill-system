---
name: stitch-design-bridge
description: Use this skill when a UI/UX project should use Google Stitch or a Stitch MCP/API workflow for rapid AI UI exploration after `ui-ux-pro-max` has produced design intelligence and before Figma/code implementation. This skill turns UX, SEO/LLM, brand, accessibility, and Pro Max constraints into Stitch-ready prompts, evaluates Stitch outputs, prepares Figma/code handoff, checks Stitch API/MCP configuration without exposing secrets, and prevents Stitch from becoming a conflicting source of truth.
---

# Stitch Design Bridge

Use this skill as the Stitch layer in the UI/UX skill system. Stitch is an exploration accelerator, not the central architect, not the final design authority, and not the source of truth.

## Role In The System

Default sequence for substantial UI projects:

```text
task-plan-v2-orchestrator
-> ui-ux-llm-product-architect
-> seo-llm-site-architect when public discoverability matters
-> ui-ux-pro-max
-> stitch-design-bridge
-> senior-figma-orchestrator when Figma is involved
-> implementation specialist
-> validation
-> obsidian/wiki context capture for large projects
```

Stitch belongs after `ui-ux-pro-max` because Pro Max should define the design intelligence inputs: product type, style candidates, color/typography direction, UX risks, accessibility priorities, and stack guidance. Stitch then explores visual/screen variants under those constraints.

## Operating Modes

- `brief`: create a Stitch-ready prompt from project constraints.
- `variant-plan`: define several Stitch exploration directions and success criteria.
- `review-output`: critique Stitch outputs against UX, SEO/LLM, accessibility, brand, and implementation constraints.
- `figma-handoff`: prepare Stitch output for `senior-figma-orchestrator`.
- `code-handoff`: prepare Stitch output for local implementation.
- `config-check`: check local Stitch API/MCP readiness without printing secrets.
- `council`: run or prepare a senior UI/UX/SEO/LLM council decision when recommendations conflict.

## Required Workflow

1. Read [references/orchestration-contract.md](references/orchestration-contract.md) before routing Stitch inside the broader system.
2. For prompt generation or output review, read [references/prompt-quality-rubric.md](references/prompt-quality-rubric.md).
3. For API, MCP, credentials, or external upload decisions, read [references/safety-and-api.md](references/safety-and-api.md).
4. Confirm inputs available:
   - product/UX brief;
   - SEO/LLM constraints when public pages are involved;
   - `ui-ux-pro-max` recommendations;
   - brand constraints and forbidden directions;
   - target output: Stitch prompt, variants, Figma handoff, code handoff, or review.
5. If using an external Stitch service, record what data will be sent and require explicit approval for private project data.
6. Never include API keys, tokens, cookies, private URLs, private screenshots, or `.env` contents in prompts, reports, wiki pages, or task plans.
7. Treat Stitch output as a candidate artifact. It must be reviewed before Figma, code, or production use.

## API And MCP Credentials

Use environment variables. Do not store credentials in this skill.

Expected variable:

```bash
STITCH_API_KEY
```

Run the config checker when needed:

```bash
python3 $CODEX_SKILLS_DIR/stitch-design-bridge/scripts/check_stitch_config.py
```

The checker reports only presence, likely shape, and redacted metadata. It must not print the full key.

## Decision Rules

Stitch may propose:

- visual directions;
- layout variants;
- component arrangements;
- screen-level concepts;
- first-pass code or canvas ideas when available.

Stitch must not override:

- visible facts and business constraints;
- SEO/LLM content architecture;
- accessibility requirements;
- semantic HTML and deterministic action labels;
- security/privacy boundaries;
- Figma design-system tokens without review;
- final implementation validation.

## Senior Council Trigger

Use `council` mode when any of these are true:

- UX wants to simplify content but SEO/LLM needs visible semantic content.
- SEO/LLM wants content density that harms comprehension or conversion.
- Stitch output is visually strong but weak on accessibility, facts, or implementation feasibility.
- Figma design-system constraints conflict with Stitch output.
- A large project changes public pages, Figma, code, and SEO/LLM artifacts in one workflow.

Council roles:

- `UI/UX lead`: journeys, IA, hierarchy, accessibility, interaction quality.
- `SEO/LLM lead`: crawlability, schema, metadata, llms.txt, visible factual content.
- `Figma lead`: design-system fit, variables, components, asset workflow.
- `Implementation lead`: framework feasibility, responsive behavior, validation evidence.
- `Planning lead`: task-plan gates, blockers, alarms, evidence, rollback.

Decision order:

1. Security, privacy, legal accuracy, and user safety.
2. Accessibility and primary task completion.
3. Truthful visible content and product facts.
4. Semantic HTML, crawlability, and LLM-readable structure.
5. Conversion UX and user comprehension.
6. Design-system consistency and implementation maintainability.
7. Visual novelty, trend alignment, and Stitch aesthetics.

## Output Shapes

### Brief Mode

Use [assets/stitch-brief.template.md](assets/stitch-brief.template.md).

Return:

- Stitch prompt;
- input constraints used;
- private data excluded;
- variants requested;
- acceptance criteria;
- required review owners.

### Review Mode

Return:

- output reviewed;
- pass/fail against the prompt;
- UX findings;
- SEO/LLM findings;
- accessibility findings;
- design-system/Figma findings;
- implementation risks;
- recommendation: accept, iterate, send to Figma, implement locally, or reject.

### Handoff Mode

Return:

- chosen Stitch variant;
- rationale;
- required Figma/code next owner;
- assets or screenshots needed;
- tokens/components to preserve;
- checks before marking done.

## Validation

When editing this skill, run:

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/stitch-design-bridge
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/stitch-design-bridge
python3 $CODEX_SKILLS_DIR/stitch-design-bridge/scripts/check_stitch_config.py
python3 -m json.tool $CODEX_SKILLS_DIR/stitch-design-bridge/evals/evals.json >/dev/null
```
