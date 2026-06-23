# Cross-Skill Contract: Security, UI/UX, And SEO/LLM

Use this when `web-security-architect`, `ui-ux-llm-product-architect`, `seo-llm-site-architect`, and/or `llm-friendly-site-optimizer` apply together.

## Ownership

`web-security-architect` owns:

- Threat model, trust boundaries, risk severity, and secure-by-design requirements.
- Auth, session, access control, cookies, CSRF, secure headers, CSP, CORS, TLS/HSTS.
- Data protection, secrets, dependency/supply-chain security, abuse controls, logging, incident readiness.
- Security of APIs, webhooks, admin surfaces, file uploads, payments, AI tools, and agent actions.

`ui-ux-llm-product-architect` owns:

- User journeys, interaction design, accessibility, semantic controls, screen states, and rendered UI quality.

`seo-llm-site-architect` owns:

- Crawl/index architecture, metadata, schema, sitemaps, `robots.txt`, `llms.txt`, bot policy, and visibility monitoring.

`llm-friendly-site-optimizer` owns:

- Tactical LLM-citation audits and answer-shaped content structure.
- Pillar topic matrices, FAQ blocks, external citation signals, and citation monitoring.
- `llms.txt` drafts that must respect public/private content boundaries.

## Conflict Order

1. Security, privacy, legal/compliance, user safety.
2. Accessibility and core user task completion.
3. Truthful visible content and business accuracy.
4. Crawlable semantic HTML and stable route/state architecture.
5. Search/AI visibility and structured summaries.
6. Visual polish, convenience, animation, and nonessential conversion tactics.

## Shared Rules

- Do not expose private content in `llms.txt`, schema, source maps, public markdown, logs, or SEO artifacts.
- Do not weaken auth, CSRF, CORS, CSP, cookies, or rate limits to make crawling, embedding, analytics, or conversion easier.
- Do not hide material security/privacy facts from users.
- Make security-critical UX clear: auth, consent, payment, cancellation, deletion, export, privacy, MFA, and recovery.
- Keep bots and AI agents within explicit permission and rate-limit boundaries.
- If an AI/user agent can trigger an action, the same server-side authorization and audit requirements apply as for a human.

## Combined Workflow

1. Security defines assets, actors, trust boundaries, and non-negotiable controls.
2. UI/UX designs clear, accessible, recoverable flows that expose security-relevant decisions.
3. SEO/LLM maps only public, truthful, user-visible content into metadata/schema/LLM-readable files.
4. Implementation preserves framework defaults and validates behavior in rendered UI and server code.
5. Verification includes security checks, UI/accessibility checks, and SEO/LLM checks without treating any single scanner as complete.
