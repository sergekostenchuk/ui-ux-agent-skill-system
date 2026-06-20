# User Journey Architecture

Use this when designing or auditing product flows.

## Journey Fields

- Role: user type, permissions, knowledge level, device, urgency.
- Trigger: why the user arrives now.
- Goal: concrete outcome, not a screen name.
- Entry point: URL, nav item, search result, notification, email, AI-agent handoff, deep link.
- Context: what the user already knows and what the system knows.
- Decision points: facts needed before action.
- Action path: primary steps and alternatives.
- Feedback: confirmation, progress, status, validation, success, receipt.
- Recovery: undo, edit, cancel, retry, support, fallback.
- Return path: what happens next time or after completion.

## Flow Types

- Learn/compare: needs hierarchy, proof, summaries, details, and stable next action.
- Configure/create: needs progressive disclosure, validation, preview, save states, undo.
- Buy/book: needs price, availability, fees, policies, trust, support, confirmation.
- Monitor/manage: needs density, filters, sorting, status, alerts, bulk actions.
- Troubleshoot: needs diagnosis, plain language, stepwise fixes, escalation path.
- AI-assisted: needs sources, confidence boundaries, editable output, review/approve, rollback.

## State Coverage

Every important component or screen should define:

- Default
- Loading
- Empty
- Partial data
- Error
- Disabled
- Success
- Warning
- Permission/auth required
- Offline or degraded mode where relevant

## Review Questions

- Can a first-time user understand what this screen is for within 5 seconds?
- Is the next action obvious without reading all copy?
- Can a returning user perform the task quickly?
- Are irreversible or expensive actions protected by clear review?
- Can the user recover from mistakes?
- Can the flow be completed on mobile and keyboard-only?
- Would an AI agent know which control to use from labels, roles, and state?
