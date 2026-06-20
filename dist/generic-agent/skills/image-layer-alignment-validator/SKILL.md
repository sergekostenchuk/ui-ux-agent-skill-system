---
name: image-layer-alignment-validator
description: Validate whether two raster image layers are suitable for reveal, before/after, morph, mask-compositing, or interactive cursor reveal effects. Use when comparing base/reveal images, checking whether the main subject stayed in the same position, separating primary subject drift from background or secondary-object differences, producing annotated overlays/difference maps, or deciding whether an image layer must be shifted, scaled, cropped, or regenerated before frontend compositing.
---

# Image Layer Alignment Validator

Use this skill to check whether two image layers can be composited as the same scene or subject. The goal is not generic image critique; the goal is to decide whether a base layer and reveal layer are spatially compatible.

## Modes

- `compare`: analyze two local image files and produce visual/report artifacts.
- `diagnose`: inspect an existing report or screenshots and explain why a reveal/morph looks misaligned.
- `advise`: convert measured drift into concrete fixes: shift, scale, crop, regenerate, or accept.
- `threshold`: tune acceptance thresholds for strict product/portrait work versus looser creative reveal effects.

## Workflow

1. Confirm there are exactly two intended layers: base and reveal/after.
2. Keep all analysis local by default. Do not upload private images to external services unless the user explicitly requests that.
3. Run `scripts/compare_layers.py` when local image paths are available:

   ```bash
   python3 $CODEX_SKILLS_DIR/image-layer-alignment-validator/scripts/compare_layers.py \
     --base /path/to/base.png \
     --reveal /path/to/reveal.png \
     --out /path/to/alignment-output
   ```

4. Inspect the generated artifacts before giving a verdict. The script is a deterministic foreground/geometry heuristic; semantic judgment still matters.
5. If the main subject is ambiguous, read `references/subject-taxonomy.md` and state the chosen primary subject explicitly.
6. Score alignment with `references/alignment-rubric.md`.
7. Report measured drift and a concrete next action.

## Evidence Artifacts

The comparison script writes:

- `alignment-report.md`: human-readable metrics, verdict, and suggested fixes.
- `alignment-metrics.json`: machine-readable dimensions, boxes, drift, IoU, and verdict.
- `annotated-base.png`: detected primary and secondary boxes on the base layer.
- `annotated-reveal.png`: detected primary and secondary boxes on the reveal layer.
- `side-by-side.png`: visual comparison with boxes.
- `overlay.png`: reveal blended over base for quick inspection.
- `difference.png`: amplified pixel difference map.

## Decision Rules

- Treat the measured primary subject box as evidence, not truth. Override it when visual inspection clearly finds a different main object.
- Prefer normalized measurements for verdicts so different canvas sizes are comparable.
- For cursor reveal or mask reveal, the main subject should usually be stricter than the background. Background, lighting, texture, and small accessory differences can change without failing the pair.
- If the subject center drift is visible in the intended reveal area, recommend image correction before frontend work.
- If the reveal image is a genuinely different subject, do not try to hide it with CSS/canvas tuning.

## Safety And Privacy

- Process local images locally by default.
- Do not upload private, client, face, identity, or unpublished creative images to external services unless the user explicitly requests that route.
- Do not overwrite source images. Write reports and derived artifacts to a separate output directory.
- When recommending regeneration, describe the intended geometry constraints instead of embedding private image details into reusable skill files.

## Validation And Eval

- Validate the script with representative pairs before trusting new thresholds.
- Check `alignment-report.md` and at least one visual artifact before returning a verdict.
- Treat `inconclusive` as a valid outcome when foreground detection fails.
- For strict effects, re-run the script after any shift, crop, scale, or regeneration step.
- Forward-test the skill with examples that include aligned pairs, small subject drift, different canvas sizes, and unrelated reveal subjects.

## Output Format

Return:

```text
Verdict: aligned | minor drift | misaligned | different subject | inconclusive

Evidence:
- Primary subject: ...
- Center drift: ... px (... normalized)
- BBox IoU: ...
- Scale delta: ...
- Secondary-object notes: ...

Action:
- ...

Artifacts:
- /absolute/path/alignment-report.md
- /absolute/path/side-by-side.png
- /absolute/path/overlay.png
```

## Resources

- Read `references/subject-taxonomy.md` when deciding what counts as the primary subject versus secondary objects.
- Read `references/alignment-rubric.md` when grading output or tuning thresholds.
- Use `scripts/compare_layers.py` for local deterministic evidence.
