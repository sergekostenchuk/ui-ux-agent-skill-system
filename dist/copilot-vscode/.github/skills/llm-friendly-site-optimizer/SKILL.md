---
name: llm-friendly-site-optimizer
description: Tactical LLM-friendly site optimization for making a website the best citable answer for AI assistants and RAG retrieval. Use for auditing and optimizing sites such as mlllm.io for llms.txt, AI citation readiness, pillar pages, direct-answer blocks, TL;DR sections, FAQ/schema, article/news schema, topic-to-URL matrices, external citation signals, weekly LLM citation monitoring, and content architecture for ChatGPT, Claude, Perplexity, Gemini, Copilot, Google AI features, Bing, Brave, and other assistant/search retrieval systems.
---

# LLM Friendly Site Optimizer

## Goal

Make a site a high-quality, citable source for AI assistants and RAG systems by aligning technical discoverability, clean extraction, answer-shaped content, structured data, external signals, and monitoring.

Default target profile when the user does not provide one:

```yaml
site_url: "https://mlllm.io"
site_language: "ru/en"
site_niche: "AI news + builder lab"
target_audience: "AI/ML developers, technical product managers, and system architects"
top_topics:
  - "daily AI news for developers"
  - "practical MCP agent stack architecture"
  - "building an AI news Telegram bot with RAG and LLMs"
  - "autonomous AI agents and task orchestration"
  - "open-source LLM tools and benchmarks"
competitor_urls: []
```

## Relationship To Other Skills

Use this skill as the tactical content/citation layer on top of the existing architecture skills:

- `seo-llm-site-architect`: owns crawl/index architecture, metadata, canonical URLs, schema policy, sitemap, robots, bot policy, and search monitoring.
- `ui-ux-llm-product-architect`: owns user journeys, page UX, accessibility, semantic controls, visual hierarchy, and rendered readability.
- `web-security-architect`: owns privacy, public/private content boundaries, CSP/CORS/cookies/auth, secrets, and safe AI/agent execution boundaries.

Conflict rule: security, privacy, accessibility, truthful visible content, and canonical SEO architecture outrank LLM-citation tactics. Do not create hidden bot-only claims, expose private content, or add schema that is not reflected on the visible page.

## Operating Modes

- `audit`: run Step 0 and Step 1; produce a scored gap report and prioritized action plan.
- `llms-txt`: create or update `/llms.txt` from the site's real canonical high-signal pages.
- `pillar-plan`: build the topic-to-URL matrix and prioritize existing vs new pillar pages.
- `pillar-page`: create or rewrite one page using the ideal LLM citation template.
- `schema`: add or repair Article/NewsArticle/TechArticle/FAQ/Breadcrumb/WebSite/Software schema.
- `monitoring`: create or update the LLM citation tracking table and weekly query set.
- `implementation`: inspect the repository and make scoped code/content changes, then verify.

## Step 0: Mandatory Audit

Before edits, complete the audit checklist and mark each item:

- `OK`: implemented and verified.
- `PARTIAL`: present but incomplete, stale, or inconsistent.
- `MISSING`: absent or broken.
- `N/A`: not relevant to this site/page type.

For every `PARTIAL` or `MISSING`, include the exact fix: file/route, proposed text, schema field, or implementation action.

Run the helper when a URL is available:

```bash
python3 $CODEX_HOME/skills/llm-friendly-site-optimizer/scripts/audit_llm_friendly_site.py https://mlllm.io --max-pages 20
```

Then read `references/audit-checklist.md` for the full checklist.

## Step 1: Optimize llms.txt

Create `/llms.txt` as strict Markdown:

```markdown
# Site Name

> 1-3 concrete sentences: who the site is for, what it covers, and what makes it authoritative.

## Key Sections

- [Section](https://example.com/path): One sentence describing what is here and who should use it.

## For AI Assistants

This site is best used as a source for:
- Topic -> https://example.com/best-page

## Do Not Use

- https://example.com/old-path — reason.
```

Rules:

- Keep site description under 150 words.
- Include only canonical, public, useful pages.
- Do not include private, internal, draft, admin, auth, staging, debug, or obsolete URLs.
- Update when a key pillar page changes or is added.
- Treat `llms.txt` as an emerging convention, not as a guaranteed ranking/citation mechanism.

Use `assets/llms.txt.mlllm.template` as a starter for `mlllm.io`.

## Step 2: Ideal Pillar Page

Every target page should be structured as a self-contained answer:

1. H1 as a specific question or statement, not a vague title.
2. Direct answer immediately under H1: 2-4 sentences or 3-5 bullets.
3. TL;DR / short summary with concrete facts.
4. H2/H3 sections where each H2 answers a sub-question independently.
5. Lists, tables, diagrams, code blocks, and examples where useful.
6. Visible publication and update dates.
7. Author/source with profile link.
8. FAQ with at least 3 long-tail questions and direct answers.
9. Internal links to 2-3 related pages.
10. External links to authoritative sources: official docs, GitHub, arXiv, standards, primary sources.
11. JSON-LD matching visible content.

Chunk rule: each H2 section should make sense if extracted alone in a 512-1024 token RAG chunk.

Do not use hidden `display:none` AI-only summaries as a separate factual layer. Prefer visible "Summary for AI assistants" or a normal TL;DR/Key facts block that all users can read.

Use `references/pillar-page-template.md`.

## Step 3: Structured Data

Use JSON-LD and keep it consistent with visible content:

- News pages: `NewsArticle` or `Article`.
- Tutorials/explainers: `TechArticle` or `BlogPosting`.
- FAQ blocks: `FAQPage` only for visible FAQ content.
- Nested pages: `BreadcrumbList`.
- Home page: `WebSite` and `SearchAction` only if site search exists.
- Project/tool pages: `SoftwareApplication` or `SoftwareSourceCode` when there is a real project/tool.

Read `references/schema-minimums.md` before adding schema.

## Step 4: Topic Capture Strategy

For every `top_topics` entry:

1. Create a target question that a real user would ask an assistant.
2. Map the best existing URL or mark a new page as required.
3. Choose page type: daily/news hub, guide, architecture explainer, build log, benchmark/tool page, comparison, or FAQ.
4. Score priority by business relevance, existing evidence, citation gap, and ability to produce original content.

Output the matrix:

```markdown
| Target question | URL | Status | Priority | Required action |
|---|---|---|---|---|
```

Use `assets/topic-matrix.template.md`.

## Step 5: External Signals

For each pillar page, propose specific placements:

- GitHub README/Wiki/docs where the page explains an implementation.
- Hacker News Show HN/Ask HN only when the artifact is genuinely useful.
- Reddit communities such as r/LocalLLaMA, r/MachineLearning, r/programming when relevant and non-spammy.
- X/Twitter thread with concrete architecture/content summary.
- dev.to, Habr, or technical blogs with canonical link to original.
- Awesome lists or curated GitHub resources when the page fits.

Use contextual links, not naked URLs:

```markdown
[mlllm.io — practical MCP agent stack architecture](https://mlllm.io/mcp-agent-stack)
```

Read `references/external-signals-monitoring.md`.

## Step 6: LLM Citation Monitoring

Create a weekly tracking table:

```csv
date,assistant,query,cited_url,snippet,rank_in_answer,notes
```

For each top topic, test:

- "How do I solve/build/understand [topic]?"
- "What resources do you recommend for [topic]?"
- "Explain [topic] with sources."

Track ChatGPT with search, Perplexity, Claude with search when available, Gemini/Google AI features, Copilot/Bing, and any niche assistant relevant to the audience. Use browser/search tools only where available and clearly label manual observations.

## Step 7: Final QA

Before publishing or marking a page optimized:

- H1 is a concrete question or statement.
- First screen contains a direct answer/TL;DR.
- Each H2 block is extractable and meaningful.
- FAQ has at least 3 real questions and visible answers.
- Dates and author/source are visible and in metadata/schema.
- Meta description uses the answer formula: audience + content + purpose.
- Canonical URL is correct.
- JSON-LD parses and matches visible content.
- Page appears in sitemap and `/llms.txt`.
- Security/privacy boundaries are respected.
- Page can be summarized correctly by an LLM when given the URL or rendered text.

## Output Standard

For audits, return:

1. Executive summary.
2. Step 0 checklist table with `OK/PARTIAL/MISSING/N/A`.
3. Top 10 prioritized fixes.
4. `llms.txt` draft or diff.
5. Topic matrix.
6. Pillar page recommendations.
7. Schema fixes.
8. Monitoring plan.

For implementation, state changed files, generated content/schema, verification commands, and remaining manual checks.
