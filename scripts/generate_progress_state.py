#!/usr/bin/env python3
"""Generate a user-facing progress-state.json from a normalized TASK-PLAN v2 file."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATUS_MAP = {
    "done": "done",
    "approved": "done",
    "needs_review": "waiting_user",
    "in_progress": "running",
    "ready": "planned",
    "draft": "planned",
    "blocked": "blocked",
    "dropped": "skipped",
    "failed": "failed",
}

CUSTOMER_TITLE_HINTS = [
    ("Freeze progress screen contract", "Фиксируем правила экрана прогресса"),
    ("Define `progress-state.json` schema", "Описываем данные для экрана прогресса"),
    ("Create `agent-progress-visualizer` skill", "Добавляем скилл экрана прогресса"),
    ("Wire progress lifecycle", "Подключаем экран к главному оркестратору"),
    ("Add task-plan to progress-state", "Собираем состояние из task-plan"),
    ("Convert prototype screen", "Превращаем прототип в рабочую страницу"),
    ("Integrate user gates", "Подключаем комментарии и решения пользователя"),
    ("Add wiki capture", "Сохраняем важные решения в wiki"),
    ("Validate progress dashboard", "Проверяем согласованность и безопасность"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_scalar(block: str, key: str, default: str = "") -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", block, re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_list(block: str, key: str) -> list[str]:
    marker = re.search(rf"^{re.escape(key)}:\s*$", block, re.MULTILINE)
    if not marker:
        inline = re.search(rf"^{re.escape(key)}:\s*\[(.*?)\]\s*$", block, re.MULTILINE)
        if inline:
            raw = inline.group(1).strip()
            return [item.strip().strip("'\"") for item in raw.split(",") if item.strip()]
        return []

    values: list[str] = []
    lines = block[marker.end() :].splitlines()
    for line in lines:
        if line.startswith("- "):
            values.append(line[2:].strip())
            continue
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            break
        if values and line.startswith("  "):
            values[-1] += " " + line.strip()
    return values


def parse_task_blocks(text: str, task_prefix: str) -> list[dict[str, Any]]:
    pattern = re.compile(r"^#### TASK\s+([A-Z0-9-]+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    tasks: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        task_id = match.group(1)
        if task_prefix and not task_id.startswith(task_prefix):
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        status = parse_scalar(block, "status", "draft")
        title = parse_scalar(block, "title", task_id)
        tasks.append(
            {
                "task_id": task_id,
                "title": title,
                "status": status,
                "owner_role": parse_scalar(block, "owner_role", "planner"),
                "dependencies": parse_list(block, "dependencies"),
                "blocked_by": parse_list(block, "blocked_by"),
                "required_approvals": parse_list(block, "required_approvals"),
                "scope_in": parse_list(block, "scope_in"),
                "artifact_locations": parse_list(block, "artifact_locations"),
                "expected_artifacts": parse_list(block, "expected_artifacts"),
                "commands_run": parse_list(block, "commands_run"),
                "raw": block,
            }
        )
    return tasks


def customer_title(title: str) -> str:
    for needle, value in CUSTOMER_TITLE_HINTS:
        if needle.lower() in title.lower():
            return value
    clean = title.replace("`", "")
    return clean[:1].upper() + clean[1:]


def description_for(task: dict[str, Any]) -> str:
    status = STATUS_MAP.get(task["status"], "planned")
    if status == "done":
        return "Этот этап завершен и зафиксирован в артефактах проекта."
    if status == "running":
        return "Система сейчас работает над этим этапом."
    if status == "waiting_user":
        return "Этап ждет просмотра, выбора или подтверждения."
    if status == "blocked":
        return "Этап остановлен до устранения блокера."
    return "Этот этап запланирован и будет выполнен после зависимостей."


def artifact_kind(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".html":
        return "html"
    if suffix == ".json":
        return "json"
    if suffix in {".md", ".txt"} and "report" in path.lower():
        return "report"
    if suffix == ".md":
        return "task-plan" if "TASK-PLAN" in path else "wiki"
    return "other"


def phase_from_task(task: dict[str, Any], index: int) -> dict[str, Any]:
    mapped_status = STATUS_MAP.get(task["status"], "planned")
    subprocesses = []
    for sub_index, item in enumerate(task["scope_in"][:6], start=1):
        subprocesses.append(
            {
                "id": f"{task['task_id'].lower()}-sub-{sub_index}",
                "title": item.strip("`"),
                "status": mapped_status,
                "description": "",
            }
        )
    if not subprocesses:
        subprocesses.append(
            {
                "id": f"{task['task_id'].lower()}-sub-1",
                "title": "Подготовить и проверить артефакты этапа",
                "status": mapped_status,
                "description": "",
            }
        )

    artifacts = []
    for path in list(dict.fromkeys(task["artifact_locations"] + task["expected_artifacts"])):
        evidence_state = "Ran" if task["commands_run"] or task["status"] == "done" else "Planned"
        artifacts.append(
            {
                "label": Path(path).name or path,
                "path": path,
                "kind": artifact_kind(path),
                "evidence_state": evidence_state,
            }
        )

    skill_routes = sorted(
        set(
            name
            for name in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", task["raw"])
            if name not in {"progress-state"}
        )
    )

    return {
        "id": f"phase-{index:02d}",
        "title": customer_title(task["title"]),
        "technical_title": task["title"],
        "status": mapped_status,
        "description": description_for(task),
        "subprocesses": subprocesses,
        "artifacts": artifacts,
        "technical": {
            "task_id": task["task_id"],
            "owner_role": task["owner_role"],
            "dependencies": task["dependencies"],
            "blocked_by": task["blocked_by"],
            "required_approvals": task["required_approvals"],
            "skill_routes": skill_routes,
        },
    }


def build_user_gates(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gates = []
    for phase in phases:
        approvals = phase["technical"].get("required_approvals", [])
        if phase["status"] != "waiting_user" and not any("user" in item for item in approvals):
            continue
        gate = {
            "id": f"gate-{phase['technical']['task_id'].lower()}",
            "phase_id": phase["id"],
            "type": "review",
            "status": "open",
            "title": f"Нужно решение по этапу: {phase['title']}",
            "description": "Оставьте комментарий или подтвердите, что этап можно продолжать.",
            "options": [
                {"id": "approve", "label": "Принять"},
                {"id": "revise", "label": "Нужны правки"},
                {"id": "question", "label": "Есть вопрос"},
            ],
            "feedback_artifact": "feedback/progress-feedback-register.json",
        }
        phase["user_gate_id"] = gate["id"]
        gates.append(gate)
    return gates


def build_summary(phases: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"done": 0, "running": 0, "waiting_user": 0, "blocked": 0, "planned": 0, "failed": 0}
    for phase in phases:
        status = phase["status"]
        if status == "skipped":
            continue
        counts[status] = counts.get(status, 0) + 1
    counts["total"] = len(phases)
    return counts


def build_activity_log(phases: list[dict[str, Any]]) -> list[dict[str, str]]:
    log = []
    for phase in phases:
        task_id = phase["technical"]["task_id"]
        status = phase["status"]
        if status == "done":
            message = f"Готово: {phase['title']}."
        elif status == "running":
            message = f"Идет работа: {phase['title']}."
        elif status == "waiting_user":
            message = f"Ожидается решение пользователя: {phase['title']}."
        elif status == "blocked":
            message = f"Есть блокер: {phase['title']}."
        else:
            message = f"Запланировано: {phase['title']}."
        log.append({"time": "auto", "status": status, "message": message, "technical_task_id": task_id})
    return log


def load_journey(registry_path: Path, journey_id: str) -> dict[str, Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for journey in registry.get("journeys", []):
        if journey.get("id") == journey_id:
            return journey
    raise SystemExit(f"Unknown journey {journey_id!r} in {registry_path}")


def stage_match_pattern(title: str) -> str:
    lower = title.lower()
    if "intake" in lower:
        return r"intake|scope|brief|progress|wiki|task-plan"
    if "search" in lower or "semantic" in lower:
        return r"serp|semantic|keyword|search"
    if "concept" in lower:
        return r"concept|prototype|journey|offer"
    if "three" in lower:
        return r"three\s+(?:distinct\s+)?(?:design|direction|variant)|3\s*(?:design|direction|variant)|DESIGN-V[0-9]"
    if "ai design" in lower:
        return r"stitch|pencil|figma|ai design"
    if "build" in lower:
        return r"build|implementation|content|asset|html|site"
    if "measurement" in lower:
        return r"analytics|assistant|paid|measurement|utm"
    if "launch" in lower:
        return r"launch|deploy|dns|ssl|webmaster|hosting"
    if "existing" in lower:
        return r"existing|audit|crawl|screenshot"
    if "migration" in lower:
        return r"migration|redirect|url|canonical"
    if "admin" in lower:
        return r"admin|cms|operator|workflow"
    if "validation" in lower:
        return r"validation|audit|schema|accessibility|performance"
    return re.escape(title.split()[0]) if title.split() else r"$^"


def journey_status_for_stage(title: str, task_text: str, phases: list[dict[str, Any]]) -> dict[str, Any]:
    lower = title.lower()
    combined = task_text + "\n" + "\n".join(
        " ".join(
            [
                phase.get("title", ""),
                phase.get("technical_title", ""),
                " ".join(phase.get("technical", {}).get("skill_routes", [])),
            ]
        )
        for phase in phases
    )
    evidence: list[str] = []
    if re.search(stage_match_pattern(title), combined, re.IGNORECASE):
        evidence.append("TASK-PLAN.md")

    if "search" in lower or "semantic" in lower:
        if re.search(r"external|proxy|serp|opense?rp", combined, re.IGNORECASE):
            return {
                "status": "requires_user_approval",
                "decision": "pause_for_user",
                "reason_code": "user_not_approved_external",
                "evidence": evidence or ["TASK-PLAN.md"],
                "message": "Поисковые данные требуют разрешения на внешний сбор или подтверждения локального режима.",
                "next_action": "Подтвердить SERP/OpenSERP/proxy-сбор или оставить локальный режим с пометкой гипотез.",
            }
    if "three" in lower and not evidence:
        return {
            "status": "skipped_by_scope",
            "decision": "skip_with_reason",
            "reason_code": "out_of_scope_demo",
            "evidence": [],
            "message": "Три дизайн-направления не запускались в текущем локальном демо.",
            "next_action": "Запустить трехвариантный дизайн отдельным этапом, если нужен полный путь.",
        }
    if "ai design" in lower:
        return {
            "status": "requires_user_approval",
            "decision": "pause_for_user",
            "reason_code": "user_not_approved_external",
            "evidence": evidence,
            "message": "Stitch/Pencil/Figma exploration требует отдельного разрешения и брифа.",
            "next_action": "Подтвердить AI/canvas exploration или пропустить с понятным влиянием.",
        }
    if "measurement" in lower:
        return {
            "status": "skipped_by_scope",
            "decision": "skip_with_reason",
            "reason_code": "out_of_scope_demo",
            "evidence": evidence or ["TASK-PLAN.md"],
            "message": "Аналитика, реклама и AI-ассистент вынесены за рамки текущего локального демо.",
            "next_action": "Создать отдельный этап, если нужен полный запуск.",
        }
    if "launch" in lower:
        return {
            "status": "requires_user_approval",
            "decision": "pause_for_user",
            "reason_code": "missing_user_data",
            "evidence": evidence or ["TASK-PLAN.md"],
            "message": "Запуск требует домена, хостинга, контактов и явного production approval.",
            "next_action": "Предоставить production-данные или оставить проект локальным демо.",
        }

    if evidence:
        return {
            "status": "covered",
            "decision": "continue",
            "reason_code": "covered_by_evidence",
            "evidence": evidence,
            "message": "Этап отражен в текущем task-plan или артефактах.",
            "next_action": "Продолжать по плану.",
        }
    return {
        "status": "not_started",
        "decision": "return_to_rework",
        "reason_code": "missing_evidence",
        "evidence": [],
        "message": "В текущих артефактах нет достаточного подтверждения этого этапа.",
        "next_action": "Добавить задачу, доказательство или зафиксировать обоснованный пропуск.",
    }


def build_journey_alignment(
    task_plan: Path,
    phases: list[dict[str, Any]],
    registry_path: Path | None,
    journey_id: str | None,
) -> dict[str, Any] | None:
    if not registry_path or not journey_id:
        return None
    journey = load_journey(registry_path, journey_id)
    task_text = read_text(task_plan)
    stages = []
    for stage in journey.get("stages", []):
        decision = journey_status_for_stage(stage.get("title", ""), task_text, phases)
        stages.append(
            {
                "id": stage["id"],
                "title": stage["title"],
                "status": decision["status"],
                "decision": decision["decision"],
                "reason_code": decision["reason_code"],
                "message": decision["message"],
                "next_action": decision["next_action"],
                "evidence": decision["evidence"],
                "skills": stage.get("skills", []),
                "subprocess_count": len(stage.get("subprocesses", [])),
            }
        )
    return {
        "declared_journey": journey_id,
        "title": journey.get("title", journey_id),
        "registry_path": str(registry_path.resolve()),
        "policy": "Shows how the current project artifacts align with the declared user journey; it does not replace TASK-PLAN.md.",
        "stages": stages,
    }


def next_action(summary: dict[str, int], gates: list[dict[str, Any]]) -> dict[str, str]:
    if gates:
        gate = gates[0]
        return {
            "status": "review",
            "label": gate["title"],
            "description": gate["description"],
            "gate_id": gate["id"],
        }
    if summary["blocked"]:
        return {"status": "provide_data", "label": "Есть блокер", "description": "Нужно устранить блокер в task-plan."}
    if summary["running"]:
        return {"status": "wait", "label": "Система работает", "description": "Сейчас можно просто наблюдать за прогрессом."}
    if summary["planned"]:
        return {"status": "wait", "label": "Следующие этапы запланированы", "description": "Система начнет их после зависимостей."}
    return {"status": "none", "label": "Действий от пользователя нет", "description": "Все этапы в текущем наборе завершены."}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate progress-state.json from TASK-PLAN.md.")
    parser.add_argument("--task-plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--task-prefix", default="UIUX-PROGRESS")
    parser.add_argument("--project-title", default="UI/UX Agent Skill System")
    parser.add_argument(
        "--user-request",
        default="Сделать понятный пользовательский экран прогресса для работы senior-ui-ux-orchestrator.",
    )
    parser.add_argument("--journey-registry", type=Path)
    parser.add_argument("--declared-journey")
    args = parser.parse_args()

    task_plan = args.task_plan.resolve()
    text = read_text(task_plan)
    tasks = parse_task_blocks(text, args.task_prefix)
    if not tasks:
        raise SystemExit(f"No tasks found for prefix {args.task_prefix!r}")

    phases = [phase_from_task(task, index) for index, task in enumerate(tasks, start=1)]
    gates = build_user_gates(phases)
    summary = build_summary(phases)
    journey_alignment = build_journey_alignment(
        task_plan,
        phases,
        args.journey_registry,
        args.declared_journey,
    )
    state = {
        "schema_version": "2026-06-22",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_of_truth": {
            "kind": "task-plan-v2",
            "path": str(task_plan),
            "policy": "TASK-PLAN.md is canonical; progress-state.json and agent-progress-screen.html are derived.",
        },
        "project": {
            "title": args.project_title,
            "user_request": args.user_request,
            "audience_label": "Пользователь без обязательной технической подготовки",
            "privacy_mode": "local-first",
        },
        "summary": summary,
        "phases": phases,
        "user_gates": gates,
        "activity_log": build_activity_log(phases),
        "next_user_action": next_action(summary, gates),
        "developer": {
            "enabled": False,
            "technical_routes": sorted({route for phase in phases for route in phase["technical"].get("skill_routes", [])}),
            "warnings": [],
        },
    }
    if journey_alignment:
        state["journey_alignment"] = journey_alignment

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
