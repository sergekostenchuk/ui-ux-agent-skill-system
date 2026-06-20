---
name: figma-assets-manager
description: Export, download, inventory, and prepare assets from Figma for UI implementation or audits. Use this skill when the user asks for icons, SVGs, PNG/JPEG/WebP exports, image assets, font references, slices, thumbnails, brand assets, asset manifests, or asset handoff from a Figma file while preserving licensing, privacy, naming, and implementation constraints.
---

# Figma Assets Manager

Use this skill for asset extraction and preparation. It is not a generic image generator and it should not mutate design files unless explicitly scoped.

## Modes

- `inventory`: list available assets and export needs.
- `export`: export selected nodes/assets in requested formats.
- `prepare`: optimize naming, density, dimensions, and implementation placement.
- `handoff`: produce a manifest for frontend integration.
- `audit`: flag missing, oversized, duplicated, or inaccessible assets.

## Workflow

1. Confirm target nodes, formats, scales, intended code destination, and privacy.
2. If Figma MCP export/download is needed, invoke `figma:figma-use` before the Figma tool.
3. Prefer SVG for icons and simple vector marks; prefer raster formats for photography or complex bitmap media.
4. Record license/usage assumptions if assets are third-party or brand-sensitive.
5. Write or request an asset manifest with source node, output path, format, scale, dimensions, and intended use.
6. For frontend integration, hand off to `webapp-ui-skill` or `marketing-site-skill` after export.

## Output Shape

Use [assets/asset-manifest-template.json](assets/asset-manifest-template.json) or summarize the same fields in Markdown.

## Boundaries

- Do not upload private assets to optimization or CDN services without explicit approval.
- Do not replace editable Figma vectors with flattened raster assets unless the target implementation requires it.
- Do not assume fonts are licensed for web embedding; report missing font/license checks.

## Validation And Eval

- Validate that exports have source node, format, scale, dimensions, output path, and intended use.
- Check that private assets remain local unless an approved external transfer is recorded.
- Use `evals/evals.json` to test SVG export manifest behavior and private-asset external optimization refusal.
