# Qwen Code Adapter

Support level: native `SKILL.md` skill folders.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Project-Local Install

```bash
mkdir -p .qwen/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/qwen-code/.qwen/skills/* .qwen/skills/
```

## Notes

- Use `senior-ui-ux-orchestrator` first for ambiguous UI/UX work.
- Use direct specialist skills only when the task is already narrowly scoped.
- Preserve scripts and references; Qwen should not receive only a pasted prompt summary.

