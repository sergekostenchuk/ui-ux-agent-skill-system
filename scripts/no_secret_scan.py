#!/usr/bin/env python3
"""Scan public planning artifacts for common secret/token patterns."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".html", ".json", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "reports/tmp"}
SKIP_NAMES = {".env"}

SECRET_PATTERNS = {
    "npm_token": re.compile(r"npm_[A-Za-z0-9]{20,}"),
    "stitch_api_key": re.compile(r"AQ\.[A-Za-z0-9_-]{20,}"),
    "openai_style_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    "raw_64_hex_recovery_code": re.compile(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])"),
    "plain_secret_assignment": re.compile(
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*(?!redacted|example|placeholder|\$\{\{)[A-Za-z0-9_.:/+=-]{16,}"
    ),
}


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if path.name in SKIP_NAMES:
        return True
    parts = set(rel.parts)
    if parts & SKIP_DIRS:
        return True
    return False


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if path.is_dir() or should_skip(path, root):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(f"read_error: {path.relative_to(root)}: {exc}")
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{name}: {path.relative_to(root)}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Markdown, HTML, JSON, YAML, and reports for secret patterns.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = scan(root)
    for finding in findings:
        print(f"ERROR: {finding}")
    if findings:
        print(f"FAIL: secret scan found {len(findings)} issue(s)")
        return 1
    print("PASS: no secret patterns found in scanned text artifacts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
