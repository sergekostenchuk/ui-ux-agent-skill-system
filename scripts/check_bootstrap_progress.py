#!/usr/bin/env python3
"""Validate bootstrap progress artifacts created before TASK-PLAN.md exists."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check bootstrap progress artifacts.")
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    request_path = project_root / "project-request.json"
    log_path = project_root / "workflow-log.jsonl"
    state_path = project_root / "progress-state.json"
    html_path = project_root / "agent-progress-screen.html"
    required = [request_path, log_path, state_path, html_path]

    findings: list[str] = []
    for path in required:
        if not path.exists():
            findings.append(f"ERROR: missing {path}")

    if findings:
        print("\n".join(findings))
        return 1

    request = json.loads(request_path.read_text(encoding="utf-8"))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    log_lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if request.get("status") != "accepted":
        findings.append("ERROR: project-request.json status must be accepted")
    if not request.get("user_request"):
        findings.append("ERROR: project-request.json must include user_request")
    if state.get("source_of_truth", {}).get("kind") != "bootstrap-request":
        findings.append("ERROR: progress-state source_of_truth.kind must be bootstrap-request")
    if Path(state.get("source_of_truth", {}).get("path", "")).resolve() != request_path:
        findings.append("ERROR: progress-state source path must point to project-request.json")
    if not state.get("phases"):
        findings.append("ERROR: progress-state must include bootstrap phases")
    if state.get("summary", {}).get("running", 0) < 1:
        findings.append("ERROR: bootstrap summary must show at least one running step")
    if "Bootstrap mode" not in html:
        findings.append("ERROR: rendered HTML must state bootstrap source policy")
    if "Формируем task-plan" not in html:
        findings.append("ERROR: rendered HTML must show task-plan formation")
    if not log_lines:
        findings.append("ERROR: workflow-log.jsonl must contain at least one event")
    else:
        has_bootstrap_event = False
        for index, line in enumerate(log_lines, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                findings.append(f"ERROR: invalid JSONL at line {index}: {exc}")
                continue
            if event.get("reason_code") == "bootstrap_progress_required":
                has_bootstrap_event = True
        if not has_bootstrap_event:
            findings.append("ERROR: workflow log must record bootstrap_progress_required")

    if findings:
        print("\n".join(findings))
        return 1

    print("PASS: bootstrap progress artifacts are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
