---
name: visual-content-director
description: Plan and govern images, video, generated visuals, hero media, asset sourcing, visual proof, and content-media fit for UI/UX projects. Use when a site or app needs premium visual direction, photo/video asset plans, generated imagery prompts, before/after media, or visual asset QA before implementation, Stitch, Pencil, Figma, or code handoff.
---

# Visual Content Director

This skill owns the visual-content layer: what images, videos, generated visuals, and asset treatments are needed to make a UI believable, inspectable, and on-brand. It does not own final UX strategy or SEO structure.

## Operating Modes

- `asset-plan`: define required images, videos, icons, maps, diagrams, and proofs.
- `hero-media`: specify first-viewport media and composition rules.
- `generation-brief`: create prompts for generated visuals without inventing factual claims.
- `asset-qa`: check whether assets are relevant, readable, aligned, and safe to use.
- `handoff`: package assets for Stitch, Pencil, Figma, or implementation.

## Required Workflow

1. Read [references/visual-content-contract.md](references/visual-content-contract.md).
2. Confirm project type, target audience, user promise, and brand constraints.
3. Identify required content media:
   - real product/place/person/object proof;
   - generated or illustrative support;
   - maps, diagrams, icons, before/after, galleries, video.
4. Use [assets/visual-content-plan.template.md](assets/visual-content-plan.template.md) for planning.
5. Distinguish real evidence assets from generated mood or placeholder assets.
6. Hand off exact media requirements to Stitch, Pencil, Figma, or code owners.

## Safety Rules

- Do not fabricate real places, people, testimonials, property facts, awards, certifications, or legal claims.
- Do not use private images externally without approval.
- Label generated visuals as generated/planned if they are not real source evidence.
- For reveal, before/after, or layered media, route alignment checks to `image-layer-alignment-validator`.
- Public websites must keep important facts as text, not only baked into images.

## Handoff Shape

```text
Visual mode:
Asset roles:
Real evidence assets:
Generated/planned assets:
Hero media direction:
Forbidden visuals:
Accessibility notes:
SEO/LLM text preservation:
Next owner:
Checks:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/visual-content-director
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/visual-content-director
python3 -m json.tool $CODEX_HOME/skills/visual-content-director/evals/evals.json >/dev/null
```
