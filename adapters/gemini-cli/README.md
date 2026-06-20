# Gemini CLI Adapter

Support level: extension projection.

Gemini CLI extensions use `gemini-extension.json` plus `GEMINI.md`. This adapter builds a Gemini extension that contains a compact routing entrypoint and the full skill folders as resources.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

Generated extension:

```text
dist/gemini-cli/ui-ux-agent-skill-system/
```

## Install

Copy the generated extension into your Gemini CLI extension location and reload extensions according to your local Gemini CLI setup.

## Notes

- `GEMINI.md` is a projection, not the source of truth.
- `core/skills` remains canonical.
- If you edit the Gemini projection, backport the change to `core/skills` or docs.

