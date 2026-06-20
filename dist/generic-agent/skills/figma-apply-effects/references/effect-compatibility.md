# Figma Effect Compatibility

## Current Source Rule

Before relying on exact advanced effect fields, check current Figma Plugin API docs or typings:

- https://developers.figma.com/docs/plugins/api/Effect/
- https://raw.githubusercontent.com/figma/plugin-typings/master/plugin-api.d.ts

At the time this skill was written, `Effect` in official plugin typings is a union of:

- `DropShadowEffect`
- `InnerShadowEffect`
- `BlurEffect`
- `NoiseEffect`
- `TextureEffect`
- `GlassEffect`

## Core Objects

Shadows:

```js
{
  type: "DROP_SHADOW" | "INNER_SHADOW",
  color: { r: 0, g: 0, b: 0, a: 0.2 },
  offset: { x: 0, y: 8 },
  radius: 24,
  spread: 0,
  visible: true
}
```

Blurs:

```js
{
  type: "LAYER_BLUR" | "BACKGROUND_BLUR",
  radius: 24,
  visible: true
}
```

## Extended Effects

Use these only when the current runtime/tool accepts them:

- `NOISE`: monotone, duotone, or multitone noise variants depending on current typings.
- `TEXTURE`: texture effects with image/scale/rotation/opacity fields depending on current typings.
- `GLASS`: glass effect fields depending on current typings.
- Progressive blur: blur variants where the effect has progressive blur fields rather than a single uniform blur.

If runtime validation fails, fall back to a core effect approximation or give manual Figma steps.

## Variable Binding

Use `figma.variables.setBoundVariableForEffect(effect, field, variable)` where supported and write the returned effect back into `node.effects`.

Supported fields in current typings:

- Shadow effects: `color`, `radius`, `spread`, `offsetX`, `offsetY`.
- Blur effects: `radius`.
- Noise, texture, and glass effects: no variable bindings in current typings.

Do not bind HEX strings. Figma effect colors are RGBA objects with channels from `0` to `1`.

## Visual Recipes

Glow:

```js
{
  type: "DROP_SHADOW",
  color: { r: 0.22, g: 0.55, b: 1, a: 0.45 },
  offset: { x: 0, y: 0 },
  radius: 32,
  spread: 0,
  visible: true
}
```

Glassmorphism:

- Use translucent fill on the node, typically alpha below `1`.
- Add `BACKGROUND_BLUR`.
- Add subtle shadow or stroke only if the design system permits it.
