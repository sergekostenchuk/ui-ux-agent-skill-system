#!/usr/bin/env python3
"""Build runtime projections for the UI/UX Agent Skill System."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


SKIP_NAMES = {"__pycache__"}


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def skill_names(root: Path) -> list[str]:
    return sorted(p.name for p in (root / "core" / "skills").iterdir() if p.is_dir() and p.name not in SKIP_NAMES)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def package_version(root: Path) -> str:
    package_json = json.loads((root / "package.json").read_text(encoding="utf-8"))
    return str(package_json["version"])


def build_skill_folder_projection(root: Path, target: Path, subpath: str) -> None:
    skills_target = target / subpath
    skills_target.mkdir(parents=True, exist_ok=True)
    for skill in skill_names(root):
        copy_tree(root / "core" / "skills" / skill, skills_target / skill)
    copy_tree(root / "core" / "shared", skills_target / "_shared")


def build_gemini(root: Path, target: Path) -> None:
    ext = target / "ui-ux-agent-skill-system"
    if ext.exists():
        shutil.rmtree(ext)
    ext.mkdir(parents=True, exist_ok=True)
    skills = skill_names(root)
    write(
        ext / "gemini-extension.json",
        json.dumps(
            {
                "name": "ui-ux-agent-skill-system",
                "version": package_version(root),
                "description": "Vendor-neutral core UI/UX skill system projection for Gemini CLI.",
                "contextFileName": "GEMINI.md",
            },
            indent=2,
        )
        + "\n",
    )
    write(
        ext / "GEMINI.md",
        "# UI/UX Agent Skill System\n\n"
        "Use `senior-ui-ux-orchestrator` as the main chair for UI/UX work. "
        "Route through product UX, SEO/LLM, Pro Max, Stitch, Figma, marketing, webapp, audit, and critic layers as needed.\n\n"
        "Skills included:\n\n"
        + "\n".join(f"- `{name}`" for name in skills)
        + "\n\nSafety: local-first by default. Do not store or print API keys, tokens, cookies, `.env` contents, private screenshots, or private URLs. "
        "External uploads require explicit approval and a data-transfer note.\n\n"
        "For full skill bodies, use the `skills/` folder bundled with this extension.\n",
    )
    build_skill_folder_projection(root, ext, "skills")


def build_generic(root: Path, target: Path, runtime_name: str) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    skills = skill_names(root)
    write(
        target / "AGENTS.md",
        f"# UI/UX Agent Skill System for {runtime_name}\n\n"
        "Primary entrypoint: `senior-ui-ux-orchestrator`.\n\n"
        "Role rule: the orchestrator is the chair. Specialist skills provide input or execute bounded stages. "
        "They do not override the orchestrator's final decision.\n\n"
        "Safety rule: local-first by default. Do not store or print secrets. External services require explicit approval.\n\n"
        "Use `skills-index.md` to choose relevant skill files.\n",
    )
    write(target / "skills-index.md", "\n".join(f"- `{name}`: `skills/{name}/SKILL.md`" for name in skills) + "\n")
    build_skill_folder_projection(root, target, "skills")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--out", default="dist")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    build_skill_folder_projection(root, out / "codex", "skills")
    build_skill_folder_projection(root, out / "claude", "skills")
    build_skill_folder_projection(root, out / "qwen-code", ".qwen/skills")
    build_skill_folder_projection(root, out / "copilot-vscode", ".github/skills")
    build_gemini(root, out / "gemini-cli")
    build_generic(root, out / "glm-zai", "GLM / Z.ai")
    build_generic(root, out / "kimi", "Kimi")
    build_generic(root, out / "generic-agent", "Generic Agent")
    print(f"built adapters into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
