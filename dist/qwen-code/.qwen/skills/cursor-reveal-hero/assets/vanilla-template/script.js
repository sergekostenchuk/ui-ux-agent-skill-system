const canvas = document.querySelector("#bioRevealCanvas");
const ctx = canvas.getContext("2d");

const maskCanvas = document.createElement("canvas");
const maskCtx = maskCanvas.getContext("2d");
const revealCanvas = document.createElement("canvas");
const revealCtx = revealCanvas.getContext("2d");

const settings = {
  radius: 245,
  feather: 0.8,
  fade: 0.028,
  strength: 0.82,
  opacity: 0.78,
  lerp: 0.14,
  idleStrength: 0
};

const pointer = {
  active: false,
  targetX: 0,
  targetY: 0,
  x: 0,
  y: 0,
  initialized: false
};

const baseImage = new Image();
const revealImage = new Image();
baseImage.decoding = "async";
revealImage.decoding = "async";
baseImage.src = canvas.dataset.baseSrc;
revealImage.src = canvas.dataset.revealSrc;

let width = 0;
let height = 0;
let loaded = false;

window.revealSettings = settings;
window.clearRevealMask = clearMask;

function resizeCanvases() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  width = Math.max(1, Math.round(rect.width * dpr));
  height = Math.max(1, Math.round(rect.height * dpr));

  for (const target of [canvas, maskCanvas, revealCanvas]) {
    target.width = width;
    target.height = height;
  }

  clearMask();
}

function clearMask() {
  maskCtx.clearRect(0, 0, width, height);
}

function drawCover(targetCtx, image) {
  if (!image.complete || image.naturalWidth === 0) {
    drawFallback(targetCtx);
    return;
  }
  const scale = Math.max(width / image.naturalWidth, height / image.naturalHeight);
  const drawWidth = image.naturalWidth * scale;
  const drawHeight = image.naturalHeight * scale;
  const x = (width - drawWidth) / 2;
  const y = (height - drawHeight) / 2;
  targetCtx.drawImage(image, x, y, drawWidth, drawHeight);
}

function drawFallback(targetCtx) {
  const gradient = targetCtx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, "#f1ecff");
  gradient.addColorStop(0.55, "#cfc2f2");
  gradient.addColorStop(1, "#8ea7e8");
  targetCtx.fillStyle = gradient;
  targetCtx.fillRect(0, 0, width, height);
}

function drawHotspot(x, y, strength = settings.strength) {
  const radius = settings.radius * Math.min(window.devicePixelRatio || 1, 2);
  const inner = Math.max(0.01, 1 - settings.feather);
  const gradient = maskCtx.createRadialGradient(x, y, radius * inner, x, y, radius);
  gradient.addColorStop(0, `rgba(255, 255, 255, ${strength})`);
  gradient.addColorStop(0.58, `rgba(255, 255, 255, ${strength * 0.58})`);
  gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
  maskCtx.globalCompositeOperation = "source-over";
  maskCtx.fillStyle = gradient;
  maskCtx.beginPath();
  maskCtx.arc(x, y, radius, 0, Math.PI * 2);
  maskCtx.fill();
}

function updateMask() {
  maskCtx.globalCompositeOperation = "destination-out";
  maskCtx.fillStyle = `rgba(0, 0, 0, ${settings.fade})`;
  maskCtx.fillRect(0, 0, width, height);
  maskCtx.globalCompositeOperation = "source-over";

  if (!pointer.active && settings.idleStrength <= 0) return;

  if (!pointer.initialized) {
    pointer.x = pointer.targetX;
    pointer.y = pointer.targetY;
    pointer.initialized = true;
  }

  pointer.x += (pointer.targetX - pointer.x) * settings.lerp;
  pointer.y += (pointer.targetY - pointer.y) * settings.lerp;

  drawHotspot(pointer.x, pointer.y, pointer.active ? settings.strength : settings.idleStrength);
}

function drawCursorBloom() {
  if (!pointer.active) return;
  const radius = settings.radius * 0.42 * Math.min(window.devicePixelRatio || 1, 2);
  const gradient = ctx.createRadialGradient(pointer.x, pointer.y, 0, pointer.x, pointer.y, radius);
  gradient.addColorStop(0, "rgba(255, 255, 255, 0.18)");
  gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(pointer.x, pointer.y, radius, 0, Math.PI * 2);
  ctx.fill();
}

function drawFrame() {
  if (!loaded) {
    ctx.clearRect(0, 0, width, height);
    drawFallback(ctx);
    requestAnimationFrame(drawFrame);
    return;
  }

  updateMask();
  ctx.clearRect(0, 0, width, height);
  drawCover(ctx, baseImage);

  revealCtx.clearRect(0, 0, width, height);
  drawCover(revealCtx, revealImage);
  revealCtx.globalCompositeOperation = "destination-in";
  revealCtx.drawImage(maskCanvas, 0, 0);
  revealCtx.globalCompositeOperation = "source-over";

  ctx.save();
  ctx.globalAlpha = settings.opacity;
  ctx.drawImage(revealCanvas, 0, 0);
  ctx.restore();
  drawCursorBloom();

  requestAnimationFrame(drawFrame);
}

function setPointerFromEvent(event) {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  pointer.targetX = (event.clientX - rect.left) * dpr;
  pointer.targetY = (event.clientY - rect.top) * dpr;
  pointer.active = true;
}

function bindControls() {
  const inputs = document.querySelectorAll("[data-setting]");
  for (const input of inputs) {
    const key = input.dataset.setting;
    const output = document.querySelector(`[data-value-for="${key}"]`);
    const apply = () => {
      settings[key] = Number(input.value);
      if (output) output.textContent = Number(input.value).toFixed(key === "radius" ? 0 : 3).replace(/0+$/, "").replace(/\.$/, "");
      clearMask();
    };
    input.addEventListener("input", apply);
    input.addEventListener("change", apply);
    apply();
  }

  document.querySelector("#clearMaskButton")?.addEventListener("click", clearMask);
}

canvas.addEventListener("pointerenter", setPointerFromEvent);
canvas.addEventListener("pointermove", setPointerFromEvent);
canvas.addEventListener("pointerdown", setPointerFromEvent);
canvas.addEventListener("pointerleave", () => {
  pointer.active = false;
  pointer.initialized = false;
});

window.addEventListener("resize", resizeCanvases);

Promise.allSettled([
  baseImage.decode().catch(() => {}),
  revealImage.decode().catch(() => {})
]).then(() => {
  loaded = true;
});

resizeCanvases();
bindControls();
requestAnimationFrame(drawFrame);
