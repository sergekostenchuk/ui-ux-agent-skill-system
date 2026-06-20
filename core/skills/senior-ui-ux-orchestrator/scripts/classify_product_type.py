#!/usr/bin/env python3
"""Classify a UI/UX prompt into the skill group's routing modes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROUTES = {
    "webapp-ui-skill": {
        "mode": "build-webapp",
        "signals": ["dashboard", "admin", "crm", "saas", "internal tool", "settings", "table", "filters", "workflow", "data-heavy", "billing"],
    },
    "marketing-site-skill": {
        "mode": "build-marketing",
        "signals": ["landing", "product page", "brand page", "venue", "campaign", "conversion", "cta", "hero", "metadata"],
    },
    "ux-audit-skill": {
        "mode": "audit",
        "signals": ["audit", "review", "url", "screenshot", "accessibility", "regression", "before", "after", "lighthouse"],
    },
    "design-critic-skill": {
        "mode": "critique",
        "signals": ["critique", "polish", "hierarchy", "taste", "anti-slop", "spacing", "typography", "visual quality"],
    },
    "ui-ux-pro-max": {
        "mode": "design-intelligence",
        "signals": [
            "design direction",
            "style options",
            "visual system",
            "color palette",
            "typography",
            "layout pattern",
            "three variants",
            "design intelligence",
            "pro max",
            "ui/ux pro max",
            "feels generic",
        ],
    },
    "senior-ui-ux-orchestrator:three-variant-design": {
        "skill": "senior-ui-ux-orchestrator",
        "mode": "three-variant-design",
        "signals": [
            "three design variants",
            "3 design versions",
            "three design versions",
            "design versions",
            "three directions",
            "different versions",
            "klimovo",
            "like klimovo",
            "multiple visual concepts",
            "approved briefs to stitch",
            "before stitch",
        ],
    },
    "stitch-design-bridge": {
        "mode": "stitch",
        "signals": [
            "stitch",
            "google stitch",
            "stitch prompt",
            "ai ui prototype",
            "generate ui variants",
            "render in stitch",
            "stitch output review",
        ],
    },
    "senior-ui-ux-orchestrator:council": {
        "skill": "senior-ui-ux-orchestrator",
        "mode": "council",
        "signals": [
            "senior council",
            "consilium",
            "ux seo conflict",
            "figma code conflict",
            "stitch conflict",
            "large cross-skill project",
        ],
    },
    "obsidian-wiki-ingest": {
        "mode": "wiki-context",
        "signals": [
            "wiki",
            "obsidian",
            "llm wiki",
            "large project memory",
            "context capture",
            "ingest decisions",
            "do not lose context",
        ],
    },
    "senior-figma-orchestrator": {
        "mode": "figma",
        "signals": [
            "figma",
            "dev mode",
            "selected node",
            "frame",
            "variables",
            "component library",
            "code connect",
            "mcp",
            "code-to-canvas",
            "canvas edit",
            "figjam",
            "slides",
            "effects",
            "shadow",
            "blur",
            "glow",
            "glass",
            "noise",
            "texture",
        ],
    },
    "cursor-reveal-hero": {
        "mode": "interactive-effect",
        "signals": [
            "cursor reveal",
            "mouse trail",
            "hover reveal",
            "trail mask",
            "mask reveal",
            "base/reveal",
            "canvas compositing",
            "soft cursor",
        ],
    },
    "image-layer-alignment-validator": {
        "mode": "image-alignment",
        "signals": [
            "image layer",
            "base image",
            "reveal image",
            "alignment",
            "aligned",
            "line up",
            "misaligned",
            "drift",
            "before/after image",
            "two images",
        ],
    },
}


def score(prompt: str) -> list[dict[str, object]]:
    lowered = prompt.lower()
    results = []
    for skill, config in ROUTES.items():
        matches = [signal for signal in config["signals"] if signal in lowered]
        results.append(
            {
                "skill": str(config.get("skill", skill)),
                "mode": config["mode"],
                "route_id": skill,
                "score": len(matches),
                "matched_signals": matches,
            }
        )
    return sorted(results, key=lambda item: (-int(item["score"]), str(item["skill"])))


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify a UI/UX task prompt into a specialist skill route.")
    parser.add_argument("--input", required=True, help="Prompt text to classify.")
    parser.add_argument("--out", required=True, help="JSON report path.")
    args = parser.parse_args()

    ranked = score(args.input)
    best = ranked[0]
    confidence = "low" if best["score"] == 0 else "medium" if best["score"] == 1 else "high"
    result = {
        "input": args.input,
        "recommended_skill": best["skill"] if best["score"] else "senior-ui-ux-orchestrator",
        "recommended_mode": best["mode"] if best["score"] else "route",
        "confidence": confidence,
        "ranked_routes": ranked,
        "privacy_mode": "local-first",
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
