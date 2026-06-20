---
name: senior-figma-orchestrator
description: Main Figma orchestration skill for the UI/UX skill system. Use this skill whenever the user asks to read Figma design context, turn Figma frames into implementation plans or code, sync live UI back to Figma, edit Figma canvas objects, manage variables/components/assets/effects, audit Figma MCP workflows, or coordinate Figma work under $senior-ui-ux-orchestrator. Routes to figma-context-reader, figma-design-to-code-bridge, figma-code-to-canvas, figma-canvas-editor, figma-design-system-sync, figma-assets-manager, figma-apply-effects, and figma-workflow-auditor while enforcing privacy, tool availability, and evidence boundaries.
---

# Senior Figma Orchestrator

This is the Figma sub-orchestrator for the UI/UX skill group. Use it below `$senior-ui-ux-orchestrator` when the work depends on Figma files, selected frames, Design Variables, Code Connect, code-to-canvas, direct canvas editing, assets, effects, or workflow governance.

## Operating Modes

- `route`: choose the smallest Figma specialist set.
- `read-context`: route to `figma-context-reader`.
- `design-to-code`: route to `figma-design-to-code-bridge`.
- `code-to-canvas`: route to `figma-code-to-canvas`.
- `edit-canvas`: route to `figma-canvas-editor`.
- `sync-system`: route to `figma-design-system-sync`.
- `manage-assets`: route to `figma-assets-manager`.
- `apply-effects`: route to `figma-apply-effects`.
- `audit-workflow`: route to `figma-workflow-auditor`.

## Required Workflow

1. Read [references/routing-matrix.md](references/routing-matrix.md) before routing.
2. Read [references/figma-mcp-compatibility.md](references/figma-mcp-compatibility.md) when current Figma MCP capability matters.
3. Confirm the available input: Figma URL, selected node context, local codebase, live URL, screenshots, exported assets, or design-system brief.
4. Classify privacy before using Figma context. Treat non-public Figma files, screenshots, design variables, component libraries, and exported assets as sensitive.
5. For any `use_figma` operation, first invoke the installed `figma:figma-use` skill. For FigJam or Slides, also invoke the relevant installed Figma skill.
6. For create/update/delete canvas work, require explicit scope: target file or node, intended mutation, rollback or duplicate strategy, and evidence to collect afterward.
7. Route to specialists and require them to label results as `Ran`, `Skipped`, `Planned`, or `Manual`.

## Routing Defaults

- Understand a file, frame, node, variable set, component tree, or Dev Mode spec: `figma-context-reader`.
- Convert a selected design into an implementation plan or component mapping: `figma-design-to-code-bridge`.
- Capture live UI from a browser/app into editable Figma layers: `figma-code-to-canvas`.
- Create or edit frames, components, autolayout, variables, FigJam objects, or Slides objects: `figma-canvas-editor`.
- Sync tokens, variables, component libraries, Code Connect, or style drift: `figma-design-system-sync`.
- Export/download/prepare image, SVG, font, or design assets: `figma-assets-manager`.
- Add, remove, bind, or audit Figma Effects: `figma-apply-effects`.
- Check whether a Figma workflow is valid, current, privacy-safe, and evidence-backed: `figma-workflow-auditor`.

## Safety And Evidence Rules

- Do not claim Figma MCP access exists until a connected tool or skill is available in the current session.
- Do not claim a Figma mutation happened unless a tool response, metadata readback, screenshot, or exported artifact proves it.
- Do not upload private Figma content, screenshots, URLs, source code, or assets to non-Figma external services without explicit approval.
- When Figma MCP is unavailable, return a blocked or fallback path: manual Figma instructions, local code implementation, screenshot audit, or asset export request.
- Prefer duplicating frames/components before broad destructive edits.

## Output

Use [assets/figma-handoff-template.md](assets/figma-handoff-template.md) for route handoffs and final reports.

## Validation

When editing this skill, run:

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/senior-figma-orchestrator
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/senior-figma-orchestrator
python3 -m json.tool $CODEX_SKILLS_DIR/senior-figma-orchestrator/evals/evals.json >/dev/null
```
