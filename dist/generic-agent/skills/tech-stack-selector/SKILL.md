---
name: tech-stack-selector
description: Select or review the frontend/CMS/deployment stack for UI/UX site projects after concept definition and before design-to-code or launch work. Use when choosing between static HTML, React/Next/Vite, CMS/admin needs, Figma/Pencil handoff, SEO constraints, existing-site rebuild, or maintainability tradeoffs.
---

# Tech Stack Selector

This skill decides the implementation stack for UI/UX projects. It is advisory until a build task is created; it does not deploy or mutate infrastructure.

## Operating Modes

- `select`: choose a stack for a new site or app after concept.
- `review`: evaluate an existing stack against SEO, UX, editing, maintainability, and deployment needs.
- `migration`: recommend whether to keep, improve, or replace the current stack.

## Required Workflow

1. Read [references/stack-decision-framework.md](references/stack-decision-framework.md).
2. Gather product type, editing needs, content volatility, SEO/LLM requirements, interaction complexity, hosting constraints, and team skills.
3. Score viable options: static HTML, Vite/React, Next.js, Astro, CMS-backed, custom admin, or existing stack.
4. Recommend one stack, one fallback, and disqualified options with reasons.
5. Hand off to `marketing-site-skill`, `webapp-ui-skill`, `pencil-design-bridge`, or infra/launch skills as appropriate.

## Safety Rules

- Do not provision servers, buy domains, change DNS, or deploy production from this skill.
- Do not claim current package versions or vendor pricing without verifying if the user needs exact current facts.
- Prefer the simplest stack that satisfies SEO, content editing, performance, and maintainability.

## Output Shape

```text
Recommended stack:
Fallback stack:
Disqualified options:
Why this fits:
SEO/LLM implications:
Editing/admin implications:
Deployment implications:
Risks:
Next skill:
```

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/tech-stack-selector
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/tech-stack-selector
```
