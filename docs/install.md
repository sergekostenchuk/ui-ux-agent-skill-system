# Install

## Build Runtime Projections

From the package root:

```bash
python3 scripts/build_adapters.py . --out dist
python3 scripts/lint_publication_package.py .
```

## npm / npx

After npm publication:

```bash
npm install -g @sergekostenchuk/ui-ux-agent-skill-system
uiux-skills install codex
```

Or:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install codex
```

More targets:

```bash
uiux-skills install qwen-code
uiux-skills install copilot-vscode
uiux-skills install claude --dest ~/.claude/skills
uiux-skills install gemini-cli --dest ~/.gemini/extensions/ui-ux-agent-skill-system
uiux-skills install generic-agent
```

## Codex

Copy generated skills:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R dist/codex/skills/* "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is not set, the common default is `~/.codex`.

## Claude / Claude Code

Copy generated skills into the Claude skills location used by your local setup:

```bash
cp -R dist/claude/skills/* /path/to/claude/skills/
```

Restart or reload Claude Code if your environment requires discovery refresh.

## Qwen Code

Project-local install:

```bash
mkdir -p .qwen/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/qwen-code/.qwen/skills/* .qwen/skills/
```

## VS Code / Copilot

Project-local install:

```bash
mkdir -p .github/skills
cp -R /path/to/ui-ux-agent-skill-system/dist/copilot-vscode/.github/skills/* .github/skills/
```

## Gemini CLI

Install the generated extension according to your Gemini CLI extension workflow:

```bash
cp -R dist/gemini-cli/ui-ux-agent-skill-system /path/to/gemini/extensions/
```

Then reload Gemini CLI extensions.

## GLM / Z.ai, Kimi, And Generic Agents

Use generated `AGENTS.md` plus `skills-index.md` from:

```text
dist/glm-zai/
dist/kimi/
dist/generic-agent/
```

These adapters preserve the role map, safety policy, and routing instructions without claiming native skill support.

## Required Environment Variables

No environment variable is required for local-only usage.

Optional:

```bash
STITCH_API_KEY=redacted
FIGMA_ACCESS_TOKEN=redacted
```

Never commit real values.
