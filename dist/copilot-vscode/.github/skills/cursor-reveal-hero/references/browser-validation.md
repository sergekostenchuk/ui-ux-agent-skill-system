# Browser Validation

Use browser validation when the effect has been implemented or repaired.

## Manual Checks

- The canvas is nonblank after images load.
- Base image is visible before pointer movement.
- Reveal image appears only around the pointer trail.
- The reveal zone has a soft edge, not a hard circle.
- Old trail fades gradually.
- Sliders immediately affect behavior.
- Changing sliders clears old mask content.
- Resize keeps the image framed and nonblurry.

## Automated Smoke Check

Run:

```bash
node $CODEX_SKILLS_DIR/cursor-reveal-hero/scripts/smoke-check-reveal.mjs \
  --url http://127.0.0.1:4173/ \
  --canvas "#bioRevealCanvas" \
  --screenshot /tmp/reveal-smoke.png
```

The script checks:

- target URL loads;
- canvas exists;
- canvas has nonblank pixels;
- pointer movement changes canvas pixels;
- optional screenshot can be saved.

Treat the script as smoke evidence, not a final visual judgment. Still inspect the screenshot or the page for composition quality.
