#!/usr/bin/env python3
"""Install skills from this repository into a Codex skills directory."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "skills" / "index.json"
DEFAULT_TARGET = Path("~/.codex/skills")


def load_skills() -> list[dict[str, object]]:
    try:
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"registry not found: {INDEX_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON in {INDEX_PATH}: {exc}") from exc

    skills = data.get("skills")
    if not isinstance(skills, list):
        raise RuntimeError(f"{INDEX_PATH} must contain a top-level 'skills' list")
    return [skill for skill in skills if isinstance(skill, dict)]


def select_skills(
    skills: list[dict[str, object]], name: str | None, category: str | None
) -> list[dict[str, object]]:
    if name is not None:
        matches = [skill for skill in skills if skill.get("name") == name]
        if not matches:
            raise RuntimeError(f"unknown skill: {name}")
        return matches

    if category is not None:
        matches = [skill for skill in skills if skill.get("category") == category]
        if not matches:
            raise RuntimeError(f"no skills found in category: {category}")
        return matches

    raise RuntimeError("pass a skill name or --category")


def resolve_skill_source(skill: dict[str, object]) -> Path:
    raw_path = skill.get("path")
    name = skill.get("name")
    if not isinstance(raw_path, str) or not raw_path:
        raise RuntimeError(f"skill {name!r} has no valid path in the registry")

    source = (REPO_ROOT / Path(raw_path)).resolve()
    try:
        source.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise RuntimeError(f"skill path escapes repository: {raw_path}") from exc
    if not source.is_dir():
        raise RuntimeError(f"skill source directory does not exist: {raw_path}")
    return source


def plan_installs(
    skills: list[dict[str, object]], target: Path
) -> list[tuple[str, Path, Path]]:
    plan: list[tuple[str, Path, Path]] = []
    for skill in skills:
        name = skill.get("name")
        if not isinstance(name, str) or not name:
            raise RuntimeError("registry entry has no valid skill name")
        source = resolve_skill_source(skill)
        destination = target / name
        plan.append((name, source, destination))
    return plan


def check_conflicts(plan: list[tuple[str, Path, Path]], overwrite: bool) -> None:
    conflicts = [
        destination
        for _, _, destination in plan
        if destination.exists() and not overwrite
    ]
    if conflicts:
        details = "\n".join(f"- {path}" for path in conflicts)
        raise RuntimeError(
            "refusing to overwrite existing skill directories without --overwrite:\n"
            f"{details}"
        )


def install_plan(
    plan: list[tuple[str, Path, Path]], target: Path, dry_run: bool, overwrite: bool
) -> None:
    action = "Would install" if dry_run else "Installing"
    print(f"{action} {len(plan)} skill(s) into {target}")

    for name, source, destination in plan:
        if dry_run:
            status = "overwrite" if destination.exists() and overwrite else "copy"
            print(f"- {name}: {source} -> {destination} ({status})")
            continue

        target.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if not destination.is_dir():
                raise RuntimeError(f"destination exists and is not a directory: {destination}")
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        print(f"- installed {name}: {destination}")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install skills from skills/index.json.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Name of one skill to install. Mutually exclusive with --category.",
    )
    parser.add_argument("--category", help="Install all skills in this category.")
    parser.add_argument(
        "--target",
        default=str(DEFAULT_TARGET),
        help="Destination skills directory. Defaults to ~/.codex/skills.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without copying.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing destination skill directories.",
    )
    args = parser.parse_args(list(argv))

    if bool(args.name) == bool(args.category):
        parser.error("pass exactly one of a skill name or --category")
    return args


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    target = Path(args.target).expanduser().resolve()

    try:
        skills = load_skills()
        selected = select_skills(skills, args.name, args.category)
        plan = plan_installs(selected, target)
        check_conflicts(plan, args.overwrite)
        install_plan(plan, target, args.dry_run, args.overwrite)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
