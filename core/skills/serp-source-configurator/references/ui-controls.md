# SERP Source UI Controls

Use this when the user wants dashboard fields, checkboxes, or a setup form for source collection.

## Required Controls

- Source checkboxes:
  - manual keywords / CSV;
  - existing site text/crawl;
  - Bing direct;
  - DuckDuckGo direct or mega search;
  - Ecosia direct;
  - Baidu direct;
  - Google via proxy;
  - Yandex via proxy.
- Locale/market fields:
  - language;
  - country/region;
  - device if supported.
- Runtime credential controls:
  - OpenSERP base URL;
  - proxy provider select, for example AKE;
  - API key input with no export/persistence;
  - credential reference display such as `env:AKE_API_KEY`.
- Budget controls:
  - max queries;
  - max results;
  - cache TTL;
  - timeout;
  - paid proxy allowed checkbox;
  - provider resource mutation allowed checkbox, default off.
- Preflight buttons:
  - check OpenSERP ready;
  - check selected engines;
  - check proxy connectivity;
  - validate redacted config.

## Status Colors

- Blue: not configured / no comment / not checked yet.
- Green: configured and preflight passed.
- Orange: partially configured or partially accepted.
- Red: failed, missing approval, secret detected, or unsafe paid setting.

## Export Rules

Exported JSON/Markdown must omit actual secret input values. It may include:

```json
{
  "proxy_provider": "ake",
  "credential_ref": "env:AKE_API_KEY",
  "api_key_present": true,
  "api_key_value": "[REDACTED]"
}
```

Do not put hidden form fields with real keys into generated static HTML.
