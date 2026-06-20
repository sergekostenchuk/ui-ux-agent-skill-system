# Package Validation Report

Date: 2026-06-20

## Commands Run

```bash
python3 scripts/lint_publication_package.py .
python3 scripts/build_adapters.py . --out dist
python3 scripts/lint_publication_package.py .
python3 -m json.tool dist/gemini-cli/ui-ux-agent-skill-system/gemini-extension.json
```

## Results

- Package linter before adapter build: passed with 0 warnings.
- Adapter build: completed.
- Package linter after adapter build: passed with 0 warnings.
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
