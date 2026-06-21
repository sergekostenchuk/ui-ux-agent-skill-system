# TASK-PLAN v2: UI/UX Agent Skill System Publication

plan_id: uiux-agent-skill-system-publication-2026-06-20
plan_version: 0.2.0
canonical_source: TASK-PLAN.md
status: active
owner_role: planner
created_at: 2026-06-20
updated_at: 2026-06-21

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
- npm package metadata and installer CLI
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

## Feature Layer: Runtime Hardening

feature_id: F-UIUX-HARDENING-002
feature_title: Runtime enforcement, CI, evals, freshness, and release hardening
rationale: Address the external critique that the package currently relies too heavily on prompt-level discipline, manual validation, and static data without CI-backed regression gates.
priority: P1
status: planned
goal: Upgrade the published skill package from a publishable v0.1 system into a mechanically checked v0.2 system with evidence validation, executable evals, CI, dist drift detection, freshness metadata, and honest vendor-neutral wording.
scope_in:
- evidence report validator
- deterministic eval runner
- GitHub Actions CI
- core-to-dist drift guard
- UI/UX Pro Max data freshness metadata
- vendor-neutral wording clarification
- npm 0.2.0 release gate
- Obsidian LLM Wiki sync
scope_out:
- automated npm publish from CI
- paid LLM eval judging
- live Stitch/Figma integration tests requiring credentials
- removing optional vendor integrations
changed_subsystems:
- `scripts`
- `.github/workflows`
- `evals`
- `core/shared`
- `core/skills/ui-ux-pro-max/data`
- `docs`
- `dist`
- `reports`
- `package.json`
constraints:
- local deterministic checks first
- no secrets in repo, docs, logs, reports, wiki, or CI
- CI cannot require private credentials
- `dist` remains generated from `core`
assumptions:
- npm release target remains `@mlllm/ui-ux-agent-skill-system`
- GitHub repository remains `sergekostenchuk/ui-ux-agent-skill-system`
- first hardening release should be `0.2.0`
open_questions:
- whether later releases should add optional LLM-judge evals outside CI
- whether `@sergekostenchuk` npm scope should be created separately
risks:
- evidence validator can be too strict for human-written reports
- freshness metadata can create false confidence if dates are invented
- CI can drift from local developer workflow
regression_risks:
- package tarball grows or excludes generated projections accidentally
- docs claim stronger guarantees than validators actually enforce
- npm package name changes would break install instructions
security_privacy_notes:
- never store npm tokens, OTP, recovery codes, API keys, private screenshots, or private URLs
- use temporary auth only for publish operations
non_functional_requirements:
- hardening checks must run locally without network by default
- CI checks must be reproducible and fail with clear errors
milestones:
- M1: plan and wiki sync
- M2: evidence/eval/drift/freshness scripts
- M3: CI integration
- M4: docs wording and validation report
- M5: npm 0.2.0 release
wiki_pages_to_read_before:
- `projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_facts_to_capture:
- critique-driven roadmap for evidence validation, evals, CI, drift, freshness, and vendor wording
- npm package is published as `@mlllm/ui-ux-agent-skill-system`
- `@sergekostenchuk` npm scope remains a separate possible future decision
wiki_do_not_store:
- npm tokens
- OTP or recovery codes
- private npm logs
- private browser/session data

## Execution Governance

mode: DOCS_AND_PACKAGE, RUNTIME_HARDENING, NO-FICTION, NO-SECRETS, NO-PLACEHOLDERS
done_policy:
- source package exists
- adapters exist
- build script runs
- linter passes before and after build
- validation evidence is recorded
- hardening tasks cannot close without executed commands in `commands_run`
- `Ran` evidence must be backed by validator-compatible artifacts or explicit supported external evidence
- eval runner, dist drift guard, freshness checker, and npm pack must pass before `0.2.0` release
- docs must distinguish vendor-neutral core from optional vendor-specific integrations
rollback_policy:
- remove `PUBLICATION/ui-ux-agent-skill-system`
- restore from git if later committed and rejected
- for hardening tasks, revert the specific script/docs/CI change and keep npm `0.1.0` as the last stable published version until all gates pass

## Task Register

| task_id | title | status | owner_role |
|---|---|---|---|
| T-001 | Create publication package structure | done | implementer |
| T-002 | Copy and sanitize canonical skills | done | implementer |
| T-003 | Add vendor adapters | done | implementer |
| T-004 | Add docs, security, evals, scripts | done | implementer |
| T-005 | Build runtime projections | done | tester |
| T-006 | Validate package | done | tester |
| T-007 | Add npm distribution layer | done | implementer |
| T-008 | Add evidence report validator | done | docs_sync |
| T-009 | Add eval runner and golden route checks | done | docs_sync |
| T-010 | Add GitHub Actions CI gates | done | docs_sync |
| T-011 | Add core-to-dist drift guard | done | docs_sync |
| T-012 | Add data freshness manifest and checker | done | docs_sync |
| T-013 | Clarify vendor-neutral core wording | done | docs_sync |
| T-014 | Prepare npm 0.2.0 release gate | ready | planner |
| T-015 | Sync hardening decisions to Obsidian LLM Wiki | done | docs_sync |

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

### T-007

task_id: T-007
title: Add npm distribution layer
status: done
owner_role: implementer
dependencies:
- T-006
acceptance_criteria:
- package metadata exists
- `uiux-skills` CLI can list targets
- npm dry-run packaging works
- npm publication blocker is explicit if auth is missing
artifact_locations:
- `package.json`
- `bin/uiux-skills.js`
- `docs/npm.md`
commands_run:
- `node bin/uiux-skills.js list`
- `node bin/uiux-skills.js path`
- `node bin/uiux-skills.js install qwen-code --dest /tmp/uiux-skills-npm-test/.qwen/skills --dry-run`
- `node bin/uiux-skills.js install generic-agent --dest /tmp/uiux-skills-npm-test/generic --dry-run`
- `npm pack --dry-run`

### T-008

task_id: T-008
title: Add evidence report validator
rationale: Convert the `Ran`/`Skipped`/`Planned`/`Manual` honesty contract from prompt-only guidance into a mechanical validation gate.
priority: P1
status: done
dependencies:
- T-007
blocked_by: none
unblocks:
- T-010
- T-014
task_size: M
goal: Add a deterministic validator that fails when reports claim executed evidence without concrete commands, paths, URLs, or supported external evidence references.
scope_in:
- `scripts/validate_evidence_report.py`
- report fixtures under `tests/fixtures/evidence/` or `evals/fixtures/evidence/`
- README/docs references to evidence validation
scope_out:
- parsing every possible freeform human report
- verifying private external systems
changed_subsystems:
- scripts
- reporting contract
- validation docs
candidate_files:
- `scripts/validate_evidence_report.py`
- `core/shared/reporting-contract.md`
- `docs/architecture.md`
- `reports/package-validation.md`
forbidden_areas:
- npm tokens
- private screenshots
- `.env` files
constraints:
- validator must not require network access for local evidence checks
- false positives should fail closed only for explicit `Ran` claims
acceptance_criteria:
- reports with `Ran` artifact paths fail when paths do not exist
- reports with `Planned` checks do not count as executed evidence
- command exits non-zero on invalid evidence
- command exits zero on known-valid fixtures
acceptance_checks:
- valid fixture passes
- missing artifact fixture fails
- planned-only fixture does not satisfy `Ran`
tests_required: yes
test_levels:
- unit
- smoke
test_targets:
- evidence parser
- artifact existence checks
- exit codes
test_data_origin: synthetic fixtures
oracle: validator exit code and fixture-specific expected failures
negative_tests:
- `Ran` with missing file path
- `Ran` with placeholder path
- accessibility claim without artifact or manual label
determinism_notes:
- local filesystem only
- no clocks except report timestamps
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `python3 scripts/validate_evidence_report.py tests/fixtures/evidence/valid.md`
- `python3 scripts/validate_evidence_report.py tests/fixtures/evidence/missing-artifact.md`
- `python3 scripts/lint_publication_package.py .`
commands_run:
- `python3 scripts/validate_evidence_report.py tests/fixtures/evidence/valid.md`
- `bash -lc 'if python3 scripts/validate_evidence_report.py tests/fixtures/evidence/missing-artifact.md; then echo unexpected-pass; exit 1; else echo expected-failure-missing-artifact; fi'`
- `bash -lc 'if python3 scripts/validate_evidence_report.py --require-ran tests/fixtures/evidence/planned-only.md; then echo unexpected-pass; exit 1; else echo expected-failure-planned-only; fi'`
- `python3 scripts/lint_publication_package.py .`
expected_artifacts:
- `scripts/validate_evidence_report.py`
- evidence fixtures
- updated docs/reporting contract
artifact_locations:
- `scripts/validate_evidence_report.py`
- `tests/fixtures/evidence/valid.md`
- `tests/fixtures/evidence/missing-artifact.md`
- `tests/fixtures/evidence/planned-only.md`
- `tests/fixtures/evidence/artifacts/browser-smoke.txt`
- `core/shared/reporting-contract.md`
- `reports/package-validation.md`
rollback_plan:
- remove validator script and fixtures
- remove CI gate references that call it
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner defines report grammar and fixture matrix
- implementer adds validator and fixtures
- reviewer checks false-positive risk and no-secret handling
- tester runs positive and negative fixtures
- docs_sync updates reporting contract and package validation report
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if report grammar cannot cover existing reports without excessive false positives, reduce scope to machine-readable validation blocks and record manual report limitations.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- tokens
- private artifact paths
- secret-bearing reports
active_alarm_ids: []
resolved_alarm_ids: []

### T-009

task_id: T-009
title: Add eval runner and golden route checks
rationale: Existing eval JSON files define expectations, but there is no executable regression runner proving routing quality.
priority: P1
status: done
dependencies:
- T-007
blocked_by: none
unblocks:
- T-010
- T-014
task_size: M
goal: Add a local eval runner that executes routing/classification checks against golden expected skills, modes, must-have, and must-not-have constraints.
scope_in:
- `scripts/run_evals.py`
- `evals/evals.json`
- per-skill `evals/evals.json`
- routing classifier checks
scope_out:
- model-output semantic grading that requires paid LLM calls
- benchmarking all vendor runtimes
changed_subsystems:
- evals
- scripts
- routing
candidate_files:
- `scripts/run_evals.py`
- `evals/evals.json`
- `core/skills/senior-ui-ux-orchestrator/scripts/classify_product_type.py`
- `core/skills/senior-ui-ux-orchestrator/assets/routing-rules.json`
forbidden_areas:
- private prompts containing secrets
- vendor API keys
constraints:
- first runner version must be local and deterministic
- LLM-based grading may be planned later but cannot be required for CI
acceptance_criteria:
- eval runner parses all eval JSON files
- route-oriented cases assert expected skill/mode
- fail cases return non-zero exit code
- results are written to `reports/eval-results.json`
acceptance_checks:
- baseline eval command passes
- injected failing fixture fails
tests_required: yes
test_levels:
- unit
- integration
- smoke
test_targets:
- eval schema parsing
- classifier expected route matching
- result report output
test_data_origin: repository eval fixtures
oracle: deterministic JSON report with pass/fail counts and non-zero failure exit
negative_tests:
- missing required eval field
- expected route mismatch
determinism_notes:
- no network
- stable sort order for eval files and cases
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `python3 scripts/lint_publication_package.py .`
commands_run:
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `bash -lc 'if python3 scripts/run_evals.py . --eval-file tests/fixtures/evals/route-mismatch.json --out /tmp/uiux-route-mismatch.json; then echo unexpected-pass; exit 1; else echo expected-failure-route-mismatch; fi'`
- `python3 -m json.tool reports/eval-results.json`
- `python3 scripts/lint_publication_package.py .`
expected_artifacts:
- `scripts/run_evals.py`
- `reports/eval-results.json`
- updated eval schema notes
artifact_locations:
- `scripts/run_evals.py`
- `reports/eval-results.json`
- `tests/fixtures/evals/route-mismatch.json`
- `evals/evals.json`
- `core/skills/senior-ui-ux-orchestrator/scripts/classify_product_type.py`
- `core/skills/senior-ui-ux-orchestrator/assets/routing-rules.json`
rollback_plan:
- remove eval runner and CI calls
- keep eval JSON files as prompt-only fixtures if runner is reverted
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner defines deterministic eval schema
- implementer adds runner and output format
- reviewer checks coverage against colleague critique
- tester runs passing and failing cases
- docs_sync updates README and validation report
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if semantic grading cannot be deterministic, limit v0.2.0 to routing/schema evals and open a later LLM-judge task.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- private user prompts
- API keys
active_alarm_ids: []
resolved_alarm_ids: []

### T-010

task_id: T-010
title: Add GitHub Actions CI gates
rationale: Current checks are manual; CI is needed to make package lint, evals, dist drift, and npm pack reproducible for contributors.
priority: P1
status: done
dependencies:
- T-008
- T-009
- T-011
- T-012
blocked_by: none
unblocks:
- T-014
task_size: M
goal: Add `.github/workflows/ci.yml` that runs deterministic package checks on push and pull request.
scope_in:
- GitHub Actions workflow
- Python and Node setup
- package lint
- eval runner
- dist regeneration drift check
- freshness checker
- npm pack dry-run
scope_out:
- npm publish automation
- secret-dependent external integration tests
changed_subsystems:
- CI
- scripts
- package validation
candidate_files:
- `.github/workflows/ci.yml`
- `reports/package-validation.md`
- `docs/install.md`
forbidden_areas:
- repository secrets creation
- real npm tokens
constraints:
- CI must not require private credentials
- CI must not upload private artifacts
acceptance_criteria:
- workflow exists and is documented
- workflow runs without secrets
- workflow fails on dist drift, eval failure, package lint failure, and invalid freshness metadata
acceptance_checks:
- `python3 scripts/lint_publication_package.py .`
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `python3 scripts/build_adapters.py . --out dist && git diff --exit-code dist`
- `python3 scripts/check_freshness.py .`
- `npm pack --dry-run`
tests_required: yes
test_levels:
- integration
- CI smoke
test_targets:
- GitHub Actions config syntax
- local command parity
test_data_origin: repository files
oracle: all required commands pass locally before push; GitHub Actions passes after push
negative_tests:
- CI should fail if generated `dist` is stale
- CI should fail if eval runner returns non-zero
determinism_notes:
- no network except package tool installation
- npm pack should run without publishing
flakiness_risk: medium
stop_on_failure: true
commands_planned:
- `python3 scripts/lint_publication_package.py .`
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `python3 scripts/build_adapters.py . --out dist`
- `git diff --exit-code dist`
- `python3 scripts/check_freshness.py .`
- `npm pack --dry-run`
commands_run:
- `npm run lint`
- `npm run validate:evidence`
- `npm run eval`
- `npm run build:adapters`
- `npm run check:dist`
- `git diff --exit-code dist`
- `npm run check:freshness`
- `npm pack --dry-run`
expected_artifacts:
- `.github/workflows/ci.yml`
- updated package validation report
artifact_locations:
- `.github/workflows/ci.yml`
- `docs/install.md`
- `reports/package-validation.md`
- `TASK-PLAN.md`
rollback_plan:
- remove workflow file
- revert docs that claim CI coverage
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner freezes required CI gates
- implementer adds workflow
- reviewer checks no-secret and no-network assumptions
- tester runs local command parity
- docs_sync records CI status and links
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if hosted CI cannot be verified locally, keep task `needs_review` until GitHub check result is observed.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- GitHub tokens
- npm tokens
active_alarm_ids: []
resolved_alarm_ids: []

### T-011

task_id: T-011
title: Add core-to-dist drift guard
rationale: Prebuilt runtime projections are useful, but they can drift from canonical `core` without a mechanical check.
priority: P1
status: done
dependencies:
- T-007
blocked_by: none
unblocks:
- T-010
- T-014
task_size: S
goal: Make generated `dist` reproducibility a first-class validation gate.
scope_in:
- build script determinism
- dist diff check
- validation docs
scope_out:
- removing `dist` from publication
changed_subsystems:
- adapter build
- validation
candidate_files:
- `scripts/build_adapters.py`
- `scripts/lint_publication_package.py`
- `reports/package-validation.md`
- `.github/workflows/ci.yml`
forbidden_areas:
- generated files edited by hand without regeneration
constraints:
- `dist` remains published for easy installs
- canonical source remains `core`
acceptance_criteria:
- documented command regenerates `dist`
- drift command fails if generated output differs
- CI task consumes this guard
acceptance_checks:
- regenerate `dist`
- verify `git diff --exit-code dist`
tests_required: yes
test_levels:
- smoke
test_targets:
- adapter generation output
- git diff drift check
test_data_origin: repository source
oracle: no diff after deterministic regeneration
negative_tests:
- hand-edit generated `dist` and verify drift is detected manually or in a fixture branch
determinism_notes:
- stable skill ordering
- stable JSON formatting
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `python3 scripts/build_adapters.py . --out dist`
- `git diff --exit-code dist`
- `python3 scripts/lint_publication_package.py .`
commands_run:
- `python3 scripts/build_adapters.py . --out dist`
- `python3 scripts/check_dist_sync.py .`
- `python3 scripts/lint_publication_package.py .`
expected_artifacts:
- documented drift command
- updated validation report
artifact_locations:
- `scripts/check_dist_sync.py`
- `dist/`
- `package.json`
- `reports/package-validation.md`
rollback_plan:
- revert guard docs and CI references
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner defines canonical/generated boundary
- implementer updates scripts/docs if needed
- reviewer checks generated-output policy
- tester runs regeneration and diff
- docs_sync records result
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if generation is non-deterministic, fix build ordering before CI is allowed to depend on the guard.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- none
active_alarm_ids: []
resolved_alarm_ids: []

### T-012

task_id: T-012
title: Add data freshness manifest and checker
rationale: UI/UX Pro Max includes static CSV data that can become stale without source dates and an update process.
priority: P1
status: done
dependencies:
- T-007
blocked_by: none
unblocks:
- T-010
- T-014
task_size: M
goal: Add machine-readable freshness metadata and a checker for static design-intelligence datasets.
scope_in:
- UI/UX Pro Max CSV freshness metadata
- source URLs or source categories
- last checked dates
- stale threshold policy
- local checker script
scope_out:
- fully automatic crawling/updating of every dataset
- web scraping during CI
changed_subsystems:
- data layer
- freshness policy
- validation scripts
candidate_files:
- `core/skills/ui-ux-pro-max/data/freshness.json`
- `scripts/check_freshness.py`
- `core/shared/freshness-sources.md`
- `reports/package-validation.md`
forbidden_areas:
- invented source dates
- unverified version-specific claims
constraints:
- stale does not always mean invalid; checker should distinguish warning and blocking states
- CI should not require live network freshness checks
acceptance_criteria:
- each major CSV group has source and `last_checked_at`
- checker reports stale or missing metadata
- stale policy is documented
- package validation records freshness status
acceptance_checks:
- freshness checker passes current metadata
- missing metadata fixture fails
tests_required: yes
test_levels:
- unit
- smoke
test_targets:
- freshness manifest parsing
- stale threshold checks
- missing source checks
test_data_origin: synthetic freshness fixture plus repository metadata
oracle: deterministic pass/fail JSON or console output
negative_tests:
- missing `last_checked_at`
- invalid date
- missing source URL/category
determinism_notes:
- CI uses recorded dates only
- no live web fetch in default mode
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `python3 scripts/check_freshness.py .`
- `python3 scripts/lint_publication_package.py .`
commands_run:
- `python3 scripts/check_freshness.py .`
- `bash -lc 'if python3 scripts/check_freshness.py tests/fixtures/freshness/missing-metadata; then echo unexpected-pass; exit 1; else echo expected-failure-missing-freshness-metadata; fi'`
- `python3 scripts/lint_publication_package.py .`
expected_artifacts:
- `core/skills/ui-ux-pro-max/data/freshness.json`
- `scripts/check_freshness.py`
- updated freshness docs
artifact_locations:
- `core/skills/ui-ux-pro-max/data/freshness.json`
- `scripts/check_freshness.py`
- `tests/fixtures/freshness/missing-metadata/core/skills/ui-ux-pro-max/data/freshness.json`
- `tests/fixtures/freshness/missing-metadata/core/skills/ui-ux-pro-max/data/example.csv`
- `core/shared/freshness-sources.md`
- `package.json`
- `reports/package-validation.md`
rollback_plan:
- remove freshness checker and metadata
- revert CI references
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner defines dataset groups and thresholds
- implementer adds manifest/checker
- reviewer checks source honesty and no invented freshness
- tester runs valid and invalid metadata cases
- docs_sync updates freshness documentation
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if source dates cannot be verified, mark the affected dataset as `manual` or `unknown` rather than inventing freshness.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- private source URLs
- credentials
active_alarm_ids: []
resolved_alarm_ids: []

### T-013

task_id: T-013
title: Clarify vendor-neutral core wording
rationale: The package has a portable core, but optional integrations such as Figma and Stitch are vendor-specific; public wording should reflect that distinction.
priority: P2
status: ready
dependencies:
- T-007
blocked_by: none
unblocks:
- T-014
task_size: S
goal: Replace overbroad `vendor-neutral` claims with `vendor-neutral core with optional vendor-specific adapters/integrations` wording.
scope_in:
- README
- package description if needed
- docs architecture and compatibility pages
- npm docs
scope_out:
- removing Stitch or Figma skills
- changing package name
changed_subsystems:
- documentation
- package metadata wording
candidate_files:
- `README.md`
- `docs/architecture.md`
- `docs/vendor-compatibility.md`
- `docs/npm.md`
- `package.json`
forbidden_areas:
- functional skill behavior
constraints:
- keep the package positioning clear for designers and developers
- do not imply Stitch or Figma are required
acceptance_criteria:
- README states optional vendor-specific integrations
- Stitch is described as optional exploration, not a required dependency
- package metadata remains accurate
acceptance_checks:
- grep for unsupported broad vendor-neutral claims
- package lint passes
tests_required: yes
test_levels:
- docs lint
- package smoke
test_targets:
- public wording
- package metadata
test_data_origin: repository docs
oracle: no misleading mandatory-vendor claims remain
negative_tests:
- broad claim that all runtime capabilities are vendor-neutral
determinism_notes:
- text-only check
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `rg -n "vendor-neutral|Stitch|Figma" README.md docs package.json`
- `python3 scripts/lint_publication_package.py .`
commands_run:
- `rg -n "vendor-neutral|Vendor-neutral|Stitch|Figma" README.md docs package.json`
- `python3 scripts/lint_publication_package.py .`
expected_artifacts:
- updated docs wording
artifact_locations:
- `README.md`
- `docs/architecture.md`
- `docs/vendor-compatibility.md`
- `docs/npm.md`
- `package.json`
- `reports/package-validation.md`
- `TASK-PLAN.md`
rollback_plan:
- revert docs/metadata wording changes
owner_role: docs_sync
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner defines exact wording boundary
- implementer updates docs
- reviewer checks promise/reality alignment
- tester runs grep and package lint
- docs_sync updates validation report
required_approvals:
- reviewer
max_review_loops: 2
escalation_rule: if wording becomes too vague for npm positioning, keep current package name but add a prominent limitations section.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- none
active_alarm_ids: []
resolved_alarm_ids: []

### T-014

task_id: T-014
title: Prepare npm 0.2.0 release gate
rationale: npm version `0.1.0` is immutable; hardening changes require a version bump and release gate after validation passes.
priority: P1
status: ready
dependencies:
- T-008
- T-009
- T-010
- T-011
- T-012
- T-013
blocked_by: none
unblocks: none
task_size: S
goal: Prepare and publish `0.2.0` only after CI, eval, evidence, dist, freshness, and docs gates pass.
scope_in:
- `package.json` version bump
- changelog/release notes
- npm pack
- npm publish
- validation report update
scope_out:
- automated npm publish from CI
- changing GitHub repository name
changed_subsystems:
- release
- npm metadata
- docs
candidate_files:
- `package.json`
- `README.md`
- `reports/package-validation.md`
- `TASK-PLAN.md`
forbidden_areas:
- npm tokens in files
- recovery codes in logs
constraints:
- publish only with temporary local auth or CI secret approved separately
- do not republish `0.1.0`
acceptance_criteria:
- version bumped to `0.2.0`
- all validation commands pass
- npm package visible after publish
- GitHub pushed before npm publish
acceptance_checks:
- `npm pack --dry-run`
- `npm view @mlllm/ui-ux-agent-skill-system version`
- `npm exec --yes --package @mlllm/ui-ux-agent-skill-system -- uiux-skills list`
tests_required: yes
test_levels:
- release smoke
test_targets:
- npm package metadata
- CLI entrypoint
test_data_origin: package registry
oracle: npm registry reports `0.2.0` and CLI runs from npm
negative_tests:
- publish without passing CI gates is forbidden
determinism_notes:
- registry propagation delay possible; verify with raw registry or fresh npm cache
flakiness_risk: medium
stop_on_failure: true
commands_planned:
- `python3 scripts/lint_publication_package.py .`
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `python3 scripts/build_adapters.py . --out dist`
- `git diff --exit-code dist`
- `python3 scripts/check_freshness.py .`
- `npm pack --dry-run`
- `npm publish --access public`
- `npm view @mlllm/ui-ux-agent-skill-system version`
commands_run:
- `python3 scripts/lint_publication_package.py .`
- `python3 scripts/run_evals.py . --out reports/eval-results.json`
- `python3 scripts/build_adapters.py . --out dist`
- `python3 scripts/check_dist_sync.py .`
- `python3 scripts/check_freshness.py .`
- `npm pack --dry-run --json`
expected_artifacts:
- GitHub commit and push
- npm `0.2.0` package
- updated validation report
artifact_locations:
- `package.json`
- `CHANGELOG.md`
- `scripts/build_adapters.py`
- `dist/gemini-cli/ui-ux-agent-skill-system/gemini-extension.json`
- `reports/package-validation.md`
- `TASK-PLAN.md`
rollback_plan:
- before publish: revert version bump
- after publish: publish follow-up patch version; npm versions are immutable
owner_role: planner
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner verifies all dependencies done
- implementer bumps version and release notes
- reviewer confirms no secrets and no stale claims
- tester runs full release gate
- docs_sync records npm/GitHub publication evidence
required_approvals:
- reviewer
- tester
max_review_loops: 2
escalation_rule: if npm auth/scope blocks publish, keep GitHub release ready and record the npm blocker without leaking credentials.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- npm tokens
- OTP or recovery codes
- private npm logs
active_alarm_ids: []
resolved_alarm_ids: []

### T-015

task_id: T-015
title: Sync hardening decisions to Obsidian LLM Wiki
rationale: The hardening critique and roadmap are project knowledge that should survive outside the chat and repository task list.
priority: P2
status: done
dependencies:
- T-007
blocked_by: none
unblocks:
- T-014
task_size: S
goal: Update the Obsidian LLM Wiki with project overview and hardening roadmap pages, including provenance and links back to the GitHub/npm artifacts.
scope_in:
- project overview page
- hardening roadmap concept page
- wiki index/log/hot updates
- manifest entry if missing
scope_out:
- storing npm tokens, recovery codes, private logs, or browser session details
changed_subsystems:
- Obsidian wiki
- project knowledge base
candidate_files:
- `$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
- `$OBSIDIAN_VAULT_PATH/index.md`
- `$OBSIDIAN_VAULT_PATH/log.md`
- `$OBSIDIAN_VAULT_PATH/hot.md`
- `$OBSIDIAN_VAULT_PATH/.manifest.json`
forbidden_areas:
- wiki entries containing secrets
- raw token values
- private npm recovery codes
constraints:
- use wiki provenance markers for inferred critique/rationale
- keep Obsidian links valid
acceptance_criteria:
- wiki project overview exists
- hardening roadmap page exists
- index/log/hot reference the update
- manifest contains project entry
acceptance_checks:
- `test -f "$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md"`
- `test -f "$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md"`
- `python3 -m json.tool "$OBSIDIAN_VAULT_PATH/.manifest.json"`
tests_required: yes
test_levels:
- smoke
test_targets:
- wiki files
- manifest JSON
- secret exclusion by grep
test_data_origin: project docs and task plan
oracle: files exist, JSON parses, no secret-like values from npm tokens/recovery codes are present
negative_tests:
- grep wiki update for token-like npm secret values
determinism_notes:
- timestamps are the only time-dependent field
flakiness_risk: low
stop_on_failure: true
commands_planned:
- `python3 -m json.tool "$OBSIDIAN_VAULT_PATH/.manifest.json"`
- `rg -n "npm_[A-Za-z0-9]|_authToken|AQ\\.[A-Za-z0-9_-]{12,}" "$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system"`
commands_run:
- `mkdir -p "$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system/concepts"`
- `python3 -m json.tool "$OBSIDIAN_VAULT_PATH/.manifest.json"`
- `rg -n "npm_[A-Za-z0-9]|_authToken|AQ\\.[A-Za-z0-9_-]{12,}" "$OBSIDIAN_VAULT_PATH/projects/ui-ux-agent-skill-system" "$OBSIDIAN_VAULT_PATH/.manifest.json" "$OBSIDIAN_VAULT_PATH/index.md" "$OBSIDIAN_VAULT_PATH/log.md" "$OBSIDIAN_VAULT_PATH/hot.md" || true`
expected_artifacts:
- wiki overview page
- wiki hardening roadmap page
- updated index/log/hot/manifest
artifact_locations:
- `projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
- `index.md`
- `log.md`
- `hot.md`
- `.manifest.json`
rollback_plan:
- remove new wiki project directory and revert index/log/hot/manifest updates
owner_role: planner
agent_sequence:
- planner
- implementer
- reviewer
- tester
- docs_sync
agent_contracts:
- planner selects wiki page structure
- implementer writes distilled pages
- reviewer checks provenance and no-secret policy
- tester validates files and manifest
- docs_sync records sync result in package validation report if release proceeds
required_approvals:
- reviewer
max_review_loops: 2
escalation_rule: if wiki vault structure is incomplete, create minimal project pages and record skipped optional QMD refresh.
wiki_pages_to_update_after:
- `projects/ui-ux-agent-skill-system/ui-ux-agent-skill-system.md`
- `projects/ui-ux-agent-skill-system/concepts/runtime-hardening-roadmap.md`
wiki_do_not_store:
- npm tokens
- OTP or recovery codes
- private npm logs
active_alarm_ids: []
resolved_alarm_ids: []

## Active Alarms

feature_active_alarms:
- none

## Remaining Decisions

- License: Apache-2.0.
- Repository name: `ui-ux-agent-skill-system` unless an existing remote blocks it.
- Repository visibility: public, because publication under an open-source license was requested.
- Include `dist/`: yes, prebuilt runtime projections should be published alongside canonical `core`.

## Publication

repository_url: https://github.com/sergekostenchuk/ui-ux-agent-skill-system
published_branch: main
initial_commit: 5f0e3ba
published_at: 2026-06-20

### Completed Work

- Standalone git repository initialized.
- GitHub remote created.
- Initial package committed and pushed.

## npm Publication

package_name: `@mlllm/ui-ux-agent-skill-system`
npm_status: published
npm_url: https://www.npmjs.com/package/@mlllm/ui-ux-agent-skill-system
npm_version: 0.1.0
npm_published_at: 2026-06-20
npm_blocker: none; previous `@sergekostenchuk` target requires separate npm scope access.
npm_pack_dry_run: passed
npm_tarball_size: 3.2 MB
npm_unpacked_size: 19.5 MB
npm_total_files: 1914
