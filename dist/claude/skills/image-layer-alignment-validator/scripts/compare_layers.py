#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError as exc:
    print(
        "Missing dependency. This script requires Pillow, numpy, and opencv-python.",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def flatten_rgba(image: Image.Image, background=(255, 255, 255)) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA")).astype(np.float32)
    alpha = rgba[:, :, 3:4] / 255.0
    bg = np.array(background, dtype=np.float32).reshape(1, 1, 3)
    rgb = rgba[:, :, :3] * alpha + bg * (1.0 - alpha)
    return np.clip(rgb, 0, 255).astype(np.uint8)


def sample_border(rgb: np.ndarray) -> np.ndarray:
    h, w = rgb.shape[:2]
    band = max(4, min(80, int(min(h, w) * 0.04)))
    samples = np.concatenate(
        [
            rgb[:band, :, :].reshape(-1, 3),
            rgb[-band:, :, :].reshape(-1, 3),
            rgb[:, :band, :].reshape(-1, 3),
            rgb[:, -band:, :].reshape(-1, 3),
        ],
        axis=0,
    )
    return np.median(samples, axis=0)


def central_weight(height: int, width: int) -> np.ndarray:
    yy, xx = np.mgrid[0:height, 0:width]
    nx = (xx - width / 2.0) / max(width, 1)
    ny = (yy - height / 2.0) / max(height, 1)
    radius = np.sqrt(nx * nx + ny * ny)
    return np.clip(1.0 - radius * 2.0, 0.0, 1.0)


def clean_mask(mask: np.ndarray) -> np.ndarray:
    h, w = mask.shape[:2]
    k = max(3, int(min(h, w) * 0.012))
    if k % 2 == 0:
        k += 1
    kernel = np.ones((k, k), np.uint8)
    out = mask.astype(np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel, iterations=2)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel, iterations=1)
    return out > 0


def estimate_subject_mask(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"))
    alpha = rgba[:, :, 3]
    transparent_ratio = float(np.mean(alpha < 245))
    if transparent_ratio > 0.02 and transparent_ratio < 0.98:
        return clean_mask(alpha > 24)

    rgb = flatten_rgba(image)
    h, w = rgb.shape[:2]
    bg = sample_border(rgb)
    diff = np.linalg.norm(rgb.astype(np.float32) - bg.reshape(1, 1, 3), axis=2)
    diff_norm = diff / max(float(np.percentile(diff, 97)), 1.0)

    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    sat_norm = hsv[:, :, 1].astype(np.float32) / 255.0

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 60, 150).astype(np.float32) / 255.0
    edges = cv2.GaussianBlur(edges, (0, 0), sigmaX=max(1.0, min(h, w) * 0.01))

    score = 0.66 * diff_norm + 0.22 * sat_norm + 0.38 * edges
    score *= 0.60 + 0.40 * central_weight(h, w)
    threshold = max(0.24, float(np.percentile(score, 73)))
    return clean_mask(score > threshold)


def component_boxes(mask: np.ndarray, max_secondary: int = 6) -> tuple[dict | None, list[dict]]:
    h, w = mask.shape[:2]
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    components = []
    min_area = max(40, int(h * w * 0.002))
    for idx in range(1, num):
        x, y, bw, bh, area = stats[idx]
        if area < min_area:
            continue
        cx, cy = centroids[idx]
        nx = (cx - w / 2.0) / max(w, 1)
        ny = (cy - h / 2.0) / max(h, 1)
        center_bonus = max(0.30, 1.0 - math.sqrt(nx * nx + ny * ny))
        box_area = max(1, bw * bh)
        fill = float(area) / float(box_area)
        score = float(area) * center_bonus * (0.75 + min(fill, 1.0))
        components.append(
            {
                "x": int(x),
                "y": int(y),
                "w": int(bw),
                "h": int(bh),
                "area": int(area),
                "cx": float(cx),
                "cy": float(cy),
                "score": float(score),
            }
        )
    if not components:
        return None, []
    components.sort(key=lambda item: item["score"], reverse=True)
    main = components[0]
    secondary = sorted(components[1:], key=lambda item: item["area"], reverse=True)[:max_secondary]
    return main, secondary


def bbox_iou(a: dict, b: dict) -> float:
    ax1, ay1, ax2, ay2 = a["x"], a["y"], a["x"] + a["w"], a["y"] + a["h"]
    bx1, by1, bx2, by2 = b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = a["w"] * a["h"] + b["w"] * b["h"] - inter
    return float(inter) / float(union) if union > 0 else 0.0


def metrics(base_box: dict | None, reveal_box: dict | None, width: int, height: int) -> dict:
    if base_box is None or reveal_box is None:
        return {
            "verdict": "inconclusive",
            "reason": "Could not detect a primary subject box in one or both layers.",
        }

    dx = float(base_box["cx"] - reveal_box["cx"])
    dy = float(base_box["cy"] - reveal_box["cy"])
    drift_px = math.sqrt(dx * dx + dy * dy)
    diag = math.sqrt(width * width + height * height)
    drift_norm = drift_px / max(diag, 1.0)
    iou = bbox_iou(base_box, reveal_box)
    width_ratio = float(reveal_box["w"]) / max(float(base_box["w"]), 1.0)
    height_ratio = float(reveal_box["h"]) / max(float(base_box["h"]), 1.0)
    scale_delta = max(abs(width_ratio - 1.0), abs(height_ratio - 1.0))
    base_aspect = float(base_box["w"]) / max(float(base_box["h"]), 1.0)
    reveal_aspect = float(reveal_box["w"]) / max(float(reveal_box["h"]), 1.0)
    aspect_delta = abs(reveal_aspect - base_aspect) / max(base_aspect, 0.001)

    if drift_norm <= 0.025 and iou >= 0.65 and scale_delta <= 0.10:
        verdict = "aligned"
    elif drift_norm <= 0.08 and iou >= 0.35 and scale_delta <= 0.25:
        verdict = "minor drift"
    elif iou < 0.15 and (drift_norm > 0.16 or scale_delta > 0.60):
        verdict = "different subject"
    else:
        verdict = "misaligned"

    return {
        "verdict": verdict,
        "center_shift_to_apply_to_reveal_px": {"x": round(dx, 2), "y": round(dy, 2)},
        "center_drift_px": round(drift_px, 2),
        "center_drift_norm": round(drift_norm, 4),
        "bbox_iou": round(iou, 4),
        "width_ratio_reveal_to_base": round(width_ratio, 4),
        "height_ratio_reveal_to_base": round(height_ratio, 4),
        "scale_delta": round(scale_delta, 4),
        "aspect_delta": round(aspect_delta, 4),
    }


def draw_boxes(image: Image.Image, main: dict | None, secondary: list[dict], label: str) -> Image.Image:
    out = image.convert("RGBA").copy()
    draw = ImageDraw.Draw(out)
    width = max(3, int(min(out.size) * 0.006))
    if main:
        rect = [main["x"], main["y"], main["x"] + main["w"], main["y"] + main["h"]]
        draw.rectangle(rect, outline=(0, 220, 90, 255), width=width)
        draw.text((main["x"] + width, main["y"] + width), f"{label} main", fill=(0, 160, 60, 255))
    for i, box in enumerate(secondary, start=1):
        rect = [box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]]
        draw.rectangle(rect, outline=(255, 190, 0, 255), width=max(2, width - 1))
        draw.text((box["x"] + width, box["y"] + width), f"secondary {i}", fill=(180, 120, 0, 255))
    return out


def make_side_by_side(base_annotated: Image.Image, reveal_annotated: Image.Image) -> Image.Image:
    w, h = base_annotated.size
    out = Image.new("RGBA", (w * 2, h), (255, 255, 255, 255))
    out.paste(base_annotated, (0, 0))
    out.paste(reveal_annotated, (w, 0))
    draw = ImageDraw.Draw(out)
    draw.line((w, 0, w, h), fill=(255, 255, 255, 255), width=max(2, w // 300))
    return out


def make_overlay(base: Image.Image, reveal: Image.Image) -> Image.Image:
    base_rgb = base.convert("RGBA")
    reveal_rgba = reveal.convert("RGBA")
    overlay = Image.blend(base_rgb, reveal_rgba, 0.45)
    return overlay


def make_difference(base: Image.Image, reveal: Image.Image) -> Image.Image:
    a = np.asarray(base.convert("RGB")).astype(np.int16)
    b = np.asarray(reveal.convert("RGB")).astype(np.int16)
    diff = np.abs(a - b).astype(np.float32)
    diff = np.clip(diff * 2.2, 0, 255).astype(np.uint8)
    return Image.fromarray(diff, "RGB")


def write_report(
    out_dir: Path,
    base_path: Path,
    reveal_path: Path,
    base_size: tuple[int, int],
    reveal_size: tuple[int, int],
    base_box: dict | None,
    reveal_box: dict | None,
    base_secondary: list[dict],
    reveal_secondary: list[dict],
    result: dict,
) -> None:
    lines = [
        "# Image Layer Alignment Report",
        "",
        "This report is generated by a deterministic foreground/geometry heuristic. Inspect the visual artifacts before accepting the verdict.",
        "",
        f"- Base: `{base_path}`",
        f"- Reveal: `{reveal_path}`",
        f"- Base size: `{base_size[0]}x{base_size[1]}`",
        f"- Reveal original size: `{reveal_size[0]}x{reveal_size[1]}`",
        f"- Verdict: `{result['verdict']}`",
        "",
        "## Primary Subject Metrics",
        "",
    ]
    if base_box and reveal_box:
        lines.extend(
            [
                f"- Base box: `{base_box['x']},{base_box['y']} {base_box['w']}x{base_box['h']}`",
                f"- Reveal box: `{reveal_box['x']},{reveal_box['y']} {reveal_box['w']}x{reveal_box['h']}`",
                f"- Center drift: `{result['center_drift_px']} px`",
                f"- Center drift normalized: `{result['center_drift_norm']}`",
                f"- BBox IoU: `{result['bbox_iou']}`",
                f"- Scale delta: `{result['scale_delta']}`",
                f"- Aspect delta: `{result['aspect_delta']}`",
                f"- Shift to apply to reveal: `x={result['center_shift_to_apply_to_reveal_px']['x']} px`, `y={result['center_shift_to_apply_to_reveal_px']['y']} px`",
            ]
        )
    else:
        lines.append(f"- Reason: `{result.get('reason', 'Detection failed')}`")

    lines.extend(
        [
            "",
            "## Secondary Objects",
            "",
            f"- Base secondary boxes detected: `{len(base_secondary)}`",
            f"- Reveal secondary boxes detected: `{len(reveal_secondary)}`",
            "",
            "## Recommended Action",
            "",
        ]
    )
    verdict = result["verdict"]
    if verdict == "aligned":
        lines.append("- Use the pair for reveal compositing. Check local edge details only if the effect exposes a narrow area.")
    elif verdict == "minor drift":
        lines.append("- Apply the measured reveal shift first. Re-run this script after the edit.")
        lines.append("- If drift remains around face, hands, helmet, or product outline, regenerate or manually align the reveal layer.")
    elif verdict == "misaligned":
        lines.append("- Do not rely on canvas tuning to hide the mismatch. Align, crop, scale, or regenerate the reveal layer.")
    elif verdict == "different subject":
        lines.append("- Treat the reveal as a different subject. Regenerate or select a better matching layer.")
    else:
        lines.append("- Inspect the annotated images and choose the intended primary subject manually.")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `annotated-base.png`",
            "- `annotated-reveal.png`",
            "- `side-by-side.png`",
            "- `overlay.png`",
            "- `difference.png`",
            "- `alignment-metrics.json`",
            "",
        ]
    )
    (out_dir / "alignment-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare base/reveal image layer alignment.")
    parser.add_argument("--base", required=True, type=Path, help="Base image path")
    parser.add_argument("--reveal", required=True, type=Path, help="Reveal image path")
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    args = parser.parse_args()

    base_path = args.base.expanduser().resolve()
    reveal_path = args.reveal.expanduser().resolve()
    out_dir = args.out.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_rgba(base_path)
    reveal_original = load_rgba(reveal_path)
    reveal = reveal_original
    if reveal.size != base.size:
        reveal = reveal.resize(base.size, Image.Resampling.LANCZOS)

    base_mask = estimate_subject_mask(base)
    reveal_mask = estimate_subject_mask(reveal)
    base_box, base_secondary = component_boxes(base_mask)
    reveal_box, reveal_secondary = component_boxes(reveal_mask)
    result = metrics(base_box, reveal_box, base.size[0], base.size[1])

    base_annotated = draw_boxes(base, base_box, base_secondary, "base")
    reveal_annotated = draw_boxes(reveal, reveal_box, reveal_secondary, "reveal")

    base_annotated.save(out_dir / "annotated-base.png")
    reveal_annotated.save(out_dir / "annotated-reveal.png")
    make_side_by_side(base_annotated, reveal_annotated).save(out_dir / "side-by-side.png")
    make_overlay(base, reveal).save(out_dir / "overlay.png")
    make_difference(base, reveal).save(out_dir / "difference.png")

    payload = {
        "base": str(base_path),
        "reveal": str(reveal_path),
        "base_size": list(base.size),
        "reveal_original_size": list(reveal_original.size),
        "analysis_size": list(base.size),
        "dimension_mismatch": reveal_original.size != base.size,
        "base_main_box": base_box,
        "reveal_main_box": reveal_box,
        "base_secondary_boxes": base_secondary,
        "reveal_secondary_boxes": reveal_secondary,
        "metrics": result,
    }
    (out_dir / "alignment-metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(
        out_dir,
        base_path,
        reveal_path,
        base.size,
        reveal_original.size,
        base_box,
        reveal_box,
        base_secondary,
        reveal_secondary,
        result,
    )

    print(json.dumps({"verdict": result["verdict"], "out": str(out_dir)}, indent=2))
    return 0 if result["verdict"] in {"aligned", "minor drift", "misaligned", "different subject", "inconclusive"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
