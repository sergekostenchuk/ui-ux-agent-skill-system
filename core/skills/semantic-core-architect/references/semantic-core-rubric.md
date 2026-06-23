# Semantic Core Rubric

## What Good Looks Like

A semantic core is a strategic map of demand, intent, entities, topics, audiences, languages, and evidence. It is not a raw keyword dump.

Good artifacts:

- separate observed facts, user-provided facts, inferred ideas, and unknowns;
- group queries by user intent and page role;
- identify entities that deserve stable canonical pages;
- include multilingual priorities without assuming every language launches at once;
- expose evidence gaps;
- prepare a clean handoff to URL architecture and link graph work.

## Required Cluster Fields

Each cluster should include:

- stable `id`;
- `label`;
- `primary_intent`;
- `audience`;
- `priority`;
- `languages`;
- `queries`;
- `entities`;
- `topics`;
- `evidence`;
- `unknown_metrics`;
- `downstream_notes`.

## Intent Categories

| Intent | Meaning | Example |
| --- | --- | --- |
| informational | User wants explanation or news context. | "AI news for builders" |
| navigational | User wants a known brand, author, project, or community. | "mlllm tg-news" |
| commercial | User compares tools, vendors, platforms, or approaches. | "best AI agent monitoring tools" |
| transactional | User wants to buy, subscribe, download, install, or join. | "subscribe AI news telegram" |
| support | User wants instructions, troubleshooting, or policy details. | "how to read llms.txt" |

## Evidence Labels

Use these source labels:

- `observed`: fetched page, logs, Search Console export, keyword tool export, or source document was directly inspected.
- `user_provided`: supplied by the user and not independently verified.
- `inferred`: reasoned from available facts.
- `unknown`: not verified.

Do not convert `inferred` into numeric volume or difficulty.

## Priority Scoring

Assign priority using this qualitative model:

| Factor | Signal |
| --- | --- |
| identity fit | The cluster describes what the site should be known for. |
| audience fit | The cluster serves the primary reader or buyer. |
| architecture value | The cluster affects URL structure, pages, or link graph. |
| evidence strength | There is observed or user-provided evidence, not only a hunch. |
| feasibility | The site can realistically publish useful content for the cluster. |

Use:

- `P0`: core identity and architecture driver.
- `P1`: important supporting cluster.
- `P2`: expansion cluster.
- `P3`: backlog or speculative.

## Entity Rules

Entities should have:

- stable lowercase id;
- human-readable name;
- type;
- canonical candidate URL when known;
- relationship to the site;
- evidence.

Allowed common types: `Organization`, `Person`, `Project`, `Product`, `SoftwareApplication`, `Topic`, `Publication`, `Community`, `Vendor`, `Technology`.

## Language Rules

For multilingual sites:

- define the default language;
- list launch languages separately from future languages;
- do not create equal priority for every language by default;
- note translation risk and review needs;
- identify locale-specific query differences.

## Handoff To IA

The semantic core may suggest page candidates, but final URL/canonical decisions belong to `information-architecture-seo`.

Handoff should include:

- clusters that need index pages;
- entities that need canonical pages;
- topics that could become pillar pages;
- language groups;
- duplicate-content risks;
- unknown data needed before final architecture.

