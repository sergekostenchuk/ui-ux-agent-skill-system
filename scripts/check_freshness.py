#!/usr/bin/env python3
"""Validate static data freshness metadata without live network calls."""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


DATA_ROOT = Path("core/skills/ui-ux-pro-max/data")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def csv_files(root: Path) -> list[Path]:
    data_root = root / DATA_ROOT
    if not data_root.is_dir():
        return []
    return sorted(path.relative_to(root) for path in data_root.rglob("*.csv"))


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / DATA_ROOT / "freshness.json"
    return json.loads(path.read_text(encoding="utf-8"))


def covered_by(entry: dict[str, Any], rel: str) -> bool:
    paths = entry.get("paths", [])
    globs = entry.get("globs", [])
    return rel in paths or any(fnmatch.fnmatch(rel, pattern) for pattern in globs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check UI/UX Pro Max static data freshness metadata.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--today", default=date.today().isoformat(), help="Override current date for deterministic tests.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    today = parse_date(args.today)
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_manifest(root)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"cannot read freshness manifest: {exc}")
        manifest = {"datasets": []}

    datasets = manifest.get("datasets", [])
    if not isinstance(datasets, list) or not datasets:
        errors.append("freshness manifest must contain a non-empty `datasets` list")
        datasets = []

    for index, entry in enumerate(datasets):
        name = entry.get("name", f"dataset-{index}")
        if not entry.get("source_url") and not entry.get("source_category"):
            errors.append(f"{name}: missing source_url or source_category")
        if not entry.get("last_checked_at"):
            errors.append(f"{name}: missing last_checked_at")
            continue
        try:
            checked = parse_date(str(entry["last_checked_at"]))
        except ValueError:
            errors.append(f"{name}: invalid last_checked_at {entry.get('last_checked_at')!r}")
            continue
        if checked > today:
            errors.append(f"{name}: last_checked_at is in the future")
        max_age = int(entry.get("max_age_days", manifest.get("default_max_age_days", 180)))
        age = (today - checked).days
        if age > max_age:
            severity = entry.get("stale_severity", "warning")
            message = f"{name}: metadata is stale, age={age} max_age_days={max_age}"
            if severity == "blocking":
                errors.append(message)
            else:
                warnings.append(message)
        if not entry.get("paths") and not entry.get("globs"):
            errors.append(f"{name}: missing paths or globs")

    uncovered: list[str] = []
    for path in csv_files(root):
        rel = path.as_posix()
        if not any(covered_by(entry, rel) for entry in datasets):
            uncovered.append(rel)
    for rel in uncovered:
        errors.append(f"uncovered csv: {rel}")

    result = {
        "ok": not errors,
        "csv_count": len(csv_files(root)),
        "dataset_count": len(datasets),
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for warning in warnings:
            print(f"WARN: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        if not errors:
            print(f"PASS: freshness metadata covers {result['csv_count']} csv file(s) in {result['dataset_count']} dataset group(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
