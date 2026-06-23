# URL Architecture Reference

## Purpose

Information architecture turns semantic demand and entities into crawlable, understandable, maintainable public URLs.

The output should help humans, search engines, and LLM agents understand what each page is for and how it relates to the rest of the site.

## Page Role Model

| Page Role | Job | Canonical Pattern |
| --- | --- | --- |
| `home` | Position the site, route readers, expose fresh and durable sections. | self-canonical |
| `news_index` | List short news briefs for a language or topic. | self-canonical |
| `news_brief` | One short news surface for one story. | self-canonical when distinct from longform |
| `longform_article` | One expanded explanation for one story. | self-canonical when distinct from brief |
| `topic` | Evergreen organization page for a topic/entity cluster. | self-canonical |
| `project` | Public project/entity page. | self-canonical |
| `blog` | Author essay or working note. | self-canonical |
| `author` | Person/entity profile and trust page. | self-canonical |
| `community` | Social/community link hub. | self-canonical or noindex depending value |
| `utility` | RSS, sitemap, llms.txt, robots, admin, API. | index only when public useful |

## One Brief Plus One Longform

For a publication model with a short news brief and one expanded article:

- the brief answers what happened quickly;
- the longform explains context, sources, implications, and related entities;
- each page can be self-canonical because the page roles differ;
- each page should link to the other;
- there should not be a third public story body except a homepage teaser or index excerpt;
- topic pages can link and summarize, but not reproduce the story body.

## Canonical Decisions

Use self-canonical when:

- the page has unique visible value;
- the page serves a different role from a related page;
- the page is meant to be indexed.

Use canonical to another URL when:

- the page is a duplicate or near-duplicate technical variant;
- the page is a print/filter/query/session variant;
- the page is not intended as a standalone search result.

Use noindex when:

- the page is useful for users but low-value or private for search;
- the page is staging, admin, internal API, or duplicate filter output.

## Hreflang Rules

Hreflang groups must connect true language equivalents.

For each localized page:

- canonical points to itself;
- `hreflang` points to alternate language equivalents;
- `x-default` points to the default language or language selector;
- localized slugs are allowed when stable and maintainable.

## Duplicate-Content Checks

Flag these:

- brief canonicalized to longform despite distinct page role;
- topic page copying article body;
- homepage carrying full news body instead of teaser;
- translated page published before translation quality is known;
- multiple public URLs for the same story body;
- tag/category pages with no unique value.

## Handoff

After URL architecture:

- `internal-link-graph-architect` designs links, anchors, breadcrumbs, and source trails;
- `technical-seo-schema-engineer` designs metadata, schema, sitemap, RSS, robots, and llms.txt;
- `llm-friendly-site-architect` designs direct answers, entity surfaces, markdown alternates, and AI crawler-readable layers.

