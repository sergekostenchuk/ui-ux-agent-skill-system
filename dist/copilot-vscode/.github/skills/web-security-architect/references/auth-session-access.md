# Authentication, Sessions, And Access Control

## Authentication

- Prefer mature auth libraries or identity providers.
- Use secure password reset: single-use, short-lived tokens, no account enumeration, clear audit logs.
- Require MFA for admins and high-risk operations where practical.
- Re-authenticate for sensitive changes: email, password, MFA, payment, withdrawal, role changes.
- Avoid leaking account existence through errors, timing, or reset flows.

## Sessions And Cookies

- Session cookies: `HttpOnly`, `Secure`, appropriate `SameSite`, scoped domain/path.
- Avoid storing sensitive data in client-readable cookies or localStorage.
- Rotate session IDs after login and privilege changes.
- Support logout and server-side revocation.
- Set reasonable idle and absolute expiry for risk level.

## CSRF

- For cookie-authenticated state-changing requests, use CSRF tokens or same-site protections backed by framework guidance.
- Do not rely only on SameSite for high-risk flows.
- Keep state-changing actions out of GET requests.

## Access Control

- Enforce authorization server-side for every sensitive object/action.
- Use object ownership checks for IDs from path, query, body, session, and nested resources.
- Centralize permission logic enough to test and audit.
- Deny by default for unknown roles, object states, tenants, or permissions.
- Test horizontal and vertical access control paths.

## Admin And Support

- Separate admin surfaces from public app where possible.
- Require MFA and stronger session policies.
- Log role changes, impersonation, data exports, refunds, deletes, and support access.
- Make impersonation explicit, scoped, logged, and reversible.
