# GLM / Z.ai Adapter

Support level: generic agent projection.

This adapter does not claim native skill-folder support. It generates:

- `AGENTS.md`
- `skills-index.md`
- `skills/`

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Use

Start the GLM/Z.ai agent with `AGENTS.md` as project guidance, then ask it to load the relevant `skills/<name>/SKILL.md` file before acting.

## Notes

- Keep `senior-ui-ux-orchestrator` as the chair.
- Treat specialist skills as bounded role instructions.
- Do not paste API keys or `.env` content into agent context.

