---
name: llm-wiki-maintainer
description: Use when the task involves a filesystem-based LLM Wiki or Obsidian vault, especially Ar9av/obsidian-wiki projects using .skills, .env, ~/.obsidian-wiki/config, AGENTS.md, .manifest.json, index.md/log.md/hot.md, ingest/query/lint workflows, or Russian prompts like "добавь в вики", "сделай ingest", "lint wiki", "обнови index/log", or "разложи по obsidian-wiki".
---

# LLM Wiki Maintainer

## Overview

Use this skill for persistent markdown knowledge bases maintained as compiled
Obsidian-compatible wiki artifacts.

Priority order:

1. For new setup/deploy/init requests, deploy `Ar9av/obsidian-wiki` by default.
2. Prefer the `Ar9av/obsidian-wiki` framework when it is present.
3. If a legacy `raw/` + `wiki/` LLM Wiki is already present, work with it
   without breaking it, but propose migrating to `obsidian-wiki`.
4. Create or extend a legacy layout only when the user explicitly requests the
   old standard LLM Wiki format.

Treat the wiki as a maintained system, not as a pile of notes.

## Default Deployment Behavior

When the user invokes this skill for setup, deployment, initialization, or a new
wiki, and no existing wiki contract has to be preserved, deploy
`Ar9av/obsidian-wiki` as the default implementation.

Default deployment means:

1. Create or populate the target directory as an `obsidian-wiki` repo from
   `https://github.com/Ar9av/obsidian-wiki`.
2. Preserve any existing user files in the target directory.
3. Create `.env` with `OBSIDIAN_VAULT_PATH` set to the target vault.
4. Initialize the vault files and directories:
   - `index.md`
   - `log.md`
   - `hot.md`
   - `.manifest.json`
   - `.obsidian/`
   - `_meta/`
   - `_raw/`
   - `_archives/`
   - `concepts/`, `entities/`, `skills/`, `references/`, `synthesis/`,
     `journal/`, `projects/`
5. Ensure `~/.obsidian-wiki/config` points to the selected vault/repo when doing
   so is safe.
6. Install only the needed Codex skill symlinks into `~/.codex/skills` unless
   the user asks to run the full upstream `setup.sh`.
7. Keep upstream framework git state clean by excluding local vault artifacts
   from accidental upstream commits when the repo uses
   `Ar9av/obsidian-wiki` as `origin`.

Do not ask whether the user wants the legacy layout when the request is simply
"set up my wiki", "разверни wiki", "создай Obsidian wiki", or similar. Use
`obsidian-wiki` unless the user explicitly names the old layout.

## Legacy LLM Wiki Compatibility

Legacy mode is for already-existing standard LLM Wiki layouts such as:

- `WIKI-SCHEMA.md`
- `raw/`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/sources/`
- `wiki/concepts/`, `wiki/entities/`, `wiki/analyses/`

When legacy mode is detected:

1. Work with the existing layout safely.
2. Do not move, rename, or rewrite the legacy wiki without explicit approval.
3. Tell the user that the current wiki is legacy/standard LLM Wiki.
4. Recommend migrating to `Ar9av/obsidian-wiki` for future work unless there is
   a clear reason to keep the old structure.
5. Offer a migration path:
   - preserve `raw/` as source material or map it to `_raw/`
   - map `wiki/sources/` to `references/`
   - map `wiki/concepts/` to `concepts/`
   - map `wiki/entities/` to `entities/`
   - map `wiki/analyses/` to `synthesis/`
   - convert `wiki/index.md` and `wiki/log.md` into root `index.md` and
     `log.md`
   - create `.manifest.json`, `hot.md`, `_meta/`, and `.obsidian/`

Only perform the migration after the user asks for it or clearly authorizes it.

## Obsidian-Wiki Priority

Assume `obsidian-wiki` mode when any of these are present:

- `.skills/llm-wiki/SKILL.md`
- `.skills/wiki-ingest/SKILL.md`, `.skills/wiki-query/SKILL.md`, or related
  wiki skills
- `AGENTS.md` beginning with Obsidian Wiki agent context
- `.env` containing `OBSIDIAN_VAULT_PATH`
- `~/.obsidian-wiki/config`
- vault files such as `.manifest.json`, `hot.md`, `_meta/taxonomy.md`, `_raw/`

In this mode, follow the framework contract before local habits:

1. Resolve config.
   - Walk up from CWD looking for `.env` with `OBSIDIAN_VAULT_PATH`.
   - If not found, read `~/.obsidian-wiki/config`.
   - The resolved `OBSIDIAN_VAULT_PATH` is the vault root.
   - The resolved `OBSIDIAN_WIKI_REPO`, when present, is the framework repo.
2. Read control files.
   - Read repo `AGENTS.md` when present.
   - Then read `$OBSIDIAN_VAULT_PATH/AGENTS.md` when present; it overrides
     framework defaults for owner-specific conventions.
   - For operation-specific work, read the matching
     `.skills/<skill-name>/SKILL.md` from the repo before acting.
3. Use the `obsidian-wiki` vault shape.
   - Root special files: `index.md`, `log.md`, `hot.md`, `.manifest.json`.
   - Metadata: `_meta/`, `_raw/`, `_archives/`, `.obsidian/`.
   - Categories: `concepts/`, `entities/`, `skills/`, `references/`,
     `synthesis/`, `journal/`, and `projects/`.
4. Keep the compiled layer in the vault root categories, not in `wiki/`, unless
   the detected contract explicitly uses legacy paths.

Local default in this environment:

- `$HOME/TG-NEWS-151` is an `obsidian-wiki` repo and vault.
- `$HOME/.obsidian-wiki/config` points to that vault.

## Quick Start

1. Find the contract.
   - First detect `obsidian-wiki` mode using the rules above.
   - In `obsidian-wiki` mode, resolve `.env` or `~/.obsidian-wiki/config`,
     read `AGENTS.md`, then read vault `index.md`, `log.md`, and `hot.md`.
   - In legacy mode, if the vault has `WIKI-SCHEMA.md`, read it first.
   - Then read local `AGENTS.md` if present.
   - Then read legacy `wiki/index.md` and `wiki/log.md`.
   - If no contract exists and the task is setup/init/deploy, create an
     `obsidian-wiki` setup by default.
   - For whole-workspace vaults, read the corpus-policy page before ingesting
     when one exists.
2. Respect source boundaries.
   - Treat `_raw/`, `raw/`, and external corpus files as read-only unless
     explicitly told to edit them.
   - In `obsidian-wiki` mode, write compiled knowledge only into vault category
     directories such as `references/`, `concepts/`, `entities/`, `synthesis/`,
     `journal/`, and `projects/`.
   - In legacy mode, write compiled knowledge only into `wiki/`.
3. Pick the operation.
   - `ingest`
   - `query`
   - `lint`

## When To Use

- The user mentions `LLM Wiki`, `Obsidian`, `vault`, `raw/`, `wiki/`,
  `wiki/index.md`, `wiki/log.md`, `WIKI-SCHEMA.md`, or `AGENTS.md`.
- The user mentions `obsidian-wiki`, `Ar9av/obsidian-wiki`, `.manifest.json`,
  `.skills/wiki-*`, `_raw/`, `hot.md`, `wiki-status`, `wiki-ingest`, or
  `wiki-query`.
- The task involves converting source files into Markdown before ingest, or the
  user mentions `MarkItDown`, `markitdown`, document-to-markdown conversion,
  PDF/DOCX/PPTX/HTML import, or asks to prepare raw source material for a wiki.
- The user wants to ingest sources, answer from the wiki, reconcile
  contradictions, or maintain a persistent knowledge base.
- The user uses Russian prompts such as:
  - `добавь в вики`
  - `сделай ingest`
  - `обнови index/log`
  - `lint wiki`
  - `разложи по вики`

## Workflow

### Obsidian-Wiki Operation Routing

When in `obsidian-wiki` mode, prefer the matching framework skill instructions:

- Setup or repair: read `.skills/wiki-setup/SKILL.md`.
- Ingest: read `.skills/wiki-ingest/SKILL.md` or
  `.skills/data-ingest/SKILL.md` for raw text/export data.
- Query: read `.skills/wiki-query/SKILL.md`.
- Status/delta: read `.skills/wiki-status/SKILL.md`.
- Lint: read `.skills/wiki-lint/SKILL.md`.
- Rebuild/archive: read `.skills/wiki-rebuild/SKILL.md`.
- Cross-linking: read `.skills/cross-linker/SKILL.md`.
- Tags: read `.skills/tag-taxonomy/SKILL.md`.
- Project sync: read `.skills/wiki-update/SKILL.md`.

If a requested workflow is already covered by an installed `obsidian-wiki`
skill, follow that skill's contract rather than reinterpreting the task from
this generic skill.

### Ingest

Use when a new source, folder, note, or workspace slice should become durable
knowledge.

In `obsidian-wiki` mode:

1. Resolve config and read control files.
2. Read the source carefully without mutating it.
3. Create or update a source/reference page in `references/` unless the
   operation-specific skill says a different category is correct.
4. Update durable pages in `concepts/`, `entities/`, `skills/`, `synthesis/`,
   `journal/`, or `projects/` as appropriate.
5. Update `index.md`, `log.md`, `hot.md`, and `.manifest.json`.
6. Preserve provenance in frontmatter fields such as `sources`, `summary`,
   `provenance`, `base_confidence`, `lifecycle`, `created`, and `updated` when
   following the framework templates.

Legacy mode:

Steps:

1. Read the source carefully.
2. Create or update one source page in `wiki/sources/`.
3. Update the affected durable pages in `wiki/entities/`,
   `wiki/concepts/`, or `wiki/analyses/`.
4. Update `wiki/index.md`.
5. Append an entry to `wiki/log.md`.

Rules:

- Prefer one source page per source item when practical.
- For tightly related documents, use one bundle source page and list every
  member in `sources`.
- Preserve provenance. Do not rewrite source material in place.

### MarkItDown-Assisted Ingest

Use when source material exists in non-markdown formats and should be prepared
for wiki ingest without inventing content.

Typical cases:

- PDF
- DOCX
- PPTX
- HTML
- copied exports or downloaded source bundles that are easier to ingest after
  markdown conversion

Rules:

- Treat original files as read-only unless explicitly told otherwise.
- In `obsidian-wiki` mode, prefer writing converted artifacts into `_raw/` or
  another explicitly chosen staging area, not into compiled category folders.
- In legacy mode, prefer writing converted artifacts into `raw/` or another
  explicitly chosen ingest staging area, not into `wiki/`.
- Do not overwrite the original source file with converted markdown.
- After conversion, ingest from the converted artifact as a source, preserving
  provenance back to the original path.
- If conversion quality is poor, say so explicitly instead of pretending the
  markdown is trustworthy.

Local tool note:

- A local `MarkItDown` environment exists at:
  `$HOME/LLM Wiki MarkItDown/MarkItDown/venv/bin/markitdown`
- Installed version observed locally: `markitdown 0.1.5`

Practical workflow:

1. Identify the original source file.
2. Convert it with local `markitdown` into a staging markdown file.
3. Keep the original file untouched.
4. Read the converted markdown critically.
5. In `obsidian-wiki` mode, create/update one `references/` page from that
   converted source, then update durable pages, `index.md`, `log.md`, `hot.md`,
   and `.manifest.json`.
6. In legacy mode, create/update one `wiki/sources/` page from that converted
   source, then update durable pages, `wiki/index.md`, and `wiki/log.md`.

### Query

Use when the user asks a question that the wiki should answer.

In `obsidian-wiki` mode:

1. Resolve config and read `index.md`, `hot.md`, and relevant frontmatter
   summaries first.
2. Read relevant durable pages only when needed.
3. Answer from the wiki first with `[[wikilink]]` citations.
4. If the wiki is insufficient, state the missing source or page explicitly.

Legacy mode:

Steps:

1. Read `wiki/index.md` first to orient.
2. Read the relevant durable pages.
3. Answer from the wiki first.
4. Cite relevant pages with `[[wikilinks]]`.
5. If the answer is durable, save or propose a new analysis page.

Rules:

- Do not silently mix source facts and inference.
- If the wiki is insufficient, say what is missing.

### Lint

Use when the user wants quality control on the wiki.

Check for:

- broken links
- orphan pages
- weakly connected pages
- duplicate or overlapping pages
- contradictions
- concepts or entities repeatedly mentioned without their own page
- stale claims or superseded pages

Fix directly when safe:

- broken links
- index drift
- missing backlinks that are clearly warranted
- obvious page placement or title cleanup
- stale `hot.md` or `.manifest.json` metadata in `obsidian-wiki` mode when the
  correction is mechanical and source-backed

Report instead of guessing when judgment is needed.

## Page Discipline

- Prefer updating durable pages over creating fragments.
- Keep source pages factual and durable pages synthetic.
- Keep YAML frontmatter valid.
- Maintain meaningful wikilinks.
- In `obsidian-wiki` mode, keep `index.md`, `log.md`, `hot.md`, and
  `.manifest.json` current.
- In legacy mode, keep `wiki/index.md` and `wiki/log.md` current.
- If a claim lacks trustworthy support, say so explicitly.

## Truthfulness Rules

- Do not invent facts.
- Distinguish source-backed facts from synthesis.
- Preserve uncertainty explicitly.
- Never fabricate provenance, citations, source counts, or page links.

## Architecture Notes

- If the wiki describes software, keep architecture pages separate from
  implementation pages.
- If comparing systems or products, ingest both sides first, then write a
  synthesis page.
- If the user supplies text directly in chat, treat it as a source note and
  record its provenance in the source page body.
- If imported source material first passes through `MarkItDown`, preserve both:
  the original file path and the converted markdown path in the resulting source
  page or provenance note when useful.

## Local Example

For a concrete working vault in this environment, read
`references/artigram-example.md`.

For a local conversion-oriented setup in this environment, note:

- wiki skeleton:
  `$HOME/LLM Wiki MarkItDown/LLM Wiki`
- MarkItDown venv:
  `$HOME/LLM Wiki MarkItDown/MarkItDown/venv`
