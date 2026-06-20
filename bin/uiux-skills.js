#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const packageRoot = path.resolve(__dirname, "..");

const targets = {
  codex: {
    source: "dist/codex/skills",
    defaultDest: () => path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "skills"),
    description: "Install Codex skill folders"
  },
  claude: {
    source: "dist/claude/skills",
    defaultDest: null,
    description: "Install Claude/Claude Code skill folders; pass --dest"
  },
  "qwen-code": {
    source: "dist/qwen-code/.qwen/skills",
    defaultDest: () => path.join(process.cwd(), ".qwen", "skills"),
    description: "Install project-local Qwen Code skills"
  },
  "copilot-vscode": {
    source: "dist/copilot-vscode/.github/skills",
    defaultDest: () => path.join(process.cwd(), ".github", "skills"),
    description: "Install project-local VS Code/Copilot skills"
  },
  "gemini-cli": {
    source: "dist/gemini-cli/ui-ux-agent-skill-system",
    defaultDest: null,
    description: "Install Gemini CLI extension; pass --dest"
  },
  "glm-zai": {
    source: "dist/glm-zai",
    defaultDest: () => path.join(process.cwd(), ".agent-skills", "glm-zai"),
    description: "Install GLM/Z.ai generic agent projection"
  },
  kimi: {
    source: "dist/kimi",
    defaultDest: () => path.join(process.cwd(), ".agent-skills", "kimi"),
    description: "Install Kimi generic agent projection"
  },
  "generic-agent": {
    source: "dist/generic-agent",
    defaultDest: () => path.join(process.cwd(), ".agent-skills", "generic-agent"),
    description: "Install generic AGENTS.md projection"
  }
};

function usage() {
  const targetLines = Object.entries(targets)
    .map(([name, cfg]) => `  ${name.padEnd(15)} ${cfg.description}`)
    .join("\n");
  console.log(`UI/UX Agent Skill System installer

Usage:
  uiux-skills list
  uiux-skills path
  uiux-skills install <target> [--dest <path>] [--force] [--dry-run]

Targets:
${targetLines}

Examples:
  uiux-skills install codex
  uiux-skills install qwen-code
  uiux-skills install claude --dest ~/.claude/skills
  uiux-skills install gemini-cli --dest ~/.gemini/extensions/ui-ux-agent-skill-system
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dest") {
      args.dest = argv[++i];
    } else if (arg === "--force") {
      args.force = true;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "-h" || arg === "--help") {
      args.help = true;
    } else {
      args._.push(arg);
    }
  }
  return args;
}

function copyRecursive(src, dest, options, stats) {
  const entry = fs.statSync(src);
  if (entry.isDirectory()) {
    if (!fs.existsSync(dest)) {
      if (!options.dryRun) fs.mkdirSync(dest, { recursive: true });
      stats.createdDirs += 1;
    }
    for (const child of fs.readdirSync(src)) {
      copyRecursive(path.join(src, child), path.join(dest, child), options, stats);
    }
    return;
  }

  if (fs.existsSync(dest) && !options.force) {
    stats.skipped += 1;
    return;
  }

  if (!options.dryRun) {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
  stats.copied += 1;
}

function install(targetName, args) {
  const target = targets[targetName];
  if (!target) {
    console.error(`Unknown target: ${targetName}\n`);
    usage();
    process.exitCode = 2;
    return;
  }

  const source = path.join(packageRoot, target.source);
  if (!fs.existsSync(source)) {
    console.error(`Missing source projection: ${source}`);
    process.exitCode = 1;
    return;
  }

  const dest = args.dest
    ? path.resolve(process.cwd(), args.dest.replace(/^~(?=$|\/|\\)/, os.homedir()))
    : target.defaultDest && target.defaultDest();

  if (!dest) {
    console.error(`Target "${targetName}" requires --dest because this runtime has no safe universal install directory.`);
    process.exitCode = 2;
    return;
  }

  const stats = { copied: 0, skipped: 0, createdDirs: 0 };
  copyRecursive(source, dest, args, stats);
  console.log(`${args.dryRun ? "Dry run" : "Installed"} ${targetName}`);
  console.log(`source: ${source}`);
  console.log(`dest:   ${dest}`);
  console.log(`files copied: ${stats.copied}`);
  console.log(`files skipped: ${stats.skipped}`);
  if (stats.skipped > 0 && !args.force) {
    console.log("Use --force to overwrite existing files.");
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command || args.help) {
    usage();
    return;
  }

  if (command === "list") {
    Object.entries(targets).forEach(([name, cfg]) => {
      console.log(`${name}\t${cfg.description}`);
    });
    return;
  }

  if (command === "path") {
    console.log(packageRoot);
    return;
  }

  if (command === "install") {
    install(args._[1], args);
    return;
  }

  console.error(`Unknown command: ${command}\n`);
  usage();
  process.exitCode = 2;
}

main();

