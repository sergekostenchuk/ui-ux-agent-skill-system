# Alignment Rubric

Use this rubric after generating or inspecting evidence artifacts.

## Core Metrics

- `center_drift_px`: pixel offset between primary subject centers.
- `center_drift_norm`: center offset divided by the canvas diagonal.
- `bbox_iou`: intersection-over-union between primary subject boxes on a common canvas.
- `scale_delta`: maximum relative width/height change between primary boxes.
- `aspect_delta`: relative aspect-ratio change between primary boxes.

## Default Verdict Thresholds

Use these as starting points, then adjust for the intended effect.

| Verdict | Typical Conditions |
| --- | --- |
| `aligned` | `center_drift_norm <= 0.025`, `bbox_iou >= 0.65`, `scale_delta <= 0.10` |
| `minor drift` | Drift is visible but likely fixable by small shift/scale; `center_drift_norm <= 0.08`, `bbox_iou >= 0.35` |
| `misaligned` | Subject is recognizably related but position, scale, or crop would make reveal look broken |
| `different subject` | Primary objects are semantically different or geometry has no useful overlap |
| `inconclusive` | Detection failed, image is too abstract, or the intended subject is unclear |

## Stricter Cases

Use stricter thresholds for:

- faces and portraits;
- helmets, eyes, hands, and product silhouettes;
- narrow cursor reveal masks where local drift is obvious;
- before/after sliders where users compare edges precisely.

## Looser Cases

Use looser thresholds for:

- abstract backgrounds;
- atmospheric reveal effects;
- wide soft masks with low reveal opacity;
- effects where the reveal layer is intentionally impressionistic.

## Fix Recommendations

- If center drift dominates, suggest shifting the reveal layer by `base_center - reveal_center`.
- If scale delta dominates, suggest scaling the reveal layer around the subject center.
- If aspect or pose differs, suggest regenerating or editing the reveal image rather than CSS tuning.
- If background differs but subject aligns, approve the pair and mention background mismatch as acceptable for reveal effects.
