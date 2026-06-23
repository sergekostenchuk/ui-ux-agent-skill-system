#!/usr/bin/env python3
"""Append one sanitized workflow governance event to workflow-log.jsonl."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"npm_[A-Za-z0-9]{20,}"),
    re.compile(r"AQ\.[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?<![A-Za-z0-9])[a-f0-9]{64}(?![A-Za-z0-9])"),
]


def reject_secrets(value: Any) -> None:
    raw = json.dumps(value, ensure_ascii=False)
    for pattern in SECRET_PATTERNS:
        if pattern.search(raw):
            raise SystemExit("Refusing to write workflow log event with secret-like value")


def csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a workflow governance event.")
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--journey", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--actual-state", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--reason-code", required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--user-options", default="")
    parser.add_argument("--owner-role", default="workflow-compliance-supervisor")
    parser.add_argument("--message", required=True)
    parser.add_argument("--next-action", default="")
    parser.add_argument("--impact", default="")
    args = parser.parse_args()

    event = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project": args.project,
        "declared_journey": args.journey,
        "expected_stage": args.stage,
        "actual_state": args.actual_state,
        "decision": args.decision,
        "reason_code": args.reason_code,
        "evidence": csv(args.evidence),
        "user_options": csv(args.user_options),
        "owner_role": args.owner_role,
        "message": args.message,
        "next_action": args.next_action,
        "impact": args.impact,
    }
    reject_secrets(event)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    with args.log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Appended workflow event to {args.log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
