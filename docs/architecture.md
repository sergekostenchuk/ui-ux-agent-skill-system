# Architecture

## Core Principle

`senior-ui-ux-orchestrator` is the chair. Other skills provide expert input or execute a bounded stage. They do not compete for final authority.

The system is vendor-neutral at the core-contract level: roles, routing, reporting, evals, gates, and validation are portable. Runtime adapters and integrations such as Figma MCP and Google Stitch are optional vendor-specific execution paths.

```text
user request
-> senior-ui-ux-orchestrator
-> task-plan gate when project is large or multi-step
-> product/UX architecture
-> SEO/LLM constraints when public discoverability matters
-> UI/UX Pro Max advisory search
-> orchestrator selects one or three directions
-> senior council when skills conflict
-> optional Stitch exploration when useful and available
-> optional Figma gate only when a Figma artifact is required
-> implementation specialist
-> audit, critic, browser/semantic validation
-> local report or wiki capture
```

## Skill Authority Model

| Layer | Authority |
|---|---|
| `senior-ui-ux-orchestrator` | final routing, conflict resolution, scope, privacy, evidence |
| `task-plan-v2-orchestrator` | canonical planning, gates, task status, handoffs |
| `ui-ux-llm-product-architect` | journeys, IA, UX logic, accessible interaction |
| `seo-llm-site-architect` | crawlability, schema, metadata, LLM-readable public site architecture |
| `ui-ux-pro-max` | searchable design intelligence and style candidates |
| `stitch-design-bridge` | optional Stitch prompts, output review, Figma/code handoff |
| `senior-figma-orchestrator` | optional Figma MCP routing, variables, canvas, design-system sync |
| `marketing-site-skill` | public pages, landing pages, conversion pages |
| `webapp-ui-skill` | dashboards, SaaS, admin, data-heavy UI |
| `ux-audit-skill` | evidence-backed UX audits |
| `design-critic-skill` | visual-quality critique and fix briefs |
| `cursor-reveal-hero` | cursor reveal/masking hero effects |
| `image-layer-alignment-validator` | local raster layer alignment checks |

## Council Rule

Use a council only when there is a real cross-domain conflict or a large project. Final decision is not majority vote. Priority order:

1. Security, privacy, legal, user safety.
2. Accessibility and primary user task.
3. Truthful visible facts.
4. Semantic HTML, crawlability, LLM-readable structure.
5. Conversion UX and user comprehension.
6. Figma/design-system consistency when Figma is part of the project.
7. Maintainability.
8. Visual novelty and AI-generated aesthetics.

## Three-Variant Design Rule

Three directions are selected by the orchestrator after UX, SEO, and Pro Max inputs:

```text
UX/product brief
-> SEO/LLM constraints
-> Pro Max style candidates
-> orchestrator selects exactly three directions
-> council checks conflicts
-> Stitch explores if useful and available
-> Figma or code implementation
```

Stitch output is a candidate, not the final design. If Stitch is unavailable, the orchestrator can still produce the three directions as briefs, code implementations, or Figma-independent design specs.
