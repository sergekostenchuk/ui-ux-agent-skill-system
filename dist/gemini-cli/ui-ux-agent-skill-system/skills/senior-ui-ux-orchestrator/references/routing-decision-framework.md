# Routing Decision Framework

## First Classification

Ask what the user is trying to change or understand:

- Build or refactor an application screen.
- Build or refactor a public marketing page.
- Audit an existing artifact.
- Critique visual quality.
- Work with Figma context, MCP, canvas, assets, effects, or design-system sync.
- Explore design intelligence, style options, palette, typography, patterns, or visual precedents.
- Create three distinct design directions or several alternative versions.
- Use Stitch, Google Stitch, or AI UI generation after design directions are defined.
- Resolve cross-skill conflict through a senior UI/UX/SEO/LLM council.
- Capture durable project context in the Obsidian/LLM wiki.
- Build an interactive cursor/mask reveal effect.
- Validate two image layers before a reveal/morph/compositing effect.
- Plan or validate the skill system itself.

Prefer the most specific specialist. Use multiple specialists only when the workflow naturally has phases, such as audit first and implementation second.

## Inputs To Identify

- Artifact type: codebase, URL, screenshot, Figma frame, text brief, task plan.
- Product surface: application workflow, marketing page, audit target, critique target.
- Privacy mode: local-only, public URL, approved external upload.
- Evidence available: source files, screenshots, browser access, reports.
- Desired output: implementation, task plan, audit findings, fix brief, validation report.
- Project scale: small/local edit, medium workflow, large multi-session system.
- External generation boundary: whether Stitch or another cloud design tool is approved and what data may be sent.
- Council need: whether UX, SEO/LLM, Figma, Stitch, implementation, or accessibility constraints conflict.

## Routing Matrix

| Signal | Route |
| :-- | :-- |
| SaaS, admin, dashboard, CRM, internal tool, data table, settings flow | `webapp-ui-skill` |
| Landing, product page, campaign, brand, venue, conversion, metadata | `marketing-site-skill` |
| URL audit, screenshot audit, source audit, Figma audit, regression | `ux-audit-skill` |
| Polish, hierarchy, taste, consistency, anti-slop, visual critique | `design-critic-skill` |
| Design intelligence, style candidates, color, typography, layout patterns, precedent signals | `ui-ux-pro-max` |
| Three design variants, three directions, multiple versions before production | `senior-ui-ux-orchestrator` in `three-variant-design` mode, supported by `ui-ux-pro-max` then `stitch-design-bridge` |
| Stitch, Google Stitch, Stitch prompt, AI UI variants, generated UI review | `stitch-design-bridge` |
| Senior council, consilium, UX vs SEO conflict, Figma vs code conflict, Stitch conflict | `senior-ui-ux-orchestrator` in `council` mode |
| Large project memory, multi-session context, wiki ingest, Obsidian capture | `obsidian-wiki-ingest` or wiki layer after sanitized decision artifacts exist |
| Figma MCP, Figma URL, selected node, variables, Code Connect, code-to-canvas, canvas edits, assets, effects | `senior-figma-orchestrator` |
| Cursor reveal, mouse trail, hover reveal, soft mask, canvas compositing | `cursor-reveal-hero` |
| Base/reveal image pair, layer alignment, before/after drift, morph suitability | `image-layer-alignment-validator` |
| Creating or validating this skill group | `senior-ui-ux-orchestrator` plus skill architecture workflow |

## Ambiguity Rules

- If the user asks for "UI" without artifact type, infer from nearby words. Dashboard and workflow terms mean webapp; offer and conversion terms mean marketing.
- If a screenshot is the only artifact, do not claim DOM, Lighthouse, axe, or runtime evidence.
- If a URL is private or authenticated, keep work local and avoid external services.
- If optional cloud tools are requested, ask for approval before upload and record what data will be sent.
- If the task asks for three variants, do not route directly to Stitch. First define product/UX and SEO/LLM constraints, use `ui-ux-pro-max` for design intelligence, then curate exactly three directions under the chair.
- If Stitch is requested, use it after approved design directions or a clear brief. Treat its output as a candidate artifact that needs review.
- If specialist recommendations conflict, convene the council rather than letting the last-used skill override earlier constraints.
- If a project is large or multi-session, add a wiki capture gate after decisions are sanitized.
- If the task mentions Figma plus a concrete Figma operation, route to `senior-figma-orchestrator` first, then to audit/build specialists as a second phase.
- If the task mentions cursor reveal or mask compositing, do not route to Figma effects unless the target is explicitly a Figma node effect.
- If the user provides two images for a reveal effect, validate layer alignment before tuning frontend compositing.

## Handoff Requirements

Every route decision should include:

- chosen skill;
- why that skill fits;
- inputs needed;
- checks to run;
- checks that cannot run yet;
- privacy mode;
- expected artifacts.
