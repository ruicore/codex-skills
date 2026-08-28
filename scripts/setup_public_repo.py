#!/usr/bin/env python3
"""Check or explicitly configure local public-repository safety prerequisites."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DENYLIST = REPO_ROOT / ".manifest" / "public-hygiene-denylist.txt"
EXPECTED_HOOKS_PATH = ".githooks"


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Explicitly set core.hooksPath to the repository-owned hook directory.",
    )
    args = parser.parse_args()

    if args.apply:
        configured = run_git("config", "core.hooksPath", EXPECTED_HOOKS_PATH)
        if configured.returncode != 0:
            print("Public repository setup failed: Git hook configuration could not be updated.")
            return 1

    current = run_git("config", "--get", "core.hooksPath")
    hooks_ok = current.returncode == 0 and current.stdout.strip() == EXPECTED_HOOKS_PATH
    denylist_exists = DENYLIST.is_file()
    denylist_ignored = run_git("check-ignore", "-q", str(DENYLIST)).returncode == 0
    denylist_tracked = run_git(
        "ls-files", "--error-unmatch", "--", ".manifest/public-hygiene-denylist.txt"
    ).returncode == 0

    problems: list[str] = []
    if not hooks_ok:
        problems.append("core.hooksPath is not .githooks; rerun with --apply")
    if not denylist_exists:
        problems.append("the ignored private public-hygiene denylist is missing")
    if denylist_exists and not denylist_ignored:
        problems.append("the private public-hygiene denylist is not ignored")
    if denylist_tracked:
        problems.append("the private public-hygiene denylist is tracked")

    if problems:
        print("Public repository setup failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("Public repository setup passed: hook configured and private denylist isolated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
