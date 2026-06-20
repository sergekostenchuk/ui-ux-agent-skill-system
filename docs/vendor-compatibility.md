# Vendor Compatibility

Verified on: 2026-06-20

This package uses a vendor-neutral core and runtime adapters. Do not assume every vendor supports the same skill mechanism.

## Compatibility Matrix

| Runtime | Support Level | Packaging Strategy | Notes |
|---|---|---|---|
| Codex | native | copy `core/skills/*` into the Codex skills directory | Uses `SKILL.md`, references, scripts, assets, evals, and `agents/openai.yaml`. |
| Claude / Claude Code | native-ish | copy `core/skills/*` into a Claude skills directory | Claude Agent Skills use directories with `SKILL.md` and progressive disclosure. |
| Qwen Code | native | copy `core/skills/*` into `.qwen/skills/` or user skills | Qwen Code skills support `SKILL.md`, scripts, and resources. |
| VS Code / Copilot | native projection | copy `core/skills/*` into `.github/skills/` or configured agent skill path | VS Code agent skills use `SKILL.md`-style folders. |
| Gemini CLI | extension projection | generate an extension with `gemini-extension.json` and `GEMINI.md` | Gemini CLI extensions are different from folder skills; adapter summarizes routing and points to core. |
| GLM / Z.ai | generic | generate `AGENTS.md` plus core skill references | Treat as portable instructions unless the target tool supports a richer skill API. |
| Kimi | generic | generate `AGENTS.md` plus core skill references | Treat as portable instructions unless the target tool supports a richer skill API. |
| Other agents | generic | generate `AGENTS.md` and `skills-index.md` | Preserve role boundaries and validation rules. |

## Primary Source Notes

- Anthropic Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Qwen Code Agent Skills: https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/
- Gemini CLI Extensions: https://google-gemini.github.io/gemini-cli/docs/extensions/
- VS Code Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills

Keep this file fresh when vendor docs change.
