# Web Security Checklist

Use this for broad audits and hardening plans.

## Architecture

- Threat model exists for assets, actors, trust boundaries, abuse cases, and security controls.
- Public, authenticated, admin, internal, webhook, and AI/tool surfaces are separated.
- Security requirements are attached to features before implementation.
- Framework security defaults are enabled and not bypassed.
- Production debug, stack traces, source maps, backups, internal docs, and admin consoles are not publicly exposed.

## Authentication And Authorization

- Authentication uses a maintained library or identity provider.
- Passwords, if used, are hashed with modern password hashing and never logged.
- MFA is available for high-risk accounts and required for admins.
- Sessions/tokens can be revoked and rotate appropriately.
- Every sensitive object/action has server-side authorization.
- Role/permission checks are centralized enough to test and reason about.

## Browser And Client

- HTTPS is enforced; HSTS is configured when safe.
- Cookies use `HttpOnly`, `Secure`, and appropriate `SameSite`.
- CSP is present or planned; unsafe inline/eval usage is understood and minimized.
- Framing, referrer, permissions, MIME sniffing, and cross-origin policies are deliberate.
- Client-side checks are treated as UX only, not authorization.

## Inputs And Data

- Inputs are validated at trust boundaries by type, length, format, and business rules.
- Database access uses parameterized queries or safe ORM patterns.
- File uploads validate size, type, content, storage location, malware risk, and access policy.
- SSRF-prone features validate destinations and block internal metadata/private networks.
- Sensitive data is minimized, encrypted where appropriate, retained deliberately, and redacted in logs.

## API And Abuse

- API routes require auth unless explicitly public.
- Object ownership and tenant boundaries are enforced.
- Pagination, exports, search, and bulk actions have limits.
- Login/signup/password reset/checkout/webhooks/AI calls have rate limits and abuse monitoring.
- CORS is explicit and not wildcarded with credentials.
- Webhooks are signed, timestamped, replay-protected, and idempotent.

## Supply Chain

- Dependencies are locked and scanned.
- CI runs tests and dependency audits appropriate to the stack.
- Secrets are injected through secure configuration, not committed.
- Third-party scripts are minimized and reviewed.
- Build artifacts do not include secrets or private config.

## Monitoring

- Security events are logged with user/account/object/action/result/IP/device context where appropriate.
- Logs redact secrets, tokens, passwords, cookies, and PII.
- Alerts exist for auth abuse, privilege changes, admin actions, exports, dependency alerts, suspicious traffic, and production errors.
- Incident response owner, rollback path, and evidence capture are known.
