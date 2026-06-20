#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const STATE_TERMS = {
  loading: [/loading/i, /skeleton/i, /spinner/i, /pending/i],
  empty: [/empty/i, /no\s+data/i, /no\s+results/i],
  error: [/error/i, /failed/i, /catch\s*\(/i],
  disabled: [/disabled/i, /aria-disabled/i],
  focus: [/focus:/i, /focus-visible/i, /:focus/i],
  selected: [/selected/i, /aria-selected/i],
  submitting: [/submitting/i, /isSubmitting/i, /saving/i],
  success: [/success/i, /saved/i, /complete/i]
};

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

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || ["node_modules", "dist", "build", "reports"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, files);
    if (entry.isFile() && /\.(tsx|ts|jsx|js|vue|svelte|html|css)$/.test(entry.name)) files.push(full);
  }
  return files;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.root || !args.out) {
    console.error("Usage: node scripts/check_state_coverage.ts --root <project-root> --out <report.json>");
    process.exit(2);
  }
  const root = path.resolve(args.root);
  const files = walk(root);
  const combined = files.map((file) => fs.readFileSync(file, "utf8")).join("\n");
  const states = {};
  for (const [state, patterns] of Object.entries(STATE_TERMS)) {
    states[state] = {
      present: patterns.some((pattern) => pattern.test(combined)),
      matched_terms: patterns.filter((pattern) => pattern.test(combined)).map(String)
    };
  }
  const missing = Object.entries(states).filter(([, value]) => !value.present).map(([state]) => state);
  const report = {
    root,
    files_scanned: files.length,
    passed: missing.length === 0,
    states,
    missing,
    note: missing.length ? "Missing markers require manual review; absence of a term is not proof the state is absent." : "All state markers found."
  };
  fs.mkdirSync(path.dirname(args.out), { recursive: true });
  fs.writeFileSync(args.out, JSON.stringify(report, null, 2) + "\n");
  console.log(JSON.stringify(report));
  process.exit(0);
}

main();
