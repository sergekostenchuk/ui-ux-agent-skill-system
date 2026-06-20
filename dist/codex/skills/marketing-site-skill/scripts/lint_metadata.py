#!/usr/bin/env python3
"""Lint basic metadata for local HTML or app files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HTML_EXTENSIONS = {".html", ".htm", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte"}


def collect_files(root: Path) -> list[Path]:
    ignored = {"node_modules", "dist", "build", ".git", "reports"}
    files: list[Path] = []
    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts
        if any(part in ignored for part in relative_parts):
            continue
        if path.is_file() and path.suffix in HTML_EXTENSIONS:
            files.append(path)
    return files


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.DOTALL) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="Check common public-page metadata markers.")
    parser.add_argument("--root", required=True, help="Project root or folder containing HTML/app files.")
    parser.add_argument("--out", required=True, help="JSON report path.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in collect_files(root))
    checks = {
        "title": has(r"<title[^>]*>.+?</title>", text) or has(r"title\s*[:=]", text),
        "description": has(r"meta\s+name=[\"']description[\"']", text) or has(r"description\s*[:=]", text),
        "canonical": has(r"rel=[\"']canonical[\"']", text),
        "og_title": has(r"property=[\"']og:title[\"']", text),
        "og_description": has(r"property=[\"']og:description[\"']", text),
        "og_image": has(r"property=[\"']og:image[\"']", text),
        "twitter_card": has(r"name=[\"']twitter:card[\"']", text),
        "h1": has(r"<h1[^>]*>.+?</h1>", text)
    }
    missing = [name for name, present in checks.items() if not present]
    report = {
        "root": str(root),
        "files_scanned": len(collect_files(root)),
        "passed": not missing,
        "checks": checks,
        "missing": missing
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
