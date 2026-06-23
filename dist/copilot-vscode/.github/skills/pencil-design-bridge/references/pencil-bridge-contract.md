# Pencil Bridge Contract

## Position

Pencil sits after product/UX framing, SEO/LLM constraints, and design intelligence. It may also sit after Stitch when Stitch output needs editable design exploration.

Correct sequence:

```text
Approved direction brief -> Pencil handoff -> Pencil tool execution or manual handoff -> review -> Figma/code
```

## Required Inputs

- approved direction name and rationale;
- user promise and primary journey;
- content hierarchy and required visible facts;
- design-system, Figma, or implementation constraints;
- accessibility constraints;
- assets available and assets missing;
- exact target output.

## `.pen` Boundary

Assume `.pen` files are tool-managed design documents. Access them only through Pencil MCP/tools. Do not rely on `.pen` being plain JSON or readable via shell.

## Review Questions

1. Does the Pencil output preserve required content as visible text?
2. Does it support the primary journey and one clear CTA?
3. Does it respect accessibility and responsive constraints?
4. Can it map to Figma variables/components or implementation tokens?
5. Are unresolved assumptions and missing assets labeled?
