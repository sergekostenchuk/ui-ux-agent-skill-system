# UI/UX Agent Skill System

[![CI](https://github.com/sergekostenchuk/ui-ux-agent-skill-system/actions/workflows/ci.yml/badge.svg)](https://github.com/sergekostenchuk/ui-ux-agent-skill-system/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/@mlllm/ui-ux-agent-skill-system.svg)](https://www.npmjs.com/package/@mlllm/ui-ux-agent-skill-system)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

Vendor-neutral core UI/UX skill cluster for AI coding and design agents, with optional vendor-specific adapters and integrations.

Repository: https://github.com/sergekostenchuk/ui-ux-agent-skill-system

This repository is not a loose prompt collection. It is a portable agent skill system with a central orchestrator, specialist skills, runtime adapters, deterministic checks, and realistic eval prompts.

The core contracts, routing model, reporting format, evals, and validation gates are portable. Runtime packaging and integrations such as Figma MCP, Google Stitch, Codex, Claude, Gemini, Qwen, Copilot, GLM, and Kimi are adapter-specific and depend on the target tool's capabilities, authentication, and local environment.

## What It Does

`senior-ui-ux-orchestrator` is the main chair. It routes UI/UX work to specialist skills and keeps them from conflicting with each other.

Use it for:

- marketing websites and landing pages;
- SaaS dashboards and dense web apps;
- product UX architecture and user journeys;
- SEO, AEO/GEO, and LLM-readable public site structure;
- optional Figma MCP workflows and design-system sync;
- optional Stitch / AI UI exploration;
- three-direction design exploration;
- UX audits and visual critique;
- cursor reveal and image-layer alignment effects;
- task-plan governance for large multi-agent work.

## Core Workflow

```text
user request
-> senior-ui-ux-orchestrator
-> task-plan gate when needed
-> product UX architecture
-> SEO/LLM constraints when public discoverability matters
-> UI/UX Pro Max design intelligence
-> three-variant direction selection when needed
-> senior council when skills conflict
-> optional Stitch exploration when useful and available
-> optional Figma gate only when a Figma artifact is required
-> implementation specialist
-> audit, critic, visual/browser/semantic validation
-> report or wiki capture
```

The orchestrator is the final routing and conflict-resolution layer. Specialist skills provide expert input or execute a bounded stage.

## Repository Layout

```text
.
├── core/
│   ├── skills/              # Canonical skills
│   └── shared/              # Shared privacy, reporting, freshness, validation contracts
├── adapters/                # Runtime-specific install notes
├── dist/                    # Prebuilt runtime projections
├── docs/                    # Architecture, install, compatibility, skill map
├── evals/                   # Forward-test prompts
├── reports/                 # Package validation evidence
├── scripts/
│   ├── build_adapters.py
│   └── lint_publication_package.py
├── FEATURE-PREPARATION.md
├── TASK-PLAN.md
├── SECURITY.md
├── NOTICE
└── LICENSE
```

## Included Skills

### Main Orchestration

- `senior-ui-ux-orchestrator` — central UI/UX chair and router.
- `task-plan-v2-orchestrator` — planning, gates, handoffs, verification policy.

### Product, SEO, And Design Intelligence

- `ui-ux-llm-product-architect` — user journeys, IA, UX logic, accessibility, agent-readable UI.
- `seo-llm-site-architect` — SEO, AEO/GEO, schema, metadata, crawlability, LLM-readability.
- `ui-ux-pro-max` — searchable design intelligence: styles, palettes, typography, patterns, stack guidance.
- `stitch-design-bridge` — optional Stitch prompts, AI UI exploration review, Figma/code handoff.

### Figma Subsystem

- `senior-figma-orchestrator`
- `figma-context-reader`
- `figma-design-to-code-bridge`
- `figma-code-to-canvas`
- `figma-canvas-editor`
- `figma-design-system-sync`
- `figma-assets-manager`
- `figma-apply-effects`
- `figma-workflow-auditor`

### Implementation And Review

- `marketing-site-skill` — public pages, landing pages, conversion, metadata, responsive storytelling.
- `webapp-ui-skill` — SaaS, dashboards, admin tools, tables, states, dense workflows.
- `ux-audit-skill` — evidence-backed UX audit and regression review.
- `design-critic-skill` — visual quality critique and anti-slop review.

### Specialist Visual Effects

- `cursor-reveal-hero` — cursor-trail masking/reveal hero effects.
- `image-layer-alignment-validator` — local image layer alignment checks for reveal/morph/compositing.

## Supported Agent Runtimes

| Runtime | Support | Prebuilt Output |
|---|---|---|
| Codex | native skill folders | `dist/codex/skills/` |
| Claude / Claude Code | `SKILL.md` skill folders | `dist/claude/skills/` |
| Qwen Code | `.qwen/skills` projection | `dist/qwen-code/.qwen/skills/` |
| VS Code / Copilot | `.github/skills` projection | `dist/copilot-vscode/.github/skills/` |
| Gemini CLI | extension projection | `dist/gemini-cli/ui-ux-agent-skill-system/` |
| GLM / Z.ai | generic `AGENTS.md` projection | `dist/glm-zai/` |
| Kimi | generic `AGENTS.md` projection | `dist/kimi/` |
| Other agents | portable Markdown projection | `dist/generic-agent/` |

See [docs/vendor-compatibility.md](docs/vendor-compatibility.md).

## Install

### npm / npx

The fastest install path is:

```bash
npm install -g @mlllm/ui-ux-agent-skill-system
uiux-skills list
uiux-skills install codex
```

Or with `npx`:

```bash
npx @mlllm/ui-ux-agent-skill-system install codex
```

Other targets:

```bash
uiux-skills install qwen-code
uiux-skills install copilot-vscode
uiux-skills install claude --dest ~/.claude/skills
uiux-skills install gemini-cli --dest ~/.gemini/extensions/ui-ux-agent-skill-system
```

See [docs/npm.md](docs/npm.md).

### Codex

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R dist/codex/skills/* "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is not set, use your Codex home directory, commonly `~/.codex`.

### Claude / Claude Code

```bash
cp -R dist/claude/skills/* /path/to/claude/skills/
```

Use the skills directory expected by your Claude or Claude Code setup.

### Qwen Code

Project-local install:

```bash
mkdir -p .qwen/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/qwen-code/.qwen/skills/* .qwen/skills/
```

### VS Code / Copilot

Project-local install:

```bash
mkdir -p .github/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/copilot-vscode/.github/skills/* .github/skills/
```

### Gemini CLI

Copy the generated extension into your Gemini CLI extensions location:

```bash
cp -R dist/gemini-cli/ui-ux-agent-skill-system /path/to/gemini/extensions/
```

### GLM / Z.ai, Kimi, Generic Agents

Use the generated `AGENTS.md`, `skills-index.md`, and `skills/` folder from:

```text
dist/glm-zai/
dist/kimi/
dist/generic-agent/
```

Load `senior-ui-ux-orchestrator` first unless the task explicitly names a specialist skill.

## Basic Usage

Start with the orchestrator:

```text
$senior-ui-ux-orchestrator
Build a premium conversion-focused website for a cottage village from the materials in ./project-assets.
Create three distinct design directions and validate them.
```

For direct specialist use:

```text
$ux-audit-skill
Audit this landing page screenshot and source code. Return severity-ranked findings and a fix brief.
```

```text
$senior-figma-orchestrator
Read this selected Figma frame, map it to our code components, and prepare a design-to-code handoff.
```

## User Journey 1: Premium Real Estate Marketing Site

Goal: create a premium selling website for a cottage village or real-estate project.

Example prompt:

```text
$senior-ui-ux-orchestrator
Create a premium conversion-focused website for a cottage village.
Materials are in ./KLIMOVO-AI.
Create three different design versions and validate desktop/mobile.
```

Skill path:

```text
senior-ui-ux-orchestrator
-> task-plan-v2-orchestrator
-> ui-ux-llm-product-architect
-> seo-llm-site-architect
-> ui-ux-pro-max
-> senior council if UX/SEO/visual conflicts appear
-> stitch-design-bridge if AI exploration is useful and available
-> marketing-site-skill
-> design-critic-skill
-> ux-audit-skill
-> browser/metadata/semantic validation
```

What each skill contributes:

- `ui-ux-llm-product-architect` defines buyer journeys: emotional entry, lot comparison, trust verification, request path.
- `seo-llm-site-architect` keeps visible facts, metadata, schema, headings, and crawlable structure aligned.
- `ui-ux-pro-max` suggests style candidates, palettes, typography, and layout patterns.
- `stitch-design-bridge` can turn approved directions into Stitch-ready prompts when Stitch is available.
- `marketing-site-skill` implements the actual public page.
- `design-critic-skill` checks premium feel, hierarchy, typography, spacing, and anti-slop risks.
- `ux-audit-skill` verifies responsive behavior and evidence-backed UX risks.

Expected outputs:

- three clearly different design directions;
- implemented pages or handoff briefs;
- CTA hierarchy;
- visible proof/trust facts;
- metadata and JSON-LD when source files exist;
- validation report with `Ran`, `Skipped`, `Planned`, and `Manual`.

## User Journey 2: SaaS Dashboard Or Internal Tool

Goal: design or refactor a dense product UI such as a dashboard, CRM, admin panel, analytics view, or settings flow.

Example prompt:

```text
$senior-ui-ux-orchestrator
Refactor this SaaS dashboard for better scanning, filtering, table actions, empty states, and mobile behavior.
Use the existing component system.
```

Skill path:

```text
senior-ui-ux-orchestrator
-> task-plan-v2-orchestrator when the change spans several screens
-> ui-ux-llm-product-architect
-> ui-ux-pro-max
-> webapp-ui-skill
-> ux-audit-skill
-> design-critic-skill
-> state coverage and visual validation
```

What each skill contributes:

- `ui-ux-llm-product-architect` maps user goals, screen states, action priority, accessible names, and semantic controls.
- `ui-ux-pro-max` supplies dashboard, table, form, navigation, color, typography, and interaction guidance.
- `webapp-ui-skill` implements or specifies dense UI patterns: tables, filters, loading/empty/error states, settings flows, responsive panels.
- `ux-audit-skill` checks evidence, severity, state coverage, regression risk, and before/after behavior.
- `design-critic-skill` reviews visual hierarchy, grouping, contrast risk, density, and action clarity.

Expected outputs:

- screen inventory;
- state matrix;
- component and interaction plan;
- implementation diff or task brief;
- visual smoke checks where runnable;
- explicit skipped checks when no browser/app target exists.

## User Journey 3: Figma To Code And Design-System Sync

Goal: use Figma as a source of truth, implementation handoff, or synchronization layer.

Example prompt:

```text
$senior-ui-ux-orchestrator
Use the selected Figma frame to prepare an implementation plan.
Map variables, components, assets, effects, and code gaps.
Do not guess missing tokens.
```

Skill path:

```text
senior-ui-ux-orchestrator
-> senior-figma-orchestrator
-> figma-context-reader
-> figma-design-to-code-bridge
-> figma-design-system-sync when variables/components matter
-> figma-assets-manager when assets are needed
-> figma-apply-effects when shadows/blur/glass/noise/effects are requested
-> marketing-site-skill or webapp-ui-skill for implementation
-> ux-audit-skill and design-critic-skill for verification
```

What each skill contributes:

- `senior-figma-orchestrator` routes Figma work and enforces privacy/tool evidence boundaries.
- `figma-context-reader` reads selected frames, nodes, variables, layout, and component context.
- `figma-design-to-code-bridge` turns Figma structure into implementation-ready component mapping.
- `figma-design-system-sync` checks tokens, variables, component drift, and code/design mismatches.
- `figma-assets-manager` exports or inventories assets for implementation.
- `figma-apply-effects` handles shadows, blur, glass, noise, texture, and effect-token binding where supported.
- `marketing-site-skill` or `webapp-ui-skill` owns the final code path.

Expected outputs:

- design context summary;
- component mapping;
- token and variable notes;
- asset inventory;
- implementation plan;
- validation evidence or explicit manual review gaps.

## Senior Council Rule

Use the council only for large projects or real conflicts:

- UX wants less text, SEO needs visible crawlable content.
- Stitch output looks good but fails accessibility.
- Figma design system conflicts with feasible implementation.
- Visual novelty conflicts with truthful product facts.

Decision priority:

1. Security, privacy, legal, user safety.
2. Accessibility and primary user task.
3. Truthful visible facts.
4. Semantic HTML, crawlability, LLM-readable structure.
5. Conversion UX and user comprehension.
6. Figma/design-system consistency when Figma is part of the project.
7. Maintainability.
8. Visual novelty and AI-generated aesthetics.

The council advises. `senior-ui-ux-orchestrator` decides.

## Rebuild Adapters

Prebuilt runtime projections are included in `dist/`. To regenerate them:

```bash
python3 scripts/build_adapters.py . --out dist
```

Validate the package:

```bash
node bin/uiux-skills.js list
python3 scripts/lint_publication_package.py .
npm pack --dry-run
python3 -m json.tool dist/gemini-cli/ui-ux-agent-skill-system/gemini-extension.json >/dev/null
```

## Safety Defaults

- Local-first by default.
- Do not store or print API keys, tokens, cookies, private URLs, `.env` contents, private screenshots, or customer data.
- Use environment variables for optional integrations such as `STITCH_API_KEY`.
- External services require explicit user approval and a data-transfer note.
- Planned checks are not evidence.
- Reports must distinguish `Ran`, `Skipped`, `Planned`, and `Manual`.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
