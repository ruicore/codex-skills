#!/usr/bin/env python3
"""Validate the codex-skills registry and skill package files.

The checks intentionally stay small and repository-shaped instead of trying to
be a full JSON Schema, YAML, or Markdown implementation.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "skills" / "index.json"

REQUIRED_ENTRY_FIELDS = {
    "name",
    "path",
    "category",
    "maturity",
    "purpose",
    "triggers",
    "do_not_use_for",
    "side_effect_level",
    "requires_credentials",
    "primary_outputs",
    "validation_expectations",
    "supporting_files",
    "agents_metadata_path",
    "portability_notes",
}

FRONTMATTER_BOUNDARY = "---"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:\$HOME/)?(?:\.codex/)?skills/[A-Za-z0-9._/-]+/scripts/[A-Za-z0-9._/-]+|"
    r"skills/[A-Za-z0-9._/-]+/scripts/[A-Za-z0-9._/-]+|"
    r"scripts/[A-Za-z0-9._/-]+\.(?:py|sh|mjs|js|ps1|ts))"
)
LOCAL_SCHEMES = ("http:", "https:", "mailto:", "tel:", "file:", "data:")


@dataclass(frozen=True)
class SkillContext:
    name: str
    skill_dir: Path
    skill_md: Path
    supporting_paths: set[Path]


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.skill_count = 0
        self.openai_metadata_count = 0
        self.markdown_link_count = 0
        self.script_reference_count = 0

    def error(self, message: str) -> None:
        self.errors.append(message)

    def run(self) -> int:
        registry = self.load_registry()
        if registry is None:
            return self.finish()

        skills = registry.get("skills")
        if not isinstance(skills, list):
            self.error("skills/index.json: required field 'skills' must be a list")
            return self.finish()

        seen_names: set[str] = set()
        contexts: list[SkillContext] = []
        for index, entry in enumerate(skills):
            context = self.validate_registry_entry(index, entry, seen_names)
            if context is not None:
                contexts.append(context)

        for context in contexts:
            self.validate_skill_markdown(context)
            self.validate_agents_metadata(context)

        self.validate_markdown_links(contexts)
        self.validate_script_references(contexts)

        self.skill_count = len(contexts)
        return self.finish()

    def load_registry(self) -> dict[str, object] | None:
        if not INDEX_PATH.exists():
            self.error(f"{rel(INDEX_PATH)}: file does not exist")
            return None

        try:
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.error(f"{rel(INDEX_PATH)}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}")
            return None

        if not isinstance(data, dict):
            self.error(f"{rel(INDEX_PATH)}: top-level JSON value must be an object")
            return None
        return data

    def validate_registry_entry(
        self, index: int, entry: object, seen_names: set[str]
    ) -> SkillContext | None:
        label = f"skills[{index}]"
        if not isinstance(entry, dict):
            self.error(f"{rel(INDEX_PATH)}:{label}: entry must be an object")
            return None

        missing = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        for field in missing:
            self.error(f"{rel(INDEX_PATH)}:{label}: missing required field '{field}'")
        if missing:
            return None

        name = entry["name"]
        path_value = entry["path"]
        if not isinstance(name, str) or not name.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.name: must be a non-empty string")
            return None
        if name in seen_names:
            self.error(f"{rel(INDEX_PATH)}:{label}.name: duplicate skill name '{name}'")
        seen_names.add(name)

        if not isinstance(path_value, str) or not path_value.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.path: must be a non-empty string")
            return None

        skill_dir = resolve_repo_path(path_value)
        if not is_within_repo(skill_dir):
            self.error(f"{rel(INDEX_PATH)}:{label}.path: path escapes repository: {path_value}")
            return None
        if not skill_dir.exists():
            self.error(f"{rel(INDEX_PATH)}:{label}.path: skill path does not exist: {path_value}")
            return None
        if not skill_dir.is_dir():
            self.error(f"{rel(INDEX_PATH)}:{label}.path: skill path is not a directory: {path_value}")
            return None

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            self.error(f"{rel(INDEX_PATH)}:{label}: missing {rel(skill_md)}")

        supporting_paths = self.validate_supporting_files(label, entry, skill_dir)
        self.validate_agents_metadata_path(label, entry, skill_dir)

        return SkillContext(
            name=name,
            skill_dir=skill_dir,
            skill_md=skill_md,
            supporting_paths=supporting_paths,
        )

    def validate_supporting_files(
        self, label: str, entry: dict[str, object], skill_dir: Path
    ) -> set[Path]:
        value = entry["supporting_files"]
        resolved_paths: set[Path] = set()
        if not isinstance(value, list):
            self.error(f"{rel(INDEX_PATH)}:{label}.supporting_files: must be a list")
            return resolved_paths

        for item_index, item in enumerate(value):
            item_label = f"{label}.supporting_files[{item_index}]"
            if not isinstance(item, str) or not item.strip():
                self.error(f"{rel(INDEX_PATH)}:{item_label}: must be a non-empty string")
                continue

            path = resolve_supporting_path(item, skill_dir)
            if path is None:
                self.error(f"{rel(INDEX_PATH)}:{item_label}: file does not exist: {item}")
                continue
            if not path.is_file():
                self.error(f"{rel(INDEX_PATH)}:{item_label}: supporting file is not a file: {item}")
                continue
            if not is_relative_to(path, skill_dir):
                self.error(
                    f"{rel(INDEX_PATH)}:{item_label}: supporting file must live under "
                    f"the skill directory {rel(skill_dir)}: {item}"
                )
                continue
            resolved_paths.add(path)

        return resolved_paths

    def validate_agents_metadata_path(
        self, label: str, entry: dict[str, object], skill_dir: Path
    ) -> None:
        value = entry["agents_metadata_path"]
        if value is None:
            return
        if not isinstance(value, str) or not value.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.agents_metadata_path: must be a string or null")
            return

        path = resolve_repo_path(value)
        if not path.exists():
            self.error(f"{rel(INDEX_PATH)}:{label}.agents_metadata_path: file does not exist: {value}")
            return
        if not path.is_file():
            self.error(f"{rel(INDEX_PATH)}:{label}.agents_metadata_path: path is not a file: {value}")
            return
        if not is_relative_to(path, skill_dir):
            self.error(
                f"{rel(INDEX_PATH)}:{label}.agents_metadata_path: metadata path must live under "
                f"the skill directory {rel(skill_dir)}: {value}"
            )

    def validate_skill_markdown(self, context: SkillContext) -> None:
        if not context.skill_md.exists():
            return

        try:
            text = context.skill_md.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self.error(f"{rel(context.skill_md)}: cannot read as UTF-8: {exc}")
            return

        frontmatter = parse_frontmatter(text, context.skill_md)
        if frontmatter is None:
            return

        fm_name = frontmatter.get("name")
        fm_description = frontmatter.get("description")
        if not fm_name:
            self.error(f"{rel(context.skill_md)}: frontmatter missing required 'name'")
        elif fm_name != context.name:
            self.error(
                f"{rel(context.skill_md)}: frontmatter name '{fm_name}' does not match "
                f"registry name '{context.name}'"
            )

        if not fm_description:
            self.error(f"{rel(context.skill_md)}: frontmatter missing required 'description'")

    def validate_agents_metadata(self, context: SkillContext) -> None:
        openai_yaml = context.skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            return

        self.openai_metadata_count += 1
        try:
            text = openai_yaml.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self.error(f"{rel(openai_yaml)}: cannot read as UTF-8: {exc}")
            return

        interface = parse_interface_yaml(text)
        for field in ("display_name", "short_description", "default_prompt"):
            if not interface.get(field):
                self.error(f"{rel(openai_yaml)}: missing interface.{field}")

    def validate_markdown_links(self, contexts: list[SkillContext]) -> None:
        markdown_files = [REPO_ROOT / "README.md"]
        markdown_files.extend(sorted((REPO_ROOT / "docs").glob("*.md")))
        markdown_files.extend(context.skill_md for context in contexts if context.skill_md.exists())

        for markdown_file in markdown_files:
            try:
                text = markdown_file.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                self.error(f"{rel(markdown_file)}: cannot read as UTF-8: {exc}")
                continue

            for line_no, line in enumerate(text.splitlines(), start=1):
                for raw_target in MARKDOWN_LINK_RE.findall(line):
                    target = normalize_markdown_target(raw_target)
                    if target is None:
                        continue
                    self.markdown_link_count += 1
                    target_path = (markdown_file.parent / target).resolve()
                    if not is_within_repo(target_path):
                        self.error(
                            f"{rel(markdown_file)}:{line_no}: local Markdown link escapes "
                            f"repository: {raw_target}"
                        )
                        continue
                    if not target_path.exists():
                        self.error(
                            f"{rel(markdown_file)}:{line_no}: local Markdown link target "
                            f"does not exist: {raw_target}"
                        )

    def validate_script_references(self, contexts: list[SkillContext]) -> None:
        for context in contexts:
            if not context.skill_md.exists():
                continue
            text = context.skill_md.read_text(encoding="utf-8")
            for line_no, line in enumerate(text.splitlines(), start=1):
                for match in PATH_TOKEN_RE.finditer(line):
                    raw_path = match.group("path").strip("'\"`")
                    resolved = resolve_script_reference(raw_path, context)
                    if resolved is None:
                        continue
                    self.script_reference_count += 1
                    if not resolved.exists():
                        self.error(
                            f"{rel(context.skill_md)}:{line_no}: local script reference "
                            f"does not exist: {raw_path}"
                        )
                    elif not resolved.is_file():
                        self.error(
                            f"{rel(context.skill_md)}:{line_no}: local script reference is "
                            f"not a file: {raw_path}"
                        )

    def finish(self) -> int:
        if self.errors:
            print("Skill validation failed:")
            for message in self.errors:
                print(f"- {message}")
            return 1

        print(
            "Skill validation passed: "
            f"{self.skill_count} skills, "
            f"{self.openai_metadata_count} agents/openai.yaml files, "
            f"{self.markdown_link_count} local Markdown links, "
            f"{self.script_reference_count} local script references checked."
        )
        return 0


def parse_frontmatter(text: str, path: Path) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return {}

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_BOUNDARY:
            end_index = index
            break
    if end_index is None:
        return {}

    frontmatter_lines = lines[1:end_index]
    data: dict[str, str] = {}
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            i += 1
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            i += 1
            continue

        key, value = match.groups()
        value = value.strip()
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            block_lines: list[str] = []
            i += 1
            while i < len(frontmatter_lines):
                next_line = frontmatter_lines[i]
                if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", next_line):
                    break
                block_lines.append(next_line.strip())
                i += 1
            data[key] = " ".join(part for part in block_lines if part).strip()
            continue

        data[key] = unquote_scalar(value)
        i += 1

    if not data:
        print(f"Warning: {rel(path)} has frontmatter delimiters but no parsed scalar fields.")
    return data


def parse_interface_yaml(text: str) -> dict[str, str]:
    interface: dict[str, str] = {}
    lines = text.splitlines()
    in_interface = False
    interface_indent = 0

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if not in_interface:
            if stripped == "interface:":
                in_interface = True
                interface_indent = indent
            continue

        if indent <= interface_indent:
            break

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", stripped)
        if match:
            key, value = match.groups()
            interface[key] = unquote_scalar(value.strip())

    return interface


def normalize_markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if any(target.lower().startswith(scheme) for scheme in LOCAL_SCHEMES):
        return None

    target = target.split()[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    target = unquote(target).strip()
    if not target or is_placeholder_path(target):
        return None
    return target


def resolve_script_reference(raw_path: str, context: SkillContext) -> Path | None:
    normalized = raw_path.replace("\\", "/")
    normalized = normalized.replace("$HOME/.codex/skills/", ".codex/skills/")

    installed_prefix = f".codex/skills/{context.name}/"
    if normalized.startswith(installed_prefix):
        return (context.skill_dir / normalized[len(installed_prefix) :]).resolve()

    repo_skill_prefix = f"skills/{context.name}/"
    if normalized.startswith(repo_skill_prefix):
        return resolve_repo_path(normalized)

    if normalized.startswith("scripts/"):
        candidate = (context.skill_dir / normalized).resolve()
        if candidate in context.supporting_paths or candidate.exists():
            return candidate

    return None


def resolve_supporting_path(path_value: str, skill_dir: Path) -> Path | None:
    repo_relative = resolve_repo_path(path_value)
    if repo_relative.exists():
        return repo_relative

    skill_relative = (skill_dir / path_value).resolve()
    if skill_relative.exists():
        return skill_relative

    return None


def resolve_repo_path(path_value: str) -> Path:
    return (REPO_ROOT / Path(path_value)).resolve()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def is_within_repo(path: Path) -> bool:
    return is_relative_to(path.resolve(), REPO_ROOT)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value


def is_placeholder_path(target: str) -> bool:
    placeholder_markers = ("YYYY", "TODO", "<", ">", "{", "}", "...")
    return any(marker in target for marker in placeholder_markers)


def main(argv: Iterable[str] | None = None) -> int:
    _ = argv
    return Validator().run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
