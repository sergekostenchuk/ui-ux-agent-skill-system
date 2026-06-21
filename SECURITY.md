# Security Policy

## Secret Handling

Do not commit:

- API keys;
- private keys;
- passwords;
- OAuth tokens;
- cookies;
- `.env` files;
- Playwright storage states;
- private screenshots;
- private URLs;
- customer data;
- unpublished business documents.

Examples must use redacted placeholders such as `STITCH_API_KEY=redacted`.

If a real token, OTP, or recovery code is pasted into a chat, issue, terminal log,
or report, treat it as exposed. Revoke the token in the vendor console and create
a replacement before using that integration again.

## External Services

Skills in this system may mention Figma MCP, Stitch, browser automation, and other optional services. These are approval-gated:

1. State the service.
2. State what data will be sent.
3. State why the service is needed.
4. Provide a local fallback where possible.
5. Do not print or store credentials.

## Reporting A Vulnerability

For now, report security issues directly to the repository owner through a private channel. Do not open public issues containing secrets, tokens, private URLs, screenshots, or customer data.
