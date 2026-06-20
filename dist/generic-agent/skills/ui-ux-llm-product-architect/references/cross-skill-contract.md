# Cross-Skill Contract: UI/UX, SEO/LLM, And Security

Use this when `ui-ux-llm-product-architect`, `seo-llm-site-architect`, `llm-friendly-site-optimizer`, and/or `web-security-architect` apply together.

## Ownership

`ui-ux-llm-product-architect` owns:

- User roles, jobs-to-be-done, journeys, flows, conversion paths, and recovery paths.
- Screen architecture, navigation, information hierarchy, and state coverage.
- Visual design system: tokens, components, typography, spacing, color, motion.
- Accessibility: semantics, focus, keyboard, labels, ARIA usage, contrast, touch targets.
- Interaction details: forms, tables, dialogs, menus, loading/empty/error/success states.
- Rendered UI verification across desktop/mobile and interaction states.

`seo-llm-site-architect` owns:

- Canonical URL and route strategy.
- Crawl/index controls: `robots.txt`, `noindex`, sitemaps, redirects, canonical tags.
- Metadata: title, description, OpenGraph/Twitter, hreflang, app/page metadata APIs.
- Structured data: schema.org/JSON-LD, entity IDs, breadcrumbs as search/AI data.
- LLM-readable public artifacts: `llms.txt`, markdown alternates, docs/content maps.
- Search and AI visibility monitoring: Search Console, Bing, bot logs, citations/referrals.
- Bot policy and crawler access rules.

`llm-friendly-site-optimizer` owns:

- Tactical LLM-citation audits and page-level answer-readiness scoring.
- `/llms.txt` drafts focused on high-signal public pages.
- Direct-answer/TL;DR/FAQ/pillar-page content structure.
- Topic-to-URL matrices for target assistant questions.
- External citation-signal plans and weekly assistant-citation tracking.

`web-security-architect` owns:

- Threat model, trust boundaries, risk severity, and secure-by-design requirements.
- Auth, session, access control, cookies, CSRF, secure headers, CSP, CORS, TLS/HSTS.
- Data protection, secrets, dependency/supply-chain security, abuse controls, logging, incident readiness.
- Security of APIs, webhooks, admin surfaces, file uploads, payments, AI tools, and agent actions.

## Shared Surface

Both skills must agree on:

- Page purpose, primary entity, and primary user/search intent.
- Visible headings and content hierarchy.
- Internal links and navigation labels.
- Pricing, availability, policies, support, trust proof, and other business facts.
- Semantic HTML landmarks, accessible names, and deterministic action labels.
- Agent-readable action paths for buy, book, sign up, compare, contact, cancel, return, export, or call API.

## Decision Order

When recommendations conflict, use this order:

1. Security, privacy, legal/compliance, and user safety.
2. Accessibility and core task completion.
3. Truthful visible content and business accuracy.
4. Crawlable semantic HTML and stable route/state architecture.
5. Search/AI visibility, structured data, and LLM-readable summaries.
6. Visual polish, trend alignment, and nonessential animation.

## Combined Workflow

1. Discover the product, audience, business model, stack, routes, design system, and public visibility goals.
2. Let UI/UX define the core journeys, screens, states, and visible content blocks.
3. Let SEO/LLM map those screens to canonical URLs, entities, metadata, schema, sitemaps, and `llms.txt`.
4. Build a shared content/action contract: each page's visible facts, primary action, supporting proof, and structured representations.
5. Implement design and semantic HTML first; then mirror it in metadata, JSON-LD, OpenGraph, and LLM-readable artifacts.
6. Verify with both audit helpers, rendered browser checks, schema parsing, sitemap/robots fetches, keyboard/focus checks, and responsive screenshots.

## Anti-Conflict Rules

- Do not add hidden SEO text or schema for facts not visible to users.
- Do not remove visible headings, links, labels, or text needed for search/AI understanding just to make a layout cleaner.
- Do not block crawlers or AI search agents without aligning with the product's visibility goals.
- Do not weaken auth, CSRF, CORS, CSP, cookies, rate limits, or private-content boundaries for crawling, analytics, embedding, conversion, or agent access.
- Do not expose private content in `llms.txt`, schema, source maps, public markdown, logs, or SEO artifacts.
- Do not prioritize keyword density over comprehension, conversion, or trust.
- Do not use canvas/image-only UI for critical content or actions unless a semantic fallback exists.
- Do not create separate "human copy" and "AI copy" that can drift; maintain one factual source.

## Output Convention

Prefix findings when both skills are active:

- `[UX]` for journey, interaction, accessibility, visual hierarchy, and component issues.
- `[SEO]` for crawl/index, metadata, structured data, canonical, sitemap, and bot issues.
- `[Shared]` for visible content, semantic HTML, agent actions, trust facts, and route-state issues.
