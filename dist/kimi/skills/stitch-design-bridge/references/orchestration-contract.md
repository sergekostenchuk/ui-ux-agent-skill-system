# Stitch Orchestration Contract

## Position

Stitch is an exploration layer between design intelligence and production design.

Correct position:

```text
Pro Max recommendation -> Stitch exploration -> Figma/code handoff -> validation
```

Incorrect positions:

- first step before product/UX framing;
- final authority after generation;
- replacement for Figma design-system sync;
- replacement for SEO/LLM architecture;
- replacement for browser validation.

## Required Inputs

Minimum useful Stitch input:

- project goal;
- target audience and primary journey;
- product type and domain;
- required visible facts;
- forbidden claims;
- SEO/LLM constraints for public pages;
- Pro Max style/pattern/color/typography signals;
- accessibility constraints;
- target platform and stack;
- number of variants requested.

If these are missing, create a brief first instead of asking Stitch for generic UI.

## Three-Variant Input Contract

For a three-variant design workflow, Stitch receives approved direction briefs from `senior-ui-ux-orchestrator`; it does not invent the final three strategic directions alone.

Each direction brief should include:

- direction name;
- user promise;
- style code;
- palette and typography intent;
- content hierarchy;
- required visible facts;
- SEO/LLM constraints;
- accessibility constraints;
- Figma/code risks;
- validation criteria.

Stitch may explore layout and visual expression inside each approved direction. If Stitch finds a stronger fourth idea, report it as an optional suggestion, not as a replacement for the agreed three-direction plan.

## Handoff Contract

Stitch output must be converted into a handoff packet before downstream work:

- variant name;
- screenshot or artifact path if available;
- prompt used;
- constraints preserved;
- constraints violated;
- recommended next owner;
- required validation checks;
- unresolved risks.

## Conflict Rules

When Stitch conflicts with another skill:

- UX journey beats visual novelty.
- Visible facts beat compactness.
- SEO/LLM source of truth beats hidden or image-only content.
- Figma variables/components beat arbitrary visual styling when design-system sync matters.
- Browser evidence beats generated preview.

## Large Project Wiki Capture

For large projects, write a compact context pack to the Obsidian/LLM wiki after major decisions:

- final accepted Stitch direction;
- rejected directions and why;
- UX/SEO/Figma constraints that mattered;
- artifact paths;
- validation caveats.

Do not store API keys, private screenshots, private URLs, or secrets in wiki pages.
