# Wiki Gate Contract

## Purpose

The wiki gate prevents long UI/UX agent projects from losing decisions, constraints, and artifact paths between sessions.

## Gate Types

| Gate | When | Output |
| --- | --- | --- |
| `pre-project` | large or multi-session project begins | project memory map and source list |
| `post-decision` | council, three-variant, SEO/UX, Figma, Stitch, migration, or launch decision accepted | decision note and rejected-options record |
| `pre-handoff` | work moves to another skill or runtime | compact context pack |
| `post-validation` | tests, screenshots, audits, or launch checks complete | evidence summary with skipped/planned checks |
| `release-handoff` | GitHub/npm/public package work changes | release note and remaining risk register |

## Backend Selection

- Use `wiki-capture` when the current conversation is the primary source.
- Use `obsidian-wiki-ingest` or `wiki-ingest` when the source is a local document, report, or exported artifact.
- Use `wiki-context-pack` when another agent needs a compact context input.
- Use `wiki-query` when a user asks what the wiki already knows.

## Done Criteria

A wiki gate is complete only when:

- source artifact paths are exact;
- sensitive data exclusions are stated;
- accepted and rejected decisions are distinguishable;
- validation evidence is labeled `Ran`, `Skipped`, `Planned`, or `Manual`;
- next owner and open blockers are recorded.
