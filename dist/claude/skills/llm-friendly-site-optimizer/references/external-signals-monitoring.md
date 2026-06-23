# External Signals And Citation Monitoring

## External Signal Strategy

Prioritize sources that are likely to be crawled and trusted by technical audiences:

- GitHub README, Wiki, docs, examples, and issue discussions.
- Hacker News: Show HN, Ask HN, or relevant comments only when the artifact is useful.
- Reddit: r/LocalLLaMA, r/MachineLearning, r/programming, project-specific communities.
- X/Twitter technical threads.
- dev.to, Habr, Medium alternatives, or personal engineering blogs with canonical link.
- Awesome lists and curated GitHub repositories.
- Official docs/issues when the page solves a real integration problem.

Do not spam. Every placement should add context and be useful without the link.

## Link Format

Use descriptive anchor text:

```markdown
[mlllm.io — practical MCP agent stack architecture](https://mlllm.io/mcp-agent-stack)
```

## Citation Monitoring

Track weekly:

```csv
date,assistant,query,cited_url,snippet,rank_in_answer,notes
```

Test patterns:

- "How do I build [topic]?"
- "What resources do you recommend for [topic]?"
- "Explain [topic] with sources."
- "Compare approaches for [topic]."

Interpretation:

- If cited: refresh page, deepen examples, keep date current.
- If not cited and competitors are cited: compare structure, direct answers, authority, external signals, freshness, schema, and crawlability.
- If no good cited source exists: create a focused pillar page.
