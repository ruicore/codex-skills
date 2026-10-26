#!/usr/bin/env python3
"""Copy selected skill packages and verify their content, with local receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "skills" / "index.json"
DEFAULT_TARGET = Path("~/.agents/skills")


def is_runtime_cache(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}


def copy_ignore(directory: str, names: list[str]) -> list[str]:
    return [name for name in names if is_runtime_cache(Path(name))]


def load_skills() -> list[dict[str, object]]:
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("registry must contain a JSON object")
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise RuntimeError("registry must contain a top-level 'skills' list")
    return [skill for skill in skills if isinstance(skill, dict)]


def select_skills(skills: list[dict[str, object]], names: list[str], category: str | None
                  ) -> list[dict[str, object]]:
    selected = []
    for name in dict.fromkeys(names):
        matches = [skill for skill in skills if skill.get("name") == name]
        if not matches:
            raise RuntimeError(f"unknown skill: {name}")
        selected.extend(matches)
    if category is not None:
        selected = [skill for skill in skills if skill.get("category") == category]
        if not selected:
            raise RuntimeError(f"no skills found in category: {category}")
    return selected


def inventory(directory: Path) -> dict[str, object]:
    """Compare bytes and empty directories; never follow package symlinks."""
    if directory.is_symlink() or not directory.is_dir():
        raise RuntimeError(f"not a regular skill directory: {directory}")
    files = {}
    directories = []
    for path in sorted(directory.rglob("*")):
        package_path = path.relative_to(directory)
        if is_runtime_cache(package_path):
            continue
        relative = package_path.as_posix()
        if path.is_symlink():
            raise RuntimeError(f"symlinks are not supported: {path}")
        if path.is_dir():
            directories.append(relative)
        elif path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            raise RuntimeError(f"not a regular package file: {path}")
    return {"files": files, "directories": directories}


def plan_installs(skills: list[dict[str, object]], target: Path
                  ) -> list[tuple[str, Path, Path, str]]:
    plan = []
    for skill in skills:
        name, raw = skill.get("name"), skill.get("path")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
            raise RuntimeError("registry has an invalid skill name")
        version = skill.get("version")
        if not isinstance(version, str) or not re.fullmatch(
            r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
        ):
            raise RuntimeError(f"skill {name} must have a valid X.Y.Z registry version")
        if not isinstance(raw, str) or not raw:
            raise RuntimeError(f"skill {name} has no valid registry path")
        source = (REPO_ROOT / raw).resolve()
        skills_root = (REPO_ROOT / "skills").resolve()
        if not source.is_relative_to(skills_root) or source == skills_root:
            raise RuntimeError(f"skill path must identify a package under skills/: {raw}")
        if not (source / "SKILL.md").is_file():
            raise RuntimeError(f"skill package has no SKILL.md: {raw}")
        destination = target / name
        if target.is_relative_to(source) or source.is_relative_to(target):
            raise RuntimeError("source and installation target must not overlap")
        plan.append((name, source, destination, version))
    return plan


def source_revision(source: Path) -> dict[str, object]:
    def git(*args: str) -> str:
        result = subprocess.run(["git", "-C", str(REPO_ROOT), *args],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    return {
        "commit": git("rev-parse", "HEAD"),
        "registry_modified": bool(git("status", "--porcelain", "--", "skills/index.json")),
        "package_modified": bool(git(
            "status", "--porcelain", "--untracked-files=all", "--ignored=matching", "--", str(source),
            ":(exclude,glob)**/__pycache__", ":(exclude,glob)**/__pycache__/**",
            ":(exclude,glob)**/*.pyc", ":(exclude,glob)**/*.pyo")),
        "package": source.relative_to(REPO_ROOT).as_posix(),
    }


def receipt_path(receipts: Path, name: str) -> Path:
    path = receipts / f"{name}.json"
    if path.is_symlink():
        raise RuntimeError(f"receipt must not be a symlink: {path}")
    return path


def check_conflicts(plan: list[tuple[str, Path, Path, str]], overwrite: bool,
                    receipts: Path) -> None:
    for name, source, destination, _version in plan:
        source_tree = inventory(source)
        if destination.is_symlink():
            raise RuntimeError(f"destination must not be a symlink: {destination}")
        if not destination.exists():
            continue
        if not overwrite:
            raise RuntimeError(f"existing destination requires --overwrite: {destination}")
        current = inventory(destination)
        path = receipt_path(receipts, name)
        if not path.exists():
            if current == source_tree:
                continue
            raise RuntimeError(f"unmanaged destination differs from source; preserve it manually: {destination}")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(receipt, dict) or receipt.get("version") != 1
                or receipt.get("skill") != name
                or receipt.get("destination") != str(destination)
                or receipt.get("content") != current):
            raise RuntimeError(f"locally modified destination; refusing replacement: {destination}")


def remove_created_tree(directory: Path) -> None:
    """Remove only a disposable copy, including copied Windows read-only bits."""
    root = directory.resolve()

    def writable_retry(operation, raw_path, exception_info) -> None:
        error = exception_info[1]
        path = Path(raw_path)
        if (not isinstance(error, PermissionError) or path.is_symlink()
                or not path.resolve().is_relative_to(root)):
            raise error
        os.chmod(path, path.stat().st_mode | stat.S_IWRITE)
        operation(path)

    shutil.rmtree(directory, onerror=writable_retry)


def install_one(name: str, source: Path, destination: Path, target: Path,
                receipts: Path, skill_version: str) -> None:
    expected = inventory(source)
    revision = source_revision(source)
    target.mkdir(parents=True, exist_ok=True)
    # Original data must never be owned by an automatic temporary-dir cleanup.
    temporary = Path(tempfile.mkdtemp(prefix=".skill-install-", dir=target.parent))
    stage, backup, failed = temporary / "package", temporary / "previous", temporary / "failed"
    preserve_temporary = False
    promoted = False
    try:
        shutil.copytree(source, stage, ignore=copy_ignore)
        if inventory(stage) != expected or inventory(source) != expected:
            raise RuntimeError(f"source changed during copy or copy verification failed: {name}")
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
            promoted = True
            if inventory(destination) != expected:
                raise RuntimeError(f"installed content verification failed: {name}")
            receipts.mkdir(parents=True, exist_ok=True)
            path = receipt_path(receipts, name)
            record = {"version": 1, "skill": name, "skill_version": skill_version,
                      "destination": str(destination),
                      "source": revision, "content": expected}
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=receipts,
                                             delete=False) as receipt_file:
                temporary_receipt = Path(receipt_file.name)
                json.dump(record, receipt_file, indent=2, sort_keys=True)
                receipt_file.write("\n")
            try:
                temporary_receipt.replace(path)
            finally:
                temporary_receipt.unlink(missing_ok=True)
        except Exception as install_error:
            try:
                # Restore first; deletion of a read-only copy must not block recovery.
                if promoted:
                    destination.rename(failed)
                if backup.exists():
                    backup.rename(destination)
            except OSError as rollback_error:
                preserve_temporary = True
                recovery = f"previous installation preserved at {backup}" if backup.exists() else f"installation copies preserved in {temporary}"
                raise RuntimeError(
                    f"install failed ({install_error}); rollback failed ({rollback_error}); {recovery}"
                ) from rollback_error
            raise
        # The new package and receipt are complete. Do not change original file
        # permissions to dispose of an obsolete backup; retain it on failure.
        if backup.exists():
            try:
                shutil.rmtree(backup)
            except OSError as cleanup_error:
                preserve_temporary = True
                print(f"Warning: installed {name}, but obsolete backup remains at {backup}: {cleanup_error}", file=sys.stderr)
    finally:
        if not preserve_temporary and not backup.exists():
            try:
                remove_created_tree(temporary)
            except OSError as cleanup_error:
                print(f"Warning: temporary installation copy remains at {temporary}: {cleanup_error}", file=sys.stderr)
    print(f"- installed and verified {name}@{skill_version}: {destination}")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="Exact registry skill names.")
    parser.add_argument("--category", help="Explicitly select every skill in this category.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Defaults to ~/.agents/skills.")
    parser.add_argument("--receipt-dir", help="Audit directory outside the target; defaults to a hidden sibling.")
    parser.add_argument("--dry-run", action="store_true", help="Check and print the plan without writing.")
    parser.add_argument("--overwrite", action="store_true", help="Replace only an unchanged receipted installation.")
    parser.add_argument("--verify", action="store_true", help="Compare installed packages with current source without writing.")
    args = parser.parse_args(list(argv))
    if bool(args.names) == bool(args.category):
        parser.error("pass skill names or --category, exclusively")
    if args.verify and (args.overwrite or args.dry_run):
        parser.error("--verify cannot be combined with --overwrite or --dry-run")
    return args


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    target = Path(args.target).expanduser().resolve()
    receipts = (Path(args.receipt_dir).expanduser().resolve() if args.receipt_dir
                else target.parent / f".{target.name}-install-receipts")
    try:
        if receipts.is_relative_to(target) or target.is_relative_to(receipts):
            raise RuntimeError("receipt directory must be outside the skills target and must not contain it")
        selected = select_skills(load_skills(), args.names, args.category)
        plan = plan_installs(selected, target)
        if any(receipts.is_relative_to(source) or source.is_relative_to(receipts) for _, source, _, _ in plan):
            raise RuntimeError("receipt directory must not overlap a source package")
        if args.verify:
            for name, source, destination, version in plan:
                if inventory(source) != inventory(destination):
                    raise RuntimeError(f"installed content differs from current source: {name}")
                print(f"- verified {name} content against registry version {version}: {destination}")
            return 0
        check_conflicts(plan, args.overwrite, receipts)
        print(f"{'Would install' if args.dry_run else 'Installing'} {len(plan)} skill(s) into {target}")
        for name, source, destination, version in plan:
            if args.dry_run:
                print(f"- {name}@{version}: {source} -> {destination}; receipt: {receipt_path(receipts, name)}")
            else:
                check_conflicts([(name, source, destination, version)], args.overwrite, receipts)
                install_one(name, source, destination, target, receipts, version)
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
