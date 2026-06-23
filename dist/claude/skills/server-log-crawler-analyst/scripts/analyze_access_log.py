#!/usr/bin/env python3
"""Summarize access-log crawler evidence without exposing raw IP addresses."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOG_RE = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" (?P<status>\d{3}) (?P<bytes>\S+) "(?P<ref>[^"]*)" "(?P<ua>[^"]*)"'
)

SUSPICIOUS_PATTERNS = (
    "/.env",
    "/wp-admin",
    "/wp-login",
    "/cgi-bin",
    "../",
    "/etc/passwd",
    "/admin.php",
)


def classify_user_agent(ua: str, path: str) -> str:
    lower = ua.lower()
    path_lower = path.lower()
    if any(pattern in path_lower for pattern in SUSPICIOUS_PATTERNS):
        return "suspicious_probe"
    if any(token in lower for token in ("googlebot", "bingbot", "yandexbot", "duckduckbot")):
        return "known_search_bot_claim"
    if any(token in lower for token in ("gptbot", "oai-searchbot", "chatgpt-user", "claudebot", "claude-searchbot", "perplexitybot")):
        return "known_ai_bot_claim"
    if any(token in lower for token in ("bot", "crawl", "spider")):
        return "generic_bot"
    return "browser_like"


def redact_ip(ip: str) -> str:
    digest = hashlib.sha256(ip.encode("utf-8")).hexdigest()
    return f"iphash:{digest[:12]}"


def summarize(path: Path) -> dict[str, Any]:
    classes: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"requests": 0, "statuses": Counter(), "paths": Counter(), "ip_hashes": Counter()}
    )
    unmatched = 0
    total = 0

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        total += 1
        match = LOG_RE.match(line)
        if not match:
            unmatched += 1
            continue
        data = match.groupdict()
        cls = classify_user_agent(data["ua"], data["path"])
        record = classes[cls]
        record["requests"] += 1
        record["statuses"][data["status"]] += 1
        record["paths"][data["path"].split("?", 1)[0]] += 1
        record["ip_hashes"][redact_ip(data["ip"])] += 1

    serializable_classes = {}
    for cls, record in sorted(classes.items()):
        serializable_classes[cls] = {
            "requests": record["requests"],
            "statuses": dict(record["statuses"].most_common()),
            "top_paths": dict(record["paths"].most_common(10)),
            "redacted_ip_hashes": [item for item, _ in record["ip_hashes"].most_common(10)],
        }

    return {
        "artifact_type": "server_log_crawler_report",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": str(path),
        "privacy": {
            "raw_ips_in_report": False,
            "ip_redaction": "sha256 prefix, 12 hex chars",
        },
        "total_lines": total,
        "unmatched_lines": unmatched,
        "classes": serializable_classes,
        "claims_refused": [
            "ranking",
            "indexing",
            "assistant citation",
            "verified bot identity without provider verification",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize access-log crawler evidence with redacted IPs.")
    parser.add_argument("log_path")
    parser.add_argument("--report")
    args = parser.parse_args()

    report = summarize(Path(args.log_path))
    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "classes": report["classes"], "unmatched_lines": report["unmatched_lines"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
