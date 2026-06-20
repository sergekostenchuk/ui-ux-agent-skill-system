# Agent-Friendly UI

Agent-friendly UI is not separate from accessible UI. It adds determinism and machine-readable action clarity.

## Core Principles

- Use real controls. A clickable `div` is worse for users, assistive tech, and agents than a `button`.
- Give every action a meaningful name: "Save invoice", "Book appointment", "Compare plans", not "Go" or an unlabeled icon.
- Keep visual order and DOM order aligned.
- Preserve URL/state for meaningful views: selected item, step, filter, tab, or document.
- Expose constraints before action: price, required fields, limits, policy, permissions, availability.
- Represent changes in text and state, not only color, motion, or canvas.
- Provide structured data or API docs when the agent should act outside the visible UI.

## HTML And ARIA

- Use landmarks: `header`, `nav`, `main`, `aside`, `footer`.
- Use headings in order; one clear H1 per page or app view.
- Use `label` for form fields; connect errors with `aria-describedby`.
- Use `fieldset` and `legend` for grouped choices.
- Use `aria-live` or role `status` for async status messages when focus does not move.
- Use dialogs with correct focus trapping, close behavior, labels, and return focus.
- Use tables for tabular data, not card grids when comparison is the user's job.
- Avoid ARIA when native HTML already solves the problem.

## Agent Action Contract

For important actions, make these discoverable:

- Action label.
- Object of action.
- Preconditions.
- Required inputs.
- Side effects and cost.
- Success/failure result.
- Undo/cancel/retry path.
- Support/escalation path.

Example: "Cancel subscription" should expose the plan, billing date, consequence, confirmation step, and support link.

## AI Feature UX

- Show what the AI used as sources or inputs when possible.
- Let users edit, regenerate, accept, reject, copy, or export outputs.
- Make confidence/uncertainty visible without pretending to be exact.
- Distinguish system action from suggestion.
- Ask for confirmation before irreversible, paid, public, or privacy-sensitive actions.
- Keep logs/audit trails for business-critical AI-assisted actions.

## Quick Checks

- Can a screen reader user identify every primary action?
- Can a keyboard-only user complete the journey?
- Can an AI browsing agent find the next step by accessible name?
- Is the same critical information present in text, DOM, and visual UI?
- Are errors specific enough for automated recovery?
