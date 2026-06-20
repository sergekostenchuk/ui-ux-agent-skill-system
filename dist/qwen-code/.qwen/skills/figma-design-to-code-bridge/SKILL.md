---
name: figma-design-to-code-bridge
description: Translate Figma frames and design context into implementation-ready frontend plans, component mappings, and code handoffs. Use this skill when a user wants to build from a Figma frame, compare Figma components to code components, use Code Connect, avoid pixel-copying, map variables to tokens, or decide whether work belongs in webapp-ui-skill, marketing-site-skill, or a local code implementation.
---

# Figma Design To Code Bridge

Use this skill after `figma-context-reader` when the goal is implementation. The output is not "code by screenshot"; it is a mapping from design intent, tokens, and components to the existing codebase.

## Modes

- `handoff-plan`: create a build/refactor plan from a Figma frame.
- `component-map`: map Figma components/variants to existing code components.
- `code-connect`: prepare or review Figma Code Connect work.
- `gap-report`: identify where the design and code system diverge.
- `implementation-route`: hand off to `webapp-ui-skill` or `marketing-site-skill`.

## Workflow

1. Get Figma context through `figma-context-reader` or a provided context brief.
2. Inspect the local codebase before recommending component choices.
3. If Code Connect is requested, invoke the installed `figma:figma-code-connect` skill before Code Connect-specific work.
4. Map tokens, components, variants, states, and responsive constraints to local implementation primitives.
5. Route dense product/app work to `webapp-ui-skill`; route public landing/product pages to `marketing-site-skill`.
6. Require local visual verification after implementation. Figma match alone is not validation.

## Output Shape

Use [assets/design-to-code-handoff.md](assets/design-to-code-handoff.md).

## Decision Rules

- Prefer existing project components and design tokens over generating one-off CSS.
- Preserve UX intent when exact visual parity conflicts with accessibility, responsiveness, or codebase conventions.
- Treat Figma-generated code or MCP-generated code as a draft until reviewed against local architecture.
- If the Figma file lacks states, include loading, empty, error, disabled, focus, hover, and mobile states in the implementation plan.

## Safety And Privacy

- Treat non-public Figma files, screenshots, variables, component names, and source code as sensitive.
- Do not send private code or Figma context to external tools without explicit approval and a data-transfer note.
- Do not overwrite local components simply to match a Figma frame; propose a scoped implementation plan first.

## Validation And Eval

- Verify that the handoff includes both Figma-to-code component mapping and local validation steps.
- For implemented work, require browser or screenshot evidence from the local app.
- Use `evals/evals.json` to test app-frame routing, marketing-page routing, and Code Connect gap behavior.

## Resources

- Read `$CODEX_SKILLS_DIR/senior-figma-orchestrator/references/figma-mcp-compatibility.md` when current Figma tools matter.
