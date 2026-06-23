# Internal Link Graph Rules

## Purpose

Internal links should help users move through the site and help search engines and LLM agents understand page relationships.

The graph must reinforce the canonical model. It must not create duplicate public content bodies or hidden SEO routes.

## Link Types

| Link Type | Purpose |
| --- | --- |
| `brief_to_longform` | Move from short news to deeper explanation. |
| `longform_to_brief` | Preserve the fast news source surface and story pair. |
| `index_to_page` | Let list/index pages expose canonical pages. |
| `page_to_index` | Let detail pages return to section indexes. |
| `topic_to_page` | Connect evergreen topic pages to related briefs, longforms, projects, or blog posts. |
| `page_to_topic` | Connect content pages to topic/entity hubs. |
| `project_to_story` | Show where a project relates to public content. |
| `story_to_project` | Let a story point to an owned project when relevant. |
| `author_to_page` | Connect author/entity profile to authored or representative work. |
| `breadcrumb` | Clarify hierarchy and current location. |
| `source_trail` | Link to visible sources or source summaries. |
| `related` | Point to strongly related content without overlinking. |

## Anchor Intent

Anchors should describe user action or page relationship:

- `Read longform`;
- `Read brief`;
- `Topic: AI news pipeline`;
- `Project: TG-NEWS`;
- `Source trail`;
- `More on this vendor`;
- `Author profile`.

Avoid repeated exact-match SEO anchors when the user reason is weak.

## Orphan Checks

Flag a page as orphaned when:

- it is indexable and has no incoming internal link;
- it appears in sitemap but not in navigation, index, topic, related, or breadcrumb paths;
- it is a project or author page with no route from relevant content.

## Overlink Checks

Flag overlinking when:

- a card/list repeats too many identical links;
- topic pages link to every page instead of selected relevant pages;
- exact-match anchors dominate;
- links point to pages with the same intent and no role distinction;
- related links are not explainable.

## Story Model Rule

For one story:

- one short brief per language;
- one longform article per language;
- optional homepage/index teaser;
- topic/project/author links can summarize and route;
- no extra duplicate story body is created by linking.

