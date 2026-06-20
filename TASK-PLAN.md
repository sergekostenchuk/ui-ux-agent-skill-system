# TASK-PLAN v2: UI/UX Agent Skill System Publication

plan_id: uiux-agent-skill-system-publication-2026-06-20
plan_version: 0.1.0
canonical_source: TASK-PLAN.md
status: in_progress
owner_role: docs_sync
created_at: 2026-06-20
updated_at: 2026-06-20

## Feature Layer

feature_id: F-UIUX-PUBLICATION-001
feature_title: Vendor-neutral UI/UX Agent Skill System package
rationale: Prepare the Senior UI/UX Orchestrator skill cluster for GitHub publication and use across Codex, Claude, Gemini CLI, Qwen Code, VS Code/Copilot, GLM/Z.ai, Kimi, and generic agents.
priority: P1
status: done
goal: Produce a clean publication package with canonical skills, runtime adapters, docs, safety policy, evals, deterministic linter, and generated runtime projections.
scope_in:
- `core/skills`
- `core/shared`
- `adapters`
- `docs`
- `evals`
- `scripts`
- `dist` generated projections
scope_out:
- live vendor CLI tests
constraints:
- No local private paths.
- No real credentials.
- No hidden placeholders.
- Native support claims only where the adapter uses a documented compatible structure.
security_privacy_notes:
- Local-first by default.
- Stitch, Figma, and external APIs require explicit approval and environment variables.
wiki_do_not_store:
- API keys
- tokens
- cookies
- private screenshots
- private URLs
- `.env` contents

## Execution Governance

mode: DOCS_AND_PACKAGE, NO-FICTION, NO-SECRETS, NO-PLACEHOLDERS
done_policy:
- source package exists
- adapters exist
- build script runs
- linter passes before and after build
- validation evidence is recorded
rollback_policy:
- remove `PUBLICATION/ui-ux-agent-skill-system`
- restore from git if later committed and rejected

## Task Register

| task_id | title | status | owner_role |
|---|---|---|---|
| T-001 | Create publication package structure | done | implementer |
| T-002 | Copy and sanitize canonical skills | done | implementer |
| T-003 | Add vendor adapters | done | implementer |
| T-004 | Add docs, security, evals, scripts | done | implementer |
| T-005 | Build runtime projections | done | tester |
| T-006 | Validate package | done | tester |

## Task Blocks

### T-001

task_id: T-001
title: Create publication package structure
status: done
owner_role: implementer
dependencies: none
scope_in:
- package directories
acceptance_criteria:
- clean staging package exists separate from local repo internals
commands_run:
- `mkdir -p .../PUBLICATION/ui-ux-agent-skill-system/...`
artifact_locations:
- `PUBLICATION/ui-ux-agent-skill-system/`

### T-002

task_id: T-002
title: Copy and sanitize canonical skills
status: done
owner_role: implementer
dependencies:
- T-001
acceptance_criteria:
- core skills copied
- shared contracts copied
- local absolute paths removed
commands_run:
- `rsync` copy from local Codex skills into `core/skills` and `core/shared`
- path sanitization from local absolute paths to portable variables/relative references
artifact_locations:
- `core/skills/`
- `core/shared/`

### T-003

task_id: T-003
title: Add vendor adapters
status: done
owner_role: implementer
dependencies:
- T-002
acceptance_criteria:
- adapters exist for Codex, Claude, Gemini CLI, Qwen Code, VS Code/Copilot, GLM/Z.ai, Kimi, generic agents
artifact_locations:
- `adapters/`

### T-004

task_id: T-004
title: Add docs, security, evals, scripts
status: done
owner_role: implementer
dependencies:
- T-003
acceptance_criteria:
- README, install, architecture, skill map, vendor compatibility, security, evals, linter, build script exist
artifact_locations:
- `README.md`
- `SECURITY.md`
- `docs/`
- `evals/evals.json`
- `scripts/`

### T-005

task_id: T-005
title: Build runtime projections
status: done
owner_role: tester
dependencies:
- T-004
acceptance_criteria:
- generated projections exist under `dist`
commands_run:
- `python3 scripts/build_adapters.py . --out dist`
artifact_locations:
- `dist/codex/`
- `dist/claude/`
- `dist/qwen-code/`
- `dist/copilot-vscode/`
- `dist/gemini-cli/`
- `dist/glm-zai/`
- `dist/kimi/`
- `dist/generic-agent/`

### T-006

task_id: T-006
title: Validate package
status: done
owner_role: tester
dependencies:
- T-005
acceptance_criteria:
- package linter passes
- Gemini extension JSON parses
- no local path or secret pattern detected
commands_run:
- `python3 scripts/lint_publication_package.py .`
- `python3 scripts/build_adapters.py . --out dist`
- `python3 scripts/lint_publication_package.py .`
- `python3 -m json.tool dist/gemini-cli/ui-ux-agent-skill-system/gemini-extension.json`
artifact_locations:
- `reports/`

## Active Alarms

feature_active_alarms:
- none

## Remaining Decisions

- License: Apache-2.0.
- Repository name: `ui-ux-agent-skill-system` unless an existing remote blocks it.
- Repository visibility: public, because publication under an open-source license was requested.
- Include `dist/`: yes, prebuilt runtime projections should be published alongside canonical `core`.

## Remaining Work

- Initialize standalone git repository for the publication package.
- Create or attach GitHub remote.
- Commit and push.
