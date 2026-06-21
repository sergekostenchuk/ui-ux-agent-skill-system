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

## Machine Validation

When a report is used as release or CI evidence, validate it with:

```bash
python3 scripts/validate_evidence_report.py path/to/report.md
```

Use `--require-ran` when the report is supposed to contain at least one executed check.

The validator fails when:

- `Ran` references a missing local artifact path;
- `Ran` contains placeholder evidence such as `TBD` or `path/to`;
- `Ran` describes planned or unexecuted work;
- `--require-ran` is set and no `Ran` entry exists.

The validator does not prove that an external service actually changed state. For external evidence, include a URL, a tool response artifact, or a separate machine-readable report.
