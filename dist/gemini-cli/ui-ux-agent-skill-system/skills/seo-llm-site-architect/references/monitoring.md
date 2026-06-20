# Monitoring And Tracking

Use monitoring when the goal includes ongoing SEO, AI visibility, crawler behavior, indexation, or regression prevention.

## Data Sources

- Google Search Console: pages, queries, impressions, clicks, indexing, sitemaps, manual actions, rich result reports.
- Bing Webmaster Tools: indexation, sitemaps, SEO reports, Bing search visibility.
- Server/CDN logs: user-agent, IP, reverse DNS where available, URL, status, bytes, latency, referrer.
- Analytics: landing pages, organic sessions, AI/search referrals, assisted conversions, engagement, funnel events.
- Site checks: sitemap fetch, robots fetch, canonical/noindex scan, schema parse, title/meta templates, status codes.
- Manual/third-party observation: AI answer citations and brand mentions, recorded with dates and prompts.

## Bot Log Segments

Track separately:

- Search crawlers: Googlebot, Bingbot, YandexBot, etc.
- AI search crawlers: OAI-SearchBot, Claude-SearchBot, PerplexityBot, and current equivalents.
- Training/product tokens: GPTBot, Google-Extended, ClaudeBot, and current equivalents.
- User-triggered fetchers/agents: ChatGPT-User, Claude-User, Google-Agent, Google NotebookLM, link preview fetchers.
- Unknown/high-volume bots: require rate limiting or verification before trust.

## Dashboard Metrics

- Indexable canonical URL count vs sitemap URL count.
- 2xx/3xx/4xx/5xx distribution for important templates.
- Pages with missing/duplicate title, meta description, canonical, H1, JSON-LD, or `noindex`.
- Search impressions/clicks by query cluster and landing page.
- Rich result/schema eligibility errors.
- Bot visits by segment, status, and important URL group.
- Freshness SLA for content where dates matter.
- Conversion from organic and AI/search referrals.

## Alert Ideas

- `robots.txt` or sitemap changes unexpectedly.
- Important route gains `noindex` or loses canonical.
- Sitemap returns non-200 or contains non-canonical URLs.
- Public templates start returning 5xx or heavy 4xx.
- JSON-LD parse fails after deploy.
- Search crawler volume drops sharply for key sections.
- AI/search crawler traffic spikes into expensive or low-value routes.

## Cadence

- Per deploy: run local audit on representative routes and parse JSON-LD.
- Weekly: check Search Console/Bing errors, sitemap status, top query/page movement, bot anomalies.
- Monthly: review content freshness, internal linking gaps, entity coverage, AI citation observations, and crawl budget waste.
- Quarterly: revisit bot policy, `llms.txt`, schema coverage, and framework metadata regressions against current official docs.
