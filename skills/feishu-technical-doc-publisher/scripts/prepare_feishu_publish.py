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
from html.parser import HTMLParser
from pathlib import Path


FENCED_BLOCK = re.compile(
    r"^(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)\n(?P<body>.*?)^(?P=fence)[ \t]*$",
    flags=re.DOTALL | re.MULTILINE | re.IGNORECASE,
)
MANUAL_NUMBERED_HEADING = re.compile(
    r"^(?P<marks>#{2,6})[ \t]+(?P<title>\d+(?:\.\d+)*\.?[ \t]+.+)$",
    flags=re.MULTILINE,
)
DEFAULT_LONG_CODE_LINES = 20

PROCESS_PHRASES = (
    "一句话结论",
    "已确认的关键决策",
    "为什么不是",
    "现有表最小扩展",
    "（PlantUML）",
    "【图：",
    "请在飞书中插入",
    "完成后删除本行",
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


def diagram_slot_id(ordinal: int) -> str:
    return f"diagram-{ordinal:02d}"


def diagram_placeholder(ordinal: int) -> str:
    """Return a visible local slot without embedding an execution command."""
    return f"【图位 {ordinal:02d}｜发布占位】"


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


def extract_plantuml_diagrams(
    text: str, diagrams_dir: Path
) -> tuple[str, list[dict[str, object]]]:
    diagrams: list[dict[str, object]] = []

    def replace_fence(match: re.Match[str]) -> str:
        if match.group("info").strip().casefold() != "plantuml":
            return match.group(0)
        ordinal = len(diagrams) + 1
        slot_id = diagram_slot_id(ordinal)
        filename = f"{slot_id}.puml"
        diagram_path = diagrams_dir / filename
        diagram_text = match.group("body").strip() + "\n"
        compatibility_warnings = plantuml_compatibility_warnings(diagram_text)
        placeholder = diagram_placeholder(ordinal)
        diagrams.append(
            {
                "ordinal": ordinal,
                "slot_id": slot_id,
                "placeholder": placeholder,
                "path": str(diagram_path),
                "sha256": sha256_bytes(diagram_text.encode("utf-8")),
                "feishu_preview_status": "required",
                "compatibility_warnings": compatibility_warnings,
                "content": diagram_text,
            }
        )
        return f"\n**{placeholder}**\n"

    # Scan every complete fence so a PlantUML example inside a longer code fence
    # remains an example rather than becoming an unintended diagram.
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    publish_text = FENCED_BLOCK.sub(replace_fence, normalized).rstrip() + "\n"
    return publish_text, diagrams


class PublicationStructure(HTMLParser):
    """Read the generated HTML, which is also the actual rich-text payload."""

    def __init__(self, long_code_lines: int) -> None:
        super().__init__(convert_charrefs=True)
        self.long_code_lines = long_code_lines
        self.headings: list[dict[str, object]] = []
        self.code_blocks: list[dict[str, object]] = []
        self.tables: list[dict[str, object]] = []
        self._heading: tuple[str, list[str]] | None = None
        self._code: dict[str, object] | None = None
        self._code_text: list[str] = []
        self._table_stack: list[dict[str, object]] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"head", "script", "style", "template"}:
            self._ignored_depth += 1
        if self._ignored_depth:
            return
        attributes = dict(attrs)
        if tag == "pre":
            self._code = {"language": None}
            self._code_text = []
        elif tag == "code" and self._code is not None:
            for value in (attributes.get("class") or "").split():
                if value.startswith("language-"):
                    self._code["language"] = value.removeprefix("language-")
        elif re.fullmatch(r"h[1-6]", tag) and self._code is None:
            self._heading = (tag, [])
        elif tag == "table":
            table: dict[str, object] = {"ordinal": len(self.tables) + 1, "rows": []}
            self.tables.append(table)
            self._table_stack.append(table)
        elif tag == "tr" and self._table_stack:
            self._table_stack[-1]["row"] = []
        elif tag in {"th", "td"} and self._table_stack:
            self._table_stack[-1]["cell"] = []
        elif tag == "br":
            self.handle_data("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        if self._heading is not None:
            self._heading[1].append(data)
        if self._code is not None:
            self._code_text.append(data)
        if self._table_stack and "cell" in self._table_stack[-1]:
            self._table_stack[-1]["cell"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"head", "script", "style", "template"} and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if self._heading is not None and tag == self._heading[0]:
            self.headings.append({
                "ordinal": len(self.headings) + 1,
                "level": int(tag[1]),
                "text": " ".join("".join(self._heading[1]).split()),
            })
            self._heading = None
        elif tag == "pre" and self._code is not None:
            content = "".join(self._code_text).replace("\r\n", "\n").replace("\r", "\n")
            lines = content.splitlines()
            nonempty = [line for line in lines if line.strip()]
            marker = next((line for line in reversed(nonempty) if any(c.isalnum() for c in line)), "")
            self.code_blocks.append({
                "ordinal": len(self.code_blocks) + 1,
                "language": self._code["language"],
                "line_count": len(lines),
                "sha256": sha256_bytes(content.encode("utf-8")),
                "requires_tail_check": len(lines) >= self.long_code_lines,
                "tail_marker": marker or (nonempty[-1] if nonempty else ""),
                "tail_lines": lines[-3:],
            })
            self._code = None
            self._code_text = []
        elif tag in {"th", "td"} and self._table_stack:
            table = self._table_stack[-1]
            if "cell" in table:
                table.setdefault("row", []).append(" ".join("".join(table.pop("cell")).split()))
        elif tag == "tr" and self._table_stack:
            table = self._table_stack[-1]
            if "row" in table:
                table["rows"].append(table.pop("row"))
        elif tag == "table" and self._table_stack:
            self._table_stack.pop()


def publication_structure(html: str, long_code_lines: int = DEFAULT_LONG_CODE_LINES) -> dict[str, object]:
    if long_code_lines < 1:
        raise ValueError("long_code_lines must be positive")
    parser = PublicationStructure(long_code_lines)
    parser.feed(html)
    parser.close()
    tables = []
    for table in parser.tables:
        rows = table["rows"]
        columns = max((len(row) for row in rows), default=0)
        tables.append({
            "ordinal": table["ordinal"],
            "headers": rows[0] if rows else [],
            "columns": columns,
            "data_rows": max(0, len(rows) - 1),
            "suggested_width_percent": suggested_table_widths(rows, columns),
            "feishu_layout_status": "required",
        })
    return {
        "headings": parser.headings,
        "headings_by_level": {
            f"h{level}": sum(item["level"] == level for item in parser.headings)
            for level in range(1, 7)
        },
        "code_blocks": parser.code_blocks,
        "tables": tables,
        "long_code_lines": long_code_lines,
    }


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
        "--long-code-lines",
        type=int,
        default=DEFAULT_LONG_CODE_LINES,
        help="Mark code blocks at least this many rendered lines for tail checks (default: 20)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated artifacts that already exist",
    )
    args = parser.parse_args()
    if args.long_code_lines < 1:
        parser.error("--long-code-lines must be positive")
    return args


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
    publish_text, diagrams = extract_plantuml_diagrams(text, diagrams_dir)
    html = markdown_to_html(publish_text)
    structure = publication_structure(html, args.long_code_lines)
    inventory = {
        "headings": len(structure["headings"]),
        "headings_by_level": structure["headings_by_level"],
        "tables": len(structure["tables"]),
        "code_blocks": len(structure["code_blocks"]),
        # Retained as a compatibility alias; version 3 counts the final payload,
        # including indented/raw-HTML blocks and excluding extracted diagrams.
        "fenced_code_blocks": len(structure["code_blocks"]),
        "plantuml_diagrams": len(diagrams),
        "long_code_blocks": sum(block["requires_tail_check"] for block in structure["code_blocks"]),
        "temporary_placeholders": len(diagrams),
    }

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
    tables = structure["tables"]
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
        "schema_version": 3,
        "source": str(source),
        "source_sha256": sha256_bytes(raw),
        "output_directory": str(output_dir),
        "planned_files": [str(path) for path in planned_files],
        "existing_files": existing_files,
        "plantuml_diagrams": len(diagrams),
        "tables": len(tables),
        "table_layout_checklist": tables,
        "plantuml_compatibility_warnings": diagram_warnings,
        "inventory": inventory,
        "publication_ledger": {
            "headings": structure["headings"],
            "code_blocks": structure["code_blocks"],
            "long_code_lines": args.long_code_lines,
        },
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
    publish_md.write_text(publish_text, encoding="utf-8", newline="\n")
    publish_html.write_text(html, encoding="utf-8", newline="\n")
    for diagram in diagrams:
        Path(str(diagram["path"])).write_text(
            str(diagram["content"]), encoding="utf-8", newline="\n"
        )

    manifest_diagrams = [
        {key: value for key, value in diagram.items() if key != "content"}
        for diagram in diagrams
    ]
    manifest = {
        "schema_version": 3,
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
            "publish_markdown_sha256": sha256_bytes(publish_text.encode("utf-8")),
            "publish_html_sha256": sha256_bytes(html.encode("utf-8")),
        },
        "inventory": inventory,
        "publication_ledger": plan["publication_ledger"],
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
        newline="\n",
    )

    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
