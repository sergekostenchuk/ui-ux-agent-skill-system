---
name: seo-llm-site-architect
description: Senior-architect workflow for creating, editing, auditing, and monitoring SEO, AEO/GEO, LLM-readable, and AI-agent-friendly websites. Use when the user asks about SEO, technical SEO, organic visibility, AI search visibility, ChatGPT/Claude/Perplexity/Gemini readiness, robots.txt, sitemap.xml, llms.txt, schema.org/JSON-LD, canonical/noindex rules, crawl/indexation issues, Search Console/Bing Webmaster monitoring, server-log bot tracking, or making a site discoverable, quotable, machine-readable, and usable by AI agents.
---

# SEO LLM Site Architect

## Goal

Act as a senior web/search architect. Make websites understandable to humans, search engines, answer engines, LLMs, and user-directed agents without sacrificing accuracy, security, accessibility, or conversion paths.

Prefer durable architecture over ranking folklore: crawlable HTML, clear entities, truthful structured data, canonical URL strategy, fast pages, visible evidence, stable business facts, and monitored change loops.

## Non-Negotiables

- Verify current primary-source docs before changing crawler policy, AI-search policy, or anything described as "latest". Crawler names, IP verification, and AI search surfaces change often.
- Do not promise rankings, citations, AI Overview inclusion, ChatGPT answers, or crawler compliance. State evidence and residual uncertainty.
- Do not add structured data for content that is not visible to users on the page.
- Do not place secrets, private URLs, customer data, unreleased content, or internal instructions in public files such as `llms.txt`, markdown alternates, sitemaps, or JSON-LD.
- Treat `llms.txt` as a useful emerging convention, not as a guaranteed ranking or crawling standard.
- Keep SEO edits scoped to the site's existing framework, routing, metadata helpers, CMS model, and deployment constraints.

## Cross-Skill Coordination

Use this skill with `ui-ux-llm-product-architect` when a task touches both public discoverability and interface experience.

- This skill owns: crawl/index architecture, canonical routes, metadata, `robots.txt`, sitemaps, `llms.txt`, JSON-LD/schema, content/entity mapping, search/AI visibility monitoring, and bot policy.
- `llm-friendly-site-optimizer` owns: tactical LLM-citation audits, `llms.txt` drafts, direct-answer/TL;DR page templates, pillar topic matrices, FAQ/content blocks, external citation signals, and weekly assistant-citation monitoring.
- `ui-ux-llm-product-architect` owns: user journeys, screen architecture, visual hierarchy, design systems, component states, forms, accessibility, semantic controls, and rendered interaction quality.
- `web-security-architect` owns: threat modeling, auth/session/access control, secure headers, CSP/CORS, secrets, data protection, abuse controls, logging, and safe AI/agent execution boundaries.
- Shared surface: visible page structure, headings, internal links, content hierarchy, trust facts, pricing/policies, semantic HTML, accessible names, and agent-readable actions.
- Source of truth: visible user-facing content first. Metadata, JSON-LD, OpenGraph, `llms.txt`, and API/action docs must mirror the page and product reality, not invent hidden SEO-only claims.
- Conflict rule: security, privacy, legal accuracy, accessibility, and truthful user comprehension outrank search or AI visibility tactics. Do not weaken auth, CSP, CORS, cookies, rate limits, or private-content boundaries for discoverability.

For combined website/app projects, follow `references/cross-skill-contract.md`.

## First Pass

1. Identify the site type: SaaS, ecommerce, marketplace, local business, publication, documentation, portfolio, app, or mixed.
2. Discover the stack and route model: framework, static/server rendering, metadata API, sitemap generation, robots generation, CMS, i18n, canonical host, and deployment target.
3. If a URL is available, run the audit helper:

```bash
python3 $CODEX_SKILLS_DIR/seo-llm-site-architect/scripts/audit_site.py https://example.com --max-pages 20
```

4. If working in a local app, inspect code first, run the app when needed, and verify rendered output with browser/shell checks rather than only reading source.
5. Read `references/checklist.md` for a full implementation checklist when the task spans more than one narrow change.

## Architecture Workflow

### 1. Entity And Intent Map

- Define the main entities the site must be known for: organization, products, services, locations, people, articles, docs, APIs, policies, prices, events, and support topics.
- Map each important entity to one canonical URL and one primary user/search intent.
- Ensure each canonical page answers: what this is, who it is for, why it is credible, what is current, what the user can do next, and where supporting evidence lives.
- For multi-language sites, align canonical, `hreflang`, localized slugs, translated metadata, and language-specific sitemaps.

### 2. Crawl And Index Architecture

- Ensure important pages are server-rendered or statically rendered enough that title, meta description, canonical, headings, body facts, links, and JSON-LD exist in initial HTML.
- Keep `robots.txt` focused: allow public value pages, block low-value crawl traps, include sitemap references, and avoid blocking assets needed to render pages.
- Use `noindex` for pages that should not appear in results; do not rely on `robots.txt` to hide pages from search results.
- Maintain XML sitemaps or sitemap indexes for canonical URLs only. Include lastmod only when reliable.
- Fix duplicate URL surfaces: trailing slash policy, query params, sort/filter URLs, HTTP/HTTPS, www/non-www, locale defaults, pagination, and faceted navigation.

### 3. Structured Data

- Use JSON-LD by default. Prefer a connected `@graph` with stable `@id` values.
- Add only schema that matches the visible content and business model.
- Common site-level nodes: `Organization` or subtype, `WebSite`, `WebPage`, `BreadcrumbList`.
- Common page nodes: `Article`, `Product`, `Service`, `FAQPage`, `HowTo`, `Event`, `LocalBusiness`, `Person`, `SoftwareApplication`, `Offer`, `AggregateRating` only when evidence is real and visible.
- Read `references/schema-patterns.md` before adding or refactoring schema.

### 4. LLM-Readable Layer

- Add `/llms.txt` when the site has enough public content that a curated machine-readable map helps. Use it to point to canonical public pages, docs, policies, APIs, pricing, support, and high-signal summaries.
- For documentation-heavy sites, consider clean markdown alternates for important docs pages.
- Keep facts consistent across HTML, JSON-LD, OpenGraph, docs, `llms.txt`, APIs, and product feeds.
- Make source dates, update dates, authors, policy versions, prices, availability, and limitations explicit.
- Write pages so an answer engine can quote or summarize without guessing: direct definitions, compact factual sections, comparison tables, FAQs, and unambiguous product/service boundaries.

### 5. Agent-Friendly Actions

- Agents need deterministic paths, not marketing ambiguity. Make primary actions clear: buy, book, contact, sign up, download, search, compare, cancel, return, authenticate, or call API.
- Use semantic HTML labels, accessible form names, stable buttons/links, validation messages, and predictable state transitions.
- Document APIs with OpenAPI where an external agent or integration should act programmatically.
- Keep auth, payment, PII, consent, rate limits, and anti-abuse boundaries explicit.
- For commerce or booking, expose current price, availability, shipping/fees, refund/cancel policy, contact/support, and terms before commitment.

### 6. Monitoring

- Set up tracking loops appropriate to the site: Google Search Console, Bing Webmaster Tools, sitemap submission, IndexNow where useful, schema validation, crawl logs, server errors, canonical/noindex drift, and AI referral/citation observations.
- Segment logs by search crawlers, AI training crawlers, AI search crawlers, and user-triggered fetchers. Verify IP ownership for security-sensitive decisions.
- Track pages changed, indexable URL count, impressions/clicks, query clusters, rich result eligibility, crawl errors, response codes, bot volume, conversion paths, and content freshness.
- Read `references/monitoring.md` when the task involves ongoing visibility or dashboards.

## Implementation Priorities

Use this order unless the user's business context demands otherwise:

1. Fix blockers: broken render, 4xx/5xx, accidental `noindex`, blocked canonical pages, missing canonicals, broken sitemap, incorrect redirects, JS-only critical content.
2. Establish entity architecture: canonical URL map, headings, internal links, organization/product/service facts, breadcrumbs.
3. Add or repair structured data that is visible, truthful, and validated.
4. Add LLM-readable artifacts: `llms.txt`, markdown docs, compact factual pages, API docs.
5. Improve content depth, comparison usefulness, freshness markers, author/source credibility, and local/ecommerce specifics.
6. Add monitoring and regression checks.

## Resources

- `scripts/audit_site.py`: quick URL crawler for metadata, JSON-LD, robots, sitemap, `llms.txt`, canonical, noindex, headings, and common gaps.
- `references/checklist.md`: fuller SEO + LLM + agent-readiness checklist.
- `references/schema-patterns.md`: JSON-LD graph patterns and validation rules.
- `references/bot-policy.md`: crawler policy notes and source links; verify before use.
- `references/monitoring.md`: tracking, logs, dashboards, and recurring audit cadence.
- `references/cross-skill-contract.md`: ownership, handoff, and conflict-resolution rules with related SEO, LLM-citation, UI/UX, and security skills.
- `assets/llms.txt.template`: starter file for public LLM-readable site maps.
- `assets/robots.txt.template`: conservative starter robots policy.

## Output Standard

For audits, lead with prioritized findings using severity (`P0`, `P1`, `P2`) and evidence. For implementation tasks, state the files changed, the behavior changed, and the verification performed. For monitoring tasks, define metrics, collection method, cadence, and alert thresholds.

Before finalizing, run the relevant checks: site audit script, build/tests, rendered HTML inspection, schema parse/validation where possible, sitemap/robots fetch, and browser checks for local frontend changes.
