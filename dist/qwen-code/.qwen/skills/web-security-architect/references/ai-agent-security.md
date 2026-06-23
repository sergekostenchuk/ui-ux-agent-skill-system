# AI And Agent Security

Use this when a website includes chatbots, RAG, LLM outputs, tool calls, browser agents, automation, code execution, file processing, or AI-generated actions.

## Threats

- Prompt injection from users, web pages, retrieved docs, emails, files, or tool outputs.
- Excessive agency: tools can do more than the task requires.
- Insecure output handling: model output is treated as trusted code, SQL, HTML, commands, emails, or browser actions.
- Sensitive data disclosure through prompts, logs, retrieval, public `llms.txt`, traces, or responses.
- Data poisoning in knowledge bases, docs, feedback, or training/eval data.
- Tool confusion, permission drift, hidden instructions, and cross-tenant retrieval leakage.
- Denial of wallet/service through expensive model, search, export, or tool loops.

## Controls

- Treat model input and output as untrusted.
- Put tools behind explicit scopes, authorization, rate limits, and audit logs.
- Require confirmation for irreversible, paid, public, privacy-sensitive, or privilege-changing actions.
- Validate and constrain tool arguments server-side.
- Keep secrets and system prompts out of user-visible content, logs, public files, and retrieval indexes.
- Separate tenants, roles, and document visibility in retrieval.
- Use allowlisted actions over free-form command execution.
- Log model/tool decisions enough for incident review without leaking sensitive content.

## Public AI/LLM Files

- `llms.txt`, markdown alternates, schema, and docs must not include secrets, private routes, hidden instructions, or unpublished content.
- SEO/LLM friendliness must not weaken access control or privacy.
