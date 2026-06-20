# Near-Miss Prompts

Use these cases to avoid over-triggering or wrong routing.

## Should Not Route To Webapp

- "Make a landing page for a new AI writing tool." Route to `marketing-site-skill`.
- "Review this hero section screenshot for visual polish." Route to `design-critic-skill`.
- "Audit this public URL for accessibility and conversion blockers." Route to `ux-audit-skill`.

## Should Not Route To Marketing

- "Refactor our billing settings screen." Route to `webapp-ui-skill`.
- "Build a dense operator dashboard with filters and tables." Route to `webapp-ui-skill`.
- "Create empty/loading/error states for an admin panel." Route to `webapp-ui-skill`.

## Evidence Boundaries

- Screenshot-only input cannot produce DOM, Lighthouse, or axe claims.
- A planned script cannot be used as evidence.
- Cloud generation output is a draft, not validation.
- Browser screenshots from authenticated products are sensitive artifacts.
- Figma context is design evidence, not runtime implementation evidence.
- Figma code-to-canvas or canvas mutation claims require tool evidence and readback.
- Cursor reveal frontend work is not the same as Figma `GLASS`, `NOISE`, `TEXTURE`, blur, or shadow effects.

## Optional Cloud Boundaries

Do not invoke v0, Framer, Stitch, Unsplash, Attention Insight, Khroma, or any external upload path unless the user explicitly approves the service and data transfer.

## Figma Near Misses

- "Audit this Figma frame for UX problems." Route to `ux-audit-skill` with `figma-context-reader` evidence, not direct canvas editing.
- "Implement this selected Figma app frame." Route to `senior-figma-orchestrator` first, then `webapp-ui-skill`.
- "Add a glow to this selected Figma node." Route to `senior-figma-orchestrator` then `figma-apply-effects`.
- "Make a mouse trail reveal on this website." Route to `cursor-reveal-hero`, not `figma-apply-effects`.
- "Check if these two reveal images line up." Route to `image-layer-alignment-validator`, not visual critique only.
