---
name: figma-code-to-canvas
description: Bring live or local web UI back into Figma as editable design layers when Figma MCP code-to-canvas or generate-design capability is available. Use this skill when the user says production, staging, localhost, or a browser-rendered page is ahead of Figma and wants to sync, capture, recreate, or convert the live UI into a Figma file while preserving privacy and evidence.
---

# Figma Code To Canvas

Use this skill for the reverse direction: code or browser UI into Figma canvas. This is tool-availability-sensitive and privacy-sensitive.

## Modes

- `capture-local`: convert a local dev server page into Figma layers.
- `capture-public`: convert a public URL into Figma layers.
- `capture-private`: plan a safe path for authenticated/staging pages.
- `reconcile`: compare generated Figma layers with the source UI and list drift.
- `fallback`: produce manual rebuild instructions when code-to-canvas tools are unavailable.

## Workflow

1. Confirm URL/app source, viewport, target Figma file/page, and privacy class.
2. For local pages, start or verify the dev server and capture a screenshot before Figma generation.
3. If code-to-canvas or generated design is requested, invoke the installed `figma:figma-generate-design` skill when present.
4. Do not send private authenticated pages, cookies, customer data, or internal URLs through remote services without explicit approval.
5. After generation, read back Figma metadata or capture a Figma screenshot when possible.
6. Produce a reconciliation report: source URL, viewport, generated target, visible mismatches, and follow-up edits.

## Output Shape

Use [assets/code-to-canvas-report.md](assets/code-to-canvas-report.md).

## Fallbacks

- If Figma MCP is unavailable: provide a manual frame/component rebuild plan.
- If the page cannot be reached: request a screenshot/export and route to `figma-canvas-editor`.
- If privacy blocks remote generation: keep the work local and describe a human-assisted import route.

## Resources

- Read `$CODEX_SKILLS_DIR/senior-figma-orchestrator/references/figma-mcp-compatibility.md` before promising capability.
