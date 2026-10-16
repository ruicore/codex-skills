#!/usr/bin/env python3
"""Snapshot task-start Git state, then inspect staged scope without changing Git."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
from typing import Iterable


def git(repo: Path, *args: str) -> bytes:
    environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                            env=environment)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def paths(raw: bytes) -> list[str]:
    return [os.fsdecode(path) for path in raw.split(b"\0") if path]


def private_snapshot_path(repo: Path, snapshot: Path) -> None:
    """An explicit path is required; inside the worktree it must be ignored."""
    if snapshot.is_relative_to(repo):
        relative = snapshot.relative_to(repo).as_posix()
        if git(repo, "ls-files", "-z", "--", relative):
            raise RuntimeError("snapshot path is tracked; choose private ignored storage")
        # check-ignore exits 1 for nonignored paths; do not create it to test.
        try:
            git(repo, "check-ignore", "--", relative)
        except RuntimeError as exc:
            raise RuntimeError("snapshot inside the repository must be ignored") from exc
    git_directory = Path(os.fsdecode(git(repo, "rev-parse", "--absolute-git-dir")).strip()).resolve()
    common_directory = Path(os.fsdecode(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")).strip()).resolve()
    if snapshot.is_relative_to(git_directory) or snapshot.is_relative_to(common_directory):
        raise RuntimeError("snapshot must be outside Git administrative directories")


def state(repo: Path, *, capture_baseline: bool = True) -> dict[str, object]:
    head = git(repo, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    staged = git(repo, "diff", "--cached", "--no-ext-diff", "--no-textconv", "--binary", "--no-renames", "HEAD", "--")
    worktree = (git(repo, "diff", "--no-ext-diff", "--no-textconv", "--binary", "--no-renames", "--")
                if capture_baseline else b"")
    staged_paths = paths(git(repo, "diff", "--cached", "--name-only", "-z", "--no-renames", "HEAD", "--"))
    worktree_paths = (paths(git(repo, "diff", "--name-only", "-z", "--no-renames", "--"))
                      if capture_baseline else [])
    untracked = (paths(git(repo, "ls-files", "--others", "--exclude-standard", "-z"))
                 if capture_baseline else [])
    ignored = (paths(git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "--directory", "-z"))
               if capture_baseline else [])
    unmerged = paths(git(repo, "diff", "--name-only", "--diff-filter=U", "-z", "--"))
    untracked_hashes = {}
    for relative in untracked:
        path = repo / relative
        if path.is_symlink():
            data = os.fsencode(os.readlink(path))
        elif path.is_file():
            data = path.read_bytes()
        else:
            raise RuntimeError(f"cannot snapshot untracked path: {relative}")
        untracked_hashes[relative] = hashlib.sha256(data).hexdigest()
    if git(repo, "rev-parse", "HEAD").decode("ascii").strip() != head:
        raise RuntimeError("HEAD changed during inspection; retry in an idle worktree")
    return {"head": head, "staged_paths": staged_paths, "worktree_paths": worktree_paths,
            "untracked_paths": untracked, "untracked_sha256": untracked_hashes,
            "ignored_paths": ignored,
            "unmerged_paths": unmerged,
            "staged_diff_base64": base64.b64encode(staged).decode("ascii"),
            "worktree_diff_base64": base64.b64encode(worktree).decode("ascii")}


def start(repo: Path, snapshot: Path) -> dict[str, object]:
    initial = state(repo)
    if initial["unmerged_paths"]:
        raise RuntimeError("resolve existing merge conflicts before starting a task snapshot")
    record = {"version": 1, "repository": str(repo), "initial": initial}
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    # A previous baseline is evidence, not a file to silently replace.
    with snapshot.open("x", encoding="utf-8") as output:
        json.dump(record, output, indent=2, sort_keys=True)
        output.write("\n")
    return {"status": "snapshot-created", "snapshot": str(snapshot), "head": initial["head"],
            "preexisting_paths": sorted(set(initial["staged_paths"] + initial["worktree_paths"] + initial["untracked_paths"]))}


def allow_path(raw: str) -> str:
    value = PurePosixPath(raw)
    if (not raw or not value.parts or raw != value.as_posix() or value.is_absolute()
            or any(part in {".", ".."} for part in value.parts)
            or "\\" in raw or ":" in raw):
        raise RuntimeError(f"allowlist requires exact repository-relative file paths: {raw!r}")
    return raw


def check(repo: Path, snapshot: Path, allowed: list[str]) -> tuple[dict[str, object], int]:
    record = json.loads(snapshot.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("version") != 1 or record.get("repository") != str(repo):
        raise RuntimeError("snapshot version or repository does not match")
    initial = record.get("initial")
    if not isinstance(initial, dict):
        raise RuntimeError("snapshot has no initial state")
    for key in ("staged_paths", "worktree_paths", "untracked_paths", "ignored_paths"):
        if not isinstance(initial.get(key), list) or not all(isinstance(p, str) for p in initial[key]):
            raise RuntimeError(f"invalid snapshot field: {key}")
    current = state(repo, capture_baseline=False)
    allowlist = {allow_path(path) for path in allowed}
    staged = set(current["staged_paths"])
    preexisting = set(initial["staged_paths"] + initial["worktree_paths"] + initial["untracked_paths"])
    ignored_overlap = {path for path in staged for ignored in initial["ignored_paths"]
                       if path == ignored or (ignored.endswith("/") and path.startswith(ignored))}
    overlap = sorted((staged & preexisting) | ignored_overlap)
    extra = sorted(staged - allowlist)
    head_changed = initial.get("head") != current["head"]
    issues = []
    if head_changed:
        issues.append("HEAD changed since task start; this baseline cannot approve the current commit")
    if extra:
        issues.append("staged paths outside the explicit allowlist")
    if overlap:
        issues.append("preexisting path overlaps staged content; attribution is ambiguous and requires manual diff review")
    if current["unmerged_paths"]:
        issues.append("unresolved merge conflicts")
    if not staged:
        issues.append("no staged changes to inspect")
    result = {"status": "needs-review" if issues else "pass", "issues": issues,
              "start_head": initial.get("head"), "current_head": current["head"],
              "staged_paths": sorted(staged), "allowlist": sorted(allowlist),
              "extra_paths": extra, "ambiguous_preexisting_paths": overlap,
              "unmerged_paths": current["unmerged_paths"],
              "staged_diff_sha256": hashlib.sha256(base64.b64decode(current["staged_diff_base64"])).hexdigest()}
    return result, 1 if issues else 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["start", "check"])
    parser.add_argument("--repo", default=".", help="Git working tree to inspect.")
    parser.add_argument("--snapshot", required=True, help="Explicit private JSON path (outside repo or ignored).")
    parser.add_argument("--allow", action="append", default=[], help="Exact repo-relative staged path; repeat per file.")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command == "check" and not args.allow:
        parser.error("check requires at least one explicit --allow file")
    if args.command == "start" and args.allow:
        parser.error("--allow is used only with check")
    try:
        root = Path(os.fsdecode(git(Path(args.repo).resolve(), "rev-parse", "--show-toplevel")).strip()).resolve()
        snapshot = Path(args.snapshot).expanduser().resolve()
        private_snapshot_path(root, snapshot)
        if args.command == "start":
            result, code = start(root, snapshot), 0
        else:
            result, code = check(root, snapshot, args.allow)
        print(json.dumps(result, indent=2, sort_keys=True))
        return code
    except (RuntimeError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
