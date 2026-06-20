# Claude Adapter

Support level: native-ish `SKILL.md` folders.

Claude Agent Skills use folder-based skill bundles with a `SKILL.md` instruction file and optional resources. This adapter preserves the same progressive-disclosure structure from `core/skills`.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Install

Copy generated folders from:

```text
dist/claude/skills/
```

into the Claude skills directory used by your local Claude or Claude Code setup.

## Notes

- Keep `senior-ui-ux-orchestrator` as the main entrypoint.
- Do not flatten all skill bodies into one giant instruction file.
- Keep shared privacy and evidence contracts available as `_shared`.

