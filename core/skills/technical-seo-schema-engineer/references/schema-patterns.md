# Schema And Metadata Patterns

## Principle

Metadata and schema describe the visible page. They do not create a second hidden version of the page for crawlers or LLM agents.

## Page Type Matrix

| Page Type | Head Metadata | JSON-LD |
| --- | --- | --- |
| `home` | title, description, canonical, hreflang, OG/Twitter, RSS autodiscovery | `WebSite`, `Organization`, `Person`, `CollectionPage` or `WebPage` |
| `news_index` | title, description, canonical, hreflang, OG/Twitter, RSS | `CollectionPage`, `BreadcrumbList` |
| `news_brief` | title, description, canonical, hreflang, OG/Twitter, article meta | `NewsArticle`, `BreadcrumbList` |
| `longform_article` | title, description, canonical, hreflang, OG/Twitter, article meta | `TechArticle` or `Article`, `BreadcrumbList` |
| `topic` | title, description, canonical, hreflang, OG/Twitter | `CollectionPage`, `DefinedTerm`, `BreadcrumbList` |
| `project` | title, description, canonical, hreflang, OG/Twitter | `SoftwareApplication` or `CreativeWork`, `BreadcrumbList` |
| `blog` | title, description, canonical, hreflang, OG/Twitter, article meta | `BlogPosting` or `Article`, `BreadcrumbList` |
| `author` | title, description, canonical, hreflang, OG/Twitter | `Person`, `ProfilePage`, `BreadcrumbList` |

## Required Visible Fields

For article-like pages:

- headline;
- description or dek;
- author;
- date published;
- date modified when available;
- language;
- image or fallback image;
- canonical URL;
- publisher.

For topic/project/author pages:

- visible name;
- description;
- canonical URL;
- relationship to the site;
- visible supporting links when schema references related pages.

## ImageObject Policy

Use this fallback order:

1. verified article media image;
2. verified video poster;
3. page-specific generated OG card;
4. stable site fallback OG card.

Never leave `NewsArticle.image` empty when a fallback can be defined.

## Canonical And Hreflang

- Canonical follows `url-map.yaml`.
- Each indexable localized page self-canonicalizes.
- Hreflang connects true equivalents only.
- `x-default` points to the default page or language selector.
- Brief and longform can both be self-canonical when page roles differ.

## FAQ And HowTo Rules

FAQPage and HowTo schema are allowed only when the relevant blocks are visible to users on the page.

Do not create hidden FAQ schema for SEO.

## Robots, Sitemap, RSS, llms.txt

- `robots.txt` should allow public value pages and block admin/API/private surfaces.
- XML sitemap contains canonical public URLs only.
- News sitemap contains eligible recent news URLs only.
- RSS exposes public feed items and should be linked in `<head>`.
- `llms.txt` links only to public useful canonical pages and must not include secrets, drafts, admin URLs, or private APIs.

## Validation Handoff

The regression validator should verify:

- title exists and is unique enough;
- meta description exists;
- canonical exists and is expected;
- hreflang alternates match URL map;
- JSON-LD parses;
- required schema fields exist;
- schema fields match visible content;
- OG/Twitter cards exist;
- image URLs return usable assets;
- sitemap/RSS/robots/llms.txt are reachable when live.

