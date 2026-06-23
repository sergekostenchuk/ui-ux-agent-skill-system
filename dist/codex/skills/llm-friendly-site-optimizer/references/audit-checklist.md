# LLM-Friendly Site Audit Checklist

Use `OK`, `PARTIAL`, `MISSING`, or `N/A`. For every gap, provide an exact recommendation.

## Technical LLM Audit

- `/llms.txt` exists and is accessible.
- `/llms.txt` has 1-3 sentence site description plus key pages with one-line descriptions.
- `/sitemap.xml` is accessible and contains current canonical URLs.
- `/news-sitemap.xml` exists when the site publishes timely news and is eligible for a news sitemap workflow.
- Key pages have meta descriptions of about 120-160 characters using audience + content + purpose.
- Canonical tags are correct and avoid duplicates.
- `robots.txt` does not block important public content or assets.
- Important content is present in initial HTML or otherwise reliably renderable.
- Key pages expose dates, authors, language, and stable URLs.

## Structured Data

- `Article` or `NewsArticle` for news pages: headline, description, datePublished, dateModified, author, inLanguage, url, image where available.
- `TechArticle` or `BlogPosting` for tutorials and explainers.
- `FAQPage` for visible FAQ sections.
- `BreadcrumbList` on nested pages.
- `WebSite` and `SearchAction` on home page only when search exists.
- `SoftwareSourceCode` or `SoftwareApplication` for real projects/tools.
- Schema uses canonical absolute URLs and stable entity IDs.

## Content

- Each key page begins with a direct answer that can be quoted.
- H1 is a specific question or statement.
- Each key page has TL;DR or short summary with 3-6 concrete points.
- H2/H3 sections are named after concrete subtopics.
- Each H2 section is meaningful as a standalone RAG chunk.
- Page uses lists, tables, diagrams, code blocks where appropriate.
- Publication and update dates are visible.
- Author/source is explicit with a profile link.
- FAQ has at least 3 real long-tail questions and concise answers.
- Internal links connect related pillar/supporting pages.
- External links point to primary or authoritative sources.

## External Signals

- At least one relevant external mention exists for each high-priority pillar page.
- GitHub README/Wiki/docs link where the content explains an implementation.
- Cross-posts use canonical references and avoid duplicate-content confusion.
- Communities are selected by fit, not spam volume.

## Monitoring

- Citation log exists.
- Weekly query set exists for each top topic.
- Competitor/cited-source observations are recorded.
- Pages that are cited are refreshed and deepened.
- Pages not cited are compared against cited sources and improved.
