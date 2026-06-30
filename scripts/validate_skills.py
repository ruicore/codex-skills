#!/usr/bin/env python3
"""Validate the codex-skills registry and skill package files.

The checks intentionally stay small and repository-shaped instead of trying to
be a full JSON Schema, YAML, or Markdown implementation.
"""

from __future__ import annotations

import ast
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "skills" / "index.json"
REGISTRY_SCHEMA_PATH = REPO_ROOT / "schemas" / "skill-registry.schema.json"

REQUIRED_ENTRY_FIELDS = {
    "name",
    "path",
    "category",
    "secondary_categories",
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

ENUM_FIELD_TO_DEFINITION = {
    "category": "category",
    "maturity": "maturity",
    "side_effect_level": "side_effect_level",
}
NON_EMPTY_STRING_FIELDS = (
    "name",
    "path",
    "purpose",
    "portability_notes",
)
NON_EMPTY_STRING_LIST_FIELDS = (
    "triggers",
    "do_not_use_for",
    "primary_outputs",
    "validation_expectations",
)
FRONTMATTER_BOUNDARY = "---"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:\$HOME/)?(?:\.codex/)?skills/[A-Za-z0-9._/-]+/scripts/[A-Za-z0-9._/-]+|"
    r"skills/[A-Za-z0-9._/-]+/scripts/[A-Za-z0-9._/-]+|"
    r"scripts/[A-Za-z0-9._/-]+\.(?:py|sh|mjs|js|ps1|ts))"
)
LOCAL_SCHEMES = ("http:", "https:", "mailto:", "tel:", "file:", "data:")
SIDE_EFFECTING_LEVELS = {
    "local-files",
    "git-working-tree",
    "external-api-write",
    "publish",
    "destructive",
}
SAFETY_MECHANISM_RE = re.compile(
    r"(--dry-run|\bdry[_ -]?run\b|\bpreview\b|--yes\b|\bconfirm(?:ation)?\b|"
    r"\bpreflight\b|\brefus(?:e|ing)\b)",
    re.IGNORECASE,
)
SCRIPT_SIDE_EFFECT_SIGNAL_RE = re.compile(
    r"(\bshutil\.(?:copy|copytree|move|rmtree)\b|"
    r"\bPath\([^)]*\)\.(?:write_text|write_bytes|unlink|rename|replace)\b|"
    r"\.(?:write_text|write_bytes|unlink|rename)\(|"
    r"\bopen\([^)]*['\"][wa]\b|"
    r"\bos\.(?:remove|unlink|rename|replace|rmdir)\b|"
    r"\bsubprocess\.(?:run|check_call|check_output|Popen)\b|"
    r"\burllib\.request\.Request\b|"
    r"\burlopen\(|"
    r"\brequests\.(?:post|put|patch|delete)\b|"
    r"\bmutation\b|"
    r"\bmethod=['\"](?:POST|PUT|PATCH|DELETE)['\"])",
    re.IGNORECASE,
)
HELP_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class SkillContext:
    name: str
    side_effect_level: str
    skill_dir: Path
    skill_md: Path
    supporting_paths: set[Path]


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.skill_count = 0
        self.openai_metadata_count = 0
        self.markdown_link_count = 0
        self.script_reference_count = 0
        self.python_script_count = 0
        self.argparse_help_count = 0

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def run(self) -> int:
        registry = self.load_registry()
        if registry is None:
            return self.finish()
        allowed_enums = self.load_registry_schema_enums()

        skills = registry.get("skills")
        if not isinstance(skills, list):
            self.error("skills/index.json: required field 'skills' must be a list")
            return self.finish()

        seen_names: set[str] = set()
        contexts: list[SkillContext] = []
        for index, entry in enumerate(skills):
            context = self.validate_registry_entry(index, entry, seen_names, allowed_enums)
            if context is not None:
                contexts.append(context)

        self.validate_skill_directory_coverage(contexts)

        for context in contexts:
            self.validate_skill_markdown(context)
            self.validate_agents_metadata(context)

        self.validate_markdown_links(contexts)
        self.validate_script_references(contexts)
        self.validate_python_scripts(contexts)

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

    def load_registry_schema_enums(self) -> dict[str, set[str]]:
        if not REGISTRY_SCHEMA_PATH.exists():
            self.error(f"{rel(REGISTRY_SCHEMA_PATH)}: file does not exist")
            return {}

        try:
            data = json.loads(REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.error(
                f"{rel(REGISTRY_SCHEMA_PATH)}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
            )
            return {}

        if not isinstance(data, dict):
            self.error(f"{rel(REGISTRY_SCHEMA_PATH)}: top-level JSON value must be an object")
            return {}

        definitions = data.get("definitions")
        if not isinstance(definitions, dict):
            self.error(f"{rel(REGISTRY_SCHEMA_PATH)}: missing object field 'definitions'")
            return {}

        allowed: dict[str, set[str]] = {}
        for field, definition_name in ENUM_FIELD_TO_DEFINITION.items():
            definition = definitions.get(definition_name)
            if not isinstance(definition, dict):
                self.error(
                    f"{rel(REGISTRY_SCHEMA_PATH)}: missing enum definition "
                    f"'{definition_name}' for registry field '{field}'"
                )
                continue

            enum_values = definition.get("enum")
            if not (
                isinstance(enum_values, list)
                and enum_values
                and all(isinstance(item, str) and item for item in enum_values)
            ):
                self.error(
                    f"{rel(REGISTRY_SCHEMA_PATH)}: definition '{definition_name}'.enum "
                    "must be a non-empty list of non-empty strings"
                )
                continue

            allowed[field] = set(enum_values)

        return allowed

    def validate_registry_entry(
        self,
        index: int,
        entry: object,
        seen_names: set[str],
        allowed_enums: dict[str, set[str]],
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

        string_values = {
            field: self.validate_non_empty_string_field(label, entry, field)
            for field in NON_EMPTY_STRING_FIELDS
        }
        name = string_values["name"]
        path_value = string_values["path"]
        for field in NON_EMPTY_STRING_LIST_FIELDS:
            self.validate_non_empty_string_list_field(label, entry, field)
        self.validate_bool_field(label, entry, "requires_credentials")
        self.validate_agents_metadata_path_type(label, entry)
        for field in ENUM_FIELD_TO_DEFINITION:
            self.validate_enum_field(label, entry, field, allowed_enums.get(field, set()))
        self.validate_secondary_categories(
            label, entry, allowed_enums.get("category", set())
        )

        if name is None or path_value is None:
            return None
        if name in seen_names:
            self.error(f"{rel(INDEX_PATH)}:{label}.name: duplicate skill name '{name}'")
        seen_names.add(name)

        side_effect_level = entry["side_effect_level"]
        if not isinstance(side_effect_level, str):
            side_effect_level = ""

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
        if skill_dir.name != name:
            self.error(
                f"{rel(INDEX_PATH)}:{label}: registry name '{name}' does not match "
                f"skill directory basename '{skill_dir.name}'"
            )

        supporting_paths = self.validate_supporting_files(label, entry, skill_dir)
        self.validate_agents_metadata_path(label, entry, skill_dir)

        return SkillContext(
            name=name,
            side_effect_level=side_effect_level,
            skill_dir=skill_dir,
            skill_md=skill_md,
            supporting_paths=supporting_paths,
        )

    def validate_non_empty_string_field(
        self, label: str, entry: dict[str, object], field: str
    ) -> str | None:
        value = entry[field]
        if not isinstance(value, str) or not value.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.{field}: must be a non-empty string")
            return None
        return value

    def validate_non_empty_string_list_field(
        self, label: str, entry: dict[str, object], field: str
    ) -> None:
        value = entry[field]
        if not isinstance(value, list):
            self.error(f"{rel(INDEX_PATH)}:{label}.{field}: must be a non-empty list")
            return
        if not value:
            self.error(f"{rel(INDEX_PATH)}:{label}.{field}: must not be empty")
            return

        for item_index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                self.error(
                    f"{rel(INDEX_PATH)}:{label}.{field}[{item_index}]: "
                    "must be a non-empty string"
                )

    def validate_bool_field(self, label: str, entry: dict[str, object], field: str) -> None:
        value = entry[field]
        if not isinstance(value, bool):
            self.error(f"{rel(INDEX_PATH)}:{label}.{field}: must be a boolean")

    def validate_agents_metadata_path_type(
        self, label: str, entry: dict[str, object]
    ) -> None:
        value = entry["agents_metadata_path"]
        if value is None:
            return
        if not isinstance(value, str) or not value.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.agents_metadata_path: must be a string or null")

    def validate_enum_field(
        self, label: str, entry: dict[str, object], field: str, allowed_values: set[str]
    ) -> None:
        value = entry[field]
        if not isinstance(value, str) or not value.strip():
            self.error(f"{rel(INDEX_PATH)}:{label}.{field}: must be a non-empty string")
            return
        if not allowed_values:
            return
        if value not in allowed_values:
            expected = ", ".join(sorted(allowed_values))
            self.error(
                f"{rel(INDEX_PATH)}:{label}.{field}: invalid value '{value}'; "
                f"expected one of: {expected}"
            )

    def validate_secondary_categories(
        self, label: str, entry: dict[str, object], allowed_values: set[str]
    ) -> None:
        value = entry["secondary_categories"]
        if not isinstance(value, list):
            self.error(f"{rel(INDEX_PATH)}:{label}.secondary_categories: must be a list")
            return

        seen: set[str] = set()
        primary_category = entry.get("category")
        for item_index, item in enumerate(value):
            item_label = f"{label}.secondary_categories[{item_index}]"
            if not isinstance(item, str) or not item.strip():
                self.error(f"{rel(INDEX_PATH)}:{item_label}: must be a non-empty string")
                continue
            if allowed_values and item not in allowed_values:
                expected = ", ".join(sorted(allowed_values))
                self.error(
                    f"{rel(INDEX_PATH)}:{item_label}: invalid value '{item}'; "
                    f"expected one of: {expected}"
                )
            if item in seen:
                self.error(
                    f"{rel(INDEX_PATH)}:{item_label}: duplicate secondary category '{item}'"
                )
            seen.add(item)
            if isinstance(primary_category, str) and item == primary_category:
                self.error(
                    f"{rel(INDEX_PATH)}:{item_label}: must not duplicate primary category "
                    f"'{primary_category}'"
                )

    def validate_skill_directory_coverage(self, contexts: list[SkillContext]) -> None:
        registered_dirs = {context.skill_dir.resolve() for context in contexts}
        skills_root = REPO_ROOT / "skills"
        if not skills_root.exists():
            self.error(f"{rel(skills_root)}: directory does not exist")
            return

        for skill_md in sorted(skills_root.glob("*/SKILL.md")):
            skill_dir = skill_md.parent.resolve()
            if skill_dir not in registered_dirs:
                self.error(
                    f"{rel(skill_md)}: skill directory is missing from "
                    f"{rel(INDEX_PATH)}"
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

    def validate_python_scripts(self, contexts: list[SkillContext]) -> None:
        script_paths = find_python_scripts()
        self.python_script_count = len(script_paths)
        self.compile_python_scripts(script_paths)
        self.validate_argparse_help(script_paths)
        self.validate_side_effecting_script_safety(contexts)

    def compile_python_scripts(self, script_paths: list[Path]) -> None:
        with tempfile.TemporaryDirectory(prefix="codex-skills-pycompile-") as temp_dir:
            cache_dir = Path(temp_dir)
            for script_path in script_paths:
                try:
                    py_compile.compile(
                        str(script_path),
                        cfile=str(cache_dir / safe_pyc_name(script_path)),
                        doraise=True,
                    )
                except py_compile.PyCompileError as exc:
                    self.error(f"{rel(script_path)}: py_compile failed: {exc.msg}")

    def validate_argparse_help(self, script_paths: list[Path]) -> None:
        for script_path in script_paths:
            try:
                text = script_path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                self.error(f"{rel(script_path)}: cannot read as UTF-8: {exc}")
                continue

            if not looks_like_argparse_cli(text):
                continue
            if not has_main_guard(text):
                self.warn(
                    f"{rel(script_path)}: argparse usage detected, but --help was not "
                    "run because no __main__ guard was found."
                )
                continue

            result = run_help(script_path)
            if result.returncode == 0:
                self.argparse_help_count += 1
                continue

            detail = (result.stderr or result.stdout).strip().splitlines()
            suffix = f": {detail[0]}" if detail else ""
            self.warn(f"{rel(script_path)}: --help probe exited {result.returncode}{suffix}")

    def validate_side_effecting_script_safety(self, contexts: list[SkillContext]) -> None:
        for context in contexts:
            if context.side_effect_level not in SIDE_EFFECTING_LEVELS:
                continue
            if not context.skill_md.exists():
                continue

            try:
                skill_text = context.skill_md.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                self.error(f"{rel(context.skill_md)}: cannot read as UTF-8: {exc}")
                continue

            documented_safety = bool(SAFETY_MECHANISM_RE.search(skill_text))
            script_paths = set(context.supporting_paths)
            script_paths.update(script_references_for_context(skill_text, context))
            for script_path in sorted(script_paths):
                if script_path.suffix != ".py" or not is_scripts_helper(script_path):
                    continue
                try:
                    script_text = script_path.read_text(encoding="utf-8")
                except UnicodeDecodeError as exc:
                    self.error(f"{rel(script_path)}: cannot read as UTF-8: {exc}")
                    continue

                if not SCRIPT_SIDE_EFFECT_SIGNAL_RE.search(script_text):
                    continue
                if SAFETY_MECHANISM_RE.search(script_text) or documented_safety:
                    continue

                self.warn(
                    f"{rel(script_path)}: referenced by side-effecting skill "
                    f"'{context.name}' ({context.side_effect_level}), but no dry-run, "
                    "preview, --yes, refusal, or documented confirmation mechanism "
                    "could be proven automatically."
                )

    def finish(self) -> int:
        if self.warnings:
            print("Skill validation warnings:")
            for message in self.warnings:
                print(f"- {message}")

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
            f"{self.script_reference_count} local script references, "
            f"{self.python_script_count} Python helper scripts compiled, "
            f"{self.argparse_help_count} argparse --help probes checked."
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


def find_python_scripts() -> list[Path]:
    paths = set((REPO_ROOT / "scripts").glob("*.py"))
    skills_root = REPO_ROOT / "skills"
    if skills_root.exists():
        paths.update(skills_root.glob("**/scripts/*.py"))
    return sorted(path.resolve() for path in paths if path.is_file())


def safe_pyc_name(script_path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", rel(script_path)) + ".pyc"


def looks_like_argparse_cli(text: str) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False

    imports_argparse = False
    builds_parser = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports_argparse = imports_argparse or any(alias.name == "argparse" for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports_argparse = imports_argparse or node.module == "argparse"
        elif isinstance(node, ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "ArgumentParser"
                and isinstance(func.value, ast.Name)
                and func.value.id == "argparse"
            ):
                builds_parser = True
            elif isinstance(func, ast.Name) and func.id == "ArgumentParser":
                builds_parser = True

    return imports_argparse and builds_parser


def has_main_guard(text: str) -> bool:
    return "__name__" in text and "__main__" in text


def run_help(script_path: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [sys.executable, str(script_path), "--help"],
            cwd=REPO_ROOT,
            env=sanitized_help_env(),
            capture_output=True,
            text=True,
            timeout=HELP_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            exc.cmd,
            124,
            output=exc.stdout or "",
            stderr=f"--help timed out after {HELP_TIMEOUT_SECONDS} seconds",
        )


def sanitized_help_env() -> dict[str, str]:
    sensitive_markers = ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AUTH")
    env = {
        key: value
        for key, value in os.environ.items()
        if not any(marker in key.upper() for marker in sensitive_markers)
    }
    env["NO_COLOR"] = "1"
    return env


def is_scripts_helper(path: Path) -> bool:
    return any(part == "scripts" for part in path.parts)


def script_references_for_context(text: str, context: SkillContext) -> set[Path]:
    paths: set[Path] = set()
    for match in PATH_TOKEN_RE.finditer(text):
        raw_path = match.group("path").strip("'\"`")
        resolved = resolve_script_reference(raw_path, context)
        if resolved is not None:
            paths.add(resolved)
    return paths


def main(argv: Iterable[str] | None = None) -> int:
    _ = argv
    return Validator().run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
