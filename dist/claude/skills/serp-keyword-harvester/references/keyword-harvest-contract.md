# Keyword Harvest Contract

## Required Inputs

- project topic or brief;
- target geography and language;
- seed keywords or source text;
- allowed data sources;
- approval status for external search/API calls.

## Output Groups

- `seed_keywords`
- `serp_snapshots`
- `autocomplete_expansion`
- `people_also_ask`
- `related_searches`
- `source_status`
- `handoff_notes`

Each group must include provenance and evidence status.

## External Source Policy

External SERP/API calls are optional and approval-gated. If approval is missing, produce a local-only harvest and mark external sources as `Planned` or `Skipped`.
