# Shared Design Token Guidance

Use project tokens first. If a project has no explicit system, use these defaults conservatively.

## Spacing

- Base grid: 4px.
- Common increments: 4, 8, 12, 16, 20, 24, 32, 40, 48.
- Dense product UI should favor 8-16px internal spacing and stable table/filter rhythm.

## Radius

- Default card/control radius: 6-8px.
- Avoid oversized pill shapes unless the existing design system uses them.
- Modals and repeated item cards may use slightly larger radii if consistent.

## Typography

- Do not scale font size with viewport width.
- Use compact headings inside dashboards and tool surfaces.
- Preserve readable line-height and avoid negative letter spacing.

## Color

- Avoid one-note palettes dominated by a single hue family.
- Check contrast for text, focus, disabled states, and critical actions.
- Keep semantic roles distinct: background, surface, border, primary, danger, warning, success, muted.
