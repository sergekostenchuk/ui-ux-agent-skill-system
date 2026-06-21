#!/usr/bin/env python3
"""Run positive and negative evidence-validator fixtures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_evidence_report.py"


def run_case(name: str, args: list[str], expect_ok: bool) -> bool:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    ok = proc.returncode == 0
    if ok == expect_ok:
        print(f"PASS: {name}")
        return True

    expected = "success" if expect_ok else "failure"
    print(f"FAIL: {name}: expected {expected}, got exit {proc.returncode}")
    print(proc.stdout)
    return False


def main() -> int:
    cases = [
        (
            "valid evidence report is accepted",
            ["tests/fixtures/evidence/valid.md"],
            True,
        ),
        (
            "missing artifact report is rejected",
            ["tests/fixtures/evidence/missing-artifact.md"],
            False,
        ),
        (
            "planned-only report is rejected when Ran evidence is required",
            ["--require-ran", "tests/fixtures/evidence/planned-only.md"],
            False,
        ),
    ]
    return 0 if all(run_case(name, args, expect_ok) for name, args, expect_ok in cases) else 1


if __name__ == "__main__":
    sys.exit(main())
