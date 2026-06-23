#!/usr/bin/env python3
"""Run the UI UX Skill System workflow compliance validator."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path("$UIUX_SKILL_SYSTEM_ROOT")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run workflow compliance validation for a project.")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--journey", default="new-premium-site")
    parser.add_argument("--fixtures", action="store_true")
    args = parser.parse_args()

    cmd = ["python3", str(ROOT / "scripts/validate_workflow_compliance.py")]
    if args.fixtures:
        cmd.append("--fixtures")
    if args.project:
        report = args.project / "reports/workflow-compliance-report.md"
        log = args.project / "workflow-log.jsonl"
        cmd.extend([
            "--project",
            str(args.project),
            "--journey",
            args.journey,
            "--journey-registry",
            str(ROOT / "data/journey-registry.json"),
            "--out",
            str(report),
            "--log",
            str(log),
        ])
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())

