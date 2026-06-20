---
name: figma-workflow-auditor
description: Audit Figma MCP, design-to-code, code-to-canvas, canvas-editing, and design-system workflows for correctness, freshness, privacy, evidence, and routing quality. Use this skill when the user asks whether a Figma workflow, skill, task plan, MCP capability claim, or agent handoff is valid, current, safe, or production-ready.
---

# Figma Workflow Auditor

Use this skill as the quality gate for Figma-related workflows. It does not mutate Figma files.

## Modes

- `capability-audit`: verify claims against current Figma MCP/tool availability.
- `privacy-audit`: check whether data transfer and permissions are acceptable.
- `evidence-audit`: check whether claimed reads/writes/exports actually ran.
- `routing-audit`: check whether the right Figma specialist was selected.
- `skill-audit`: review a Figma skill draft or existing skill.

## Workflow

1. Identify the workflow under review: prompt, plan, skill, transcript, report, or file change.
2. Check official/current sources when capability details may have changed.
3. Verify tool evidence: tool response, metadata readback, screenshot/export, local diff, or report artifact.
4. Flag overclaims separately from implementation bugs.
5. Return findings ordered by severity, with concrete fixes.

## Findings Format

Use [assets/audit-report-template.md](assets/audit-report-template.md).

## Audit Rules

- A Figma MCP claim is weak if it lacks session tool availability and evidence.
- A mutation claim is invalid without a target, scope, executed tool, and readback.
- A privacy plan is weak if it omits what data is sent to Figma or another service.
- A design-to-code plan is weak if it skips local component inspection and visual verification.
- An effects plan is weak if it treats `NOISE`, `TEXTURE`, `GLASS`, or progressive blur as universally available without runtime checks.
