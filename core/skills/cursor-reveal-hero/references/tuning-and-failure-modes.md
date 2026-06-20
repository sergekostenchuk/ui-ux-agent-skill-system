# Tuning And Failure Modes

## Starting Settings

Use these as a baseline for a soft cursor trail:

```js
const settings = {
  radius: 245,
  feather: 0.8,
  fade: 0.028,
  strength: 0.82,
  opacity: 0.78,
  lerp: 0.14,
  idleStrength: 0
};
```

## Parameter Meaning

- `radius`: size of the reveal zone.
- `feather`: softness of the mask edge. Higher means softer/wider transition.
- `fade`: speed old trail disappears. Higher means faster clearing.
- `strength`: alpha written by each new hotspot.
- `opacity`: final reveal layer opacity over the base.
- `lerp`: momentum. Lower values lag more behind the pointer.
- `idleStrength`: optional idle reveal when no pointer is active. Keep `0` unless requested.

## Control Binding Checklist

- Use `input` for immediate response.
- Use `change` as a fallback for keyboard or browser-specific behavior.
- Parse numbers with `Number(input.value)`.
- Update visible numeric labels with `textContent`.
- Clear the mask after settings changes.
- Keep slider min/max aligned with the expected setting range.
- Expose `window.revealSettings` during debugging.

## Failure Patterns

- Hard circle: feather too low or gradient stops are wrong.
- Sticky helmet/object ghosting: opacity too high, fade too low, or reveal/base images misaligned.
- No reveal after movement: image failed to load, pointer coordinates are wrong, or mask never reaches reveal canvas.
- Reveal visible everywhere: `destination-in` not applied or reveal canvas not cleared before drawing.
- Trail stutters: too many allocations inside the animation frame or canvas is much larger than needed.
- Controls appear broken: old mask content persists after parameter changes, causing false visual feedback.
