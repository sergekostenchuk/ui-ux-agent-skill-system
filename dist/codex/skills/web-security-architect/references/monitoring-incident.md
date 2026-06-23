# Monitoring And Incident Readiness

## Security Logs

Capture:

- Login, logout, failed login, password reset, MFA changes.
- Session revocation, token rotation, suspicious device/IP changes.
- Authorization failures and object-access denials.
- Role, permission, billing, payment, refund, admin, support, and impersonation actions.
- File upload/download, exports, webhook events, AI/tool calls.
- Rate-limit hits, WAF events, dependency alerts, CSP violations, production errors.

Redact:

- Passwords, tokens, cookies, API keys, secrets, full payment data, sensitive PII, private prompts unless explicitly needed and protected.

## Alerts

- Credential stuffing or reset abuse.
- Privilege changes and admin access from unusual context.
- Spikes in 401/403/429/5xx.
- Unusual exports/downloads.
- Webhook signature failures.
- CSP violation spikes after deploy.
- Dependency critical CVEs.
- Public exposure of debug/admin/internal routes.

## Incident Readiness

- Define severity, owner, escalation, rollback, communication, and evidence capture.
- Keep runbooks for account takeover, data leak, secret leak, payment abuse, dependency CVE, bot abuse, and AI/tool misuse.
- Document how to revoke sessions/tokens, rotate keys, disable features, invalidate caches, and block abusive traffic.
