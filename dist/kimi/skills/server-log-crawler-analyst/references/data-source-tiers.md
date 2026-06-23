# Monitoring Data Source Tiers

## Tier 0: Public Fetch

Examples:

- `curl -I https://example.com/`
- `robots.txt`
- `llms.txt`
- `sitemap.xml`
- `news-sitemap.xml`
- RSS feed

Can prove:

- endpoint availability;
- HTTP status;
- content type;
- file size;
- presence of public discovery surfaces.

Cannot prove:

- ranking;
- indexing;
- assistant citation;
- real crawler visits.

## Tier 1: Server Logs

Examples:

- nginx/apache access logs;
- CDN request logs;
- reverse proxy logs.

Can prove:

- a request happened;
- path, status, byte count, timestamp, and user agent;
- user-agent string claiming a bot.

Cannot prove without extra verification:

- true bot identity;
- indexing;
- ranking;
- citation.

Privacy:

- raw IP must be redacted, hashed, or kept local;
- query strings and admin paths should be removed from public reports.

## Tier 2: Exported Search/Analytics Summaries

Examples:

- Search Console exported rows;
- analytics dashboard screenshots or CSV summaries;
- server aggregate reports.

Can prove:

- metrics as represented by the export;
- date range, query/page/country/device if present.

Requires:

- timestamp;
- export source;
- privacy review;
- no raw private rows in public skill artifacts.

## Tier 3: Credentialed APIs

Examples:

- Search Console API;
- analytics API;
- paid rank tracking API;
- assistant/search monitoring APIs.

This skill does not implement these. Hand off to future credentialed monitoring skills.

## User-Agent Classification

Classify conservatively:

- `known_search_bot_claim`: user-agent claims Googlebot/Bingbot/Yandex/etc.
- `known_ai_bot_claim`: user-agent claims GPTBot/OAI-SearchBot/ChatGPT-User/ClaudeBot/PerplexityBot/etc.
- `generic_bot`: user-agent contains bot/crawl/spider but is not recognized.
- `browser_like`: normal browser-like UA.
- `suspicious_probe`: paths such as `/wp-admin`, `/.env`, `/cgi-bin`, traversal attempts, or auth probes.

Use "claim" unless bot identity is verified by provider-specific method.
