#!/usr/bin/env python3
"""List skills from the repository registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "skills" / "index.json"
DISPLAY_FIELDS = (
    "name",
    "category",
    "maturity",
    "side_effect_level",
    "path",
    "purpose",
)


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


def filter_skills(
    skills: Iterable[dict[str, object]], category: str | None, maturity: str | None
) -> list[dict[str, object]]:
    filtered = list(skills)
    if category is not None:
        filtered = [skill for skill in filtered if skill.get("category") == category]
    if maturity is not None:
        filtered = [skill for skill in filtered if skill.get("maturity") == maturity]
    return filtered


def render_table(skills: list[dict[str, object]]) -> None:
    if not skills:
        print("No skills matched.")
        return

    rows = [
        {field: stringify(skill.get(field, "")) for field in DISPLAY_FIELDS}
        for skill in skills
    ]
    widths = {
        field: max(len(field), *(len(row[field]) for row in rows))
        for field in DISPLAY_FIELDS
    }

    header = "  ".join(field.ljust(widths[field]) for field in DISPLAY_FIELDS)
    separator = "  ".join("-" * widths[field] for field in DISPLAY_FIELDS)
    print(header)
    print(separator)
    for row in rows:
        print("  ".join(row[field].ljust(widths[field]) for field in DISPLAY_FIELDS))
    print(f"\n{len(rows)} skill(s) listed.")


def stringify(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List skills from skills/index.json.",
    )
    parser.add_argument("--category", help="Only show skills in this category.")
    parser.add_argument("--maturity", help="Only show skills with this maturity.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        skills = load_skills()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    render_table(filter_skills(skills, args.category, args.maturity))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
