# LLM-Readable Architecture

## Purpose

LLM-friendly architecture makes public site content easier for assistants, RAG systems, and user-directed agents to discover, cite, and traverse.

It must not create a separate hidden site for bots. The human page remains the source of truth.

## Useful Surfaces

| Surface | Use | Boundary |
| --- | --- | --- |
| `llms.txt` | Curated public map of useful canonical URLs. | No secrets, drafts, admin, or private APIs. |
| visible summary | Helps humans and agents identify the page answer quickly. | Must be visible; no bot-only summaries. |
| source trail | Shows where claims came from. | Link only to public or approved visible sources. |
| entity page | Defines Person, Organization, Project, Topic, Tool, or Community. | Must not invent relationships. |
| topic page | Groups related canonical pages and explains the topic. | Does not duplicate article bodies. |
| markdown alternate | Cleaner parse surface for docs/longform. | Must map to canonical HTML and follow noindex/alternate policy. |
| RSS | Machine-readable feed for public updates. | Public canonical items only. |

## Direct Answer Policy

Add direct-answer or TLDR blocks when:

- page role supports durable explanation;
- the block helps humans;
- the text is visible;
- it does not duplicate another page body;
- it does not replace the short brief page role.

Good candidates:

- longform articles;
- topic pages;
- docs;
- project pages;
- author/about pages.

Weak candidates:

- every short news brief by default;
- thin tag pages;
- private/admin pages;
- index pages that already contain brief cards.

## `llms.txt` Structure

Recommended sections:

- site identity and purpose;
- key sections;
- best-used-for map;
- current public indexes;
- evergreen topics;
- author/project/community pages;
- do-not-use section for admin/API/private paths;
- freshness and source caveats when relevant.

## Markdown Alternate Policy

Markdown alternates are useful when content is long, technical, or documentation-like.

Rules:

- HTML remains canonical.
- Markdown must not include facts absent from HTML.
- Markdown should be linked with `rel="alternate"` and `type="text/markdown"` when implemented.
- Markdown pages can be `noindex` if used only for agents/tools.
- Do not put markdown alternates in the public sitemap unless they are intended as independent search results.

## AI Crawler Policy

Crawler rules change. Before editing bot-specific allow/block policy, verify current primary sources.

Separate:

- search/citation crawlers;
- training crawlers;
- user-triggered fetchers;
- generic bots;
- abusive scanners.

Do not weaken security controls for crawler access. Public content can be accessible without exposing admin/API/private surfaces.

## One Brief Plus One Longform

LLM-friendly architecture should strengthen this model:

- brief: fast short news surface;
- longform: durable explanation;
- topic: organizer and explainer;
- project/author: entity/trust surfaces;
- homepage/index: teaser and routing.

It should not create extra public story variants.

