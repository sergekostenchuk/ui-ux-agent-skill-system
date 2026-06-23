# LLM Discovery Report

artifact_type: llm_discovery_report
generated_at: 2026-06-11T00:00:00Z
producer_skill: llm-friendly-site-architect

## Target

- site:
- default_language:
- launch_languages:
- source_inputs:

## Public Canonical Surfaces

| Role | URL | Why Useful For Agents | Visibility |
| --- | --- | --- | --- |
| home | https://example.com/ | Site identity and routing. | public |
| news_index | https://example.com/news/ | Short public news feed. | public |
| articles_index | https://example.com/articles/ | Durable longform explanations. | public |

## llms.txt Plan

- identity:
- key sections:
- best used for:
- do not use:
- freshness caveats:

## Visible Answer Blocks

| Page Role | Block Type | Rule |
| --- | --- | --- |
| longform_article | summary or key facts | Use only when visible to humans. |
| topic | direct answer | Explain topic and route to canonical pages. |
| news_brief | none by default | Brief is already the short form. |

## Source Trails

- longform source trail:
- news source link:
- project evidence:
- author evidence:

## Markdown Alternates

- eligible pages:
- rel alternate policy:
- noindex policy:
- sitemap policy:

## Crawler Policy Verification

| Item | Status | Evidence Needed |
| --- | --- | --- |
| OpenAI crawler names | requires_verification | Official docs before production edit. |
| Anthropic crawler names | requires_verification | Official docs before production edit. |
| Perplexity crawler names | requires_verification | Official docs before production edit. |

## Refused Or Deferred

- hidden bot-only content:
- doorway pages:
- duplicate story variants:
- credentialed citation monitoring:

