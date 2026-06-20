# VS Code / Copilot Adapter

Support level: skill-folder projection.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Project-Local Install

```bash
mkdir -p .github/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/copilot-vscode/.github/skills/* .github/skills/
```

## Notes

- This adapter preserves `SKILL.md` folders.
- Use project-local install when a repository should carry its own UI/UX agent behavior.
- Keep secrets and local-only paths out of `.github/skills`.

