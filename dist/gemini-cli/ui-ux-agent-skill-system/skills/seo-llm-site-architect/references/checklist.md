# SEO, LLM, And Agent Readiness Checklist

Use this checklist for multi-page audits, new site architecture, and major SEO/AI-readiness changes.

## Discovery

- Confirm business model, target geographies, languages, audience, conversion actions, regulated content constraints, and source-of-truth systems.
- Identify framework routing, rendering mode, metadata helpers, CMS/data source, deployment host, edge/CDN rules, analytics, and access to search/log data.
- Inventory templates: home, category, product/service, article, docs, listing, location, legal/policy, contact, search, account, checkout/booking.

## Technical SEO

- Public canonical pages return 200, have unique title, meta description, one clear H1, canonical URL, crawlable body content, internal links, and no accidental `noindex`.
- Duplicate variants redirect or canonicalize consistently: protocol, host, trailing slash, locale, query params, sort/filter, pagination, uppercase/lowercase.
- Sitemaps include canonical indexable URLs only; sitemap index is used for large sites; `lastmod` is truthful.
- `robots.txt` includes sitemap references and does not block public assets needed for rendering.
- Important pages are not hidden behind client-only rendering, blocked scripts, consent walls, auth, geo blocks, or unsupported content types.
- Images have useful alt text when informative; videos and PDFs have crawlable surrounding context or transcripts.
- Core pages meet practical performance expectations: fast server response, stable layout, compressed assets, responsive images, cache headers, and no severe mobile usability issues.

## Content And Entity Quality

- Each page has a single primary entity and intent.
- The page states concrete facts: name, category, audience, locations served, prices or pricing model, availability, limitations, support, policies, dates, and next actions.
- Claims are supported by visible evidence: specs, screenshots, customer proof, author bios, citations, changelog, docs, or policies.
- Dates are explicit for time-sensitive content: published, updated, valid-through, policy version, event dates, product availability.
- Internal links connect related entities using descriptive anchor text.
- Important definitions, comparisons, FAQs, and decision criteria are written plainly enough for answer engines to summarize without inventing missing context.

## Structured Data

- JSON-LD matches visible page content and uses canonical URLs.
- Site-wide graph includes stable IDs for organization, website, and key pages.
- Breadcrumbs match visual/internal navigation.
- Product/service schema includes real offers only when price/availability/policy evidence is visible.
- FAQ/HowTo schema is used only for real, visible Q&A/instructional content.
- Reviews/ratings are not fabricated and comply with platform policies.
- Schema is parsed locally and, for public pages, checked with relevant rich-result/schema validators.

## LLM-Readable Layer

- `/llms.txt` exists when useful, is public, concise, and points to canonical high-signal pages.
- Documentation-heavy sites expose markdown or low-noise equivalents for core docs where practical.
- `llms.txt` avoids secrets, internal routes, unpublished pages, private docs, and manipulative instructions.
- Public facts are consistent across HTML, JSON-LD, OpenGraph, docs, feeds, APIs, and `llms.txt`.
- Pages include compact factual sections that can be quoted: summaries, definitions, capabilities, limitations, pricing model, policy excerpts, and support paths.

## Agent-Friendly UX

- Primary user actions are visible, deterministic, and semantically labeled.
- Forms use labels, autocomplete where appropriate, accessible error messages, stable submit controls, and clear success/failure states.
- Product, booking, or checkout flows expose fees, taxes, cancellation/refund rules, delivery/availability, and support before commitment.
- APIs intended for external automation have OpenAPI docs, auth requirements, rate limits, examples, and error semantics.
- Bot/user-agent access rules are aligned with business goals and abuse controls.

## Monitoring

- Search Console and Bing Webmaster Tools are connected where possible.
- Sitemaps are submitted and monitored for discovered vs indexed deltas.
- Logs segment major search crawlers, AI crawlers, and user-triggered fetchers.
- Dashboards track impressions, clicks, query clusters, landing pages, crawl errors, schema eligibility, bot visits, AI referrals/citations where measurable, and conversion impact.
- Alerts catch accidental `noindex`, robots changes, sitemap failures, canonical drift, 5xx spikes, title/template regressions, and schema parse failures.
