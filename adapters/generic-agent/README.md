# Generic Agent Adapter

Support level: portable Markdown projection.

This adapter is for agents that can read project instructions but do not have a native skill format.

## Build

```bash
python3 scripts/build_adapters.py . --out dist
```

## Use

Provide the agent with:

```text
dist/generic-agent/AGENTS.md
dist/generic-agent/skills-index.md
```

Then load individual skill files from:

```text
dist/generic-agent/skills/
```

## Rule

Do not flatten the whole system into one giant prompt. Load the orchestrator first, then only the specialist files required by the task.

