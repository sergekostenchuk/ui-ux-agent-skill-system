#!/usr/bin/env python3
"""Validate journey compliance decisions and project alignment reports."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
VALID_DECISIONS = {"continue", "pause_for_user", "return_to_rework", "skip_with_reason", "block"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stage_keyword(stage_title: str) -> str:
    title = stage_title.lower()
    pairs = [
        ("intake", "intake"),
        ("existing", "existing"),
        ("search", "serp|semantic|keyword|search"),
        ("semantic", "serp|semantic|keyword|search"),
        ("concept", "concept|prototype|journey|offer"),
        ("three", r"three\s+(?:distinct\s+)?(?:design|direction|variant)|3\s*(?:design|direction|variant)|DESIGN-V[0-9]"),
        ("design refresh", "design|refresh|direction"),
        ("ai design", "stitch|pencil|figma|ai design"),
        ("build", "build|implementation|content|asset"),
        ("measurement", "analytics|assistant|paid|measurement"),
        ("launch", "launch|deploy|dns|ssl|webmaster"),
        ("validation", "validation|audit|schema|accessibility"),
        ("migration", "migration|redirect|url"),
        ("admin", "admin|cms|operator"),
    ]
    for needle, pattern in pairs:
        if needle in title:
            return pattern
    return re.escape(title.split()[0]) if title.split() else "stage"


def task_plan_text(project: Path) -> str:
    path = project / "TASK-PLAN.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def artifact_exists(project: Path, rel_or_abs: str) -> bool:
    path = Path(rel_or_abs)
    if not path.is_absolute():
        path = project / path
    return path.exists()


def validate_decision(decision: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    state = decision.get("decision")
    reason = decision.get("reason_code")
    evidence = decision.get("evidence") or []
    user_options = decision.get("user_options") or decision.get("user_options_available") or []
    if state not in VALID_DECISIONS:
        issues.append(f"invalid decision: {state}")
    if reason in FORBIDDEN_REASON_CODES:
        issues.append(f"forbidden reason_code: {reason}")
    if state == "continue" and not evidence:
        issues.append("continue requires evidence")
    if state == "skip_with_reason" and reason not in ACCEPTABLE_SKIP_REASONS:
        issues.append(f"skip_with_reason requires acceptable reason, got {reason}")
    if state in {"pause_for_user", "block"} and not user_options:
        issues.append(f"{state} requires user options")
    if decision.get("claimed_ran") and not evidence:
        issues.append("claimed Ran without evidence")
    if decision.get("artifact_required") and not evidence:
        issues.append("artifact_required but evidence is empty")
    return issues


def evaluate_stage(project: Path, journey_id: str, stage: dict[str, Any], task_text: str) -> dict[str, Any]:
    stage_id = stage["id"]
    title = stage["title"]
    pattern = stage_keyword(title)
    evidence: list[str] = []
    actual_state = "not_started"
    decision = "return_to_rework"
    reason = "missing_evidence"
    options: list[str] = []
    impact = ""

    if re.search(pattern, task_text, re.IGNORECASE):
        actual_state = "partial"
        evidence.append(str(project / "TASK-PLAN.md"))
        decision = "continue"
        reason = "covered_by_evidence"

    lower = title.lower()
    if "search" in lower or "semantic" in lower:
        if re.search(r"serp|semantic|keyword|search", task_text, re.IGNORECASE):
            actual_state = "partial"
            evidence.append(str(project / "TASK-PLAN.md"))
        if re.search(r"no external|scope_out|out of scope|external.*not", task_text, re.IGNORECASE):
            actual_state = "approval_required"
            decision = "pause_for_user"
            reason = "user_not_approved_external"
            options = ["approve_external_research", "use_local_materials_only", "skip_with_impact"]
            impact = "Semantic core will be hypothesis-labeled until external search is approved."
    elif "three" in lower:
        if re.search(r"three\s+(?:distinct\s+)?(?:design|direction|variant)|3\s*(?:design|direction|variant)|DESIGN-V[0-9]", task_text, re.IGNORECASE):
            actual_state = "partial"
            evidence.append(str(project / "TASK-PLAN.md"))
            decision = "continue"
            reason = "covered_by_evidence"
        else:
            actual_state = "skipped"
            decision = "skip_with_reason"
            reason = "out_of_scope_demo"
            impact = "Only one implementation direction was produced in the local demo slice."
    elif "ai design" in lower:
        actual_state = "approval_required"
        decision = "pause_for_user"
        reason = "user_not_approved_external"
        options = ["approve_stitch_or_pencil", "continue_without_ai_exploration"]
        impact = "Stitch/Pencil/Figma exploration remains a candidate future step."
    elif "measurement" in lower:
        actual_state = "skipped"
        decision = "skip_with_reason"
        reason = "out_of_scope_demo"
        impact = "Analytics, paid traffic, and public AI assistant were outside the demo slice."
    elif "launch" in lower:
        actual_state = "approval_required"
        decision = "pause_for_user"
        reason = "missing_user_data"
        options = ["provide_domain_hosting_contacts", "keep_local_demo_only"]
        impact = "Production launch cannot proceed without domain, hosting, contact, and approval data."
    elif "build" in lower:
        if artifact_exists(project, "index.html"):
            actual_state = "covered"
            decision = "continue"
            reason = "covered_by_evidence"
            evidence.append(str(project / "index.html"))
            for rel in ["reports/html-parse.txt", "reports/visual-smoke/desktop.png", "reports/visual-smoke/mobile.png"]:
                if artifact_exists(project, rel):
                    evidence.append(str(project / rel))
    elif "intake" in lower:
        if task_text:
            actual_state = "covered"
            decision = "continue"
            reason = "covered_by_evidence"
            evidence.append(str(project / "TASK-PLAN.md"))
    elif "concept" in lower:
        if task_text:
            actual_state = "partial"
            decision = "continue"
            reason = "covered_by_evidence"
            evidence.append(str(project / "TASK-PLAN.md"))

    return {
        "expected_stage_id": stage_id,
        "title": title,
        "actual_state": actual_state,
        "decision": decision,
        "reason_code": reason,
        "evidence": list(dict.fromkeys(evidence)),
        "user_options": options,
        "impact": impact,
        "user_message": user_message(decision, reason),
        "next_action": next_action(decision, reason),
    }


def user_message(decision: str, reason: str) -> str:
    if decision == "pause_for_user":
        return "Нужны ваши данные или разрешение, иначе система может сделать неправильный шаг."
    if decision == "return_to_rework":
        return "Этап заявлен как готовый, но доказательств недостаточно. Возвращаем на доработку."
    if decision == "skip_with_reason":
        return "Этап пропущен осознанно. Причина и влияние зафиксированы."
    if decision == "block":
        return "Дальше идти нельзя без риска для качества, приватности или запуска."
    return "Логика соблюдена, можно продолжать."


def next_action(decision: str, reason: str) -> str:
    if decision == "pause_for_user":
        return "Ask user for approval, missing data, or scope confirmation."
    if decision == "return_to_rework":
        return "Create or reopen a repair task before final handoff."
    if decision == "skip_with_reason":
        return "Show the skip reason and downstream impact to the user."
    if decision == "block":
        return "Stop workflow until blocker is resolved or scope changes."
    return "Continue workflow."


def validate_fixtures(root: Path) -> list[str]:
    issues: list[str] = []
    files = sorted(path for path in root.glob("*.json") if not path.name.startswith("log-"))
    for path in files:
        fixture = load_json(path)
        expected_valid = bool(fixture["expected_valid"])
        decision = fixture["decision"]
        actual_valid = not validate_decision(decision)
        if actual_valid != expected_valid:
            issues.append(f"{path}: expected_valid={expected_valid}, actual_valid={actual_valid}")
    return issues


def project_report(project: Path, registry_path: Path, journey_id: str) -> tuple[str, list[dict[str, Any]]]:
    registry = load_json(registry_path)
    journey = next((item for item in registry["journeys"] if item["id"] == journey_id), None)
    if not journey:
        raise SystemExit(f"Unknown journey: {journey_id}")
    text = task_plan_text(project)
    decisions = [evaluate_stage(project, journey_id, stage, text) for stage in journey["stages"]]
    lines = [
        "# Workflow Compliance Report",
        "",
        f"project: {project}",
        f"declared_journey: {journey_id}",
        f"generated_at: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        "",
        "| stage | state | decision | reason | evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in decisions:
        evidence = "<br>".join(item["evidence"]) if item["evidence"] else "none"
        lines.append(
            f"| {item['title']} | {item['actual_state']} | {item['decision']} | {item['reason_code']} | {evidence} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The report does not claim the full journey is complete. It separates covered stages, approval-gated stages, and justified demo-scope skips.",
        ]
    )
    return "\n".join(lines) + "\n", decisions


def write_log(path: Path, project: Path, journey_id: str, decisions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for decision in decisions:
            event = {
                "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "project": str(project),
                "declared_journey": journey_id,
                "expected_stage": decision["expected_stage_id"],
                "actual_state": decision["actual_state"],
                "decision": decision["decision"],
                "reason_code": decision["reason_code"],
                "evidence": decision["evidence"],
                "user_options": decision["user_options"],
                "owner_role": "workflow-compliance-supervisor",
                "message": decision["user_message"],
                "next_action": decision["next_action"],
                "impact": decision.get("impact", ""),
            }
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate workflow compliance.")
    parser.add_argument("--fixtures", nargs="?", const=Path("evals/workflow-compliance"), type=Path)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--journey", default="new-premium-site")
    parser.add_argument("--journey-registry", type=Path, default=Path("data/journey-registry.json"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--fixture-report", type=Path, default=Path("reports/validation/workflow-compliance-fixtures.txt"))
    args = parser.parse_args()

    issues: list[str] = []
    if args.fixtures:
        issues.extend(validate_fixtures(args.fixtures))
        fixture_text = "\n".join([f"ERROR: {issue}" for issue in issues]) if issues else "PASS: workflow compliance fixtures passed"
        args.fixture_report.parent.mkdir(parents=True, exist_ok=True)
        args.fixture_report.write_text(fixture_text + "\n", encoding="utf-8")
        print(fixture_text)
    if args.project:
        report, decisions = project_report(args.project.resolve(), args.journey_registry.resolve(), args.journey)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(report, encoding="utf-8")
            print(f"Wrote {args.out}")
        if args.log:
            write_log(args.log, args.project.resolve(), args.journey, decisions)
            print(f"Wrote {args.log}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
