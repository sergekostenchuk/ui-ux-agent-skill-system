# Freshness Sources

Tooling changes quickly. Before updating command contracts or making version-specific claims, verify primary sources.

## Primary Sources

- shadcn/ui official docs and changelog.
- Tailwind CSS official docs and blog.
- Storybook official docs and blog.
- Playwright official docs.
- Deque axe-core official package/repo docs.
- Lighthouse CI official repo/docs.
- Vercel v0 official docs/changelog.
- Figma MCP official docs/catalog/blog.
- Google Stitch official Google Labs/developer pages.
- Framer official docs.

## Rule

If a primary source does not confirm the claim, mark the claim as `unverified`, `manual`, or `planned`. Do not present remembered version behavior as current fact.

## Machine Validation

Static data snapshots must be covered by a freshness manifest when they are distributed with the package.

For UI/UX Pro Max data, validate coverage with:

```bash
python3 scripts/check_freshness.py .
```

The default check is intentionally offline. It verifies:

- every bundled CSV is covered by `core/skills/ui-ux-pro-max/data/freshness.json`;
- each dataset has `last_checked_at`;
- each dataset has either `source_url` or `source_category`;
- dates are valid and not in the future;
- stale datasets are reported according to their configured severity.

Live source refreshes are a separate maintenance operation and must not run in baseline CI unless explicitly approved.
