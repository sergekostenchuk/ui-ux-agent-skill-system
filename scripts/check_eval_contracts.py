#!/usr/bin/env python3
"""Validate deterministic eval contract coverage.

This is not an LLM judge. It enforces that top-level eval prompts have
acceptance constraints that can later be used by stronger artifact/UI evals.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TERMS = {
    "accessibility": ("accessibility", "accessible", "inaccessible"),
    "validation": ("validation", "validate", "evidence", "browser"),
    "privacy": ("secret", "key", "private", "approval"),
    "truthful_content": ("truthful", "visible facts", "crawlable", "hidden SEO"),
}


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError(f"{path}: missing top-level `cases` list")
    return cases


def terms_text(cases: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for case in cases:
        chunks.append(str(case.get("prompt", "")))
        chunks.extend(str(item) for item in case.get("must_have", []))
        chunks.extend(str(item) for item in case.get("must_not_have", []))
    return "\n".join(chunks).lower()


def validate(path: Path) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    cases = load_cases(path)

    for index, case in enumerate(cases):
        case_id = str(case.get("id", index))
        if not case.get("expected_route"):
            errors.append(f"{case_id}: missing expected_route")
        if not isinstance(case.get("must_have"), list) or not case["must_have"]:
            errors.append(f"{case_id}: missing non-empty must_have list")
        if not isinstance(case.get("must_not_have"), list) or not case["must_not_have"]:
            errors.append(f"{case_id}: missing non-empty must_not_have list")

    text = terms_text(cases)
    covered = {
        dimension: any(term.lower() in text for term in terms)
        for dimension, terms in REQUIRED_TERMS.items()
    }
    for dimension, ok in covered.items():
        if not ok:
            errors.append(f"missing top-level eval coverage for {dimension}")

    return errors, {"cases": len(cases), "coverage": covered}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate top-level eval contract coverage.")
    parser.add_argument("eval_file", nargs="?", default="evals/evals.json")
    parser.add_argument("--out", default="reports/eval-contract-results.json")
    args = parser.parse_args()

    root = Path.cwd()
    eval_file = Path(args.eval_file)
    if not eval_file.is_absolute():
        eval_file = root / eval_file
    errors, summary = validate(eval_file)

    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"ok": not errors, "summary": summary, "errors": errors}, indent=2) + "\n",
        encoding="utf-8",
    )

    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print(
            "PASS: eval contracts passed "
            f"cases={summary['cases']} coverage={','.join(sorted(summary['coverage']))}"
        )
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
