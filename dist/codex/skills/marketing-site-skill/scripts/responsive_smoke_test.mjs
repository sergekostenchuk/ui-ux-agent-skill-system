#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const result = {};
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i].startsWith("--")) {
      result[argv[i].slice(2)] = argv[i + 1];
      i += 1;
    }
  }
  return result;
}

const args = parseArgs(process.argv);
if (!args.url || !args.out) {
  console.error("Usage: node scripts/responsive_smoke_test.mjs --url <url> --out <reports/visual-smoke>");
  process.exit(2);
}

const summary = {
  url: args.url,
  started_at: new Date().toISOString(),
  viewports_planned: [
    { name: "desktop", width: 1280, height: 800 },
    { name: "mobile", width: 390, height: 844 }
  ],
  checks: {
    fetch_reachable: false,
    html_non_empty: false,
    browser_screenshots: "skipped-no-browser-driver"
  },
  errors: []
};

try {
  const response = await fetch(args.url);
  const text = await response.text();
  summary.status = response.status;
  summary.checks.fetch_reachable = response.ok;
  summary.checks.html_non_empty = text.trim().length > 0;
  summary.html_length = text.length;
} catch (error) {
  summary.errors.push(String(error && error.message ? error.message : error));
}

fs.mkdirSync(args.out, { recursive: true });
fs.writeFileSync(path.join(args.out, "summary.json"), JSON.stringify(summary, null, 2) + "\n");
console.log(JSON.stringify(summary));
process.exit(summary.checks.fetch_reachable && summary.checks.html_non_empty ? 0 : 1);
