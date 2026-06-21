#!/usr/bin/env python3
"""Check that generated runtime projections in dist match canonical core."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


IGNORE_NAMES = {".DS_Store", "__pycache__"}


def compare_dirs(expected: Path, actual: Path, rel: Path = Path("")) -> list[str]:
    issues: list[str] = []
    expected_names = {p.name for p in expected.iterdir() if p.name not in IGNORE_NAMES}
    actual_names = {p.name for p in actual.iterdir() if p.name not in IGNORE_NAMES} if actual.exists() else set()

    for name in sorted(expected_names - actual_names):
        issues.append(f"missing in dist: {(rel / name).as_posix()}")
    for name in sorted(actual_names - expected_names):
        issues.append(f"extra in dist: {(rel / name).as_posix()}")

    for name in sorted(expected_names & actual_names):
        left = expected / name
        right = actual / name
        child_rel = rel / name
        if left.is_dir() and right.is_dir():
            issues.extend(compare_dirs(left, right, child_rel))
        elif left.is_file() and right.is_file():
            if not filecmp.cmp(left, right, shallow=False):
                issues.append(f"different file: {child_rel.as_posix()}")
        else:
            issues.append(f"type mismatch: {child_rel.as_posix()}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify dist/ matches build_adapters.py output.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    dist = root / "dist"
    with tempfile.TemporaryDirectory(prefix="uiux-dist-sync-") as tmp:
        generated = Path(tmp) / "dist"
        subprocess.run(
            [sys.executable, str(root / "scripts" / "build_adapters.py"), str(root), "--out", str(generated)],
            check=True,
            cwd=root,
        )
        issues = compare_dirs(generated, dist)

    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        print(f"FAIL: dist drift detected ({len(issues)} issue(s))")
        return 1
    print("PASS: dist matches generated adapter output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
