# Canvas Compositing Pattern

Use this reference for the core render loop.

## Layer Model

Create:

- `canvas` / `ctx`: visible output.
- `maskCanvas` / `maskCtx`: grayscale alpha map for cursor trail.
- `revealCanvas` / `revealCtx`: temporary reveal layer before masking.
- `baseImage`: image visible at all times.
- `revealImage`: image visible only through the mask.

## Frame Order

1. Fade old mask content:

   ```js
   maskCtx.globalCompositeOperation = "destination-out";
   maskCtx.fillStyle = `rgba(0, 0, 0, ${settings.fade})`;
   maskCtx.fillRect(0, 0, width, height);
   maskCtx.globalCompositeOperation = "source-over";
   ```

2. Smooth pointer position with `lerp`.
3. Draw a radial gradient hotspot into `maskCanvas`.
4. Clear visible canvas and draw the base image.
5. Draw reveal image into `revealCanvas`.
6. Apply the mask:

   ```js
   revealCtx.globalCompositeOperation = "destination-in";
   revealCtx.drawImage(maskCanvas, 0, 0);
   revealCtx.globalCompositeOperation = "source-over";
   ```

7. Draw the masked reveal layer over the base with `globalAlpha = settings.opacity`.
8. Optionally draw a subtle cursor bloom over the result.

## Image Fit

Use the same object-fit strategy for both layers. Default to `cover` for hero scenes:

```js
const scale = Math.max(canvasWidth / image.width, canvasHeight / image.height);
const drawWidth = image.width * scale;
const drawHeight = image.height * scale;
const x = (canvasWidth - drawWidth) / 2;
const y = (canvasHeight - drawHeight) / 2;
ctx.drawImage(image, x, y, drawWidth, drawHeight);
```

If the images were prepared to a fixed matching canvas, use exact canvas sizing and avoid independent crop changes.

## Resize

On resize:

- update CSS-independent backing width and height;
- scale contexts for DPR or draw in backing-store coordinates consistently;
- clear `maskCanvas`;
- redraw immediately;
- avoid preserving masks across radically changed dimensions.
