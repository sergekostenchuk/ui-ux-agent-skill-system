---
name: figma-design-system-sync
description: Sync and audit design-system contracts between Figma and code. Use this skill when the user asks about Figma Variables, styles, tokens, component libraries, variants, Code Connect, effect styles, naming drift, token exports/imports, library governance, or keeping implementation and Figma design systems aligned under the UI/UX skill system.
---

# Figma Design System Sync

Use this skill when Figma work touches reusable system contracts: variables, styles, components, variants, effects, assets, Code Connect, and local code tokens.

## Modes

- `audit`: compare Figma system artifacts to local code conventions.
- `sync-plan`: plan variable/style/component updates.
- `token-map`: map Figma variables to local tokens.
- `component-map`: map components and variants to code components.
- `code-connect`: create or review Code Connect files through the installed Figma skill.
- `governance`: propose naming, versioning, and rollout rules.

## Workflow

1. Read Figma context with `figma-context-reader` unless a current context brief exists.
2. Inspect the local code tokens/components before recommending sync actions.
3. If Code Connect is requested, invoke `figma:figma-code-connect` when present.
4. Build a diff: Figma source, code target, status, risk, and proposed change.
5. For mutations, route to `figma-canvas-editor` or `figma-apply-effects` with explicit scope.
6. Validate JSON/token outputs locally before treating them as evidence.

## Guardrails

- Do not rename or delete variables/components/styles without a migration map.
- Do not treat generated code or generated variables as source of truth until reviewed.
- Record which direction is authoritative for each artifact: Figma to code, code to Figma, or reconcile manually.
- Keep variable binding promises compatible with current Figma Plugin API support.

## Safety And Privacy

- Treat unpublished tokens, library names, component inventories, and source component code as sensitive.
- Do not push variable/component renames without an explicit migration map and rollback path.
- Do not upload private token exports or component snapshots to external services without approval.

## Output Shape

Use [assets/design-system-sync-report.md](assets/design-system-sync-report.md).

## Resources

- Read `$CODEX_SKILLS_DIR/senior-figma-orchestrator/references/figma-mcp-compatibility.md` for current capability checks.
