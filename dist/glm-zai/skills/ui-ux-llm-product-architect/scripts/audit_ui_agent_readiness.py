#!/usr/bin/env python3
"""Quick UI, accessibility, and agent-readiness audit for URL or HTML file.

This is a lightweight static check. Use browser testing for final validation.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CONTROL_INPUT_TYPES = {
    "button",
    "submit",
    "reset",
    "checkbox",
    "radio",
    "text",
    "email",
    "password",
    "search",
    "tel",
    "url",
    "number",
    "date",
    "time",
    "datetime-local",
    "file",
}

LANDMARK_TAGS = {"header", "nav", "main", "aside", "footer"}
LANDMARK_ROLES = {
    "banner",
    "navigation",
    "main",
    "complementary",
    "contentinfo",
    "search",
    "form",
}


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


@dataclass
class Capture:
    tag: str
    attrs: dict[str, str]
    parts: list[str] = field(default_factory=list)


class UIParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.capture_stack: list[Capture] = []
        self.headings: list[tuple[int, str]] = []
        self.landmarks: list[str] = []
        self.buttons: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.forms: list[dict[str, Any]] = []
        self.current_form: dict[str, Any] | None = None
        self.labels_by_for: dict[str, str] = {}
        self.inputs: list[dict[str, str]] = []
        self.live_regions: list[str] = []
        self.dialogs: list[dict[str, str]] = []
        self.clickable_noncontrols: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {k.lower(): (v or "") for k, v in attrs_raw}

        if tag == "title":
            self.in_title = True
        if tag in LANDMARK_TAGS:
            self.landmarks.append(tag)
        if attrs.get("role") in LANDMARK_ROLES:
            self.landmarks.append(f"role:{attrs['role']}")
        if attrs.get("aria-live") or attrs.get("role") in {"status", "alert", "log"}:
            self.live_regions.append(tag_or_role(tag, attrs))
        if attrs.get("role") == "dialog" or tag == "dialog":
            self.dialogs.append(attrs)

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "button", "a", "label"}:
            self.capture_stack.append(Capture(tag, attrs))
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "form":
            form = {"attrs": attrs, "inputs": []}
            self.forms.append(form)
            self.current_form = form
        elif tag in {"input", "select", "textarea"}:
            if tag == "input":
                input_type = attrs.get("type", "text").lower()
                if input_type not in CONTROL_INPUT_TYPES and input_type != "hidden":
                    input_type = "text"
                attrs["type"] = input_type
            else:
                attrs["type"] = tag
            self.inputs.append(attrs)
            if self.current_form is not None:
                self.current_form["inputs"].append(attrs)

        if tag in {"div", "span"} and (
            attrs.get("onclick") or attrs.get("role") in {"button", "link", "menuitem"}
        ):
            self.clickable_noncontrols.append(attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag == "form":
            self.current_form = None

        if not self.capture_stack:
            return
        current = self.capture_stack[-1]
        if current.tag != tag:
            return
        self.capture_stack.pop()
        text = clean(" ".join(current.parts))
        attrs = current.attrs
        if tag.startswith("h") and tag[1:].isdigit():
            self.headings.append((int(tag[1:]), text))
        elif tag == "button":
            self.buttons.append({**attrs, "_text": text})
        elif tag == "a":
            self.links.append({**attrs, "_text": text})
        elif tag == "label":
            target = attrs.get("for", "")
            if target:
                self.labels_by_for[target] = text

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.capture_stack:
            self.capture_stack[-1].parts.append(data)


def tag_or_role(tag: str, attrs: dict[str, str]) -> str:
    role = attrs.get("role")
    return f"{tag}[role={role}]" if role else tag


def accessible_name(attrs: dict[str, str], text_key: str = "_text") -> str:
    return clean(attrs.get(text_key) or attrs.get("aria-label") or attrs.get("title") or attrs.get("value"))


def read_target(target: str, timeout: int) -> tuple[str, str]:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"}:
        req = Request(target, headers={"User-Agent": "UI-UX-LLM-Product-Architect/1.0"})
        with urlopen(req, timeout=timeout) as res:
            return res.geturl(), res.read(2_000_000).decode("utf-8", errors="replace")
    path = os.path.abspath(os.path.expanduser(target))
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return path, handle.read()


def analyze(parser: UIParser) -> dict[str, Any]:
    title = clean(" ".join(parser.title_parts))
    issues: list[tuple[str, str]] = []

    h1_count = sum(1 for level, _ in parser.headings if level == 1)
    if not title:
        issues.append(("P1", "Missing document title"))
    if h1_count != 1:
        issues.append(("P1", f"Expected one H1, found {h1_count}"))
    if "main" not in parser.landmarks and "role:main" not in parser.landmarks:
        issues.append(("P1", "Missing main landmark"))
    if not any(item in parser.landmarks for item in ("nav", "role:navigation")):
        issues.append(("P2", "No navigation landmark found"))

    previous = 0
    for level, text in parser.headings:
        if previous and level > previous + 1:
            issues.append(("P2", f"Heading level jumps from H{previous} to H{level}: {text}"))
        previous = level

    unnamed_buttons = [button for button in parser.buttons if not accessible_name(button)]
    if unnamed_buttons:
        issues.append(("P1", f"{len(unnamed_buttons)} button(s) lack accessible names"))

    iconish_links = [
        link for link in parser.links if link.get("href") and not accessible_name(link)
    ]
    if iconish_links:
        issues.append(("P1", f"{len(iconish_links)} link(s) lack readable text or labels"))

    missing_alt = [img for img in parser.images if "alt" not in img]
    if missing_alt:
        issues.append(("P1", f"{len(missing_alt)} image(s) missing alt attributes"))

    unlabeled_inputs = []
    for item in parser.inputs:
        input_type = item.get("type", "text")
        if input_type == "hidden":
            continue
        has_label = bool(
            item.get("aria-label")
            or item.get("aria-labelledby")
            or item.get("id") in parser.labels_by_for
            or item.get("placeholder")
            or item.get("value") and input_type in {"submit", "button", "reset"}
        )
        if not has_label:
            unlabeled_inputs.append(item)
    if unlabeled_inputs:
        issues.append(("P1", f"{len(unlabeled_inputs)} form control(s) lack labels"))

    if parser.forms and not parser.live_regions:
        issues.append(("P2", "Forms exist but no live/status region was detected for async feedback"))
    if parser.clickable_noncontrols:
        issues.append(("P1", f"{len(parser.clickable_noncontrols)} non-semantic clickable element(s) detected"))
    for dialog in parser.dialogs:
        if not (dialog.get("aria-label") or dialog.get("aria-labelledby")):
            issues.append(("P1", "Dialog lacks accessible label"))

    return {
        "title": title,
        "headings": parser.headings,
        "landmarks": parser.landmarks,
        "buttons": len(parser.buttons),
        "links": len(parser.links),
        "images": len(parser.images),
        "forms": len(parser.forms),
        "inputs": len(parser.inputs),
        "live_regions": parser.live_regions,
        "dialogs": len(parser.dialogs),
        "issues": issues,
    }


def print_report(target: str, result: dict[str, Any]) -> None:
    print(f"UI/UX agent-readiness audit: {target}")
    print("")
    print(f"Title: {result['title'] or 'MISSING'}")
    print(f"Landmarks: {', '.join(result['landmarks']) or 'none'}")
    print(f"Headings: {', '.join('H%s %s' % item for item in result['headings'][:10]) or 'none'}")
    print(
        "Counts: "
        f"buttons={result['buttons']}, links={result['links']}, images={result['images']}, "
        f"forms={result['forms']}, inputs={result['inputs']}, dialogs={result['dialogs']}"
    )
    print(f"Live/status regions: {', '.join(result['live_regions']) or 'none'}")
    print("")
    print("Issues")
    if not result["issues"]:
        print("- none")
    else:
        for severity, issue in result["issues"]:
            print(f"- {severity}: {issue}")


def main() -> int:
    arg_parser = argparse.ArgumentParser(description="Audit HTML for UI, accessibility, and agent-readiness basics.")
    arg_parser.add_argument("target", help="URL or local HTML file")
    arg_parser.add_argument("--timeout", type=int, default=10)
    args = arg_parser.parse_args()

    try:
        final_target, html = read_target(args.target, args.timeout)
    except OSError as exc:
        print(f"Failed to read target: {exc}", file=sys.stderr)
        return 1

    parser = UIParser()
    parser.feed(html)
    result = analyze(parser)
    print_report(final_target, result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
