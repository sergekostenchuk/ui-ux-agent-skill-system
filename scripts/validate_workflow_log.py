#!/usr/bin/env python3
"""Validate workflow-log.jsonl events and fixture expectations."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DECISIONS = {"continue", "pause_for_user", "return_to_rework", "skip_with_reason", "block"}
ACTUAL_STATES = {"covered", "partial", "not_started", "skipped", "approval_required", "blocked", "failed"}
ACCEPTABLE_SKIP_REASONS = {
    "out_of_scope_demo",
    "user_not_approved_external",
    "missing_user_data",
    "tool_unavailable",
    "service_bug",
    "not_required_for_selected_mode",
    "user_accepted_skip",
}
FORBIDDEN_REASON_CODES = {
    "model_convenience",
    "time_saving_without_user_notice",
    "implicit_assumption",
    "tool_not_called_but_marked_done",
    "planned_counted_as_ran",
}
SECRET_PATTERNS = [
    re.compile(r"npm_[A-Za-z0-9]{20,}"),
    re.compile(r"AQ\.[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])"),
]


REQUIRED = [
    "timestamp",
    "project",
    "declared_journey",
    "expected_stage",
    "actual_state",
    "decision",
    "reason_code",
    "evidence",
    "user_options",
    "owner_role",
    "message",
]


def validate_event(event: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key in REQUIRED:
        if key not in event:
            issues.append(f"missing field: {key}")
    raw = json.dumps(event, ensure_ascii=False)
    for pattern in SECRET_PATTERNS:
        if pattern.search(raw):
            issues.append("secret-like value found")
    decision = event.get("decision")
    actual_state = event.get("actual_state")
    reason = event.get("reason_code")
    evidence = event.get("evidence") or []
    options = event.get("user_options") or []
    if decision not in DECISIONS:
        issues.append(f"invalid decision: {decision}")
    if actual_state not in ACTUAL_STATES:
        issues.append(f"invalid actual_state: {actual_state}")
    if reason in FORBIDDEN_REASON_CODES:
        issues.append(f"forbidden reason_code: {reason}")
    if decision == "continue" and not evidence:
        issues.append("continue requires evidence")
    if decision == "skip_with_reason" and reason not in ACCEPTABLE_SKIP_REASONS:
        issues.append(f"skip_with_reason requires acceptable reason, got {reason}")
    if decision in {"pause_for_user", "block"} and not options:
        issues.append(f"{decision} requires user_options")
    if decision == "return_to_rework" and reason not in {"missing_evidence", "service_bug", "quality_or_privacy_risk"}:
        issues.append(f"return_to_rework requires rework reason, got {reason}")
    return issues


def iter_events(path: Path):
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            yield line_number, json.loads(line)
        except json.JSONDecodeError as exc:
            yield line_number, {"__json_error__": str(exc)}


def validate_log(path: Path) -> list[str]:
    issues: list[str] = []
    for line_number, event in iter_events(path):
        if "__json_error__" in event:
            issues.append(f"{path}:{line_number}: invalid json: {event['__json_error__']}")
            continue
        for issue in validate_event(event):
            issues.append(f"{path}:{line_number}: {issue}")
    return issues


def validate_fixtures(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.glob("log-*.json")):
        fixture = json.loads(path.read_text(encoding="utf-8"))
        expected_valid = bool(fixture["expected_valid"])
        actual_valid = not validate_event(fixture["event"])
        if actual_valid != expected_valid:
            issues.append(f"{path}: expected_valid={expected_valid}, actual_valid={actual_valid}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate workflow governance logs.")
    parser.add_argument("--log", type=Path)
    parser.add_argument("--fixtures", nargs="?", const=Path("evals/workflow-compliance"), type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    issues: list[str] = []
    if args.log:
        if not args.log.exists():
            issues.append(f"missing log: {args.log}")
        else:
            issues.extend(validate_log(args.log))
    if args.fixtures:
        issues.extend(validate_fixtures(args.fixtures))
    text = "\n".join([f"ERROR: {issue}" for issue in issues]) if issues else "PASS: workflow log validation passed"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
