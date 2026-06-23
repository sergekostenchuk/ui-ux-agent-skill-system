# Threat Modeling

Use this before major features, auth changes, payment/PII flows, admin surfaces, APIs, uploads, webhooks, and AI/agent features.

## Method

1. Define scope: feature, routes, APIs, data stores, users, integrations, deployment.
2. List assets: accounts, sessions, PII, payment data, files, admin data, secrets, model prompts, retrieved docs, logs.
3. List actors: anonymous, user, owner, admin, support, partner, crawler, bot, AI agent, insider.
4. Draw trust boundaries: browser/server, API/database, CDN/app, app/third party, webhook/app, AI/tool, file store/app.
5. Identify abuse cases: unauthorized read/write, privilege escalation, account takeover, scraping, fraud, injection, data leakage, denial of wallet/service.
6. Define controls: prevention, detection, response, and residual risk.

## STRIDE Prompts

- Spoofing: Can an actor pretend to be another user, service, webhook, or agent?
- Tampering: Can request data, object IDs, files, prompts, or webhook payloads be modified?
- Repudiation: Can sensitive actions be denied because logs lack identity/action/result?
- Information disclosure: Can private data leak through UI, APIs, logs, errors, public files, cache, or AI outputs?
- Denial of service: Can expensive routes, exports, uploads, search, checkout, or AI calls be abused?
- Elevation of privilege: Can a lower role perform admin, tenant, support, or owner actions?

## Output

- Scope and assumptions.
- Data-flow sketch or route/API map.
- Risk table with severity, likelihood, impact, owner, mitigation, verification.
- Residual risks and monitoring.
