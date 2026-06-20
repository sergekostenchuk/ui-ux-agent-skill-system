#!/usr/bin/env node

function getArg(name, fallback = null) {
  const index = process.argv.indexOf(name);
  if (index === -1 || index + 1 >= process.argv.length) return fallback;
  return process.argv[index + 1];
}

function fail(message, extra = {}) {
  console.error(JSON.stringify({ ok: false, message, ...extra }, null, 2));
  process.exit(1);
}

const url = getArg("--url", process.argv[2]);
const canvasSelector = getArg("--canvas", "#bioRevealCanvas");
const screenshotPath = getArg("--screenshot", null);

if (!url || url.startsWith("--")) {
  fail("Provide a URL with --url http://127.0.0.1:PORT/");
}

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch (error) {
  fail("Missing playwright dependency. Install it in the target project or run from an environment that provides playwright.", {
    error: String(error && error.message ? error.message : error),
  });
}

function checksumFromData(data, step) {
  let checksum = 0;
  let nonTransparent = 0;
  let lumaSum = 0;
  let lumaSq = 0;
  let samples = 0;
  for (let i = 0; i < data.length; i += 4 * step) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];
    const a = data[i + 3];
    const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    checksum = (checksum + ((r * 3 + g * 5 + b * 7 + a * 11) >>> 0)) >>> 0;
    if (a > 12) nonTransparent += 1;
    lumaSum += luma;
    lumaSq += luma * luma;
    samples += 1;
  }
  const mean = lumaSum / Math.max(samples, 1);
  const variance = lumaSq / Math.max(samples, 1) - mean * mean;
  return {
    checksum,
    samples,
    nonTransparentRatio: nonTransparent / Math.max(samples, 1),
    lumaVariance: variance,
  };
}

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 30000 });
  await page.waitForSelector(canvasSelector, { timeout: 10000 });

  const box = await page.locator(canvasSelector).boundingBox();
  if (!box) fail("Canvas exists but has no layout box.", { canvasSelector });

  const stats = async () =>
    page.$eval(canvasSelector, (canvas) => {
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!ctx) return { error: "2d context unavailable" };
      const width = canvas.width;
      const height = canvas.height;
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;
      const step = Math.max(1, Math.floor((width * height) / 40000));
      let checksum = 0;
      let nonTransparent = 0;
      let lumaSum = 0;
      let lumaSq = 0;
      let samples = 0;
      for (let i = 0; i < data.length; i += 4 * step) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];
        const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b;
        checksum = (checksum + ((r * 3 + g * 5 + b * 7 + a * 11) >>> 0)) >>> 0;
        if (a > 12) nonTransparent += 1;
        lumaSum += luma;
        lumaSq += luma * luma;
        samples += 1;
      }
      const mean = lumaSum / Math.max(samples, 1);
      return {
        width,
        height,
        checksum,
        samples,
        nonTransparentRatio: nonTransparent / Math.max(samples, 1),
        lumaVariance: lumaSq / Math.max(samples, 1) - mean * mean,
      };
    });

  await page.waitForTimeout(300);
  const before = await stats();
  if (before.error) fail(before.error);
  if (before.width < 10 || before.height < 10) fail("Canvas backing store is too small.", { before });
  if (before.nonTransparentRatio < 0.01 || before.lumaVariance < 1) fail("Canvas appears blank or nearly flat.", { before });

  const x0 = box.x + box.width * 0.25;
  const y0 = box.y + box.height * 0.50;
  const x1 = box.x + box.width * 0.75;
  const y1 = box.y + box.height * 0.38;
  await page.mouse.move(x0, y0);
  await page.mouse.down();
  for (let i = 0; i <= 16; i += 1) {
    const t = i / 16;
    await page.mouse.move(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t);
  }
  await page.mouse.up();
  await page.waitForTimeout(500);

  const after = await stats();
  const checksumDelta = Math.abs(after.checksum - before.checksum);
  if (checksumDelta === 0) {
    fail("Pointer movement did not change sampled canvas pixels.", { before, after, checksumDelta });
  }

  if (screenshotPath) {
    await page.screenshot({ path: screenshotPath, fullPage: true });
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        url,
        canvasSelector,
        before,
        after,
        checksumDelta,
        screenshot: screenshotPath,
      },
      null,
      2,
    ),
  );
} finally {
  await browser.close();
}
