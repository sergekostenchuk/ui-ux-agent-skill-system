#!/usr/bin/env python3
"""Small deterministic SEO/LLM HTML regression checker."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


USER_AGENT = "seo-regression-validator/0.1"


def utc_now() -> str:
    fixed = os.environ.get("SEO_REGRESSION_TIMESTAMP")
    if fixed:
        return fixed
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_target(target: str) -> tuple[str, dict[str, Any]]:
    if target.startswith(("http://", "https://")):
        req = Request(target, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=20) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace"), {
                "method": "http",
                "status_code": response.status,
                "content_type": response.headers.get("content-type", "unknown"),
                "user_agent": USER_AGENT,
            }
    path = Path(target)
    return path.read_text(encoding="utf-8", errors="replace"), {
        "method": "file",
        "status_code": "file",
        "content_type": "text/html",
        "user_agent": "none",
    }


def first_match(pattern: str, html: str, flags: int = re.I | re.S) -> str | None:
    match = re.search(pattern, html, flags)
    return unescape(match.group(1).strip()) if match else None


def all_matches(pattern: str, html: str, flags: int = re.I | re.S) -> list[str]:
    return [unescape(m.strip()) for m in re.findall(pattern, html, flags)]


def extract_jsonld(html: str) -> tuple[list[Any], list[str]]:
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, flags=re.I | re.S)
    parsed: list[Any] = []
    errors: list[str] = []
    for idx, block in enumerate(blocks, 1):
        text = unescape(block.strip())
        try:
            parsed.append(json.loads(text))
        except json.JSONDecodeError as exc:
            errors.append(f"jsonld block {idx}: {exc}")
    return parsed, errors


def schema_types(node: Any) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        value = node.get("@type")
        if isinstance(value, str):
            found.append(value)
        elif isinstance(value, list):
            found.extend([v for v in value if isinstance(v, str)])
        graph = node.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                found.extend(schema_types(item))
    elif isinstance(node, list):
        for item in node:
            found.extend(schema_types(item))
    return found


def find_newsarticle_nodes(node: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if isinstance(node, dict):
        value = node.get("@type")
        values = value if isinstance(value, list) else [value]
        if "NewsArticle" in values:
            nodes.append(node)
        graph = node.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                nodes.extend(find_newsarticle_nodes(item))
    elif isinstance(node, list):
        for item in node:
            nodes.extend(find_newsarticle_nodes(item))
    return nodes


def image_present(value: Any) -> bool:
    if not value:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(image_present(item) for item in value)
    if isinstance(value, dict):
        return bool(value.get("url") or value.get("contentUrl"))
    return False


def add_issue(report: dict[str, Any], severity: str, code: str, message: str) -> None:
    report["issues"].append({"severity": severity, "code": code, "message": message})


def audit_html(target: str, html: str, meta: dict[str, Any]) -> dict[str, Any]:
    report: dict[str, Any] = {
        "artifact_type": "seo_regression_report",
        "generated_at": utc_now(),
        "target": target,
        "fetch": meta,
        "status": "pass",
        "issues": [],
        "observed": {},
    }

    title = first_match(r"<title[^>]*>(.*?)</title>", html)
    description = first_match(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html)
    canonicals = all_matches(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html)
    hreflangs = all_matches(r'<link[^>]+rel=["\']alternate["\'][^>]+hreflang=["\']([^"\']+)["\']', html)
    og_title = first_match(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html)
    og_description = first_match(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html)
    og_image = first_match(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
    twitter_card = first_match(r'<meta[^>]+name=["\']twitter:card["\'][^>]+content=["\']([^"\']+)["\']', html)
    viewport = first_match(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\']([^"\']+)["\']', html)
    rss = first_match(r'<link[^>]+type=["\']application/rss\+xml["\'][^>]+href=["\']([^"\']+)["\']', html)
    article_published = first_match(r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']', html)
    article_modified = first_match(r'<meta[^>]+property=["\']article:modified_time["\'][^>]+content=["\']([^"\']+)["\']', html)
    article_author = first_match(r'<meta[^>]+property=["\']article:author["\'][^>]+content=["\']([^"\']+)["\']', html)
    jsonld, jsonld_errors = extract_jsonld(html)
    types = sorted(set(t for block in jsonld for t in schema_types(block)))
    news_nodes = [node for block in jsonld for node in find_newsarticle_nodes(block)]

    report["observed"] = {
        "title": title,
        "meta_description": description,
        "canonical_count": len(canonicals),
        "canonicals": canonicals,
        "hreflang_count": len(hreflangs),
        "hreflangs": hreflangs,
        "og_title": bool(og_title),
        "og_description": bool(og_description),
        "og_image": og_image,
        "twitter_card": twitter_card,
        "viewport": viewport,
        "rss": rss,
        "article_published_time": article_published,
        "article_modified_time": article_modified,
        "article_author": article_author,
        "jsonld_blocks": len(jsonld),
        "jsonld_types": types,
    }

    if not title:
        add_issue(report, "critical", "title_missing", "Missing title tag")
    if not description:
        add_issue(report, "critical", "meta_description_missing", "Missing meta description")
    if len(canonicals) == 0:
        add_issue(report, "critical", "canonical_missing", "Missing canonical link")
    if len(canonicals) > 1:
        add_issue(report, "critical", "canonical_duplicate", "More than one canonical link")
    if jsonld_errors:
        add_issue(report, "critical", "jsonld_invalid", "; ".join(jsonld_errors))
    if not jsonld:
        add_issue(report, "critical", "jsonld_missing", "No JSON-LD blocks found")
    for idx, node in enumerate(news_nodes, 1):
        if not image_present(node.get("image")):
            add_issue(report, "critical", "newsarticle_image_missing", f"NewsArticle node {idx} has no usable image")
    if not hreflangs:
        add_issue(report, "warning", "hreflang_missing", "No hreflang alternates found")
    if not (og_title and og_description and og_image):
        add_issue(report, "warning", "opengraph_incomplete", "OpenGraph title, description, or image missing")
    if not twitter_card:
        add_issue(report, "warning", "twitter_card_missing", "Twitter card missing")
    if not viewport:
        add_issue(report, "warning", "viewport_missing", "Viewport meta missing")
    if not rss:
        add_issue(report, "warning", "rss_autodiscovery_missing", "RSS autodiscovery link missing")
    if any(t in types for t in ["NewsArticle", "Article", "TechArticle", "BlogPosting"]):
        if not article_published:
            add_issue(report, "warning", "article_published_time_missing", "article:published_time missing")
        if not article_modified:
            add_issue(report, "warning", "article_modified_time_missing", "article:modified_time missing")
        if not article_author:
            add_issue(report, "warning", "article_author_missing", "article:author missing")

    critical_count = sum(1 for issue in report["issues"] if issue["severity"] == "critical")
    report["status"] = "fail" if critical_count else "pass"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit one HTML URL or file for SEO regression signals.")
    parser.add_argument("target")
    parser.add_argument("--report", help="Write JSON report to path")
    args = parser.parse_args()

    try:
        html, meta = read_target(args.target)
        report = audit_html(args.target, html, meta)
    except Exception as exc:
        report = {
            "artifact_type": "seo_regression_report",
            "generated_at": utc_now(),
            "target": args.target,
            "status": "fail",
            "issues": [{"severity": "critical", "code": "fetch_failed", "message": str(exc)}],
            "observed": {},
        }

    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": report["status"], "issues": report["issues"], "observed": report.get("observed", {})}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
