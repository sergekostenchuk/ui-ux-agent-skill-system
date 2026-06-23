#!/usr/bin/env python3
"""Check TASK-PLAN, progress-state JSON, and progress HTML consistency."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


VALID_STATUSES = {"planned", "running", "waiting_user", "blocked", "done", "failed", "skipped"}
VALID_JOURNEY_STATUSES = {
    "covered",
    "partial",
    "skipped_by_scope",
    "requires_user_approval",
    "needs_rework",
    "not_started",
}


def fail(message: str, findings: list[str]) -> None:
    findings.append(f"ERROR: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate progress view consistency.")
    parser.add_argument("--task-plan", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--html", required=True, type=Path)
    args = parser.parse_args()

    findings: list[str] = []
    for path in [args.task_plan, args.state, args.html]:
        if not path.exists():
            fail(f"missing required artifact: {path}", findings)

    if findings:
        print("\n".join(findings))
        return 1

    task_plan = args.task_plan.resolve()
    state = json.loads(args.state.read_text(encoding="utf-8"))
    html = args.html.read_text(encoding="utf-8")
    task_text = args.task_plan.read_text(encoding="utf-8")

    source_path = Path(state["source_of_truth"]["path"]).resolve()
    if source_path != task_plan:
        fail(f"state source path mismatch: {source_path} != {task_plan}", findings)

    if "TASK-PLAN.md is canonical" not in html:
        fail("HTML does not state canonical TASK-PLAN policy", findings)

    phases = state.get("phases", [])
    summary = state.get("summary", {})
    counted = {
        "done": 0,
        "running": 0,
        "waiting_user": 0,
        "blocked": 0,
        "planned": 0,
        "failed": 0,
    }
    for phase in phases:
        status = phase.get("status")
        if status not in VALID_STATUSES:
            fail(f"invalid phase status: {phase.get('id')} -> {status}", findings)
        elif status != "skipped":
            counted[status] += 1
        if phase.get("id", "") not in html:
            fail(f"phase id missing from HTML: {phase.get('id')}", findings)
        if phase.get("title", "") not in html:
            fail(f"phase title missing from HTML: {phase.get('title')}", findings)
        task_id = phase.get("technical", {}).get("task_id", "")
        if task_id and task_id not in task_text:
            fail(f"phase task id not found in TASK-PLAN: {task_id}", findings)

    for key, value in counted.items():
        if summary.get(key) != value:
            fail(f"summary mismatch for {key}: state={summary.get(key)} counted={value}", findings)
    if summary.get("total") != len(phases):
        fail(f"summary total mismatch: state={summary.get('total')} counted={len(phases)}", findings)

    for gate in state.get("user_gates", []):
        if gate.get("id", "") not in html:
            fail(f"user gate missing from HTML: {gate.get('id')}", findings)
        if gate.get("phase_id") not in {phase.get("id") for phase in phases}:
            fail(f"user gate references unknown phase: {gate.get('id')} -> {gate.get('phase_id')}", findings)

    alignment = state.get("journey_alignment")
    if alignment:
        if "Соответствие обещанному пути" not in html:
            fail("HTML does not render journey alignment section", findings)
        stages = alignment.get("stages", [])
        if not stages:
            fail("journey_alignment has no stages", findings)
        for stage in stages:
            stage_id = stage.get("id", "")
            stage_title = stage.get("title", "")
            status = stage.get("status")
            if status not in VALID_JOURNEY_STATUSES:
                fail(f"invalid journey stage status: {stage_id} -> {status}", findings)
            if stage_id and stage_id not in html:
                fail(f"journey stage id missing from HTML: {stage_id}", findings)
            if stage_title and stage_title not in html:
                fail(f"journey stage title missing from HTML: {stage_title}", findings)
            decision = stage.get("decision")
            reason = stage.get("reason_code")
            if status in {"skipped_by_scope", "requires_user_approval", "needs_rework"} and not reason:
                fail(f"journey stage needs reason_code: {stage_id}", findings)
            if status == "covered" and not stage.get("evidence"):
                fail(f"covered journey stage has no evidence: {stage_id}", findings)

    if findings:
        print("\n".join(findings))
        return 1

    print("PASS: progress state, HTML, and task-plan are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
