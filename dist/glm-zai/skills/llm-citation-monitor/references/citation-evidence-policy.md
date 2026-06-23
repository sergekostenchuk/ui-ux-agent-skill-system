# Citation Evidence Policy

## Required Fields Per Observation

| Field | Required |
| --- | --- |
| Surface | yes |
| Model/product/version if visible | yes, if visible |
| Date and time | yes |
| Locale/language | yes |
| Account state | anonymous, logged-in, paid, API, unknown |
| Query text | yes |
| Target URL cited | yes/no |
| Cited URL list | yes, if citations appear |
| Answer snippet or summary | yes |
| Screenshot/transcript path | optional but recommended |
| Caveats | yes |

## Query Matrix Types

- brand query;
- topic query;
- problem query;
- comparison query;
- how-to query;
- citation-check query;
- competitor query.

## What Can Be Claimed

Allowed:

- "Observed citation on this surface for this query at this time."
- "Not observed in this run."
- "Competitor domain was cited in this run."

Not allowed:

- "Assistant always cites the site."
- "Assistant never cites the site."
- "The site ranks in LLMs."
- "This caused traffic growth" without analytics evidence.

## Caveats To Record

- personalization;
- account state;
- locale;
- model/product changes;
- freshness;
- citation UI variability;
- cached answers;
- limited query sample size.

## Privacy

- Remove account email, profile info, private chats, private files, and private prompts from stored artifacts.
- Do not store API keys or cookies.
- Ask before preserving private screenshots or transcripts.
