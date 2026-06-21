# Package Validation Report

Date: 2026-06-20

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
