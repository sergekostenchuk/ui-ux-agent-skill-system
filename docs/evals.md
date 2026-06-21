# Evals

The current eval layer is deterministic and local. It does not call an LLM judge
and does not claim to measure final visual quality.

## Layer 1: Route Evals

`npm run eval` checks prompt routing against the bundled
`senior-ui-ux-orchestrator` classifier.

It catches regressions such as:

- marketing prompts routing to dashboard skills;
- Figma prompts skipping the Figma orchestrator;
- three-variant design prompts skipping the orchestrator/council flow;
- secret-handling prompts losing the Stitch safety route.

## Layer 2: Eval Contract Coverage

`npm run check:eval-contracts` checks that top-level eval cases include:

- `expected_route`;
- non-empty `must_have`;
- non-empty `must_not_have`;
- coverage for accessibility, validation evidence, privacy, and truthful content.

This makes future artifact-level evals easier because each case already has
explicit acceptance and rejection constraints.

## Not Yet Covered

These checks do not score final UI taste, screenshot quality, implemented HTML,
accessibility trees, schema output, or generated audit quality.

Those should be added as artifact-level evals, for example:

- Playwright screenshot checks for representative generated pages;
- accessibility scans for rendered fixtures;
- schema and metadata parse checks;
- report contract validation for generated UX/SEO audits;
- screenshot diff or visual review gates for selected examples.
