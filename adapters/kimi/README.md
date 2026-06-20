# Kimi Adapter

Support level: generic agent projection.

This adapter generates a portable `AGENTS.md` and skill index for Kimi-style agents or tools that do not yet expose a stable public skill-bundle contract.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Use

Use:

```text
dist/kimi/AGENTS.md
dist/kimi/skills-index.md
dist/kimi/skills/
```

Load `senior-ui-ux-orchestrator` first unless the task explicitly names a specialist skill.

