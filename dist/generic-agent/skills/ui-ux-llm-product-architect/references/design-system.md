# Design System Architecture

Use this when creating or editing UI kits, tokens, components, Tailwind themes, CSS variables, or component libraries.

## Token Layers

- Global tokens: raw color, spacing, radius, font, shadow, duration, easing, breakpoint, z-index.
- Alias tokens: semantic use, such as `color.background.surface`, `color.text.muted`, `space.form.gap`.
- Component tokens: local overrides for button, input, card, modal, table, sidebar.

Prefer semantic alias tokens in app code. Keep raw values close to the theme source.

## Component Contract

Each component should define:

- Purpose and allowed use cases.
- Anatomy: slots, labels, icons, helper text, actions.
- Variants: primary/secondary/destructive/quiet, size, density, mode.
- States: default, hover, active, focus, disabled, loading, selected, invalid, success.
- Accessibility: role, accessible name, keyboard interaction, focus behavior.
- Responsive behavior: wrapping, truncation, collapse, overflow.
- Content rules: label length, empty text, error text, loading text.

## Visual Direction

- Operational tools: restrained palette, high information density, clear tables/forms, minimal decoration.
- SaaS marketing: sharper hierarchy, proof, product screenshots, pricing clarity, CTA continuity.
- Ecommerce: product visibility, comparison, price/availability, trust, shipping/returns, checkout clarity.
- Creative/portfolio: expressive visual system, but maintain navigation and content semantics.
- AI tools: explain capability, inputs/outputs, sources, review, correction, and safety boundaries.

## Common Failure Modes

- Component states are visually designed but not implemented.
- Buttons have icons but no accessible names.
- Cards are nested inside cards and hierarchy collapses.
- Color palette is decorative but not semantic.
- Empty/error/loading states are missing.
- Desktop design does not specify mobile behavior.
- Figma components do not map to code components.
- Agent-visible DOM order differs from visual order.

## Implementation Notes

- Use existing libraries and tokens where present.
- Use lucide or the repo's icon system for common actions.
- Keep controls stable in size to avoid layout shift.
- Use real semantic elements before ARIA.
- Prefer CSS variables/Tailwind theme tokens over ad hoc values.
- Add Storybook or component demos when the repo already uses them.
