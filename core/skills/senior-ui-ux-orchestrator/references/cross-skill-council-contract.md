# Cross-Skill Council Contract

## Purpose

The council is a lightweight governance mechanism for large or conflicted UI/UX workflows. It is not another orchestrator. `senior-ui-ux-orchestrator` remains the chair and final cross-domain decision owner.

Use the council to prevent specialist skills from competing for control when product UX, SEO/LLM, Figma, Stitch, implementation, accessibility, or project-memory needs collide.

## Trigger Conditions

Convene the council when any condition is true:

- The project is large or multi-session.
- The user asks for three distinct design variants or strategic design directions.
- A public site needs UI/UX, SEO/LLM, content architecture, and visual design decisions together.
- `ui-ux-pro-max`, Stitch, Figma, SEO, or implementation recommendations conflict.
- Stitch output looks visually strong but weak on facts, accessibility, SEO/LLM structure, Figma consistency, or implementation feasibility.
- A release-facing decision requires validation evidence before handoff.
- The user explicitly asks for a senior council, consilium, or cross-skill coordination.

Skip the council for small localized edits unless there is a real conflict.

## Roles

| Role | Default Skill | Authority |
| :-- | :-- | :-- |
| Chair / Central Architect | `senior-ui-ux-orchestrator` | Owns routing, scope, final cross-domain decision, and handoff shape. |
| Product UX Lead | `ui-ux-llm-product-architect` | Owns journeys, IA, task success, comprehension, accessibility intent, and interaction quality. |
| SEO/LLM Lead | `seo-llm-site-architect` | Owns crawlability, semantic structure, metadata, schema, llms.txt, visible factual content, and AI-search readability. |
| Design Intelligence Lead | `ui-ux-pro-max` | Supplies searchable design intelligence: patterns, style candidates, color/type signals, risks, and precedent-informed options. |
| Stitch Exploration Lead | `stitch-design-bridge` | Converts approved directions into Stitch-ready prompts, reviews Stitch outputs, and prepares handoffs. |
| Figma Lead | `senior-figma-orchestrator` | Owns Figma context, components, variables, canvas edits, assets, and design-system sync. |
| Implementation Lead | `marketing-site-skill` or `webapp-ui-skill` | Owns local code feasibility, responsive behavior, browser verification, and implementation evidence. |
| Planning Secretary | `task-plan-v2-orchestrator` | Owns task-plan state, gates, blockers, validation records, and progress visibility. |
| Wiki Context Keeper | `obsidian-wiki-ingest` or wiki layer | Captures sanitized decisions and durable context for large projects. |

Add a security, privacy, legal, or accessibility specialist only when the project risk requires it.

## Rounds

Default council flow:

1. `Round 0 - Intake`: chair states goal, artifact state, project size, privacy mode, known constraints, and the specific decision needed.
2. `Round 1 - Independent Positions`: each needed role gives a short position with recommendation, risks, must-preserve constraints, compromise options, and required evidence.
3. `Round 2 - Conflict Resolution`: run only if positions conflict. The chair isolates conflicts and asks only affected roles for revised options.
4. `Round 3 - Final Decision`: run only if a material conflict remains. The chair decides, records accepted tradeoffs, rejected options, owner, next action, and validation gate.

Maximum normal depth is three decision rounds after intake. Do not keep looping. If evidence is missing, mark the decision as `Planned` or `Blocked by evidence` instead of inventing certainty.

Small tasks may use a one-round mini-council: chair plus one specialist position and a final decision.

## Decision Model

The council is not a democratic majority vote.

- Domain owners decide within their domain unless a higher-priority constraint overrides them.
- The chair resolves cross-domain tradeoffs using the decision order below.
- Vetoes are allowed for security, privacy, legal accuracy, user safety, accessibility blockers, and factual correctness.
- Stitch and `ui-ux-pro-max` are advisory/exploration inputs, not final authorities.
- Browser, source, Figma readback, schema parse, screenshot, and other real evidence beat generated previews.

Decision order:

1. Security, privacy, legal accuracy, and user safety.
2. Accessibility and primary task completion.
3. Truthful visible facts and product constraints.
4. Semantic HTML, crawlability, and LLM-readable structure.
5. Conversion UX and user comprehension.
6. Design-system and Figma consistency.
7. Implementation maintainability and validation cost.
8. Visual novelty, trend fit, and Stitch aesthetics.

## Required Council Output

Return or record:

- decision name;
- active roles;
- final decision;
- owner of next action;
- accepted tradeoffs;
- rejected options and why;
- required evidence;
- downstream skill handoff;
- wiki capture decision for large projects;
- checks marked `Ran`, `Skipped`, `Planned`, or `Manual`.

## Three-Variant Design Workflow

Use this workflow when the user asks for several design versions, alternatives, directions, or a Klimovo-style multi-version exploration.

Ownership:

- Chair: `senior-ui-ux-orchestrator`.
- Product framing: `ui-ux-llm-product-architect`.
- SEO/LLM constraints for public sites: `seo-llm-site-architect`.
- Candidate style intelligence: `ui-ux-pro-max`.
- Rendering/exploration after approval: `stitch-design-bridge`.
- Figma handoff when needed: `senior-figma-orchestrator`.
- Code handoff: `marketing-site-skill` or `webapp-ui-skill`.

Process:

1. Frame the product, audience, primary journey, conversion goal, content hierarchy, and required facts.
2. Ask `ui-ux-pro-max` for design intelligence and candidate styles. It proposes signals; it does not choose final directions alone.
3. The chair curates exactly three meaningfully different directions using product, SEO/LLM, brand, content, assets, feasibility, and validation constraints.
4. Each direction must include:
   - direction name;
   - user promise;
   - style code;
   - palette and typography intent;
   - content hierarchy;
   - required visible facts;
   - SEO/LLM constraints;
   - Figma/code risks;
   - Stitch prompt seed;
   - validation criteria.
5. Run a council check if directions conflict with SEO/LLM, accessibility, Figma, or implementation constraints.
6. Send only approved direction briefs to `stitch-design-bridge` for Stitch prompts or variants.
7. Review Stitch outputs before sending anything to Figma or code.
8. Capture final accepted and rejected directions in the wiki for large projects.

## Wiki Capture Gate

For large or multi-session projects, capture a compact context pack after major decisions:

- accepted design direction and rationale;
- rejected directions and rationale;
- UX/SEO/Figma/Stitch constraints that mattered;
- artifact paths;
- validation caveats;
- next owner and open blockers.

Never store API keys, tokens, cookies, `.env` contents, private URLs, private screenshots, or confidential data unless the user explicitly approves the specific data transfer and storage.
