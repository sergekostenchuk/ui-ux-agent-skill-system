# SEO Regression Checklist

## Required Evidence

Every report should include:

- target URL or file path;
- fetched/read timestamp;
- method;
- status code or file status;
- user agent when fetched;
- checks run;
- critical findings;
- warnings;
- skipped checks.

## HTML Checks

Critical:

- title missing;
- meta description missing;
- canonical missing;
- duplicate canonical;
- JSON-LD missing on pages expected to have schema;
- invalid JSON-LD;
- NewsArticle.image missing or empty.

Warnings:

- hreflang missing;
- OpenGraph incomplete;
- Twitter card incomplete;
- RSS autodiscovery missing;
- viewport missing;
- article meta missing for article pages.

## Public Artifact Checks

When live URL access is available, also check:

- `/robots.txt`;
- `/llms.txt`;
- `/sitemap.xml`;
- `/news-sitemap.xml` when news exists;
- `/rss.xml` or feed URL;
- markdown alternate URLs when expected.

## Crawler Checks

Crawler allow/block conclusions require:

- current official crawler docs when bot-specific rules are discussed;
- fetched `robots.txt`;
- server/WAF evidence when available;
- caveat that robots policy is not the same as indexing, WAF, or crawler compliance.

## Performance Checks

If Lighthouse/PageSpeed is unavailable, record it as skipped. Do not invent Core Web Vitals.

## Result Semantics

- `pass`: check ran and expected evidence exists.
- `fail`: check ran and expected evidence is missing or invalid.
- `warning`: check ran and non-critical evidence is missing.
- `skipped`: check did not run; reason required.

