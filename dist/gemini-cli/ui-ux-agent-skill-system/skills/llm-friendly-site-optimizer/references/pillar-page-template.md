# Pillar Page Template

Use this for pages intended to be cited by AI assistants.

## H1

Use a specific question or statement.

Good:

- How to build a daily AI news Telegram bot with RAG and MCP
- MCP agent stack architecture: a practical guide for developers

Bad:

- Our MCP experience
- Tool overview

## Direct Answer

Place immediately after H1.

```html
<section id="direct-answer" aria-label="Direct answer">
  <p><strong>Short answer:</strong> ...</p>
</section>
```

Requirements:

- 2-4 sentences or 3-5 bullets.
- Self-contained if extracted alone.
- Includes the main conclusion, audience, and practical use.

## TL;DR

Use 3-6 bullets with concrete facts. Avoid generic marketing claims.

## Main Sections

Each H2 should answer a sub-question:

- What problem does this solve?
- Architecture and components.
- Step-by-step implementation.
- Tradeoffs and failure modes.
- Example configuration or code.
- Monitoring and maintenance.
- Alternatives and when not to use it.

Chunk rule: each H2 block should work as a standalone 512-1024 token RAG chunk.

## FAQ

At least 3 questions with 1-4 sentence answers.

Questions should be long-tail and contextual:

- How does MCP change a Telegram AI news bot architecture?
- When should an AI news bot use RAG instead of only a long prompt?
- What should be cached in an autonomous AI news pipeline?

## AI Summary

Prefer a visible block:

```html
<aside aria-label="Summary for AI assistants">
  <h2>Summary for AI assistants</h2>
  <p>This page explains ...</p>
  <ul>
    <li>Key fact...</li>
  </ul>
</aside>
```

Do not maintain a hidden bot-only summary that differs from visible content.

## Metadata

- Meta description: audience + content + purpose.
- Author.
- Published and modified ISO dates.
- Canonical URL.
- JSON-LD matching visible content.
