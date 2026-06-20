# FEATURE-PREPARATION: UI/UX Agent Skill System Publication Package

feature_id: F-UIUX-PUBLICATION-001
feature_title: Vendor-neutral UI/UX Agent Skill System package
status: in_progress
date: 2026-06-20

## Problem And Goal

- [x] Package the existing UI/UX skill group for GitHub publication.
- [x] Preserve `senior-ui-ux-orchestrator` as the main chair.
- [x] Support more than Codex through runtime adapters.
- [x] Avoid publishing local paths, secrets, `.env` contents, private reports, or wiki internals.
- [x] Add deterministic validation.
- [x] Switch license to Apache-2.0.
- [x] Include detailed README with three user journeys.

## Scope In

- Canonical skills under `core/skills/`.
- Shared contracts under `core/shared/`.
- Runtime adapters for Codex, Claude, Gemini CLI, Qwen Code, VS Code/Copilot, GLM/Z.ai, Kimi, and generic agents.
- README, install docs, architecture docs, vendor compatibility docs, security policy, eval prompts.
- Build and lint scripts.

## Scope Out

- Guaranteeing native support for vendors that do not expose a stable public skill-bundle format.
- Running vendor CLIs locally.

## Security And Privacy

- No real API keys or tokens are included.
- `.env.example` uses redacted values only.
- External service usage is approval-gated.
- Generic adapters do not claim native vendor support.

## Verification

- [x] Package linter passes.
- [x] Runtime adapter build completes.
- [x] Linter passes after `dist` generation.
- [x] Gemini extension JSON parses.
