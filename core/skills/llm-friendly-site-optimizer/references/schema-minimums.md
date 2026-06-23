# Schema Minimums

Use JSON-LD. Keep structured data synchronized with visible content.

## TechArticle

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Page H1",
  "description": "Meta description",
  "datePublished": "2026-06-07T00:00:00+03:00",
  "dateModified": "2026-06-07T00:00:00+03:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author"
  },
  "publisher": {
    "@type": "Organization",
    "name": "mlllm.io",
    "url": "https://mlllm.io"
  },
  "inLanguage": "ru",
  "url": "https://mlllm.io/page",
  "mainEntityOfPage": "https://mlllm.io/page",
  "keywords": "MCP, RAG, Telegram bot",
  "articleSection": "Architecture"
}
```

## NewsArticle

Use for timely news pages. Include headline, description, dates, author, publisher, URL, language, and image when available.

## FAQPage

Only use visible FAQ content:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Direct answer."
      }
    }
  ]
}
```

## WebSite

Use `SearchAction` only when there is a real search URL:

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://mlllm.io",
  "name": "mlllm.io",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://mlllm.io/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

## Validation

- Parse JSON locally.
- Validate with schema.org validator or official rich-result tools when relevant.
- Do not mark up hidden claims, invented authors, fake ratings, or unavailable images.
