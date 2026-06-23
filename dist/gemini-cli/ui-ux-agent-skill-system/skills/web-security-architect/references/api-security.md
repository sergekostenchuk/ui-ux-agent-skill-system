# API Security

Use this for REST, GraphQL, RPC, mobile backends, webhooks, and public/private APIs.

## Core Controls

- Authenticate every non-public API.
- Authorize every object and action server-side.
- Validate request bodies, path params, query params, headers, file inputs, and content type.
- Limit pagination, search, export, and nested expansions.
- Return consistent errors without leaking secrets or internal state.
- Keep API docs aligned with auth, rate limits, scopes, and error behavior.

## BOLA/IDOR

- Treat IDs as untrusted.
- Check tenant/account/object ownership at every route.
- Do not rely on hidden UI controls to protect actions.
- Test same-role cross-user access and lower-role admin access.

## Rate Limiting And Abuse

- Rate-limit login, signup, reset, OTP, checkout, search, upload, export, webhook, and AI/tool endpoints.
- Add business-flow protections: fake account creation, scraping, inventory hoarding, scalping, credential stuffing, coupon abuse.
- Use idempotency keys for payment and critical write operations.

## Webhooks

- Verify signatures and timestamp freshness.
- Protect against replay.
- Keep idempotency and retry semantics.
- Log source, event ID, result, and failure reason.
- Do not trust webhook payload object state without server-side lookup if the provider supports it.

## SSRF-Prone Features

- Treat user-provided URLs as high risk.
- Allowlist schemes and hosts when possible.
- Block private, loopback, link-local, metadata, and internal networks.
- Limit redirects, response size, content type, timeout, and DNS rebinding risk.
