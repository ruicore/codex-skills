#!/usr/bin/env python3
"""Create a local Feishu publication package from authoritative Markdown.

The source file is read-only. PlantUML fences are extracted because Feishu
requires them to be inserted separately through UML Board.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


PLANTUML_FENCE = re.compile(
    r"^```plantuml[ \t]*\r?\n(?P<body>.*?)^```[ \t]*$",
    flags=re.DOTALL | re.MULTILINE | re.IGNORECASE,
)
MANUAL_NUMBERED_HEADING = re.compile(
    r"^(?P<marks>#{2,6})[ \t]+(?P<title>\d+(?:\.\d+)*\.?[ \t]+.+)$",
    flags=re.MULTILINE,
)
FENCED_CODE = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.DOTALL | re.MULTILINE)

PROCESS_PHRASES = (
    "一句话结论",
    "已确认的关键决策",
    "为什么不是",
    "现有表最小扩展",
    "（PlantUML）",
    "【图：",
)
DEFERRED_MARKERS = ("待定", "TBD", "TODO")
PLANTUML_COMPATIBILITY_PATTERNS = (
    (
        re.compile(r"^\s*diamond\s+", flags=re.MULTILINE | re.IGNORECASE),
        "Standalone 'diamond' is not portable to Feishu's embedded PlantUML. "
        "Use activity-diagram if/then/else/endif or supported rectangle nodes.",
    ),
    (
        re.compile(r"^\s*!include(?:url)?\s+https?://", flags=re.MULTILINE | re.IGNORECASE),
        "Remote PlantUML includes are not suitable for a durable Feishu document.",
    ),
)


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith(r"\|"):
        stripped = stripped[:-1]
    return [
        cell.strip().replace(r"\|", "|")
        for cell in re.split(r"(?<!\\)\|", stripped)
    ]


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells
    )


def display_width(text: str) -> int:
    plain = re.sub(r"`([^`]*)`", r"\1", text)
    plain = re.sub(r"!?(?:\[([^]]*)\])\([^)]*\)", r"\1", plain)
    return sum(
        2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        for char in plain
    )


def normalized_percentages(weights: list[int]) -> list[int]:
    total = sum(weights) or 1
    exact = [100 * weight / total for weight in weights]
    result = [int(value) for value in exact]
    remainder = 100 - sum(result)
    order = sorted(
        range(len(weights)), key=lambda index: exact[index] - result[index], reverse=True
    )
    for index in order[:remainder]:
        result[index] += 1
    return result


def suggested_table_widths(rows: list[list[str]], columns: int) -> list[int]:
    weights: list[int] = []
    for column in range(columns):
        widths = [
            display_width(row[column])
            for row in rows
            if column < len(row) and row[column]
        ]
        weights.append(max(8, min(60, max(widths, default=8))))
    return normalized_percentages(weights)


def extract_markdown_tables(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    tables: list[dict[str, object]] = []
    in_fence = False
    index = 0
    while index < len(lines) - 1:
        line = lines[index]
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            index += 1
            continue
        if in_fence or "|" not in line or "|" not in lines[index + 1]:
            index += 1
            continue

        header = split_markdown_row(line)
        separator = split_markdown_row(lines[index + 1])
        if len(header) < 2 or len(separator) != len(header) or not is_table_separator(separator):
            index += 1
            continue

        rows = [header]
        cursor = index + 2
        while cursor < len(lines):
            candidate = lines[cursor]
            if not candidate.strip() or "|" not in candidate:
                break
            cells = split_markdown_row(candidate)
            if len(cells) != len(header):
                break
            rows.append(cells)
            cursor += 1

        tables.append(
            {
                "ordinal": len(tables) + 1,
                "line": index + 1,
                "headers": header,
                "columns": len(header),
                "data_rows": len(rows) - 1,
                "suggested_width_percent": suggested_table_widths(rows, len(header)),
                "feishu_layout_status": "required",
            }
        )
        index = cursor
    return tables


def plantuml_compatibility_warnings(text: str) -> list[dict[str, object]]:
    warnings: list[dict[str, object]] = []
    for pattern, message in PLANTUML_COMPATIBILITY_PATTERNS:
        for match in pattern.finditer(text):
            warnings.append(
                {
                    "line": text.count("\n", 0, match.start()) + 1,
                    "text": match.group(0).strip(),
                    "message": message,
                }
            )
    return warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Markdown/HTML and extracted PlantUML for Feishu publishing."
    )
    parser.add_argument("source", type=Path, help="Authoritative UTF-8 Markdown file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for generated publication artifacts",
    )
    parser.add_argument(
        "--name",
        help="Output stem; defaults to the source filename stem",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned artifacts without writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated artifacts that already exist",
    )
    return parser.parse_args()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def markdown_to_html(text: str) -> str:
    try:
        import markdown  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "Python package 'markdown' is required. Install it in the active "
            "workspace environment or use the repository's existing publisher."
        ) from exc

    fragment = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>Feishu publication draft</title>\n"
        "</head>\n"
        "<body>\n"
        f"{fragment.rstrip()}\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> None:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"Source Markdown does not exist: {source}")

    raw = source.read_bytes()
    text = raw.decode("utf-8-sig")
    output_dir = args.output_dir.resolve()
    diagrams_dir = output_dir / "diagrams"

    stem = args.name or source.stem
    diagrams: list[dict[str, object]] = []

    def extract_diagram(match: re.Match[str]) -> str:
        ordinal = len(diagrams) + 1
        filename = f"diagram-{ordinal:02d}.puml"
        diagram_path = diagrams_dir / filename
        diagram_text = match.group("body").strip() + "\n"
        compatibility_warnings = plantuml_compatibility_warnings(diagram_text)
        diagrams.append(
            {
                "ordinal": ordinal,
                "path": str(diagram_path),
                "sha256": sha256_bytes(diagram_text.encode("utf-8")),
                "feishu_preview_status": "required",
                "compatibility_warnings": compatibility_warnings,
                "content": diagram_text,
            }
        )
        return f"\n**图位 {ordinal:02d}：请在飞书中插入 `{filename}`，完成后删除本行。**\n"

    publish_text = PLANTUML_FENCE.sub(extract_diagram, text).rstrip() + "\n"

    publish_md = output_dir / f"{stem}.publish.md"
    publish_html = output_dir / f"{stem}.publish.html"
    manifest_path = output_dir / "publish-manifest.json"

    numbered_headings = [
        {
            "line": text.count("\n", 0, match.start()) + 1,
            "text": match.group("title"),
        }
        for match in MANUAL_NUMBERED_HEADING.finditer(text)
    ]
    process_hits = {
        phrase: text.count(phrase) for phrase in PROCESS_PHRASES if phrase in text
    }
    deferred_hits = {
        marker: text.count(marker) for marker in DEFERRED_MARKERS if marker in text
    }
    tables = extract_markdown_tables(text)
    diagram_warnings = [
        {
            "diagram": diagram["ordinal"],
            "path": diagram["path"],
            "warnings": diagram["compatibility_warnings"],
        }
        for diagram in diagrams
        if diagram["compatibility_warnings"]
    ]

    planned_files = [publish_md, publish_html, manifest_path]
    planned_files.extend(Path(str(diagram["path"])) for diagram in diagrams)
    existing_files = [str(path) for path in planned_files if path.exists()]
    plan = {
        "source": str(source),
        "source_sha256": sha256_bytes(raw),
        "output_directory": str(output_dir),
        "planned_files": [str(path) for path in planned_files],
        "existing_files": existing_files,
        "plantuml_diagrams": len(diagrams),
        "tables": len(tables),
        "table_layout_checklist": tables,
        "plantuml_compatibility_warnings": diagram_warnings,
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    if existing_files and not args.force:
        raise SystemExit(
            "Refusing to overwrite generated artifacts. Review --dry-run output "
            "and rerun with --force if the target is correct:\n- "
            + "\n- ".join(existing_files)
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    publish_md.write_text(publish_text, encoding="utf-8")
    publish_html.write_text(markdown_to_html(publish_text), encoding="utf-8")
    for diagram in diagrams:
        Path(str(diagram["path"])).write_text(
            str(diagram["content"]), encoding="utf-8"
        )

    manifest_diagrams = [
        {key: value for key, value in diagram.items() if key != "content"}
        for diagram in diagrams
    ]
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(source),
            "sha256": sha256_bytes(raw),
            "bytes": len(raw),
        },
        "outputs": {
            "publish_markdown": str(publish_md),
            "publish_html": str(publish_html),
            "diagrams_directory": str(diagrams_dir),
        },
        "inventory": {
            "headings": len(re.findall(r"^#{1,6}[ \t]+", text, flags=re.MULTILINE)),
            "tables": len(tables),
            "fenced_code_blocks": len(FENCED_CODE.findall(text)),
            "plantuml_diagrams": len(diagrams),
        },
        "tables": tables,
        "diagrams": manifest_diagrams,
        "review_warnings": {
            "manual_numbered_headings": numbered_headings,
            "discussion_or_process_phrases": process_hits,
            "deferred_markers_to_confirm": deferred_hits,
            "plantuml_compatibility": diagram_warnings,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
