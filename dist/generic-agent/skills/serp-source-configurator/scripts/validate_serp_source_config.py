#!/usr/bin/env python3
"""Validate a redacted SERP source configuration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VALID_STATUSES = {"Ran", "Skipped", "Planned", "Manual"}
DIRECT_MODES = {"direct", "direct-or-mega", "manual", "local"}
PROXY_MODES = {"proxy", "proxy-tag"}
ALLOWED_SECRET_REFS = {
    "",
    "redacted",
    "[REDACTED]",
    "env:AKE_API_KEY",
    "env:OPENSERP_API_KEY",
    "env:OPENSERP_BASE_URL",
}

SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|token|secret(?![_-]?scan)|password|passwd|pwd|cookie|authorization|proxy_url|credential)",
    re.IGNORECASE,
)
LONG_TOKEN_RE = re.compile(r"\b[A-Za-z0-9_-]{24,}\b")
CREDENTIAL_URL_RE = re.compile(r"[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@", re.IGNORECASE)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - exact message depends on JSON parser
        raise SystemExit(f"ERROR: cannot read JSON {path}: {exc}") from exc


def walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, f"{path}[{index}]")
    else:
        yield path, value


def is_allowed_secret_ref(value: str) -> bool:
    raw = value.strip()
    return raw in ALLOWED_SECRET_REFS or raw.startswith("env:")


def add(findings: list[dict[str, str]], level: str, path: str, message: str) -> None:
    findings.append({"level": level, "path": path, "message": message})


def validate_no_secrets(config: dict[str, Any], findings: list[dict[str, str]]) -> None:
    for path, value in walk(config):
        if not isinstance(value, str):
            continue
        lower_path = path.lower()
        if CREDENTIAL_URL_RE.search(value):
            add(findings, "P0", path, "credential-bearing URL is not allowed in config artifacts")
        if SECRET_KEY_RE.search(lower_path) and value and not is_allowed_secret_ref(value):
            add(findings, "P0", path, "secret-like field must contain only a redacted placeholder or env: reference")
        if LONG_TOKEN_RE.search(value) and not is_allowed_secret_ref(value):
            # URLs may contain long cache-busting path parts; only make token-like values fatal in secret-ish fields.
            level = "P0" if SECRET_KEY_RE.search(lower_path) else "P2"
            add(findings, level, path, "long token-like string found; verify it is not a secret")


def validate_shape(config: dict[str, Any], findings: list[dict[str, str]]) -> None:
    if config.get("schema") != "serp-source-config/v1":
        add(findings, "P1", "$.schema", "expected schema serp-source-config/v1")

    sources = config.get("sources")
    if not isinstance(sources, dict) or not sources:
        add(findings, "P0", "$.sources", "sources must be a non-empty object")
        return

    approval = config.get("approval") or {}
    budget = config.get("budget") or {}
    external_direct = bool(approval.get("external_direct"))
    proxy_approved = bool(approval.get("proxy"))
    paid_proxy_allowed = bool(budget.get("paid_proxy_allowed"))
    create_provider_resources = bool(budget.get("create_provider_resources_allowed"))

    enabled_count = 0
    proxy_enabled = []
    direct_enabled = []

    for name, source in sources.items():
        source_path = f"$.sources.{name}"
        if not isinstance(source, dict):
            add(findings, "P1", source_path, "source entry must be an object")
            continue
        enabled = bool(source.get("enabled"))
        status = source.get("status")
        mode = source.get("mode", "local" if name in {"manual_keywords", "existing_site"} else "")
        if status not in VALID_STATUSES:
            add(findings, "P1", f"{source_path}.status", f"status must be one of {sorted(VALID_STATUSES)}")
        if enabled:
            enabled_count += 1
            if mode in PROXY_MODES:
                proxy_enabled.append(name)
                if not source.get("proxy_tag"):
                    add(findings, "P1", f"{source_path}.proxy_tag", "proxy-enabled source needs proxy_tag")
            elif mode in DIRECT_MODES or name in {"manual_keywords", "existing_site"}:
                direct_enabled.append(name)
            else:
                add(findings, "P1", f"{source_path}.mode", "enabled source needs a known mode")

    if enabled_count == 0:
        add(findings, "P0", "$.sources", "at least one source must be enabled")

    if direct_enabled and any(name not in {"manual_keywords", "existing_site"} for name in direct_enabled) and not external_direct:
        add(findings, "P1", "$.approval.external_direct", "direct external engines are enabled without approval")

    if proxy_enabled:
        if not proxy_approved:
            add(findings, "P0", "$.approval.proxy", "proxy sources are enabled without proxy approval")
        if not paid_proxy_allowed:
            add(findings, "P0", "$.budget.paid_proxy_allowed", "proxy sources are enabled while paid_proxy_allowed is false")

    if create_provider_resources and not approval.get("provider_mutation"):
        add(findings, "P0", "$.approval.provider_mutation", "provider resource mutation budget is enabled without explicit approval")

    for key in ["max_queries", "max_results_per_query", "cache_ttl_seconds", "timeout_seconds"]:
        value = budget.get(key)
        if not isinstance(value, int) or value <= 0:
            add(findings, "P1", f"$.budget.{key}", "budget value must be a positive integer")

    if isinstance(budget.get("max_queries"), int) and budget["max_queries"] > 100:
        add(findings, "P2", "$.budget.max_queries", "large query budget; verify cost approval")

    handoff = config.get("handoff") or {}
    if handoff.get("next_skill") != "serp-keyword-harvester":
        add(findings, "P1", "$.handoff.next_skill", "next_skill should be serp-keyword-harvester")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--json", action="store_true", help="emit JSON findings")
    args = parser.parse_args()

    config = load_json(args.config)
    if not isinstance(config, dict):
        raise SystemExit("ERROR: config root must be an object")

    findings: list[dict[str, str]] = []
    validate_no_secrets(config, findings)
    validate_shape(config, findings)

    if args.json:
        print(json.dumps({"ok": not any(f["level"] in {"P0", "P1"} for f in findings), "findings": findings}, indent=2))
    else:
        if not findings:
            print("OK: SERP source config is valid")
        else:
            for finding in findings:
                print(f"{finding['level']} {finding['path']}: {finding['message']}")

    return 1 if any(finding["level"] in {"P0", "P1"} for finding in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
