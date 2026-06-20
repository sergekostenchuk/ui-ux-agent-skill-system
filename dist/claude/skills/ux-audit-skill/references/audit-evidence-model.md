# Audit Evidence Model

## Evidence Types

- `automated`: validator, browser, axe, Lighthouse, or script report exists.
- `DOM`: actual rendered DOM was inspected.
- `screenshot`: image or browser screenshot was reviewed.
- `source`: source files were inspected.
- `Manual`: expert judgment without machine evidence.

## Claims Allowed

| Evidence | Allowed Claims |
| :-- | :-- |
| screenshot | visual hierarchy, obvious overlap, visible affordances, contrast risk |
| source | semantics present in code, likely state gaps, implementation risks |
| DOM | rendered headings, landmarks, labels, focusability where inspected |
| automated | only the exact checks the report ran |
| Manual | hypotheses and recommendations clearly labeled manual |

## Claims Not Allowed

- No Lighthouse score without Lighthouse report.
- No axe issue count without axe report.
- No DOM statement from screenshot-only input.
- No screenshot claim without image/browser artifact.
