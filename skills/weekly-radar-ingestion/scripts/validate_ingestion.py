#!/usr/bin/env python3
"""Validate weekly radar ingestion consistency."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RADAR_PATH_RE = re.compile(r"radars/\d{4}/\d{4}-\d{2}-\d{2}\.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--date", help="Optional report date to validate, formatted YYYY-MM-DD.")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def as_relative(path_text: str) -> Path:
    return Path(path_text.replace("\\", "/"))


def record_paths(repo: Path, report_date: str) -> tuple[Path, Path]:
    year = report_date[:4]
    return repo / "radars" / year / f"{report_date}.md", repo / "data" / year / f"{report_date}.json"


def validate_record(repo: Path, record: dict[str, Any], source_path: Path, errors: list[str]) -> None:
    date_value = record.get("date")
    if not isinstance(date_value, str) or not DATE_RE.match(date_value):
        errors.append(f"{source_path}: missing or invalid date")
        return

    radar_path, expected_data_path = record_paths(repo, date_value)
    if source_path.resolve() != expected_data_path.resolve():
        errors.append(f"{source_path}: expected data path {expected_data_path.relative_to(repo)}")

    if not radar_path.exists():
        errors.append(f"{source_path}: missing report {radar_path.relative_to(repo)}")

    if record.get("status") != "reviewed":
        errors.append(f"{source_path}: status must be reviewed")

    if record.get("reviewed_by") not in (None, "Ray"):
        errors.append(f"{source_path}: reviewed_by must be Ray when present")

    markdown_path = record.get("markdown_path")
    if isinstance(markdown_path, str):
        if repo.joinpath(as_relative(markdown_path)).resolve() != radar_path.resolve():
            errors.append(f"{source_path}: markdown_path does not match expected report path")
    elif "markdown_path" in record:
        errors.append(f"{source_path}: markdown_path must be a string")

    themes = record.get("themes", [])
    if not isinstance(themes, list) or any(not isinstance(theme, str) or not theme for theme in themes):
        errors.append(f"{source_path}: themes must be an array of non-empty strings")
        return

    for theme in themes:
        theme_path = repo / "themes" / f"{theme}.md"
        if not theme_path.exists():
            errors.append(f"{source_path}: missing theme file themes/{theme}.md")


def validate_theme_files(repo: Path, errors: list[str]) -> None:
    themes_root = repo / "themes"
    if not themes_root.exists():
        return

    for theme_path in sorted(themes_root.glob("*.md")):
        if theme_path.name == "README.md":
            continue
        text = theme_path.read_text(encoding="utf-8")
        for match in RADAR_PATH_RE.finditer(text):
            report_path = repo / match.group(0)
            if not report_path.exists():
                errors.append(f"{theme_path}: missing linked report {match.group(0)}")


def validate_index_path(repo: Path, owner: Path, value: Any, errors: list[str]) -> None:
    if isinstance(value, str) and (
        value.startswith("radars/") or value.startswith("data/") or value.startswith("themes/")
    ):
        if not repo.joinpath(as_relative(value)).exists():
            errors.append(f"{owner}: indexed path does not exist: {value}")


def walk_index_paths(repo: Path, owner: Path, payload: Any, errors: list[str]) -> None:
    if isinstance(payload, dict):
        for value in payload.values():
            walk_index_paths(repo, owner, value, errors)
    elif isinstance(payload, list):
        for item in payload:
            walk_index_paths(repo, owner, item, errors)
    else:
        validate_index_path(repo, owner, payload, errors)


def validate_indexes(repo: Path, report_date: str | None, errors: list[str]) -> None:
    index_root = repo / "indexes"
    if not index_root.exists():
        errors.append("indexes/ directory is missing")
        return

    saw_report_date = report_date is None
    for index_path in sorted(index_root.glob("*.json")):
        payload = load_json(index_path)
        walk_index_paths(repo, index_path, payload, errors)
        if report_date and report_date in json.dumps(payload, ensure_ascii=False):
            saw_report_date = True

    if not saw_report_date:
        errors.append(f"indexes/: no JSON index references {report_date}")


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    errors: list[str] = []

    if args.date and not DATE_RE.match(args.date):
        errors.append("--date must use YYYY-MM-DD")

    for dirname in ("radars", "data", "themes", "indexes"):
        if not (repo / dirname).exists():
            errors.append(f"{dirname}/ directory is missing")

    if args.date:
        radar_path, data_path = record_paths(repo, args.date)
        if not radar_path.exists():
            errors.append(f"missing report {radar_path.relative_to(repo)}")
        if not data_path.exists():
            errors.append(f"missing metadata {data_path.relative_to(repo)}")
            data_files: list[Path] = []
        else:
            data_files = [data_path]
    else:
        data_files = sorted((repo / "data").glob("*/*.json"))

    for data_path in data_files:
        payload = load_json(data_path)
        if not isinstance(payload, dict):
            errors.append(f"{data_path}: metadata must be a JSON object")
            continue
        validate_record(repo, payload, data_path, errors)

    validate_theme_files(repo, errors)
    validate_indexes(repo, args.date, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    target = args.date or "repository"
    print(f"OK: weekly radar ingestion consistency validated for {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
