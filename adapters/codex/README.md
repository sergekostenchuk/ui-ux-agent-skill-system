# Codex Adapter

Support level: native skill folders.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Install

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R dist/codex/skills/* "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is not set, use your local Codex home directory.

## Notes

- `agents/openai.yaml` files are preserved.
- Shared contracts are copied as `_shared`.
- Restart or reload Codex if newly installed skills do not appear in discovery.

