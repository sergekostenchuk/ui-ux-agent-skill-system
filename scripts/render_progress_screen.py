#!/usr/bin/env python3
"""Render a static user-facing progress cockpit from progress-state.json."""

from __future__ import annotations

import argparse
import html
import json
import webbrowser
from pathlib import Path
from typing import Any


STATUS_LABELS = {
    "done": "Готово",
    "running": "Идет",
    "waiting_user": "Ждет вас",
    "blocked": "Блокер",
    "planned": "Впереди",
    "failed": "Ошибка",
    "skipped": "Пропущено",
}

JOURNEY_STATUS_LABELS = {
    "covered": "Покрыт",
    "partial": "Частично",
    "skipped_by_scope": "Пропущен по scope",
    "requires_user_approval": "Нужно решение",
    "needs_rework": "На доработку",
    "not_started": "Не начат",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def status_class(status: str) -> str:
    return status.replace("_", "-")


def render_artifacts(artifacts: list[dict[str, Any]]) -> str:
    if not artifacts:
        return '<p class="muted">Артефакты появятся после выполнения этапа.</p>'
    items = []
    for artifact in artifacts:
        path = artifact.get("path", "")
        label = artifact.get("label", path)
        items.append(
            f'<li><a href="{esc(path)}">{esc(label)}</a><span>{esc(artifact.get("evidence_state", "Planned"))}</span></li>'
        )
    return '<ul class="artifact-list">' + "".join(items) + "</ul>"


def render_gate(gate: dict[str, Any]) -> str:
    options = []
    for option in gate.get("options", []):
        options.append(
            f'''
            <label class="choice">
              <input type="radio" name="{esc(gate["id"])}" value="{esc(option["id"])}">
              <span>{esc(option["label"])}</span>
            </label>
            '''
        )
    return f'''
      <section class="gate" id="{esc(gate["id"])}">
        <div class="gate-head">
          <span class="gate-kicker">Нужно ваше решение</span>
          <h3>{esc(gate["title"])}</h3>
          <p>{esc(gate["description"])}</p>
        </div>
        <div class="choices">{"".join(options)}</div>
        <textarea aria-label="Комментарий к решению" placeholder="Комментарий, вопрос или уточнение"></textarea>
        <button type="button" onclick="copyGateFeedback('{esc(gate["id"])}')">Скопировать комментарий для агента</button>
        <p class="muted">Файл для фиксации: {esc(gate.get("feedback_artifact", ""))}</p>
      </section>
    '''


def render_journey_alignment(alignment: dict[str, Any] | None) -> str:
    if not alignment:
        return ""
    stages = []
    for stage in alignment.get("stages", []):
        status = stage.get("status", "not_started")
        evidence = stage.get("evidence", [])
        evidence_html = "".join(f"<li>{esc(item)}</li>" for item in evidence) or "<li>Пока нет артефактов.</li>"
        stages.append(
            f'''
            <article class="journey-stage {status_class(status)}" id="{esc(stage.get("id", ""))}">
              <header>
                <div>
                  <h3>{esc(stage.get("title", ""))}</h3>
                  <p>{esc(stage.get("message", ""))}</p>
                </div>
                <span>{esc(JOURNEY_STATUS_LABELS.get(status, status))}</span>
              </header>
              <dl>
                <dt>Решение</dt><dd>{esc(stage.get("decision", ""))}</dd>
                <dt>Причина</dt><dd>{esc(stage.get("reason_code", ""))}</dd>
                <dt>Следующее действие</dt><dd>{esc(stage.get("next_action", ""))}</dd>
                <dt>Скиллы</dt><dd>{esc(", ".join(stage.get("skills", [])) or "none")}</dd>
              </dl>
              <details>
                <summary>Доказательства и подпроцессы</summary>
                <p class="muted">Подпроцессов в registry: {esc(stage.get("subprocess_count", 0))}</p>
                <ul>{evidence_html}</ul>
              </details>
            </article>
            '''
        )
    return f'''
      <section class="journey-alignment" aria-label="Соответствие пользовательскому пути">
        <div class="section-head">
          <p class="eyebrow">Надсмотрщик логики</p>
          <h2>Соответствие обещанному пути</h2>
          <p>{esc(alignment.get("policy", ""))}</p>
          <p class="muted">Заявленный путь: {esc(alignment.get("title", alignment.get("declared_journey", "")))}</p>
        </div>
        <div class="journey-stages">{"".join(stages)}</div>
      </section>
    '''


def render_phase(phase: dict[str, Any], gate_by_id: dict[str, dict[str, Any]]) -> str:
    status = phase["status"]
    subprocesses = []
    for subprocess in phase.get("subprocesses", []):
        subprocesses.append(
            f'''
            <li class="subprocess {status_class(subprocess.get("status", status))}">
              <span></span>
              <div>
                <strong>{esc(subprocess.get("title", ""))}</strong>
                <p>{esc(subprocess.get("description", ""))}</p>
              </div>
            </li>
            '''
        )
    gate_html = ""
    gate_id = phase.get("user_gate_id")
    if gate_id and gate_id in gate_by_id:
        gate_html = render_gate(gate_by_id[gate_id])
    technical = phase.get("technical", {})
    return f'''
      <article class="phase {status_class(status)}" id="{esc(phase["id"])}">
        <div class="phase-marker"><span></span></div>
        <div class="phase-card">
          <header>
            <div>
              <p class="eyebrow">{esc(technical.get("task_id", ""))}</p>
              <h2>{esc(phase["title"])}</h2>
            </div>
            <span class="badge">{esc(STATUS_LABELS.get(status, status))}</span>
          </header>
          <p class="desc">{esc(phase.get("description", ""))}</p>
          <ul class="subprocess-list">{"".join(subprocesses)}</ul>
          {gate_html}
          <details class="developer">
            <summary>Технические детали</summary>
            <dl>
              <dt>Исходная задача</dt><dd>{esc(phase.get("technical_title", ""))}</dd>
              <dt>Owner</dt><dd>{esc(technical.get("owner_role", ""))}</dd>
              <dt>Dependencies</dt><dd>{esc(", ".join(technical.get("dependencies", [])) or "none")}</dd>
              <dt>Routes</dt><dd>{esc(", ".join(technical.get("skill_routes", [])) or "none")}</dd>
            </dl>
          </details>
          <div class="artifacts">
            <h3>Артефакты</h3>
            {render_artifacts(phase.get("artifacts", []))}
          </div>
        </div>
      </article>
    '''


def render(state: dict[str, Any]) -> str:
    summary = state["summary"]
    gate_by_id = {gate["id"]: gate for gate in state.get("user_gates", [])}
    phase_html = "\n".join(render_phase(phase, gate_by_id) for phase in state["phases"])
    journey_html = render_journey_alignment(state.get("journey_alignment"))
    log_html = "\n".join(
        f'<li class="{status_class(item["status"])}"><span>{esc(item["time"])}</span><p>{esc(item["message"])}</p></li>'
        for item in state.get("activity_log", [])
    )
    next_action = state["next_user_action"]
    source = state["source_of_truth"]
    state_json = json.dumps(state, ensure_ascii=False).replace("</", "<\\/")

    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(state["project"]["title"])} · Progress</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f3f0e7;
      --paper: #fffdf8;
      --ink: #182123;
      --muted: #687276;
      --line: #d9d1bf;
      --done: #28765a;
      --running: #0e7c86;
      --waiting: #b7791f;
      --blocked: #bd3b2e;
      --planned: #7d8588;
      --shadow: 0 20px 60px rgba(37, 34, 25, .12);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, Arial, sans-serif; background: var(--bg); color: var(--ink); }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0 56px; }}
    .hero {{ display: grid; grid-template-columns: 1.45fr .85fr; gap: 18px; align-items: stretch; margin-bottom: 22px; }}
    .panel, .phase-card, .activity, .source-note, .journey-alignment {{ background: var(--paper); border: 1px solid var(--line); border-radius: 14px; box-shadow: var(--shadow); }}
    .panel {{ padding: 24px; }}
    h1 {{ margin: 0 0 10px; font-size: clamp(30px, 4vw, 54px); line-height: 1; letter-spacing: 0; }}
    p {{ line-height: 1.55; }}
    .request {{ color: var(--muted); margin: 0; max-width: 75ch; }}
    .next {{ border-left: 5px solid var(--running); }}
    .next h2 {{ margin: 0 0 8px; font-size: 20px; }}
    .summary {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin: 16px 0 28px; }}
    .metric {{ background: rgba(255,255,255,.58); border: 1px solid var(--line); border-radius: 12px; padding: 14px; }}
    .metric strong {{ display: block; font-size: 26px; }}
    .metric span {{ display: block; color: var(--muted); font-size: 13px; margin-top: 4px; }}
    .source-note {{ padding: 14px 18px; margin-bottom: 24px; color: var(--muted); }}
    .journey-alignment {{ padding: 20px; margin-bottom: 24px; }}
    .section-head h2 {{ margin: 0 0 8px; font-size: 26px; }}
    .section-head p {{ margin: 0 0 8px; color: var(--muted); }}
    .journey-stages {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 16px; }}
    .journey-stage {{ border: 1px solid var(--line); border-radius: 12px; padding: 14px; background: #f8f5ed; }}
    .journey-stage header {{ display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: start; }}
    .journey-stage h3 {{ margin: 0 0 5px; font-size: 17px; }}
    .journey-stage header p {{ margin: 0; color: var(--muted); font-size: 14px; }}
    .journey-stage header span {{ border-radius: 999px; padding: 6px 9px; background: #fff; border: 1px solid var(--line); font-size: 12px; white-space: nowrap; }}
    .journey-stage.covered {{ border-color: rgba(40,118,90,.45); }}
    .journey-stage.partial {{ border-color: rgba(14,124,134,.42); }}
    .journey-stage.skipped-by-scope {{ border-color: rgba(125,133,136,.5); }}
    .journey-stage.requires-user-approval {{ border-color: rgba(183,121,31,.55); background: #fff7e8; }}
    .journey-stage.needs-rework, .journey-stage.not-started {{ border-color: rgba(189,59,46,.35); }}
    .journey-stage dl {{ display: grid; grid-template-columns: 120px 1fr; gap: 6px 10px; margin: 12px 0; font-size: 14px; }}
    .journey-stage dt {{ font-weight: 700; }}
    .journey-stage dd {{ margin: 0; color: var(--muted); }}
    .journey-stage details {{ color: var(--muted); font-size: 14px; }}
    .timeline {{ position: relative; }}
    .phase {{ display: grid; grid-template-columns: 34px 1fr; gap: 14px; margin-bottom: 16px; }}
    .phase-marker {{ display: flex; justify-content: center; }}
    .phase-marker span {{ width: 18px; height: 18px; border-radius: 50%; margin-top: 22px; background: var(--planned); box-shadow: 0 0 0 6px rgba(125,133,136,.16); }}
    .phase.done .phase-marker span {{ background: var(--done); box-shadow: 0 0 0 6px rgba(40,118,90,.16); }}
    .phase.running .phase-marker span {{ background: var(--running); box-shadow: 0 0 0 6px rgba(14,124,134,.16); animation: pulse 1.4s infinite; }}
    .phase.waiting-user .phase-marker span {{ background: var(--waiting); box-shadow: 0 0 0 6px rgba(183,121,31,.18); animation: pulse 1.4s infinite; }}
    .phase.blocked .phase-marker span, .phase.failed .phase-marker span {{ background: var(--blocked); box-shadow: 0 0 0 6px rgba(189,59,46,.16); }}
    .phase-card {{ padding: 20px; }}
    .phase-card header {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; }}
    .eyebrow {{ margin: 0 0 4px; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    .phase-card h2 {{ margin: 0; font-size: 23px; letter-spacing: 0; }}
    .badge {{ flex: 0 0 auto; border: 1px solid var(--line); border-radius: 999px; padding: 7px 10px; font-size: 13px; background: #fff; }}
    .desc {{ margin: 12px 0 0; color: var(--muted); }}
    .subprocess-list {{ list-style: none; padding: 0; margin: 18px 0; display: grid; gap: 8px; }}
    .subprocess {{ display: grid; grid-template-columns: 12px 1fr; gap: 10px; align-items: start; padding: 10px; background: #f8f5ed; border-radius: 10px; }}
    .subprocess > span {{ width: 9px; height: 9px; border-radius: 50%; background: var(--planned); margin-top: 7px; }}
    .subprocess.done > span {{ background: var(--done); }}
    .subprocess.running > span {{ background: var(--running); }}
    .subprocess.waiting-user > span {{ background: var(--waiting); }}
    .subprocess p {{ margin: 2px 0 0; color: var(--muted); font-size: 14px; }}
    .gate {{ margin: 18px 0; padding: 16px; border: 1px solid rgba(183,121,31,.35); border-radius: 12px; background: #fff7e8; }}
    .gate-kicker {{ display: inline-block; color: var(--waiting); font-size: 13px; font-weight: 700; margin-bottom: 4px; }}
    .gate h3 {{ margin: 0; }}
    .choices {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 14px 0; }}
    .choice {{ display: inline-flex; gap: 8px; align-items: center; border: 1px solid var(--line); border-radius: 999px; padding: 9px 12px; background: #fff; }}
    textarea {{ display: block; width: 100%; min-height: 88px; resize: vertical; border: 1px solid var(--line); border-radius: 10px; padding: 12px; font: inherit; }}
    button {{ margin-top: 10px; border: 0; border-radius: 10px; padding: 11px 14px; background: #1c706c; color: #fff; font: inherit; cursor: pointer; }}
    .developer {{ margin: 14px 0; color: var(--muted); }}
    .developer dl {{ display: grid; grid-template-columns: 140px 1fr; gap: 8px 14px; }}
    .developer dt {{ font-weight: 700; color: var(--ink); }}
    .artifacts h3 {{ margin-bottom: 8px; font-size: 16px; }}
    .artifact-list {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }}
    .artifact-list li {{ display: flex; justify-content: space-between; gap: 14px; padding: 8px 0; border-top: 1px solid var(--line); }}
    a {{ color: #0b666a; }}
    .muted {{ color: var(--muted); }}
    .activity {{ padding: 18px; margin-top: 22px; }}
    .activity h2 {{ margin: 0 0 12px; }}
    .activity ul {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }}
    .activity li {{ display: grid; grid-template-columns: 72px 1fr; gap: 10px; color: var(--muted); }}
    .activity p {{ margin: 0; }}
    @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.12); }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; scroll-behavior: auto !important; }} }}
    @media (max-width: 820px) {{
      main {{ width: min(100% - 20px, 720px); padding-top: 18px; }}
      .hero {{ grid-template-columns: 1fr; }}
      .summary {{ grid-template-columns: repeat(2, 1fr); }}
      .journey-stages {{ grid-template-columns: 1fr; }}
      .phase {{ grid-template-columns: 22px 1fr; gap: 10px; }}
      .phase-card header {{ flex-direction: column; }}
      .developer dl {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <div class="panel">
      <p class="eyebrow">Экран прогресса</p>
      <h1>{esc(state["project"]["title"])}</h1>
      <p class="request">{esc(state["project"]["user_request"])}</p>
    </div>
    <aside class="panel next">
      <p class="eyebrow">Что сейчас</p>
      <h2>{esc(next_action["label"])}</h2>
      <p>{esc(next_action["description"])}</p>
    </aside>
  </section>
  <section class="summary" aria-label="Сводка статусов">
    <div class="metric"><strong>{summary["done"]}</strong><span>готово</span></div>
    <div class="metric"><strong>{summary["running"]}</strong><span>идет</span></div>
    <div class="metric"><strong>{summary["waiting_user"]}</strong><span>ждет вас</span></div>
    <div class="metric"><strong>{summary["blocked"]}</strong><span>блокеры</span></div>
    <div class="metric"><strong>{summary["planned"]}</strong><span>впереди</span></div>
    <div class="metric"><strong>{summary["total"]}</strong><span>всего</span></div>
  </section>
  <div class="source-note">
    Источник правды: <a href="{esc(source["path"])}">TASK-PLAN.md</a>. {esc(source["policy"])}
  </div>
  {journey_html}
  <section class="timeline" aria-label="Этапы работы">
    {phase_html}
  </section>
  <section class="activity">
    <h2>Журнал действий</h2>
    <ul>{log_html}</ul>
  </section>
</main>
<script>
const PROGRESS_STATE = {state_json};
function copyGateFeedback(gateId) {{
  const gate = document.getElementById(gateId);
  const checked = gate.querySelector('input[type="radio"]:checked');
  const textarea = gate.querySelector('textarea');
  const payload = {{
    gate_id: gateId,
    selected_option: checked ? checked.value : "",
    comment: textarea ? textarea.value : "",
    target_artifact: PROGRESS_STATE.user_gates.find((item) => item.id === gateId)?.feedback_artifact || "",
    source: "agent-progress-screen.html"
  }};
  navigator.clipboard?.writeText(JSON.stringify(payload, null, 2));
}}
</script>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Render agent-progress-screen.html from progress-state.json.")
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the rendered HTML file in the default browser after writing it. Use for init/user-facing runs.",
    )
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    output = "\n".join(line.rstrip() for line in render(state).splitlines()) + "\n"
    args.out.write_text(output, encoding="utf-8")
    print(f"Wrote {args.out}")
    if args.open_browser:
        uri = args.out.resolve().as_uri()
        opened = webbrowser.open(uri, new=2)
        if opened:
            print(f"Opened {uri}")
        else:
            print(f"WARNING: browser open requested but no browser accepted {uri}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
