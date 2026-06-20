# UI/UX Skills Reporting Contract

Every UI/UX skill must separate plan, action, evidence, and judgment.

## Evidence Labels

- `Ran`: command or tool actually ran and the artifact path exists.
- `Skipped`: the check was applicable but not run; include the reason.
- `Planned`: the tool or check is documented but not implemented or not available.
- `Manual`: expert judgment based on available context without machine evidence.

## Required Final Shape

Use a compact final report:

```text
Chosen skill(s):
Work completed:
Ran:
Skipped:
Manual:
Artifacts:
Risks:
Next step:
```

If no command ran, say so directly. Do not convert planned commands into `Ran`.

## Evidence Minimums

- Visual claims need screenshot, browser, or clearly marked manual evidence.
- Accessibility claims need axe/browser evidence or a clearly marked manual review.
- Performance claims need Lighthouse or a project-specific metric report.
- Metadata/SEO claims need source inspection or metadata linter output.
