#!/usr/bin/env python3
"""Validate the public UI/UX Agent Skill System package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "README.md",
    "SECURITY.md",
    "LICENSE",
    "docs/architecture.md",
    "docs/skill-map.md",
    "docs/vendor-compatibility.md",
    "docs/install.md",
    "evals/evals.json",
]

REQUIRED_ADAPTERS = [
    "codex",
    "claude",
    "gemini-cli",
    "qwen-code",
    "copilot-vscode",
    "glm-zai",
    "kimi",
    "generic-agent",
]

FORBIDDEN_PATTERNS = [
    re.compile("/Users/" + "kostenchuksergey"),
    re.compile(r"AQ\.[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*=\s*(?!redacted|example|placeholder)[A-Za-z0-9_.:/+=-]{10,}"),
]

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".mjs",
    ".js",
    ".ts",
    ".csv",
    ".html",
    ".css",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end].strip().splitlines()
    data: dict[str, str] = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def check_json(path: Path, errors: list[str]) -> None:
    try:
        json.loads(read_text(path))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid json: {path}: {exc}")


def lint(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_TOP_LEVEL:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for adapter in REQUIRED_ADAPTERS:
        if not (root / "adapters" / adapter).is_dir():
            errors.append(f"missing adapter directory: adapters/{adapter}")

    skills_dir = root / "core" / "skills"
    if not skills_dir.is_dir():
        errors.append("missing core/skills")
    else:
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"missing SKILL.md: {skill_dir.relative_to(root)}")
                continue
            fm = parse_frontmatter(read_text(skill_md))
            if not fm:
                errors.append(f"invalid frontmatter: {skill_md.relative_to(root)}")
                continue
            if fm.get("name") != skill_dir.name:
                errors.append(
                    f"frontmatter name mismatch: {skill_md.relative_to(root)} name={fm.get('name')} folder={skill_dir.name}"
                )
            if not fm.get("description"):
                errors.append(f"missing description: {skill_md.relative_to(root)}")

    for path in root.rglob("*"):
        if path.is_dir():
            if path.name == "__pycache__":
                errors.append(f"pycache must not be published: {path.relative_to(root)}")
            continue
        if path.name == ".env":
            errors.append(f".env must not be published: {path.relative_to(root)}")
        if path.suffix == ".pyc":
            errors.append(f"pyc must not be published: {path.relative_to(root)}")
        if path.suffix == ".json":
            check_json(path, errors)
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = read_text(path)
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(text):
                    errors.append(f"forbidden pattern {pattern.pattern!r}: {path.relative_to(root)}")

    if not (root / "core" / "shared" / "privacy-policy.md").is_file():
        warnings.append("core/shared/privacy-policy.md missing; shared privacy contract should exist")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors, warnings = lint(root)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} errors, {len(warnings)} warnings")
        return 1
    print(f"PASS: publication package lint passed with {len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
