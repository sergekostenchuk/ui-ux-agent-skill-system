# JSON-LD Templates

These are pattern templates. Replace example values with visible page values from the site implementation.

## NewsArticle

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "@id": "https://example.com/news/123-example-story/#newsarticle",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/news/123-example-story/"
  },
  "headline": "Example story headline",
  "description": "Visible summary from the short news page.",
  "datePublished": "2026-06-11T00:00:00Z",
  "dateModified": "2026-06-11T00:00:00Z",
  "inLanguage": "en",
  "author": {
    "@type": "Person",
    "name": "Example Author",
    "url": "https://example.com/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "example.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/assets/logo.png"
    }
  },
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/assets/example-og-card.png"
  },
  "isPartOf": {
    "@type": "WebSite",
    "@id": "https://example.com/#website"
  }
}
```

## TechArticle

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "https://example.com/articles/123-example-story/#article",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/articles/123-example-story/"
  },
  "headline": "Example longform headline",
  "description": "Visible longform article summary.",
  "datePublished": "2026-06-11T00:00:00Z",
  "dateModified": "2026-06-11T00:00:00Z",
  "inLanguage": "en",
  "author": {
    "@type": "Person",
    "name": "Example Author",
    "url": "https://example.com/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "example.com"
  },
  "about": [
    {
      "@type": "Thing",
      "name": "Example topic"
    }
  ],
  "citation": [
    "https://source.example/article"
  ]
}
```

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "News",
      "item": "https://example.com/news/"
    }
  ]
}
```

## Site Graph

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com/",
      "name": "example.com",
      "inLanguage": "en"
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "example.com",
      "url": "https://example.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example.com/assets/logo.png"
      }
    },
    {
      "@type": "Person",
      "@id": "https://example.com/about/#person",
      "name": "Example Author",
      "url": "https://example.com/about/"
    }
  ]
}
```

