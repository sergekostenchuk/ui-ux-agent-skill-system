---
name: semantic-core-builder
description: Build an evidence-labeled semantic core and crawlable site structure from keyword harvests, existing content, or user-provided search-demand data. Use before SEO/LLM site architecture, concept prototypes, paid traffic planning, IA, or public-site redesign decisions.
---

# Semantic Core Builder

This skill turns raw keyword/search inputs into a structured semantic core. It hands the result to `seo-llm-site-architect`, `concept-prototyper`, and later design/implementation skills.

## Operating Modes

- `build`: create `reports/semantic-core.json` and `docs/site-structure.md`.
- `merge`: merge existing-site keywords, user-provided terms, and harvested demand.
- `audit`: review a semantic core for missing provenance, duplicate clusters, or weak intent mapping.

## Required Workflow

1. Read [references/semantic-core-contract.md](references/semantic-core-contract.md).
2. Load `reports/keyword-harvest.json` or a user-provided equivalent.
3. Cluster keywords by intent and topic; label any LLM grouping as `Inference`.
4. Produce cluster records: intent, priority, canonical URL candidate, page type, evidence, and confidence.
5. Write machine-readable `reports/semantic-core.json` and human-readable `docs/site-structure.md`.
6. Hand off to `concept-prototyper` and `seo-llm-site-architect`.

## Safety And Evidence

- Do not invent search volume or SERP facts.
- If no real SERP/source evidence exists, label the output as `Manual` or `Inference`.
- Do not bury conflicts; record cannibalization, unclear intent, or missing evidence.

## Handoff Shape

```text
Input path:
Clusters:
High-priority URLs:
Conflicts:
Evidence gaps:
Output paths:
Next skills: concept-prototyper, seo-llm-site-architect
```

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/semantic-core-builder
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/semantic-core-builder
```
