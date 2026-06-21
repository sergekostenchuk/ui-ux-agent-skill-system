#!/usr/bin/env python3
"""Run deterministic UI/UX skill system evals.

The first eval layer is intentionally local and deterministic. It validates
eval file schemas and checks route-oriented cases against the bundled prompt
classifier. It does not call an LLM judge.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load_classifier(root: Path):
    sys.dont_write_bytecode = True
    path = root / "core" / "skills" / "senior-ui-ux-orchestrator" / "scripts" / "classify_product_type.py"
    spec = importlib.util.spec_from_file_location("uiux_classifier", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load classifier: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def eval_files(root: Path, explicit: list[str]) -> list[Path]:
    if explicit:
        return [Path(item).resolve() for item in explicit]
    files = [root / "evals" / "evals.json"]
    files.extend(sorted((root / "core" / "skills").glob("*/evals/evals.json")))
    return [path for path in files if path.is_file()]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def get_cases(data: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    if "cases" in data:
        cases = data["cases"]
    elif "evals" in data:
        cases = data["evals"]
    else:
        raise ValueError(f"{path}: missing `cases` or `evals`")
    if not isinstance(cases, list):
        raise ValueError(f"{path}: cases/evals must be a list")
    return cases


def expected_matches(expected: str, best: dict[str, Any]) -> bool:
    route_id = str(best.get("route_id", ""))
    skill = str(best.get("skill", ""))
    mode = str(best.get("mode", ""))
    return expected in {route_id, skill, f"{skill}:{mode}"}


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def run(root: Path, files: list[Path]) -> dict[str, Any]:
    classifier = load_classifier(root)
    results: list[dict[str, Any]] = []
    summary = {
        "files": 0,
        "cases": 0,
        "route_checked": 0,
        "passed": 0,
        "failed": 0,
        "skipped_route": 0,
    }

    for path in files:
        summary["files"] += 1
        try:
            data = load_json(path)
            cases = get_cases(data, path)
        except Exception as exc:  # noqa: BLE001
            summary["failed"] += 1
            results.append({"file": display_path(path, root), "ok": False, "error": str(exc)})
            continue

        for index, case in enumerate(cases):
            summary["cases"] += 1
            case_id = str(case.get("id", index))
            prompt = case.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                summary["failed"] += 1
                results.append({"file": display_path(path, root), "case_id": case_id, "ok": False, "error": "missing prompt"})
                continue

            expected_route = case.get("expected_route")
            if not expected_route:
                summary["skipped_route"] += 1
                results.append({"file": display_path(path, root), "case_id": case_id, "ok": True, "route_check": "skipped"})
                continue

            ranked = classifier.score(prompt)
            best = ranked[0]
            ok = expected_matches(str(expected_route), best)
            summary["route_checked"] += 1
            summary["passed" if ok else "failed"] += 1
            results.append(
                {
                    "file": display_path(path, root),
                    "case_id": case_id,
                    "ok": ok,
                    "expected_route": expected_route,
                    "actual_route_id": best.get("route_id"),
                    "actual_skill": best.get("skill"),
                    "actual_mode": best.get("mode"),
                    "score": best.get("score"),
                    "matched_signals": best.get("matched_signals", []),
                }
            )

    return {"ok": summary["failed"] == 0, "summary": summary, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic UI/UX skill system evals.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument("--out", default="reports/eval-results.json", help="Output JSON report path.")
    parser.add_argument("--eval-file", action="append", default=[], help="Specific eval file to run; repeatable.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = eval_files(root, args.eval_file)
    result = run(root, files)

    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for item in result["results"]:
        if not item.get("ok"):
            print(f"FAIL: {item}")
    if result["ok"]:
        print(
            "PASS: evals passed "
            f"files={result['summary']['files']} cases={result['summary']['cases']} "
            f"route_checked={result['summary']['route_checked']} skipped_route={result['summary']['skipped_route']}"
        )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
