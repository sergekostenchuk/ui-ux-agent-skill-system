---
name: marketing-site-skill
description: Build, refactor, audit, and validate marketing websites and public product pages. Use this skill whenever the user asks for landing pages, product pages, brand pages, venue pages, campaign pages, conversion flows, hero sections, CTA hierarchy, social proof, metadata, responsive storytelling, media-heavy public pages, SEO-facing UI, or launch pages. Do not use for private dashboards, admin panels, CRM screens, or dense app workflows.
---

# Marketing Site Skill

Use this specialist for public-facing pages where the first viewport, product/place/person signal, conversion path, media quality, metadata, and responsive behavior matter.

## Operating Modes

- `build`: create or refactor a marketing/public page.
- `audit`: review a page for conversion, metadata, responsive behavior, and visual clarity.
- `metadata`: inspect title, description, canonical, Open Graph, Twitter, headings, and social preview basics.
- `verify`: run local checks and distinguish evidence from manual review.

## Required Workflow

1. Read [references/hero-first-viewport.md](references/hero-first-viewport.md) before designing the top of the page.
2. Read [references/conversion-framework.md](references/conversion-framework.md) for CTA and proof decisions.
3. Read [references/metadata-checklist.md](references/metadata-checklist.md) when source files or HTML are available.
4. Use [assets/landing-brief.template.md](assets/landing-brief.template.md) and [assets/metadata.template.json](assets/metadata.template.json) when producing durable page briefs or metadata specs.
5. Apply `../../shared/privacy-policy.md` before using external images, AI page builders, or cloud tools.
6. If source files are available, run [scripts/lint_metadata.py](scripts/lint_metadata.py) or report why it was skipped.
7. If a URL is available, run [scripts/responsive_smoke_test.mjs](scripts/responsive_smoke_test.mjs) or report why it was skipped.
8. Return `Ran`, `Skipped`, `Planned`, and `Manual` sections.

## Design Doctrine

- The first viewport must show the product, place, offer, brand, object, or person clearly.
- Do not hide the real subject inside a decorative card or generic gradient.
- Use real or generated bitmap media when a visual signal is needed.
- Keep CTA hierarchy obvious and avoid many visually equal primary actions.
- Keep mobile text readable and avoid overlap, horizontal overflow, and viewport-scaled font tricks.

## Tool Contracts

- Metadata lint: `python3 scripts/lint_metadata.py --root "$PROJECT_ROOT" --out reports/metadata.json`.
- Responsive smoke: `node scripts/responsive_smoke_test.mjs --url "$URL" --out reports/visual-smoke`.
- Optional cloud tools require explicit approval and cannot be validation evidence by themselves.

## Validation

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/marketing-site-skill
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/marketing-site-skill
```

## Output Shape

```text
Page type:
Primary offer or object:
First viewport:
CTA path:
Metadata:
Ran:
Skipped:
Manual findings:
Risks:
```
