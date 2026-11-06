#!/usr/bin/env python3
"""Exercise real helper CLIs using only disposable installations and Git data."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def git_environment() -> dict[str, str]:
    # cwd does not override inherited repository/index selectors. Pass this to
    # Python helpers too, because they launch their own Git subprocesses.
    environment = {name: value for name, value in os.environ.items()
                   if not name.upper().startswith("GIT_")}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_SYSTEM=os.devnull,
                       GIT_CONFIG_GLOBAL=os.devnull)
    return environment


def run(*args: str, cwd: Path = ROOT, expected: int = 0, diagnostic: str | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, env=git_environment(),
                            capture_output=True, text=True, check=False)
    if result.returncode != expected:
        raise RuntimeError(f"unexpected exit {result.returncode}, expected {expected}: {result.stderr}")
    if diagnostic is not None and diagnostic not in result.stderr:
        raise RuntimeError("expected refusal diagnostic was not observed")
    return result.stdout


def helper(script: str, *args: str, expected: int = 0, diagnostic: str | None = None) -> str:
    return run(sys.executable, "-B", str(ROOT / "scripts" / script), *args,
               expected=expected, diagnostic=diagnostic)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def install_demo(base: Path) -> dict[str, object]:
    name = "agent-legibility-review"
    target, receipts = base / "skills", base / "receipts"
    options = (name, "--target", str(target), "--receipt-dir", str(receipts))
    helper("install_skill.py", *options)
    receipt_path = receipts / f"{name}.json"
    original_receipt = receipt_path.read_bytes()
    receipt = json.loads(original_receipt)
    registry = json.loads((ROOT / "skills/index.json").read_text(encoding="utf-8"))
    entry = next(item for item in registry["skills"] if item["name"] == name)
    require(receipt["skill_version"] == entry["version"], "version does not match registry")
    require(receipt["source"]["commit"] == run("git", "rev-parse", "HEAD").strip(), "wrong source commit")
    observed = {path.relative_to(target / name).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (target / name).rglob("*") if path.is_file()}
    require(receipt["content"]["files"] == observed, "receipt file hashes differ")
    helper("install_skill.py", *options, "--verify")
    edited = target / name / "SKILL.md"
    edited.write_text(edited.read_text(encoding="utf-8") + "\nLocal demo edit.\n", encoding="utf-8")
    expected_content = edited.read_bytes()
    helper("install_skill.py", *options, "--overwrite", expected=1,
           diagnostic="locally modified destination; refusing replacement")
    require(edited.read_bytes() == expected_content, "local edit was changed")
    require(receipt_path.read_bytes() == original_receipt, "receipt was changed after refusal")
    return {"skill": name, "version": entry["version"], "receipt_verified": True,
            "content_verified": True, "overwrite_refused": True, "local_edit_preserved": True}


def scope_demo(base: Path) -> dict[str, bool]:
    repo = base / "repo"
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.name", "Demo", cwd=repo)
    run("git", "config", "user.email", "demo@example.invalid", cwd=repo)
    for name in ("existing.txt", "task.txt"):
        (repo / name).write_text("initial\n", encoding="utf-8")
    run("git", "add", "existing.txt", "task.txt", cwd=repo)
    run("git", "-c", "core.hooksPath=", "-c", "commit.gpgsign=false",
        "commit", "-qm", "synthetic baseline", cwd=repo)
    (repo / "existing.txt").write_text("pre-existing change\n", encoding="utf-8")
    snapshot = base / "baseline.json"
    options = ("--repo", str(repo), "--snapshot", str(snapshot))
    helper("check_commit_scope.py", "start", *options)
    (repo / "task.txt").write_text("task change\n", encoding="utf-8")
    run("git", "add", "existing.txt", "task.txt", cwd=repo)
    rejected = json.loads(helper("check_commit_scope.py", "check", *options,
                                 "--allow", "task.txt", expected=1))
    require(rejected["extra_paths"] == ["existing.txt"], "extra staged path not detected")
    require(rejected["ambiguous_preexisting_paths"] == ["existing.txt"], "overlap not detected")
    run("git", "restore", "--staged", "--", "existing.txt", cwd=repo)
    accepted = json.loads(helper("check_commit_scope.py", "check", *options, "--allow", "task.txt"))
    require(accepted["status"] == "pass" and accepted["staged_paths"] == ["task.txt"], "scope did not narrow")
    require((repo / "existing.txt").read_text(encoding="utf-8") == "pre-existing change\n", "edit not preserved")
    return {"extra_path_detected": True, "preexisting_overlap_detected": True,
            "narrowed_scope_passed": True, "preexisting_edit_preserved": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", choices=("all", "install", "scope"), default="all")
    args = parser.parse_args()
    result = {}
    with tempfile.TemporaryDirectory(prefix="workflow-tools-demo-") as directory:
        base = Path(directory)
        if args.demo in ("all", "install"):
            result["installation"] = install_demo(base)
        if args.demo in ("all", "scope"):
            result["commit_scope"] = scope_demo(base)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
