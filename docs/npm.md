# npm Distribution

This package can be distributed through npm as:

```text
@sergekostenchuk/ui-ux-agent-skill-system
```

The npm package includes:

- canonical skills in `core/skills`;
- shared contracts in `core/shared`;
- prebuilt runtime projections in `dist`;
- an installer CLI named `uiux-skills`.

## Use With npx

Install Codex skills:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install codex
```

Install Qwen Code skills into the current project:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install qwen-code
```

Install VS Code/Copilot project skills:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install copilot-vscode
```

Install Claude skills:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install claude --dest ~/.claude/skills
```

Install Gemini CLI extension:

```bash
npx @sergekostenchuk/ui-ux-agent-skill-system install gemini-cli --dest ~/.gemini/extensions/ui-ux-agent-skill-system
```

## Global Install

```bash
npm install -g @sergekostenchuk/ui-ux-agent-skill-system
uiux-skills list
uiux-skills install codex
```

## Publish

Before publishing:

```bash
npm login
npm whoami
npm pack --dry-run
npm publish --access public
```

The package is scoped. Public publication requires `--access public`.
