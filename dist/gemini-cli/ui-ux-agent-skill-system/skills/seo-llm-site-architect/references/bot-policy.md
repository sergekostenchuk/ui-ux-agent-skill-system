# Bot Policy Notes

Crawler policy changes are high-risk and time-sensitive. Verify current official docs before editing production `robots.txt`, WAF rules, or bot allow/block lists.

## Current Source Links

- OpenAI crawlers: https://platform.openai.com/docs/bots
- Google crawler overview: https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
- Google common crawlers: https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- Google special-case crawlers: https://developers.google.com/search/docs/crawling-indexing/google-special-case-crawlers
- Google user-triggered fetchers: https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers
- Google robots.txt interpretation: https://developers.google.com/search/reference/robots_txt
- Anthropic crawler docs: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Perplexity robots.txt docs: https://www.perplexity.ai/help-center/en/articles/10354969-how-does-perplexity-follow-robots-txt
- Bing webmaster guidelines: https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- IndexNow: https://www.indexnow.org/
- llms.txt proposal: https://llmstxt.org/

## Policy Split

Separate these decisions:

- Search indexing: normal search crawler access, sitemap discovery, rich result eligibility.
- AI search/answers: systems that crawl or fetch to answer user queries.
- Model training: crawlers or product tokens that signal use in future model training.
- User-triggered fetches: agents or product features fetching because a user requested it.
- Abuse/security: WAF, rate limits, IP verification, bot authentication, and fraud controls.

## Common Tokens To Verify Before Use

- OpenAI: `OAI-SearchBot`, `GPTBot`, `ChatGPT-User`, plus any newly documented bot.
- Anthropic: `ClaudeBot`, `Claude-User`, `Claude-SearchBot`.
- Google: `Googlebot`, `Google-Extended`, `GoogleOther`, `Google-Agent`, and relevant special-case/user-triggered fetchers.
- Perplexity: `PerplexityBot`.
- Microsoft/Bing: `bingbot`, plus Bing Webmaster and IndexNow guidance.

## Robots Examples

Allow search while blocking selected training use only after confirming business intent:

```txt
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Selective examples must be tailored. Do not paste broad allow/block blocks blindly:

```txt
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /
```

## Verification

- Fetch `/robots.txt` over the canonical host and protocol.
- Confirm syntax with official or trusted validators.
- Confirm crawler groups do not accidentally override generic rules.
- Check CDN/WAF rules separately; they may contradict `robots.txt`.
- For sensitive allow/block decisions, verify bot IP ownership rather than trusting user-agent strings.
