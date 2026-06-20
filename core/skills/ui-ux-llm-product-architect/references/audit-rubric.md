# UI/UX Audit Rubric

Use this for design reviews and code reviews. Lead findings by severity.

## Severity

- P0: Blocks primary journey, creates legal/security/privacy risk, hides material cost/policy, or makes core action inaccessible.
- P1: Causes frequent confusion, abandonment, accessibility failure, agent unreadability, or major responsive breakage.
- P2: Reduces polish, speed, consistency, or confidence but does not block the journey.

## Audit Areas

- Journey fit: user goal, entry, primary action, decision points, recovery.
- Information architecture: page purpose, hierarchy, navigation, URL/state, grouping.
- Visual design: layout, spacing, typography, color, density, responsive behavior.
- Interaction: controls, affordance, feedback, loading, error, empty, success states.
- Accessibility: contrast, keyboard, focus, labels, semantic HTML, motion, touch target.
- Agent readiness: landmarks, accessible names, deterministic labels, text alternatives, state announcements, structured action paths.
- Trust and clarity: pricing, policies, availability, support, data use, source/evidence.
- Implementation: component reuse, tokens, performance, layout stability, cross-device behavior.

## Output Shape

For each finding:

```text
P1 - Finding title
Evidence: concrete screen, route, component, or code reference.
Impact: user and/or agent consequence.
Fix: specific design or implementation change.
Verification: how to confirm it is fixed.
```
