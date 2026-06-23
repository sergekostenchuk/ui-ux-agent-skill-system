# Package Validation Report

Date: 2026-06-23

## 0.3.0 GitHub Publication Preparation

### Scope

- Expanded canonical `core/skills` from 21 to 68 UI/UX Agent Skill System skills.
- Rebuilt all runtime projections with 68 skills each: Codex, Claude, Qwen Code, VS Code/Copilot, Gemini CLI, GLM/Z.ai, Kimi, and generic agents.
- Added package-level progress/compliance runtime helpers and `data/journey-registry.json`.
- Added interactive documentation artifacts: `docs/skill-review-board.html`, `docs/skill-graph.html`, `docs/task-dashboard.html`, and `docs/agent-progress-screen.example.html`.
- Recorded NMT / AJTBD as an optional external product-strategy source without bundling upstream CC BY-NC-SA content.

### Commands Run

```bash
npm run build:adapters
npm run lint
npm run test:evidence
npm run eval
npm run check:eval-contracts
npm run check:dist
npm run check:freshness
npm pack --dry-run --json
```

### Results

- `npm run lint`: passed with 0 warnings.
- `npm run test:evidence`: passed; valid evidence accepted, missing-artifact rejected, planned-only rejected when Ran evidence is required.
- `npm run eval`: passed with 39 files, 76 cases, 27 route checks, and 49 non-route contract cases.
- `npm run check:eval-contracts`: passed; coverage includes accessibility, privacy, truthful content, and validation.
- `npm run check:dist`: passed; regenerated adapter output matches committed `dist`.
- `npm run check:freshness`: passed; freshness metadata covers 30 CSV files in 4 dataset groups.
- `npm pack --dry-run --json`: passed for `@mlllm/ui-ux-agent-skill-system@0.3.0`; packed size about 4.1 MB, unpacked size about 24.2 MB, 4173 package entries.
- Secret/local path scan: no local absolute user path, Stitch API token, npm token, or non-redacted secret assignment remains in package files.

## Historical Validation Notes

## Commands Run

```bash
python3 scripts/lint_publication_package.py .
python3 scripts/build_adapters.py . --out dist
python3 scripts/lint_publication_package.py .
python3 scripts/validate_evidence_report.py tests/fixtures/evidence/valid.md
python3 scripts/run_evals.py . --out reports/eval-results.json
python3 scripts/build_adapters.py . --out dist
python3 scripts/check_dist_sync.py .
python3 scripts/check_freshness.py .
rg -n "vendor-neutral|Vendor-neutral|Stitch|Figma" README.md docs package.json
python3 scripts/lint_publication_package.py .
npm run lint
npm run validate:evidence
npm run eval
npm run build:adapters
npm run check:dist
git diff --exit-code dist
npm run check:freshness
npm pack --dry-run
python3 scripts/lint_publication_package.py .
python3 scripts/run_evals.py . --out reports/eval-results.json
python3 scripts/build_adapters.py . --out dist
python3 scripts/check_dist_sync.py .
python3 scripts/check_freshness.py .
npm pack --dry-run --json
git diff --exit-code dist
npm view @mlllm/ui-ux-agent-skill-system version
npm whoami
npm whoami # with temporary userconfig; token redacted
npm publish --access public # with temporary userconfig; token redacted
npm view @mlllm/ui-ux-agent-skill-system name version dist-tags.latest license bin repository.url
npm install --ignore-scripts @mlllm/ui-ux-agent-skill-system@0.2.0 # in temporary directory
./node_modules/.bin/uiux-skills list # in temporary directory
npm run test:evidence
npm run check:eval-contracts
npm run lint
npm run eval
npm run check:freshness
npm run build:adapters
git diff --exit-code dist
npm run check:dist
npm pack --dry-run
rg -n "npm_[A-Za-z0-9]{10,}|[a-f0-9]{64}" . || true
gh release create v0.2.0 --target f13bce03a5ea8c919d685b35015960735eee06d6 --title "v0.2.0" --notes "..."
gh release view v0.2.0 --json url,tagName,targetCommitish,createdAt
node bin/uiux-skills.js list
npm pack --dry-run
python3 -m json.tool dist/gemini-cli/ui-ux-agent-skill-system/gemini-extension.json
```

## Results

- Package linter before adapter build: passed with 0 warnings.
- Adapter build: completed.
- Package linter after adapter build: passed with 0 warnings.
- Evidence validator fixture check: passed.
- Deterministic eval runner: passed, 16 files, 50 cases, 27 route checks, 0 failures.
- Adapter regeneration and dist sync check: passed.
- Freshness metadata check: passed.
- Vendor-neutral wording grep: passed; public docs now describe a vendor-neutral core with optional vendor-specific adapters and integrations.
- Package linter after wording update: passed with 0 warnings.
- GitHub Actions CI workflow added for push and pull request checks without secrets.
- Local CI parity: package lint, evidence validator, eval runner, adapter rebuild, dist sync, freshness metadata, and npm pack dry-run all passed.
- `git diff --exit-code dist`: passed after adapter rebuild.
- Release prep for `0.2.0`: package version bumped, `CHANGELOG.md` added, and Gemini adapter generation now reads the version from `package.json`.
- Release prep checks for `0.2.0`: package lint, eval runner, adapter rebuild, dist sync, freshness metadata, and npm dry-run pack passed.
- `npm pack --dry-run --json` for `0.2.0`: passed, 3.2 MB packed, 19.6 MB unpacked, 1928 files.
- Post-push `git diff --exit-code dist`: passed.
- `npm view @mlllm/ui-ux-agent-skill-system version`: returned `0.1.0`; `0.2.0` is not published yet.
- `npm whoami`: blocked with `E401 Unauthorized`; current shell has no active npm authentication. `npm publish` was not run because a fresh publish token or interactive npm login is required.
- Temporary npm userconfig authentication: passed as `mlllm`; token was not committed or stored in repository files.
- `npm publish --access public` for `@mlllm/ui-ux-agent-skill-system@0.2.0`: passed.
- Registry verification: `name=@mlllm/ui-ux-agent-skill-system`, `version=0.2.0`, `dist-tags.latest=0.2.0`, `license=Apache-2.0`, `bin.uiux-skills=bin/uiux-skills.js`.
- Clean temporary install of `@mlllm/ui-ux-agent-skill-system@0.2.0`: passed; `.bin/uiux-skills list` printed all runtime targets.
- Negative evidence fixtures: passed; valid fixture accepted, missing-artifact fixture rejected, planned-only fixture rejected when `--require-ran` is set.
- Eval contract coverage: passed for 4 top-level cases across accessibility, privacy, truthful content, and validation coverage.
- CI workflow now runs `npm run test:evidence`, `npm run eval`, and `npm run check:eval-contracts`.
- Manual `Release` workflow added with `workflow_dispatch`, version match check, duplicate npm version guard, validation gates, and `NPM_TOKEN` secret publish.
- README badges added for CI, npm version, and Apache-2.0 license.
- Exact npm token and 2FA/recovery-code strings used during manual publish were not found in repository files after the hardening update.
- GitHub Release `v0.2.0` created at the npm-published commit `f13bce03a5ea8c919d685b35015960735eee06d6`: https://github.com/sergekostenchuk/ui-ux-agent-skill-system/releases/tag/v0.2.0
- `node bin/uiux-skills.js list`: passed.
- `node bin/uiux-skills.js path`: passed.
- `node bin/uiux-skills.js install qwen-code --dest /tmp/uiux-skills-npm-test/.qwen/skills --dry-run`: passed.
- `node bin/uiux-skills.js install generic-agent --dest /tmp/uiux-skills-npm-test/generic --dry-run`: passed.
- `npm pack --dry-run`: passed.
- `npm publish --access public`: blocked by npm 2FA policy; the provided token authenticated but does not allow package publication under the account's current security settings.
- `npm publish --access public` with a new token: authenticated as `mlllm`, then blocked because the npm scope `@sergekostenchuk` is not available to that account.
- `npm publish --access public` as `@mlllm/ui-ux-agent-skill-system@0.1.0`: passed.
- `npm access set status=public @mlllm/ui-ux-agent-skill-system`: passed.
- `npm view @mlllm/ui-ux-agent-skill-system name version dist-tags.latest license bin repository.url`: passed.
- `npm exec --yes --package @mlllm/ui-ux-agent-skill-system -- uiux-skills list`: passed.
- Gemini extension JSON parse: passed.

## Generated Adapter Outputs

- `dist/codex/skills/`
- `dist/claude/skills/`
- `dist/qwen-code/.qwen/skills/`
- `dist/copilot-vscode/.github/skills/`
- `dist/gemini-cli/ui-ux-agent-skill-system/`
- `dist/glm-zai/`
- `dist/kimi/`
- `dist/generic-agent/`

## Publication Notes

- The publication package intentionally excludes real credentials.
- `.env.example` contains redacted examples only.
- The current license is Apache-2.0.
- `dist/` is generated but intentionally included in the GitHub publication package so users can install prebuilt runtime projections.
- Public repository: https://github.com/sergekostenchuk/ui-ux-agent-skill-system
- npm package name prepared: `@mlllm/ui-ux-agent-skill-system`.
- npm package published: https://www.npmjs.com/package/@mlllm/ui-ux-agent-skill-system
- npm publication target changed to the authenticated npm user's scope after npm rejected the unavailable `@sergekostenchuk` scope.
- npm dry-run tarball for `0.2.0`: 3.2 MB packed, 19.6 MB unpacked, 1928 files.
- npm `0.2.0` published as latest on 2026-06-21.
