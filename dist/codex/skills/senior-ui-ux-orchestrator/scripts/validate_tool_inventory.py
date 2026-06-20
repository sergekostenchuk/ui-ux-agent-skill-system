#!/usr/bin/env python3
"""Validate the shared UI/UX tool inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_TOOL_FIELDS = {
    "id",
    "class",
    "status",
    "skills",
    "path",
    "command",
    "inputs",
    "outputs",
    "privacy",
    "failure_behavior",
}


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    classes = set(data.get("tool_classes", []))
    tools = data.get("tools", [])

    if not isinstance(tools, list) or not tools:
        errors.append("tools must be a non-empty list")
        return errors, warnings

    seen: set[str] = set()
    for index, tool in enumerate(tools):
        prefix = f"tools[{index}]"
        if not isinstance(tool, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(REQUIRED_TOOL_FIELDS - set(tool))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        tool_id = str(tool.get("id", ""))
        if not tool_id:
            errors.append(f"{prefix} has empty id")
        elif tool_id in seen:
            errors.append(f"duplicate tool id: {tool_id}")
        seen.add(tool_id)

        tool_class = tool.get("class")
        if tool_class not in classes:
            errors.append(f"{tool_id or prefix} uses unknown class: {tool_class}")
        if not tool.get("privacy"):
            errors.append(f"{tool_id or prefix} privacy is required")
        if not tool.get("failure_behavior"):
            errors.append(f"{tool_id or prefix} failure_behavior is required")
        if tool_class == "optional-cloud" and "approval" not in str(tool.get("privacy", "")).lower():
            errors.append(f"{tool_id or prefix} optional-cloud tool must require approval in privacy")
        if tool_class == "planned" and "cannot be used as evidence" not in str(tool.get("failure_behavior", "")).lower():
            warnings.append(f"{tool_id or prefix} planned tool should state it cannot be evidence")
        for list_field in ["skills", "inputs", "outputs"]:
            if not isinstance(tool.get(list_field), list) or not tool.get(list_field):
                errors.append(f"{tool_id or prefix} {list_field} must be a non-empty list")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate UI/UX tool inventory JSON.")
    parser.add_argument("--inventory", required=True, help="Path to tool_inventory.json")
    parser.add_argument("--out", required=True, help="Path to write validation report JSON")
    args = parser.parse_args()

    inventory = Path(args.inventory)
    data = json.loads(inventory.read_text(encoding="utf-8"))
    errors, warnings = validate(data)
    report = {
        "inventory": str(inventory),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "tool_count": len(data.get("tools", [])),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
