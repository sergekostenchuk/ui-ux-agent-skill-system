#!/usr/bin/env python3
"""Validate evidence labels in Markdown reports.

This is intentionally conservative: it does not try to prove that a shell
command really ran, but it does fail when a report claims `Ran` evidence with
missing artifact paths, placeholder paths, or planned-only content.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SECTION_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LABEL_RE = re.compile(r"^(Ran|Skipped|Planned|Manual|Artifacts|Risks|Next step):\s*$", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>\"]+")
BACKTICK_RE = re.compile(r"`([^`]+)`")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

PLACEHOLDER_RE = re.compile(r"(?i)\b(TBD|TODO|placeholder|example/path|path/to|fake|dummy)\b")
PLANNED_LANGUAGE_RE = re.compile(r"(?i)\b(planned|will run|to be run|not run|not executed|todo)\b")

COMMAND_PREFIXES = {
    "bash",
    "cat",
    "curl",
    "find",
    "git",
    "mkdir",
    "node",
    "npm",
    "npx",
    "python",
    "python3",
    "rg",
    "sed",
    "test",
}

PATH_HINT_RE = re.compile(
    r"(^|/|\$[A-Z_]+/|\.{1,2}/).+|.+\.(json|md|txt|html|css|js|mjs|ts|py|csv|yaml|yml|png|jpg|jpeg|webp|svg|pdf)$"
)


@dataclass
class ReportResult:
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ran_items: int = 0
    checked_paths: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def normalize_heading(text: str) -> str:
    return text.strip().strip(":").lower()


def extract_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = SECTION_RE.match(line)
        if heading:
            name = normalize_heading(heading.group(2))
            current = name
            sections.setdefault(current, [])
            continue

        label = LABEL_RE.match(line.strip())
        if label:
            current = normalize_heading(label.group(1))
            sections.setdefault(current, [])
            continue

        if current is not None:
            sections[current].append(line)

    return sections


def bullet_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("-", "*")):
            out.append(stripped[1:].strip())
        elif stripped.startswith(tuple(f"{i}." for i in range(1, 10))):
            out.append(stripped.split(".", 1)[1].strip())
        elif stripped.lower() not in {"none", "n/a", "not applicable"}:
            out.append(stripped)
    return out


def is_command(value: str) -> bool:
    first = value.strip().split(maxsplit=1)[0] if value.strip() else ""
    return first in COMMAND_PREFIXES


def is_path_like(value: str) -> bool:
    if URL_RE.fullmatch(value.strip()):
        return False
    if is_command(value):
        return False
    return bool(PATH_HINT_RE.match(value.strip()))


def resolve_path(raw: str, report_path: Path, root: Path) -> Path:
    value = raw.strip().strip("\"'")
    if value.startswith("$OBSIDIAN_VAULT_PATH/"):
        # Portable docs may mention this env var. It is not a local artifact path
        # unless the caller expands it before validation.
        return Path(value)
    path = Path(value)
    if path.is_absolute():
        return path
    local = (report_path.parent / path).resolve()
    if local.exists():
        return local
    return (root / path).resolve()


def evidence_tokens(item: str) -> list[str]:
    tokens = BACKTICK_RE.findall(item)
    tokens.extend(MD_LINK_RE.findall(item))
    tokens.extend(URL_RE.findall(item))
    return tokens


def validate_report(path: Path, root: Path, require_ran: bool) -> ReportResult:
    result = ReportResult(path=str(path))
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = extract_sections(text)
    ran_items = bullet_lines(sections.get("ran", []))
    result.ran_items = len(ran_items)

    if require_ran and not ran_items:
        result.errors.append("required Ran evidence is missing")

    for idx, item in enumerate(ran_items, start=1):
        if PLACEHOLDER_RE.search(item):
            result.errors.append(f"Ran item {idx} contains placeholder language: {item}")
        if PLANNED_LANGUAGE_RE.search(item):
            result.errors.append(f"Ran item {idx} appears to describe planned or unexecuted work: {item}")

        tokens = evidence_tokens(item)
        has_supported_evidence = bool(URL_RE.search(item)) or item.lower().startswith(("tool:", "external:"))
        has_command = any(is_command(token) for token in tokens)

        for token in tokens:
            if URL_RE.fullmatch(token):
                has_supported_evidence = True
                continue
            if not is_path_like(token):
                continue
            resolved = resolve_path(token, path, root)
            result.checked_paths.append(token)
            if str(resolved).startswith("$OBSIDIAN_VAULT_PATH/"):
                result.warnings.append(f"portable env path not checked: {token}")
                continue
            if not resolved.exists():
                result.errors.append(f"Ran item {idx} references missing artifact path: {token}")
            else:
                has_supported_evidence = True

        if not tokens and not has_supported_evidence:
            result.errors.append(f"Ran item {idx} has no command, URL, tool marker, or artifact path: {item}")
        elif has_command:
            has_supported_evidence = True

        if not has_supported_evidence:
            result.errors.append(f"Ran item {idx} has no supported evidence token: {item}")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Markdown evidence report labels.")
    parser.add_argument("reports", nargs="+", help="Markdown report files to validate.")
    parser.add_argument("--root", default=".", help="Repository root for relative artifact paths.")
    parser.add_argument("--require-ran", action="store_true", help="Fail when a report has no Ran entries.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    results = [validate_report(Path(report).resolve(), root, args.require_ran) for report in args.reports]

    if args.json:
        print(
            json.dumps(
                {
                    "ok": all(result.ok for result in results),
                    "results": [result.__dict__ for result in results],
                },
                indent=2,
            )
        )
    else:
        for result in results:
            for warning in result.warnings:
                print(f"WARN: {result.path}: {warning}")
            for error in result.errors:
                print(f"ERROR: {result.path}: {error}")
        if all(result.ok for result in results):
            print(f"PASS: evidence report validation passed for {len(results)} report(s)")

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
