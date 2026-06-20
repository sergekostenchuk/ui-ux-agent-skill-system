# Figma MCP Compatibility

## Primary Sources

- Figma MCP server documentation: https://developers.figma.com/docs/figma-mcp-server/
- Figma MCP tools and prompts: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
- Figma write-to-canvas documentation: https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/
- Figma skills for MCP: https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP
- Use skills with the Figma MCP server: https://help.figma.com/hc/en-us/articles/39287396773399-Use-skills-with-the-Figma-MCP-server
- Plugin API Effect docs: https://developers.figma.com/docs/plugins/api/Effect/
- Plugin typings source: https://raw.githubusercontent.com/figma/plugin-typings/master/plugin-api.d.ts

## Freshness Rule

Figma MCP and Plugin API capabilities change. If the task depends on an exact tool, server mode, prompt name, effect field, or variable binding, check current primary sources or current installed plugin skills before committing to an implementation.

## Tool Availability Rules

- Treat Figma MCP as connected only when the session exposes a Figma MCP tool or installed Figma plugin skill for the requested action.
- For `use_figma`, load the installed `figma:figma-use` skill first.
- For generated design/code-to-canvas tasks, load the installed `figma:figma-generate-design` skill when present.
- For Code Connect, load the installed `figma:figma-code-connect` skill when present.
- If the available tool surface is read-only, do not promise canvas edits.
- If the available tool surface is remote-only or client-specific, say so and offer a fallback.

## Evidence Rules

Acceptable evidence includes tool responses, readback metadata, screenshots, downloaded/exported assets, generated design links, Code Connect files, local diffs, and validation reports. Planned checks are not evidence.
