#!/usr/bin/env python3
"""Passive website security baseline audit.

This script fetches one URL and checks browser/security signals. It does not
exploit vulnerabilities, fuzz inputs, brute-force, or perform active scans.
"""

from __future__ import annotations

import argparse
import re
import socket
import ssl
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.cookies import SimpleCookie
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


SECURITY_HEADERS = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "CSP",
    "x-content-type-options": "MIME sniffing protection",
    "referrer-policy": "Referrer policy",
    "permissions-policy": "Permissions policy",
    "cross-origin-opener-policy": "COOP",
    "cross-origin-embedder-policy": "COEP",
    "cross-origin-resource-policy": "CORP",
}


def normalize_url(value: str) -> str:
    if not re.match(r"^https?://", value):
        value = "https://" + value
    return value


@dataclass
class Capture:
    tag: str
    attrs: dict[str, str]
    parts: list[str] = field(default_factory=list)


class SecurityHTMLParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.external_scripts: list[dict[str, str]] = []
        self.inline_script_count = 0
        self.forms: list[dict[str, Any]] = []
        self.current_form: dict[str, Any] | None = None
        self.password_inputs = 0
        self.mixed_content: list[str] = []

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {k.lower(): (v or "") for k, v in attrs_raw}
        if tag == "script":
            src = attrs.get("src")
            if src:
                full = urljoin(self.base_url, src)
                if urlparse(full).netloc != urlparse(self.base_url).netloc:
                    self.external_scripts.append({"src": full, "integrity": attrs.get("integrity", "")})
                if self.base_url.startswith("https://") and full.startswith("http://"):
                    self.mixed_content.append(full)
            else:
                self.inline_script_count += 1
        elif tag in {"img", "link", "iframe", "audio", "video", "source"}:
            src = attrs.get("src") or attrs.get("href")
            if src:
                full = urljoin(self.base_url, src)
                if self.base_url.startswith("https://") and full.startswith("http://"):
                    self.mixed_content.append(full)
        elif tag == "form":
            form = {"attrs": attrs, "password": False}
            self.forms.append(form)
            self.current_form = form
        elif tag == "input":
            if attrs.get("type", "text").lower() == "password":
                self.password_inputs += 1
                if self.current_form is not None:
                    self.current_form["password"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "form":
            self.current_form = None


def fetch(url: str, timeout: int) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": "Web-Security-Architect/1.0"})
    try:
        with urlopen(req, timeout=timeout) as res:
            body = res.read(2_000_000)
            return {
                "url": url,
                "final_url": res.geturl(),
                "status": res.status,
                "headers": {k.lower(): v for k, v in res.headers.items()},
                "set_cookie": res.headers.get_all("Set-Cookie") or [],
                "body": body,
                "error": None,
            }
    except HTTPError as exc:
        body = exc.read(500_000)
        return {
            "url": url,
            "final_url": exc.geturl(),
            "status": exc.code,
            "headers": {k.lower(): v for k, v in exc.headers.items()},
            "set_cookie": exc.headers.get_all("Set-Cookie") or [],
            "body": body,
            "error": None,
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "url": url,
            "final_url": url,
            "status": None,
            "headers": {},
            "set_cookie": [],
            "body": b"",
            "error": str(exc),
        }


def tls_info(url: str, timeout: int) -> dict[str, Any] | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return None
    port = parsed.port or 443
    context = ssl.create_default_context()
    try:
        with socket.create_connection((parsed.hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = cert.get("notAfter")
                expiry = None
                days_left = None
                if not_after:
                    expiry_ts = ssl.cert_time_to_seconds(not_after)
                    expiry = datetime.fromtimestamp(expiry_ts, timezone.utc)
                    days_left = int((expiry - datetime.now(timezone.utc)).total_seconds() // 86400)
                return {
                    "version": ssock.version(),
                    "cipher": ssock.cipher()[0] if ssock.cipher() else None,
                    "cert_expires": expiry.isoformat() if expiry else None,
                    "cert_days_left": days_left,
                }
    except OSError as exc:
        return {"error": str(exc)}


def parse_cookies(set_cookie_headers: list[str]) -> list[dict[str, Any]]:
    cookies: list[dict[str, Any]] = []
    for header in set_cookie_headers:
        cookie = SimpleCookie()
        try:
            cookie.load(header)
        except Exception:
            cookies.append({"name": "unparsed", "issues": ["could_not_parse"], "raw": header[:120]})
            continue
        for name, morsel in cookie.items():
            flags = {key.lower(): morsel[key] for key in morsel.keys() if morsel[key]}
            issues = []
            if "secure" not in flags:
                issues.append("missing_secure")
            if "httponly" not in flags and re.search(r"(session|sid|auth|token)", name, re.I):
                issues.append("session_like_cookie_missing_httponly")
            if "samesite" not in flags:
                issues.append("missing_samesite")
            cookies.append({"name": name, "flags": sorted(flags.keys()), "issues": issues})
    return cookies


def analyze(url: str, response: dict[str, Any], timeout: int) -> dict[str, Any]:
    headers = response["headers"]
    final_url = response["final_url"] or url
    parsed = urlparse(final_url)
    body_text = response["body"].decode("utf-8", errors="replace")
    html = SecurityHTMLParser(final_url)
    html.feed(body_text)
    cookies = parse_cookies(response["set_cookie"])
    issues: list[tuple[str, str]] = []

    if response["error"]:
        issues.append(("P1", f"Fetch failed: {response['error']}"))
    if response["status"] and response["status"] >= 400:
        issues.append(("P1", f"HTTP status {response['status']}"))
    if parsed.scheme != "https":
        issues.append(("P1", "Final URL is not HTTPS"))
    if parsed.scheme == "https" and "strict-transport-security" not in headers:
        issues.append(("P1", "Missing Strict-Transport-Security"))
    if "content-security-policy" not in headers:
        issues.append(("P1", "Missing Content-Security-Policy"))
    else:
        csp = headers["content-security-policy"].lower()
        if "'unsafe-inline'" in csp:
            issues.append(("P2", "CSP allows unsafe-inline"))
        if "'unsafe-eval'" in csp:
            issues.append(("P2", "CSP allows unsafe-eval"))
        if "object-src" not in csp:
            issues.append(("P2", "CSP missing object-src directive"))
        if "base-uri" not in csp:
            issues.append(("P2", "CSP missing base-uri directive"))
    if "x-content-type-options" not in headers:
        issues.append(("P2", "Missing X-Content-Type-Options"))
    elif headers["x-content-type-options"].lower() != "nosniff":
        issues.append(("P2", "X-Content-Type-Options is not nosniff"))
    if "referrer-policy" not in headers:
        issues.append(("P2", "Missing Referrer-Policy"))
    if "permissions-policy" not in headers:
        issues.append(("P2", "Missing Permissions-Policy"))
    if "x-frame-options" not in headers and "frame-ancestors" not in headers.get("content-security-policy", "").lower():
        issues.append(("P2", "No X-Frame-Options or CSP frame-ancestors"))

    acao = headers.get("access-control-allow-origin", "")
    acac = headers.get("access-control-allow-credentials", "")
    if acao == "*" and acac.lower() == "true":
        issues.append(("P1", "CORS wildcard is combined with credentials"))
    elif acao == "*":
        issues.append(("P2", "CORS allows any origin"))

    for cookie in cookies:
        for issue in cookie["issues"]:
            severity = "P1" if "httponly" in issue else "P2"
            issues.append((severity, f"Cookie {cookie['name']}: {issue}"))

    if html.inline_script_count and "content-security-policy" not in headers:
        issues.append(("P2", f"{html.inline_script_count} inline script(s) and no CSP"))
    external_without_sri = [item["src"] for item in html.external_scripts if not item["integrity"]]
    if external_without_sri:
        issues.append(("P2", f"{len(external_without_sri)} external script(s) without SRI"))
    if html.mixed_content:
        issues.append(("P1", f"{len(html.mixed_content)} mixed-content resource(s) detected"))
    for form in html.forms:
        action = form["attrs"].get("action", "")
        full_action = urljoin(final_url, action) if action else final_url
        if form.get("password") and not full_action.startswith("https://"):
            issues.append(("P1", "Password form posts to non-HTTPS action"))

    tls = tls_info(final_url, timeout)
    if tls and tls.get("cert_days_left") is not None and tls["cert_days_left"] < 14:
        issues.append(("P1", f"TLS certificate expires in {tls['cert_days_left']} days"))

    return {
        "url": url,
        "final_url": final_url,
        "status": response["status"],
        "tls": tls,
        "headers_present": {label: key in headers for key, label in SECURITY_HEADERS.items()},
        "cors": {
            "access_control_allow_origin": headers.get("access-control-allow-origin"),
            "access_control_allow_credentials": headers.get("access-control-allow-credentials"),
        },
        "cookies": cookies,
        "html": {
            "forms": len(html.forms),
            "password_inputs": html.password_inputs,
            "inline_scripts": html.inline_script_count,
            "external_scripts": len(html.external_scripts),
            "external_scripts_without_sri": len(external_without_sri),
            "mixed_content": html.mixed_content[:10],
        },
        "issues": issues,
    }


def print_report(result: dict[str, Any]) -> None:
    print(f"Web security passive audit: {result['url']}")
    print(f"Final URL: {result['final_url']}")
    print(f"Status: {result['status']}")
    print("")
    print("TLS")
    tls = result["tls"]
    if not tls:
        print("- not HTTPS")
    elif tls.get("error"):
        print(f"- error: {tls['error']}")
    else:
        print(f"- version: {tls.get('version')}")
        print(f"- cipher: {tls.get('cipher')}")
        print(f"- cert expires: {tls.get('cert_expires')} ({tls.get('cert_days_left')} days)")
    print("")
    print("Security headers")
    for name, present in result["headers_present"].items():
        print(f"- {name}: {'present' if present else 'missing'}")
    print("")
    print("Cookies")
    if not result["cookies"]:
        print("- none set in response")
    else:
        for cookie in result["cookies"]:
            issues = ", ".join(cookie["issues"]) or "none"
            flags = ", ".join(cookie.get("flags", [])) or "none"
            print(f"- {cookie['name']}: flags={flags}; issues={issues}")
    print("")
    print("HTML signals")
    html = result["html"]
    print(f"- forms: {html['forms']}; password inputs: {html['password_inputs']}")
    print(f"- inline scripts: {html['inline_scripts']}")
    print(f"- external scripts: {html['external_scripts']}; without SRI: {html['external_scripts_without_sri']}")
    print(f"- mixed content: {len(html['mixed_content'])}")
    print("")
    print("Issues")
    if not result["issues"]:
        print("- none")
    else:
        for severity, issue in result["issues"]:
            print(f"- {severity}: {issue}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Passive web security baseline audit for one URL.")
    parser.add_argument("url", help="URL, e.g. https://example.com or http://localhost:3000")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()

    url = normalize_url(args.url)
    response = fetch(url, args.timeout)
    result = analyze(url, response, args.timeout)
    print_report(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
