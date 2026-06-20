# Figma Safety And Evidence

## Sensitive Inputs

Treat these as sensitive unless the user says they are public:

- Figma URLs, file keys, page names, node IDs, screenshots, and exports.
- Design Variables, tokens, component library names, brand systems, and unpublished assets.
- Browser captures from staging, admin panels, internal tools, or authenticated pages.
- Source code, API responses, customer data, analytics, and product roadmap details.

## Mutation Scope

Before modifying Figma:

1. Identify target file, page, frame, node, or component set.
2. State the intended operation: create, update, delete, bind, export, or generate.
3. Prefer duplicate-frame or branch-like workflows for broad changes.
4. Capture before/after evidence when possible.
5. Report what was skipped if the MCP tool was not available.

## Data Transfer Note

When an operation sends local code, screenshots, browser pages, or exported assets to Figma or another external service, record what is sent, why it is needed, and whether the user approved it.
