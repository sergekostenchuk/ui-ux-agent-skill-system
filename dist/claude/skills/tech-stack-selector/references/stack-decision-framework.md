# Stack Decision Framework

## Required Inputs

- product type: marketing site, web app, hybrid, existing-site redesign;
- content editing needs;
- SEO/LLM-readability requirements;
- interactivity and data needs;
- Figma/Pencil/design-to-code expectations;
- deployment and hosting constraints;
- team skill and maintenance expectations.

## Decision Order

1. Must satisfy user journey and content editing needs.
2. Must preserve semantic HTML, crawlability, performance, and accessibility.
3. Must be maintainable by the expected owner.
4. Should minimize deployment complexity.
5. May use heavier frameworks only when the product needs them.

## Common Fits

- Static HTML: small brochure/landing, low editing frequency, fastest handoff.
- Vite/React: interactive frontend without server rendering needs.
- Next.js/Astro: structured content, SEO, routing, componentized public sites.
- CMS-backed: frequent non-developer editing.
- Existing stack: keep when migration risk exceeds benefits.
