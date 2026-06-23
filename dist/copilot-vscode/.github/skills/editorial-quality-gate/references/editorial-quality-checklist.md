# Editorial Quality Checklist

## Gate Decisions

| Decision | Meaning |
| --- | --- |
| `pass` | Publishable after normal copy edit. No severe factual, source, duplication, residue, or page-role issues. |
| `revise` | Useful content, but needs targeted fixes before publication. |
| `block` | Do not publish until major factual, source, duplication, translation, or residue issue is fixed. |

## Severity

| Severity | Examples |
| --- | --- |
| Critical | unsupported material claim, prompt residue, fabricated source, duplicate public article body, hidden SEO filler |
| Major | weak source framing, repeated context, unclear page role, literal translation causing meaning drift |
| Minor | awkward phrasing, missing context link, inconsistent terminology, weak summary |

## Source Support

Check:

- What happened?
- Who is involved?
- What changed?
- What source or artifact supports this?
- Is the claim stated as fact, inference, or opinion?
- Are dates and product/version names preserved?

Reject:

- "reportedly" without source;
- confident claims from a single weak source without framing;
- invented metrics;
- untraceable quotes;
- author opinions presented as external fact.

## Prompt Residue

Block or revise if public text contains:

- internal instructions such as "start with practical effect";
- planning comments such as "add reality check";
- meta commentary about how to write the article;
- leftover prompt labels;
- duplicated context from generation steps;
- "as an AI language model" or similar artifacts.

## Duplication And Content Model

For one-brief-plus-one-longform systems:

- brief is the short factual surface;
- longform is the explanatory surface;
- homepage/topic teasers summarize and route;
- do not create a third near-duplicate public story body;
- do not repeat the brief body verbatim across multiple index pages when a teaser can serve the page role.

## Translation Quality

Check:

- factual meaning preserved;
- target-language reader gets natural phrasing;
- product names and proper nouns are consistent;
- local idioms do not distort the technical meaning;
- dates and numeric claims are unchanged;
- source links and source titles remain traceable.

## Page-Type Checklist

### News Brief

- clear one-sentence event summary;
- source-backed claim;
- date visible;
- no unnecessary background padding;
- link to longform if available.

### Longform

- visible explanation of what changed;
- why it matters;
- source trail;
- uncertainties or limits;
- related links;
- no prompt residue.

### Blog

- author voice is clear;
- factual claims are supported;
- opinion is not disguised as news;
- useful takeaway for reader.

### Project

- purpose, status, audience, and artifacts are clear;
- repo/demo/docs links if public;
- limitations are not hidden;
- relation to site expertise is explicit.

### Topic

- direct definition;
- why this topic matters;
- representative stories/projects;
- no thin aggregation.
