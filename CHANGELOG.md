# Changelog

## Unreleased

- Added negative evidence-validator fixture coverage to CI.
- Added eval contract coverage checks for top-level route and acceptance constraints.
- Added README status badges for CI, npm, and license.
- Added a manual GitHub Actions release workflow for npm publication through a protected `NPM_TOKEN` secret.
- Documented npm token rotation expectations after any chat/log exposure.

## 0.2.0 - 2026-06-21

- Added mechanical evidence report validation for `Ran`, `Skipped`, `Planned`, and `Manual` sections.
- Added deterministic eval runner with route checks for orchestrator scenarios.
- Added GitHub Actions CI for package lint, evidence validation, evals, adapter drift, freshness metadata, and npm pack smoke tests.
- Added `dist` sync validation and freshness metadata checks for UI/UX Pro Max CSV datasets.
- Clarified public positioning: the package has a vendor-neutral core with optional vendor-specific adapters and integrations.
- Updated Gemini adapter generation to inherit the package version from `package.json`.

## 0.1.0 - 2026-06-20

- Initial public npm package for the UI/UX Agent Skill System.
