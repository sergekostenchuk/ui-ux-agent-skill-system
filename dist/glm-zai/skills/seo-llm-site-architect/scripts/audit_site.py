#!/usr/bin/env python3
"""Quick SEO/LLM readiness audit for a public or local URL.

The script intentionally uses only the Python standard library so it can run in
most project worktrees without dependency setup.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen


DEFAULT_UA = "SEO-LLM-Site-Architect/1.0"
HTML_TYPES = ("text/html", "application/xhtml+xml")
AI_TOKENS = (
    "GPTBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "ClaudeBot",
    "Claude-User",
    "Claude-SearchBot",
    "PerplexityBot",
    "Google-Extended",
    "Google-Agent",
)


def normalize_url(url: str) -> str:
    parsed = urlparse(url if re.match(r"^https?://", url) else f"https://{url}")
    path = parsed.path or "/"
    return urlunparse((parsed.scheme, parsed.netloc, path, "", parsed.query, ""))


def same_site(url: str, root: str) -> bool:
    return urlparse(url).netloc.lower() == urlparse(root).netloc.lower()


def strip_fragment(url: str) -> str:
    return urldefrag(url)[0]


def looks_crawlable_link(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    lowered = parsed.path.lower()
    blocked_suffixes = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".ico",
        ".pdf",
        ".zip",
        ".mp4",
        ".mp3",
        ".css",
        ".js",
    )
    return not lowered.endswith(blocked_suffixes)


def fetch(url: str, timeout: int, user_agent: str) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": user_agent})
    try:
        with urlopen(req, timeout=timeout) as res:
            body = res.read(2_000_000)
            return {
                "url": url,
                "final_url": res.geturl(),
                "status": res.status,
                "headers": dict(res.headers.items()),
                "body": body,
                "error": None,
            }
    except HTTPError as exc:
        body = exc.read(500_000)
        return {
            "url": url,
            "final_url": exc.geturl(),
            "status": exc.code,
            "headers": dict(exc.headers.items()),
            "body": body,
            "error": None,
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "url": url,
            "final_url": url,
            "status": None,
            "headers": {},
            "body": b"",
            "error": str(exc),
        }


class SignalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.capture_tag: str | None = None
        self.capture_attrs: dict[str, str] = {}
        self.capture_parts: list[str] = []
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.scripts: list[str] = []
        self.headings: dict[str, list[str]] = {"h1": [], "h2": []}
        self.anchors: list[str] = []
        self.text_parts: list[str] = []
        self.image_count = 0
        self.images_missing_alt = 0

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): (v or "") for k, v in attrs_raw}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "a" and attrs.get("href"):
            self.anchors.append(attrs["href"])
        elif tag == "img":
            self.image_count += 1
            if not attrs.get("alt", "").strip():
                self.images_missing_alt += 1
        elif tag in ("h1", "h2"):
            self.capture_tag = tag
            self.capture_attrs = attrs
            self.capture_parts = []
        elif tag == "script" and "ld+json" in attrs.get("type", "").lower():
            self.capture_tag = "script"
            self.capture_attrs = attrs
            self.capture_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if self.capture_tag and tag == self.capture_tag:
            text = clean_text(" ".join(self.capture_parts))
            if self.capture_tag in ("h1", "h2") and text:
                self.headings[self.capture_tag].append(text)
            elif self.capture_tag == "script" and text:
                self.scripts.append(text)
            self.capture_tag = None
            self.capture_attrs = {}
            self.capture_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.capture_tag:
            self.capture_parts.append(data)
        if data.strip():
            self.text_parts.append(data)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def meta_content(parser: SignalParser, key: str, value: str) -> str | None:
    key = key.lower()
    value = value.lower()
    for meta in parser.metas:
        if meta.get(key, "").lower() == value:
            return clean_text(meta.get("content", ""))
    return None


def link_href(parser: SignalParser, rel_value: str) -> str | None:
    rel_value = rel_value.lower()
    for link in parser.links:
        rels = {part.lower() for part in link.get("rel", "").split()}
        if rel_value in rels:
            return link.get("href") or None
    return None


def schema_types_from_json(value: Any) -> list[str]:
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            node_type = node.get("@type")
            if isinstance(node_type, str):
                found.append(node_type)
            elif isinstance(node_type, list):
                found.extend(str(item) for item in node_type)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return found


def analyze_page(url: str, response: dict[str, Any]) -> dict[str, Any]:
    content_type = response["headers"].get("Content-Type", "")
    body = response["body"]
    html = body.decode("utf-8", errors="replace")
    parser = SignalParser()
    if any(item in content_type.lower() for item in HTML_TYPES) or html.lstrip().startswith("<"):
        parser.feed(html)

    schema_types: list[str] = []
    schema_errors = 0
    for script in parser.scripts:
        try:
            schema_types.extend(schema_types_from_json(json.loads(script)))
        except json.JSONDecodeError:
            schema_errors += 1

    title = clean_text(" ".join(parser.title_parts))
    description = meta_content(parser, "name", "description")
    robots = meta_content(parser, "name", "robots")
    canonical = link_href(parser, "canonical")
    og_title = meta_content(parser, "property", "og:title")
    og_description = meta_content(parser, "property", "og:description")
    text = clean_text(" ".join(parser.text_parts))
    word_count = len(re.findall(r"\b[\w'-]+\b", text))

    issues: list[str] = []
    if response["error"]:
        issues.append(f"fetch_error: {response['error']}")
    if response["status"] and response["status"] >= 400:
        issues.append(f"http_status_{response['status']}")
    if not title:
        issues.append("missing_title")
    elif len(title) > 70:
        issues.append("long_title")
    if not description:
        issues.append("missing_meta_description")
    if not canonical:
        issues.append("missing_canonical")
    if robots and "noindex" in robots.lower():
        issues.append("meta_noindex")
    if len(parser.headings["h1"]) != 1:
        issues.append(f"h1_count_{len(parser.headings['h1'])}")
    if not schema_types:
        issues.append("missing_jsonld_schema")
    if schema_errors:
        issues.append(f"jsonld_parse_errors_{schema_errors}")
    if word_count < 250:
        issues.append("thin_visible_text")
    if not og_title or not og_description:
        issues.append("incomplete_open_graph")
    if parser.images_missing_alt:
        issues.append(f"images_missing_alt_{parser.images_missing_alt}")

    return {
        "url": url,
        "final_url": response["final_url"],
        "status": response["status"],
        "content_type": content_type,
        "title": title,
        "meta_description": description,
        "robots": robots,
        "canonical": canonical,
        "h1": parser.headings["h1"],
        "h2_sample": parser.headings["h2"][:5],
        "schema_types": sorted(set(schema_types)),
        "schema_errors": schema_errors,
        "og_title": og_title,
        "og_description": og_description,
        "word_count": word_count,
        "image_count": parser.image_count,
        "images_missing_alt": parser.images_missing_alt,
        "links": parser.anchors,
        "issues": issues,
    }


def root_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, "/", "", "", ""))


def check_public_file(root: str, path: str, timeout: int, user_agent: str) -> dict[str, Any]:
    url = urljoin(root, path)
    response = fetch(url, timeout, user_agent)
    text = response["body"].decode("utf-8", errors="replace")
    return {
        "url": url,
        "status": response["status"],
        "error": response["error"],
        "bytes": len(response["body"]),
        "text_sample": text[:2000],
    }


def analyze_site_files(root: str, timeout: int, user_agent: str) -> dict[str, Any]:
    files = {
        "robots": check_public_file(root, "/robots.txt", timeout, user_agent),
        "sitemap": check_public_file(root, "/sitemap.xml", timeout, user_agent),
        "llms": check_public_file(root, "/llms.txt", timeout, user_agent),
    }
    robots_text = files["robots"]["text_sample"]
    files["robots"]["has_sitemap_directive"] = "sitemap:" in robots_text.lower()
    files["robots"]["ai_tokens_mentioned"] = [
        token for token in AI_TOKENS if re.search(rf"\b{re.escape(token)}\b", robots_text, re.I)
    ]
    return files


def crawl(start_url: str, max_pages: int, timeout: int, user_agent: str) -> dict[str, Any]:
    start = normalize_url(start_url)
    root = root_url(start)
    queue: deque[str] = deque([start])
    seen: set[str] = set()
    pages: list[dict[str, Any]] = []

    while queue and len(pages) < max_pages:
        url = queue.popleft()
        url = strip_fragment(url)
        if url in seen:
            continue
        seen.add(url)
        response = fetch(url, timeout, user_agent)
        page = analyze_page(url, response)
        pages.append(page)
        if page["status"] and page["status"] >= 400:
            continue
        for href in page.pop("links", []):
            next_url = strip_fragment(urljoin(page["final_url"] or url, href))
            if same_site(next_url, start) and looks_crawlable_link(next_url) and next_url not in seen:
                queue.append(next_url)

    return {
        "start_url": start,
        "root_url": root,
        "site_files": analyze_site_files(root, timeout, user_agent),
        "pages": pages,
    }


def print_report(result: dict[str, Any]) -> None:
    print(f"SEO/LLM site audit: {result['start_url']}")
    print("")
    print("Public files")
    for name, data in result["site_files"].items():
        status = data["status"] if data["status"] is not None else "ERR"
        print(f"- {name}: {status} {data['url']} ({data['bytes']} bytes)")
        if name == "robots":
            print(f"  sitemap directive: {data['has_sitemap_directive']}")
            tokens = ", ".join(data["ai_tokens_mentioned"]) or "none"
            print(f"  AI/user-triggered tokens mentioned: {tokens}")
    print("")
    print("Pages")
    issue_counts: dict[str, int] = {}
    for page in result["pages"]:
        for issue in page["issues"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        schema = ", ".join(page["schema_types"]) or "none"
        h1 = " | ".join(page["h1"]) or "none"
        print(f"- {page['status']} {page['url']}")
        print(f"  title: {page['title'] or 'MISSING'}")
        print(f"  h1: {h1}")
        print(f"  canonical: {page['canonical'] or 'MISSING'}")
        print(f"  schema: {schema}")
        print(f"  issues: {', '.join(page['issues']) if page['issues'] else 'none'}")
    print("")
    print("Issue summary")
    if not issue_counts:
        print("- none")
    else:
        for issue, count in sorted(issue_counts.items(), key=lambda item: (-item[1], item[0])):
            print(f"- {issue}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Quick SEO/LLM readiness audit for a site URL.")
    parser.add_argument("url", help="Starting URL, e.g. https://example.com or http://localhost:3000")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum same-host HTML pages to crawl")
    parser.add_argument("--timeout", type=int, default=10, help="Fetch timeout in seconds")
    parser.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header for audit requests")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = crawl(args.url, max(1, args.max_pages), args.timeout, args.user_agent)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
