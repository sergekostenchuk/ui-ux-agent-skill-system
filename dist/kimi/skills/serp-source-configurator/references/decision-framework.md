# SERP Source Configuration Decision Framework

Use this reference when deciding what search-demand sources should be enabled before keyword harvesting.

## Primary Decision

Choose the cheapest source set that can answer the project question.

1. If the project has enough user-provided keywords, existing site text, CSV exports, or manual SERP notes, start local/manual.
2. If live public SERP evidence is useful, enable direct engines first: Bing, DuckDuckGo, Ecosia, and sometimes Baidu depending on market.
3. If Google/Yandex evidence is necessary, use proxy-backed OpenSERP only after explicit approval, budget limits, and proxy precheck.
4. If a provider requires account mutation or port creation, stop and ask for explicit confirmation for that action.

## Engine Matrix

| Engine | Default | Proxy | Notes |
| :-- | :-- | :-- | :-- |
| Bing | direct | normally off | Good low-cost first pass. |
| DuckDuckGo | direct through mega search if supported | normally off | Useful fallback, may not have a dedicated endpoint. |
| Ecosia | direct | normally off | Optional broadening source. |
| Baidu | direct or off | market-specific | Use for China/Baidu-relevant markets only. |
| Google | off until approved | residential HTTP proxy preferred | Highest block risk; set low rate and cache. |
| Yandex | off until approved | residential HTTP proxy preferred | Use for relevant markets; set low rate and cache. |
| Manual CSV/user keywords | on when provided | not applicable | Mark as `Manual` or `Ran` depending on processing. |
| Existing site crawl | local or public URL approval | not proxy by default | Avoid authenticated/private crawls without explicit scope. |

## Proxy Policy

- Prefer per-engine proxy tags over global proxy.
- Do not route every engine through paid proxy.
- Use HTTP/HTTPS authenticated proxy for browser-mode OpenSERP. Avoid authenticated SOCKS for browser mode unless verified by current OpenSERP docs/runtime.
- Use existing provider ports before creating new paid ports.
- Run a lightweight connectivity precheck before starting a proxy-backed SERP job.
- If precheck fails, keep the proxy source `Skipped`; do not spend retries.

## Budget Defaults

- `max_queries`: 20 for first proof run.
- `max_results_per_query`: 10.
- `cache_ttl_seconds`: 3600.
- `timeout_seconds`: 30.
- `paid_proxy_allowed`: false by default.
- `create_provider_resources_allowed`: false by default.

## Handoff Rule

The handoff to `serp-keyword-harvester` must include selected engines, disabled engines, approval status, locale/market, query set, budget limits, proxy preflight status, and failure behavior.
