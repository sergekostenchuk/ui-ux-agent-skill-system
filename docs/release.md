# Release Process

## Preferred Path

Use the `Release` GitHub Actions workflow.

1. Bump `package.json` to a new npm version.
2. Regenerate adapters:

```bash
npm run build:adapters
```

3. Run local parity checks:

```bash
npm run lint
npm run test:evidence
npm run eval
npm run check:eval-contracts
git diff --exit-code dist
npm run check:dist
npm run check:freshness
npm pack --dry-run
```

4. Commit and push.
5. Create a git tag and GitHub release for the exact release commit.
6. Run the `Release` workflow with the target version.

The workflow requires a repository or environment secret named `NPM_TOKEN`.
Use a granular npm automation token with package publish permission. Protect the
`npm-production` environment if releases should require manual approval.

## Manual Fallback

Manual publish is allowed only after the same checks pass:

```bash
npm whoami
npm publish --access public
npm view @mlllm/ui-ux-agent-skill-system name version dist-tags.latest
```

Use temporary auth only. Do not write tokens to repository files.

## Token Hygiene

If a token appears in chat, an issue, a shell transcript, or a generated report,
revoke it in npm and create a replacement token before the next release.

## Release Evidence

Record release evidence in `reports/package-validation.md` and update
`TASK-PLAN.md` only with redacted commands. Never store tokens, OTPs, recovery
codes, private npm logs, or local `.npmrc` contents.
