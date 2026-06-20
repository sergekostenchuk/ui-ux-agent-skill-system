#!/usr/bin/env python3
import os
import re
import sys


def redact(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "<redacted>"
    return f"{value[:3]}...{value[-4:]}"


def main() -> int:
    key = os.environ.get("STITCH_API_KEY", "")
    has_key = bool(key.strip())
    likely_shape = bool(re.match(r"^[A-Za-z0-9_.-]{20,}$", key)) if has_key else False
    print("Stitch config check")
    print(f"STITCH_API_KEY present: {has_key}")
    print(f"STITCH_API_KEY likely shape: {likely_shape}")
    if has_key:
        print(f"STITCH_API_KEY redacted: {redact(key)}")
    if not has_key:
        print("status: missing credential; set STITCH_API_KEY outside skill files")
        return 2
    print("status: credential available to current process")
    return 0


if __name__ == "__main__":
    sys.exit(main())
