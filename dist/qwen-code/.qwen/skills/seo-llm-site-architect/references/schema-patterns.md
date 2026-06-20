# Schema Patterns

Use JSON-LD unless the existing site has a strong established alternative. Keep structured data faithful to visible content.

## Graph Shape

Prefer one `@graph` per page with stable IDs:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example",
      "url": "https://example.com/"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com/",
      "name": "Example",
      "publisher": { "@id": "https://example.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/page/#webpage",
      "url": "https://example.com/page/",
      "name": "Page title",
      "isPartOf": { "@id": "https://example.com/#website" },
      "about": { "@id": "https://example.com/#organization" }
    }
  ]
}
```

## Common Nodes

- `Organization`: name, legalName if useful, url, logo, sameAs, contactPoint, address for real public businesses.
- `LocalBusiness`: use the most specific subtype practical; include NAP, geo, openingHours, areaServed, priceRange only when true.
- `WebSite`: name, url, publisher, optional `SearchAction` only when on-site search works.
- `WebPage`: url, name, description, inLanguage, isPartOf, about, datePublished/dateModified when meaningful.
- `BreadcrumbList`: mirror the actual breadcrumb path.
- `Article`/`BlogPosting`/`NewsArticle`: headline, author, publisher, datePublished, dateModified, image, mainEntityOfPage.
- `Product`: name, image, description, brand, sku/gtin when available, offers with priceCurrency, price, availability, url, seller.
- `Service`: serviceType, provider, areaServed, description, offers only when visible and specific.
- `FAQPage`: only visible questions and answers, not hidden SEO-only text.
- `SoftwareApplication`: operatingSystem, applicationCategory, offers, aggregateRating only with real visible data.

## Validation Rules

- Every URL in schema should be canonical and absolute.
- Use one consistent `@id` for the same entity across pages.
- Do not duplicate competing organization/product identities.
- Do not create review/rating markup without first-party evidence and policy compliance.
- Do not mark up content hidden from users.
- Parse JSON before shipping; malformed JSON-LD can silently remove eligibility.
- Use official rich-result docs for feature-specific requirements before claiming eligibility.
