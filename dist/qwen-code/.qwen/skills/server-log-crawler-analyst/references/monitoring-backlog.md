# Monitoring Backlog

task: T-012
status: deferred beyond credential-free baseline

## Deferred Skill: search-console-analyst

Purpose:

- interpret Search Console exports or API data for indexing, impressions, clicks, query/page groups, and coverage issues.

Dependencies:

- explicit credential/export access;
- privacy policy for private query/page rows;
- semantic core and URL map.

Acceptance criteria:

- records property, date range, export time, filters, dimensions;
- separates observed Search Console data from ranking conclusions;
- redacts private rows when reports are public.

## Deferred Skill: rank-serp-monitor

Purpose:

- track query rankings in a compliant, locale/device-aware way.

Dependencies:

- approved rank-tracking provider or manual method;
- query set from semantic core;
- locale/device/persona policy.

Acceptance criteria:

- records query, locale, device, timestamp, method, result URL, and caveats;
- does not scrape search engines against terms;
- does not generalize one query result to all users.

## Deferred Skill: credentialed-crawler-monitor

Purpose:

- combine CDN/server logs, verified bot IP methods, Search Console crawl stats, and alerting.

Dependencies:

- server/CDN access;
- bot verification policy;
- raw-log privacy controls.

Acceptance criteria:

- verified bot categories where possible;
- alert thresholds;
- redacted public reporting;
- raw data kept local or in approved private storage.
