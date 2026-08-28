#!/usr/bin/env python3
"""Scan public repository content and proposed Git history without echoing matches."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DENYLIST = Path(".manifest/public-hygiene-denylist.txt")
DENYLIST_ENV = "PUBLIC_HYGIENE_DENYLIST"
DENYLIST_FILE_ENV = "PUBLIC_HYGIENE_DENYLIST_FILE"

GENERIC_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private_ipv4_address",
        re.compile(
            r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
            r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
        ),
    ),
    (
        "internal_dns_name",
        re.compile(r"(?i)\b[a-z0-9][a-z0-9.-]*\.(?:corp|internal|intranet|lan)\b"),
    ),
    (
        "machine_specific_user_path",
        re.compile(r"(?i)\b[a-z]:\\users\\(?!<(?:user|username)>\\)[^\s`\"']+"),
    ),
    (
        "credential_like_literal",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*"
            r"[\"'][a-z0-9_./+=-]{8,}[\"']"
        ),
    ),
)


class HygieneConfigurationError(RuntimeError):
    """Raised when the requested scan cannot be configured safely."""


@dataclass(frozen=True)
class Finding:
    scope: str
    location: str
    line: int | None
    category: str

    def render(self) -> str:
        line_suffix = f":{self.line}" if self.line is not None else ""
        return f"{self.scope}:{self.location}{line_suffix}: {self.category}"


@dataclass(frozen=True)
class ScanResult:
    findings: tuple[Finding, ...]
    files_scanned: int
    commits_scanned: int


def normalized_identifier(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def parse_denylist(text: str) -> tuple[str, ...]:
    normalized: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        value = normalized_identifier(line)
        if len(value) < 4:
            raise HygieneConfigurationError(
                "private denylist entries must contain at least four letters or digits"
            )
        normalized.add(value)
    return tuple(sorted(normalized))


def load_denylist(repo_root: Path, explicit_path: Path | None = None) -> tuple[str, ...]:
    sources: list[str] = []
    env_value = os.environ.get(DENYLIST_ENV, "")
    if env_value:
        sources.append(env_value)

    configured_path: Path | None = explicit_path
    if configured_path is None and os.environ.get(DENYLIST_FILE_ENV):
        configured_path = Path(os.environ[DENYLIST_FILE_ENV])
    if configured_path is None:
        candidate = repo_root / DEFAULT_DENYLIST
        if candidate.is_file():
            configured_path = candidate

    if configured_path is not None:
        if not configured_path.is_absolute():
            configured_path = repo_root / configured_path
        if not configured_path.is_file():
            raise HygieneConfigurationError("configured private denylist file does not exist")
        sources.append(configured_path.read_text(encoding="utf-8"))

    return parse_denylist("\n".join(sources))


def scan_value(
    value: str,
    *,
    scope: str,
    location: str,
    line: int | None,
    denylist: Sequence[str],
) -> list[Finding]:
    findings: list[Finding] = []
    normalized = normalized_identifier(value)
    if any(term in normalized for term in denylist):
        findings.append(Finding(scope, location, line, "private_identifier"))

    for category, pattern in GENERIC_PATTERNS:
        if pattern.search(value):
            findings.append(Finding(scope, location, line, category))
    return findings


def scan_blob(
    data: bytes,
    *,
    scope: str,
    location: str,
    denylist: Sequence[str],
) -> list[Finding]:
    findings = scan_value(
        location,
        scope=scope,
        location=location,
        line=None,
        denylist=denylist,
    )
    text = data.decode("utf-8", errors="ignore")
    for line_number, line in enumerate(text.splitlines(), start=1):
        findings.extend(
            scan_value(
                line,
                scope=scope,
                location=location,
                line=line_number,
                denylist=denylist,
            )
        )
    return findings


def run_git(repo_root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise HygieneConfigurationError("Git could not resolve the requested public-hygiene scope")
    return completed.stdout


def nul_separated_paths(data: bytes) -> list[str]:
    return [item.decode("utf-8", errors="surrogateescape") for item in data.split(b"\0") if item]


def worktree_paths(repo_root: Path) -> list[str]:
    output = run_git(repo_root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return nul_separated_paths(output)


def scan_worktree(repo_root: Path, denylist: Sequence[str]) -> ScanResult:
    findings: list[Finding] = []
    paths = worktree_paths(repo_root)
    for relative_path in paths:
        path = repo_root / relative_path
        if not path.is_file():
            continue
        findings.extend(
            scan_blob(
                path.read_bytes(),
                scope="worktree",
                location=relative_path,
                denylist=denylist,
            )
        )
    return ScanResult(tuple(findings), len(paths), 0)


def changed_paths(repo_root: Path, commit: str) -> list[str]:
    output = run_git(
        repo_root,
        "diff-tree",
        "--root",
        "-m",
        "--no-commit-id",
        "--name-only",
        "-r",
        "-z",
        commit,
    )
    return sorted(set(nul_separated_paths(output)))


def read_blob_at_commit(repo_root: Path, commit: str, relative_path: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout


def scan_history(repo_root: Path, revision_range: str, denylist: Sequence[str]) -> ScanResult:
    commits = run_git(repo_root, "rev-list", "--reverse", revision_range).decode().splitlines()
    findings: list[Finding] = []
    files_scanned = 0

    for commit in commits:
        short_commit = commit[:12]
        scope = f"commit-{short_commit}"
        message = run_git(repo_root, "show", "-s", "--format=%B", commit)
        findings.extend(
            scan_blob(
                message,
                scope=scope,
                location="<commit-message>",
                denylist=denylist,
            )
        )

        paths = changed_paths(repo_root, commit)
        for relative_path in paths:
            data = read_blob_at_commit(repo_root, commit, relative_path)
            if data is None:
                findings.extend(
                    scan_value(
                        relative_path,
                        scope=scope,
                        location=relative_path,
                        line=None,
                        denylist=denylist,
                    )
                )
                continue
            files_scanned += 1
            findings.extend(
                scan_blob(
                    data,
                    scope=scope,
                    location=relative_path,
                    denylist=denylist,
                )
            )

    return ScanResult(tuple(findings), files_scanned, len(commits))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan public working-tree content or every commit in a revision range."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Git repository to scan (default: this repository).",
    )
    parser.add_argument(
        "--range",
        dest="revision_range",
        help="Git revision range whose complete commit snapshots must be scanned.",
    )
    parser.add_argument(
        "--denylist",
        type=Path,
        help="Private newline-delimited identifier file; values are never printed.",
    )
    parser.add_argument(
        "--require-denylist",
        action="store_true",
        help="Fail when neither a local nor environment-provided private denylist exists.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        denylist = load_denylist(repo_root, args.denylist)
        if args.require_denylist and not denylist:
            raise HygieneConfigurationError("a private denylist is required for this scan")
        result = (
            scan_history(repo_root, args.revision_range, denylist)
            if args.revision_range
            else scan_worktree(repo_root, denylist)
        )
    except HygieneConfigurationError as exc:
        print(f"public-hygiene configuration error: {exc}", file=sys.stderr)
        return 2

    if result.findings:
        for finding in result.findings:
            print(finding.render())
        print(
            f"Public hygiene failed: {len(result.findings)} finding(s) across "
            f"{result.files_scanned} file snapshot(s) and {result.commits_scanned} commit(s)."
        )
        return 1

    print(
        f"Public hygiene passed: {result.files_scanned} file snapshot(s), "
        f"{result.commits_scanned} commit(s), {len(denylist)} private identifier rule(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
