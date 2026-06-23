#!/usr/bin/env python3
"""Passive LLM-friendly site audit.

Checks public files and a small crawl for extraction/citation readiness. It does
not make claims about actual AI assistant ranking or citations.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen


DEFAULT_UA = "LLM-Friendly-Site-Optimizer/1.0"


def normalize_url(url: str) -> str:
    if not re.match(r"^https?://", url):
        url = "https://" + url
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))


def site_root(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, "/", "", "", ""))


def same_host(a: str, b: str) -> bool:
    return urlparse(a).netloc.lower() == urlparse(b).netloc.lower()


def fetch(url: str, timeout: int) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": DEFAULT_UA})
    try:
        with urlopen(req, timeout=timeout) as res:
            return {
                "url": url,
                "final_url": res.geturl(),
                "status": res.status,
                "headers": dict(res.headers.items()),
                "body": res.read(2_000_000),
                "error": None,
            }
    except HTTPError as exc:
        return {
            "url": url,
            "final_url": exc.geturl(),
            "status": exc.code,
            "headers": dict(exc.headers.items()),
            "body": exc.read(500_000),
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


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.capture_tag: str | None = None
        self.capture_parts: list[str] = []
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.anchors: list[str] = []
        self.scripts: list[str] = []
        self.headings: list[tuple[int, str]] = []
        self.text_parts: list[str] = []
        self.time_values: list[str] = []
        self.faq_markers = 0
        self.code_blocks = 0
        self.tables = 0
        self.images_missing_alt = 0
        self.images = 0

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {k.lower(): (v or "") for k, v in attrs_raw}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "a" and attrs.get("href"):
            self.anchors.append(attrs["href"])
        elif tag == "script" and "ld+json" in attrs.get("type", "").lower():
            self.capture_tag = "script"
            self.capture_parts = []
        elif tag in {"h1", "h2", "h3"}:
            self.capture_tag = tag
            self.capture_parts = []
        elif tag == "time":
            value = attrs.get("datetime")
            if value:
                self.time_values.append(value)
        elif tag == "img":
            self.images += 1
            if not attrs.get("alt", "").strip():
                self.images_missing_alt += 1
        elif tag == "code":
            self.code_blocks += 1
        elif tag == "table":
            self.tables += 1
        if "faq" in " ".join(attrs.values()).lower():
            self.faq_markers += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if self.capture_tag and tag == self.capture_tag:
            text = clean(" ".join(self.capture_parts))
            if self.capture_tag.startswith("h") and self.capture_tag[1:].isdigit():
                self.headings.append((int(self.capture_tag[1:]), text))
            elif self.capture_tag == "script" and text:
                self.scripts.append(text)
            self.capture_tag = None
            self.capture_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.capture_tag:
            self.capture_parts.append(data)
        if data.strip():
            self.text_parts.append(data)


def meta(parser: PageParser, key: str, value: str) -> str | None:
    for item in parser.metas:
        if item.get(key, "").lower() == value.lower():
            return clean(item.get("content", ""))
    return None


def link_rel(parser: PageParser, rel: str) -> str | None:
    for item in parser.links:
        rels = {part.lower() for part in item.get("rel", "").split()}
        if rel.lower() in rels:
            return item.get("href") or None
    return None


def schema_types(value: Any) -> list[str]:
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
    html = response["body"].decode("utf-8", errors="replace")
    parser = PageParser()
    parser.feed(html)

    schema_found: list[str] = []
    schema_errors = 0
    for block in parser.scripts:
        try:
            schema_found.extend(schema_types(json.loads(block)))
        except json.JSONDecodeError:
            schema_errors += 1

    title = clean(" ".join(parser.title_parts))
    description = meta(parser, "name", "description")
    author = meta(parser, "name", "author") or meta(parser, "property", "article:author")
    published = meta(parser, "property", "article:published_time")
    modified = meta(parser, "property", "article:modified_time")
    canonical = link_rel(parser, "canonical")
    h1 = [text for level, text in parser.headings if level == 1]
    h2 = [text for level, text in parser.headings if level == 2]
    text = clean(" ".join(parser.text_parts))
    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    first_text = text[:900].lower()
    has_direct_answer = any(marker in first_text for marker in ("кратко", "short answer", "tl;dr", "tldr", "direct answer", "summary"))
    has_faq = parser.faq_markers > 0 or "FAQPage" in schema_found or re.search(r"\bfaq\b|частые вопросы", text, re.I)
    path = urlparse(url).path.strip("/")
    hub_paths = {"", "news", "articles", "blog", "projects", "tools", "benchmarks"}
    has_article_schema = any(t in schema_found for t in ("Article", "NewsArticle", "TechArticle", "BlogPosting"))
    has_hub_schema = any(t in schema_found for t in ("CollectionPage", "Blog", "WebSite"))
    looks_like_hub = path in hub_paths or path.endswith(("/news", "/articles", "/blog", "/projects"))

    issues: list[str] = []
    if response["error"]:
        issues.append("fetch_error")
    if not title:
        issues.append("missing_title")
    if not description:
        issues.append("missing_meta_description")
    elif not 90 <= len(description) <= 180:
        issues.append("meta_description_length_outside_target")
    if not canonical:
        issues.append("missing_canonical")
    if len(h1) != 1:
        issues.append(f"h1_count_{len(h1)}")
    if not h2:
        issues.append("missing_h2_sections")
    if not has_direct_answer:
        issues.append("missing_direct_answer_near_top")
    if not has_faq:
        issues.append("missing_faq")
    if not has_article_schema and not (has_hub_schema and looks_like_hub):
        issues.append("missing_article_or_collection_schema")
    if has_faq and "FAQPage" not in schema_found:
        issues.append("faq_visible_but_missing_faqpage_schema")
    if not (published or parser.time_values):
        issues.append("missing_visible_or_meta_publish_date")
    if not modified:
        issues.append("missing_modified_time_meta")
    if not author:
        issues.append("missing_author")
    if word_count < 800:
        issues.append("thin_for_pillar_or_citation_page")
    if schema_errors:
        issues.append(f"jsonld_parse_errors_{schema_errors}")
    if parser.images and parser.images_missing_alt:
        issues.append(f"images_missing_alt_{parser.images_missing_alt}")

    return {
        "url": url,
        "status": response["status"],
        "title": title,
        "description": description,
        "canonical": canonical,
        "h1": h1,
        "h2_count": len(h2),
        "word_count": word_count,
        "has_direct_answer": has_direct_answer,
        "has_faq": bool(has_faq),
        "schema_types": sorted(set(schema_found)),
        "author": author,
        "published": published or (parser.time_values[0] if parser.time_values else None),
        "modified": modified,
        "code_blocks": parser.code_blocks,
        "tables": parser.tables,
        "issues": issues,
        "links": parser.anchors,
    }


def fetch_public_file(root: str, path: str, timeout: int) -> dict[str, Any]:
    url = urljoin(root, path)
    response = fetch(url, timeout)
    text = response["body"].decode("utf-8", errors="replace")
    return {
        "url": url,
        "status": response["status"],
        "bytes": len(response["body"]),
        "error": response["error"],
        "text": text[:4000],
    }


def crawl(start: str, max_pages: int, timeout: int) -> dict[str, Any]:
    start = normalize_url(start)
    root = site_root(start)
    queue: deque[str] = deque([start])
    seen: set[str] = set()
    pages: list[dict[str, Any]] = []
    while queue and len(pages) < max_pages:
        url = urldefrag(queue.popleft())[0]
        if url in seen:
            continue
        seen.add(url)
        response = fetch(url, timeout)
        page = analyze_page(url, response)
        pages.append(page)
        for href in page.pop("links"):
            target = urldefrag(urljoin(url, href))[0]
            if same_host(target, start) and target not in seen and urlparse(target).scheme in {"http", "https"}:
                if not re.search(r"\.(png|jpg|jpeg|gif|webp|svg|pdf|zip|mp4|mp3|css|js)$", urlparse(target).path, re.I):
                    queue.append(target)
    files = {
        "llms": fetch_public_file(root, "/llms.txt", timeout),
        "robots": fetch_public_file(root, "/robots.txt", timeout),
        "sitemap": fetch_public_file(root, "/sitemap.xml", timeout),
        "news_sitemap": fetch_public_file(root, "/news-sitemap.xml", timeout),
    }
    return {"start_url": start, "root_url": root, "files": files, "pages": pages}


def print_report(result: dict[str, Any]) -> None:
    print(f"LLM-friendly site audit: {result['start_url']}")
    print("")
    print("Public files")
    for name, data in result["files"].items():
        status = data["status"] if data["status"] is not None else "ERR"
        print(f"- {name}: {status} {data['url']} ({data['bytes']} bytes)")
        if name == "llms" and status == 200:
            has_desc = bool(re.search(r"^>\s+\S", data["text"], re.M))
            has_sections = "##" in data["text"]
            print(f"  description block: {has_desc}; sections: {has_sections}")
        if name == "robots" and status == 200:
            print(f"  has sitemap directive: {'sitemap:' in data['text'].lower()}")
    print("")
    print("Pages")
    counts: dict[str, int] = {}
    for page in result["pages"]:
        for issue in page["issues"]:
            counts[issue] = counts.get(issue, 0) + 1
        print(f"- {page['status']} {page['url']}")
        print(f"  h1: {' | '.join(page['h1']) or 'MISSING'}")
        print(f"  words: {page['word_count']}; h2: {page['h2_count']}; direct_answer: {page['has_direct_answer']}; faq: {page['has_faq']}")
        print(f"  schema: {', '.join(page['schema_types']) or 'none'}")
        print(f"  issues: {', '.join(page['issues']) if page['issues'] else 'none'}")
    print("")
    print("Issue summary")
    if not counts:
        print("- none")
    else:
        for issue, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            print(f"- {issue}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Passive LLM-friendly site audit.")
    parser.add_argument("url")
    parser.add_argument("--max-pages", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()
    result = crawl(args.url, max(1, args.max_pages), args.timeout)
    print_report(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
