# Site Growth Orchestrator Workflow

## Purpose

The orchestrator keeps complex site-growth work coherent across SEO, LLM-readability, UX, content, monitoring, security, authority placement, task planning, validation, and skill packaging.

It owns ordering and evidence. It does not make specialist decisions that belong to a domain skill.

## Routing Matrix

| User Intent | Primary Owner | Supporting Owners | Required Evidence |
| --- | --- | --- | --- |
| Build a full SEO/LLM site architecture | `site-growth-orchestrator` | `semantic-core-architect`, `information-architecture-seo`, `technical-seo-schema-engineer`, `llm-friendly-site-architect` | task plan, semantic core, URL map, schema report, validation summary |
| Build semantic core, entities, queries, intents | `semantic-core-architect` | `seo-llm-site-architect` | sources, query clusters, entity-topic map |
| Define URL structure, canonical, hreflang, page roles | `information-architecture-seo` | `semantic-core-architect`, `technical-seo-schema-engineer` | URL map with rationale |
| Design internal links, breadcrumbs, source trails | `internal-link-graph-architect` | `information-architecture-seo`, `ui-ux-llm-product-architect` | internal-link graph and orphan/overlink checks |
| Add title/meta/schema/sitemap/robots/llms/RSS rules | `technical-seo-schema-engineer` | `seo-regression-validator`, `web-security-architect` | schema/head templates and static checks |
| Make site LLM-friendly without duplicate content | `llm-friendly-site-architect` | `technical-seo-schema-engineer`, `seo-regression-validator` | LLM discovery plan and visible-content policy |
| Verify live HTML, schema, canonical, hreflang, robots, llms.txt | `seo-regression-validator` | `agent-browser-codex`, `technical-seo-schema-engineer` | JSON/Markdown audit report, command output |
| Improve UX journey, onboarding, layout, accessibility | `ui-ux-llm-product-architect` | `seo-llm-site-architect`, `agent-browser-codex` | journey map, screenshots, accessibility notes |
| Harden admin, auth, logs, crawler exposure, headers | `web-security-architect` | `seo-llm-site-architect` | threat model, header/auth findings, safe allow/deny policy |
| Monitor Search Console, AI citations, server crawler logs | `seo-regression-validator` first, then `llm-citation-monitor` | `web-security-architect` | credential status, timestamped checks, privacy notes |
| Find places where links could help | `external-authority-placement-scout` after policy | `backlink-quality-validator`, `web-security-architect` | white-hat policy, opportunity register, user approval |
| Create or package skills | `senior-skill-architect` | `cluster-consistency-linter`, `task-plan-v2-orchestrator` | skill lint, evals, install/rollback plan |

## Sequencing Rules

1. Start with goal and constraints.
2. If the request spans more than one domain, create or update TASK-PLAN v2.
3. For SEO/LLM structure, run this order:
   - semantic core;
   - information architecture;
   - internal link graph;
   - technical SEO/schema;
   - LLM-readable layer;
   - regression validation;
   - UX or conversion polish;
   - monitoring or external authority only after the core is stable.
4. If the user asks for external links, citations, rankings, crawler access, or "latest" platform behavior, require fresh primary-source evidence.
5. If credentials or account actions are needed, stop at a dry-run plan until the user grants access.
6. If a task can harm an existing production pipeline, add a gate and rollback plan before any edit.

## Active Alarm Handling

Keep active alarms visible in every broad handoff.

| Alarm Type | Default Handling |
| --- | --- |
| Unknown external placement policy | Keep external-authority work dry-run. No posting, outreach, submissions, or account actions. |
| Unknown monitoring credentials | Use credential-free checks only. Do not claim Search Console, analytics, or assistant dashboard evidence. |
| Current platform/crawler policy | Browse or verify primary sources before changing rules. |
| Live production system risk | Require rollback plan, tests, and explicit scope. |

## Handoff Packet Requirements

Every handoff should include:

- objective;
- current task id and status;
- source artifacts;
- target artifacts;
- active alarms;
- forbidden areas;
- validation command or review method;
- expected output shape;
- stop condition.

Use the asset template when a handoff is large enough to persist.

## Review Checklist

Before marking orchestration work complete:

- the next owner is unambiguous;
- no specialist work was silently absorbed by the orchestrator;
- every claim has evidence or is labeled as assumption;
- active alarms are preserved;
- external actions are gated;
- task status matches committed artifacts;
- validation commands are recorded;
- rollback or defer path exists.

