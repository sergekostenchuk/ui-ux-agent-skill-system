#!/usr/bin/env python3
"""Create the earliest possible progress screen before TASK-PLAN.md exists."""

from __future__ import annotations

import argparse
import json
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from render_progress_screen import render


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_journey(registry_path: Path | None, journey_id: str | None) -> dict[str, Any] | None:
    if not registry_path or not journey_id or not registry_path.exists():
        return None
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    return next((item for item in registry.get("journeys", []) if item.get("id") == journey_id), None)


def build_journey_alignment(journey: dict[str, Any] | None, registry_path: Path | None, journey_id: str | None) -> dict[str, Any] | None:
    if not journey:
        return None
    stages = []
    for stage in journey.get("stages", []):
        stages.append(
            {
                "id": stage.get("id", ""),
                "title": stage.get("title", ""),
                "status": "not_started",
                "decision": "continue",
                "reason_code": "bootstrap_pending_task_plan",
                "message": "Этап еще не начат: система сначала формирует canonical TASK-PLAN.md.",
                "next_action": "Дождаться генерации TASK-PLAN.md; затем экран обновится по полному пути.",
                "evidence": [],
                "skills": stage.get("skills", []),
                "subprocess_count": len(stage.get("subprocesses", [])),
            }
        )
    return {
        "declared_journey": journey_id or journey.get("id", ""),
        "title": journey.get("title", journey_id or ""),
        "registry_path": str(registry_path.resolve()) if registry_path else "",
        "policy": "Bootstrap view shows the promised journey before TASK-PLAN.md exists. It is replaced by task-plan-derived state after planning.",
        "stages": stages,
    }


def phase(
    phase_id: str,
    title: str,
    status: str,
    description: str,
    subprocesses: list[str],
    artifacts: list[dict[str, str]],
    task_id: str,
) -> dict[str, Any]:
    return {
        "id": phase_id,
        "title": title,
        "technical_title": title,
        "status": status,
        "description": description,
        "subprocesses": [
            {
                "id": f"{phase_id}-sub-{index}",
                "title": item,
                "status": status,
                "description": "",
            }
            for index, item in enumerate(subprocesses, start=1)
        ],
        "artifacts": artifacts,
        "technical": {
            "task_id": task_id,
            "owner_role": "senior-ui-ux-orchestrator",
            "dependencies": [],
            "blocked_by": [],
            "required_approvals": [],
            "skill_routes": ["agent-progress-visualizer", "task-plan-v2-orchestrator"],
        },
    }


def build_state(
    project_root: Path,
    project_title: str,
    user_request: str,
    request_path: Path,
    log_path: Path,
    registry_path: Path | None,
    declared_journey: str | None,
) -> dict[str, Any]:
    journey = read_journey(registry_path, declared_journey)
    phases = [
        phase(
            "phase-00",
            "Запрос принят",
            "done",
            "Система получила задание и создала стартовые артефакты наблюдаемости.",
            ["Зафиксировать исходный запрос", "Создать локальную папку проекта", "Записать первый workflow log"],
            [
                {"label": "project-request.json", "path": str(request_path), "kind": "json", "evidence_state": "Ran"},
                {"label": "workflow-log.jsonl", "path": str(log_path), "kind": "json", "evidence_state": "Ran"},
            ],
            "BOOTSTRAP-REQUEST",
        ),
        phase(
            "phase-01",
            "Формируем task-plan",
            "running",
            "Система определяет полный путь работ, скиллы, user gates, проверки и артефакты.",
            ["Классифицировать тип проекта", "Определить полный пользовательский путь", "Подготовить canonical TASK-PLAN.md"],
            [],
            "BOOTSTRAP-PLAN",
        ),
        phase(
            "phase-02",
            "Подготовим подробные этапы",
            "planned",
            "После появления TASK-PLAN.md эта же страница обновится этапами, подпроцессами и точками выбора.",
            ["Сгенерировать progress-state.json из TASK-PLAN.md", "Перерисовать agent-progress-screen.html", "Проверить согласованность"],
            [],
            "BOOTSTRAP-DERIVED-VIEW",
        ),
        phase(
            "phase-03",
            "Начнем выполнение полного цикла",
            "planned",
            "После планирования система пойдет по research, semantic core, concept, design, Stitch/Figma/code, validation и launch gates.",
            ["Запустить первый утвержденный этап", "Логировать причины действий", "Обновлять экран после новых артефактов"],
            [],
            "BOOTSTRAP-FULL-JOURNEY",
        ),
    ]
    state: dict[str, Any] = {
        "schema_version": "2026-06-22-bootstrap",
        "generated_at": utc_now(),
        "source_of_truth": {
            "kind": "bootstrap-request",
            "path": str(request_path),
            "policy": "Bootstrap mode: project-request.json and workflow-log.jsonl are temporary startup sources. TASK-PLAN.md becomes canonical after planning; then progress-state.json and agent-progress-screen.html are regenerated from it.",
        },
        "project": {
            "title": project_title,
            "user_request": user_request,
            "audience_label": "Пользователь без обязательной технической подготовки",
            "privacy_mode": "local-first",
        },
        "summary": {"done": 1, "running": 1, "waiting_user": 0, "blocked": 0, "planned": 2, "failed": 0, "total": 4},
        "phases": phases,
        "user_gates": [],
        "activity_log": [
            {"time": "auto", "status": "done", "message": "Запрос принят и записан.", "technical_task_id": "BOOTSTRAP-REQUEST"},
            {"time": "auto", "status": "running", "message": "Формируется TASK-PLAN.md.", "technical_task_id": "BOOTSTRAP-PLAN"},
            {"time": "auto", "status": "planned", "message": "После плана экран обновится подробными этапами.", "technical_task_id": "BOOTSTRAP-DERIVED-VIEW"},
        ],
        "next_user_action": {
            "status": "wait",
            "label": "Система формирует план",
            "description": "Можно наблюдать за стартом. Следующее обновление появится после создания TASK-PLAN.md.",
        },
        "developer": {
            "enabled": False,
            "technical_routes": ["senior-ui-ux-orchestrator", "agent-progress-visualizer", "task-plan-v2-orchestrator"],
            "warnings": [],
        },
    }
    alignment = build_journey_alignment(journey, registry_path, declared_journey)
    if alignment:
        state["journey_alignment"] = alignment
    return state


def append_log(log_path: Path, project_root: Path, declared_journey: str | None, request_path: Path) -> None:
    event = {
        "timestamp": utc_now(),
        "project": str(project_root),
        "declared_journey": declared_journey or "unknown",
        "expected_stage": "bootstrap-request-accepted",
        "actual_state": "started",
        "decision": "continue",
        "reason_code": "bootstrap_progress_required",
        "evidence": [str(request_path)],
        "user_options": [],
        "owner_role": "agent-progress-visualizer",
        "message": "Запрос принят; bootstrap progress screen создается до TASK-PLAN.md.",
        "next_action": "Create canonical TASK-PLAN.md and regenerate progress screen from it.",
        "impact": "User sees immediate progress instead of waiting for planning to finish.",
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an immediate bootstrap progress screen before TASK-PLAN.md exists.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--project-title", required=True)
    parser.add_argument("--user-request", required=True)
    parser.add_argument("--declared-journey", default="new-premium-site")
    parser.add_argument("--journey-registry", type=Path)
    parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    project_root.mkdir(parents=True, exist_ok=True)
    (project_root / "reports").mkdir(exist_ok=True)
    (project_root / "feedback").mkdir(exist_ok=True)

    now = utc_now()
    request_path = project_root / "project-request.json"
    log_path = project_root / "workflow-log.jsonl"
    state_path = project_root / "progress-state.json"
    html_path = project_root / "agent-progress-screen.html"

    request = {
        "schema_version": "2026-06-22-bootstrap",
        "created_at": now,
        "project_root": str(project_root),
        "project_title": args.project_title,
        "user_request": args.user_request,
        "declared_journey": args.declared_journey,
        "status": "accepted",
        "privacy_mode": "local-first",
        "next_action": "Create canonical TASK-PLAN.md, then regenerate progress-state.json and agent-progress-screen.html from TASK-PLAN.md.",
    }
    request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_log(log_path, project_root, args.declared_journey, request_path)

    state = build_state(
        project_root=project_root,
        project_title=args.project_title,
        user_request=args.user_request,
        request_path=request_path,
        log_path=log_path,
        registry_path=args.journey_registry,
        declared_journey=args.declared_journey,
    )
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text("\n".join(line.rstrip() for line in render(state).splitlines()) + "\n", encoding="utf-8")

    print(f"Wrote {request_path}")
    print(f"Wrote {log_path}")
    print(f"Wrote {state_path}")
    print(f"Wrote {html_path}")
    if args.open_browser:
        uri = html_path.as_uri()
        opened = webbrowser.open(uri, new=2)
        if opened:
            print(f"Opened {uri}")
        else:
            print(f"WARNING: browser open requested but no browser accepted {uri}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
