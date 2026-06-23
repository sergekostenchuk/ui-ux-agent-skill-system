# SERP Source Safety Boundaries

Use this reference whenever a setup mentions OpenSERP, AKE, proxy providers, API keys, paid traffic, external network calls, or provider account actions.

## Secret Handling

Never write real values for:

- API keys;
- proxy usernames/passwords;
- proxy URLs containing credentials;
- cookies;
- recovery codes;
- `.env` values;
- private/authenticated URLs.

Allowed references:

- `env:AKE_API_KEY`;
- `env:OPENSERP_BASE_URL`;
- `[REDACTED]`;
- local private path without credential contents, for example `~/.codex/private/openserp/openserp.runtime.yaml`.

## Approval Levels

| Level | Meaning | Allowed Action |
| :-- | :-- | :-- |
| `local` | User-provided files/text only | Normalize local inputs. |
| `external-direct-approved` | Public queries may be sent to direct engines | Query selected direct engines within budget. |
| `proxy-approved` | Public queries may use configured proxy | Query selected proxy-backed engines after precheck. |
| `provider-mutation-approved` | Provider resources may be changed | Create/refresh/rotate ports only for the approved action. |

If a level is missing, mark the source `Planned` or `Skipped`.

## Paid Traffic Guard

Paid proxy usage requires:

- selected engine list;
- max query count;
- max results per query;
- cache TTL;
- timeout;
- proxy provider name;
- credential reference, not credential value;
- precheck result;
- failure behavior.

## Provider Actions

Do not create, refresh, rotate, buy, delete, or mutate proxy-provider resources as a side effect of setup. These actions need a separate confirmation immediately before execution.

## Reporting

Reports may say:

- `AKE key present in runtime env`;
- `proxy precheck failed`;
- `Google selected via ake-google-residential`;
- `credential_ref: env:AKE_API_KEY`.

Reports must not include the key, proxy credential, full provider URL with token, or `.env` content.
