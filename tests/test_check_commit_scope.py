from __future__ import annotations

import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_commit_scope.py"


class CommitScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "sample"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.write("plan.md", "first\nsecond\nthird\n")
        self.write("other.md", "other\n")
        self.write(".gitignore", ".private/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial synthetic tree")
        self.snapshot = self.repo / ".private" / "task.json"

    def git(self, *args: str) -> bytes:
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True).stdout

    def write(self, name: str, content: str) -> None:
        (self.repo / name).write_text(content, encoding="utf-8")

    def run_scope(self, command: str, *args: str, expected: int = 0) -> dict:
        index = (self.repo / ".git" / "index").read_bytes()
        head = self.git("rev-parse", "HEAD")
        staged = self.git("diff", "--cached", "--binary")
        worktree = self.git("diff", "--binary")
        result = subprocess.run([sys.executable, str(SCRIPT), command, "--repo", str(self.repo),
                                 "--snapshot", str(self.snapshot), *args], capture_output=True, text=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        self.assertEqual(index, (self.repo / ".git" / "index").read_bytes())
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(staged, self.git("diff", "--cached", "--binary"))
        self.assertEqual(worktree, self.git("diff", "--binary"))
        return json.loads(result.stdout if result.stdout else result.stderr)

    def test_clean_start_and_exact_allowed_staged_file_pass(self) -> None:
        self.run_scope("start")
        self.write("plan.md", "task change\n")
        self.git("add", "plan.md")
        result = self.run_scope("check", "--allow", "plan.md")
        self.assertEqual("pass", result["status"])
        self.assertEqual(["plan.md"], result["staged_paths"])
        self.assertEqual(64, len(result["staged_diff_sha256"]))

    def test_extra_staged_file_fails(self) -> None:
        self.run_scope("start")
        self.write("plan.md", "task change\n")
        self.write("other.md", "extra change\n")
        self.git("add", "plan.md", "other.md")
        result = self.run_scope("check", "--allow", "plan.md", expected=1)
        self.assertEqual(["other.md"], result["extra_paths"])

    def test_snapshot_captures_existing_staged_worktree_and_untracked(self) -> None:
        self.write("plan.md", "staged before task\n")
        self.git("add", "plan.md")
        self.write("plan.md", "unstaged before task\n")
        self.write("draft.md", "existing untracked\n")
        self.run_scope("start")
        initial = json.loads(self.snapshot.read_text(encoding="utf-8"))["initial"]
        self.assertEqual(["plan.md"], initial["staged_paths"])
        self.assertEqual(["plan.md"], initial["worktree_paths"])
        self.assertEqual(["draft.md"], initial["untracked_paths"])
        self.assertIn(b"staged before task", base64.b64decode(initial["staged_diff_base64"]))
        self.assertIn(b"unstaged before task", base64.b64decode(initial["worktree_diff_base64"]))
        self.assertIn("draft.md", initial["untracked_sha256"])
        result = self.run_scope("check", "--allow", "plan.md", expected=1)
        self.assertEqual(["plan.md"], result["ambiguous_preexisting_paths"])

    def test_same_file_new_changes_require_review_even_on_different_lines(self) -> None:
        self.write("plan.md", "existing first\nsecond\nthird\n")
        self.run_scope("start")
        self.write("plan.md", "existing first\nsecond\ntask third\n")
        self.git("add", "plan.md")
        result = self.run_scope("check", "--allow", "plan.md", expected=1)
        self.assertEqual(["plan.md"], result["ambiguous_preexisting_paths"])

    def test_existing_untracked_path_cannot_be_approved_as_new_task_file(self) -> None:
        self.write("draft.md", "existing draft\n")
        self.run_scope("start")
        self.git("add", "draft.md")
        result = self.run_scope("check", "--allow", "draft.md", expected=1)
        self.assertEqual(["draft.md"], result["ambiguous_preexisting_paths"])

    def test_existing_unstaged_change_on_other_file_does_not_block(self) -> None:
        self.write("other.md", "existing local work\n")
        self.run_scope("start")
        self.write("plan.md", "task work\n")
        self.git("add", "plan.md")
        self.run_scope("check", "--allow", "plan.md")

    def test_rename_requires_both_old_and_new_path_allowances(self) -> None:
        self.run_scope("start")
        self.git("mv", "plan.md", "renamed.md")
        result = self.run_scope("check", "--allow", "renamed.md", expected=1)
        self.assertEqual(["plan.md"], result["extra_paths"])
        self.run_scope("check", "--allow", "renamed.md", "--allow", "plan.md")

    def test_head_change_invalidates_baseline(self) -> None:
        self.run_scope("start")
        self.git("commit", "--allow-empty", "-qm", "Another synthetic commit")
        self.write("plan.md", "task work\n")
        self.git("add", "plan.md")
        result = self.run_scope("check", "--allow", "plan.md", expected=1)
        self.assertNotEqual(result["start_head"], result["current_head"])

    def test_unignored_or_tracked_snapshot_is_rejected(self) -> None:
        self.snapshot = self.repo / "baseline.json"
        self.run_scope("start", expected=2)
        self.assertFalse(self.snapshot.exists())
        self.snapshot = self.repo / "plan.md"
        self.run_scope("start", expected=2)
        self.assertEqual("first\nsecond\nthird\n", self.snapshot.read_text(encoding="utf-8"))

    def test_external_snapshot_works_but_cannot_replace_prior_evidence(self) -> None:
        self.snapshot = self.base / "private" / "task.json"
        self.run_scope("start")
        original = self.snapshot.read_bytes()
        self.run_scope("start", expected=2)
        self.assertEqual(original, self.snapshot.read_bytes())

    def test_git_administrative_snapshot_is_rejected(self) -> None:
        self.snapshot = self.repo / ".git" / "baseline.json"
        self.run_scope("start", expected=2)
        self.assertFalse(self.snapshot.exists())

    def test_no_staged_changes_is_not_a_pass(self) -> None:
        self.run_scope("start")
        self.run_scope("check", "--allow", "plan.md", expected=1)

    def test_allowlist_is_exact_not_a_glob_or_directory(self) -> None:
        self.run_scope("start")
        self.write("plan.md", "task work\n")
        self.git("add", "plan.md")
        result = self.run_scope("check", "--allow", "*.md", expected=1)
        self.assertEqual(["plan.md"], result["extra_paths"])
        self.run_scope("check", "--allow", "../plan.md", expected=2)

    def test_staged_deletion_and_space_in_name_are_inspected(self) -> None:
        self.run_scope("start")
        self.git("rm", "other.md")
        self.write("release notes.md", "new task notes\n")
        self.git("add", "release notes.md")
        result = self.run_scope("check", "--allow", "other.md", "--allow", "release notes.md")
        self.assertEqual(["other.md", "release notes.md"], result["staged_paths"])

    def test_wrong_repository_snapshot_is_rejected(self) -> None:
        self.run_scope("start")
        record = json.loads(self.snapshot.read_text(encoding="utf-8"))
        record["repository"] = str(self.base / "another-sample")
        self.snapshot.write_text(json.dumps(record), encoding="utf-8")
        self.run_scope("check", "--allow", "plan.md", expected=2)

    def test_force_staged_existing_ignored_content_requires_review(self) -> None:
        (self.repo / ".private").mkdir()
        self.write(".private/local.md", "existing ignored content\n")
        self.run_scope("start")
        initial = json.loads(self.snapshot.read_text(encoding="utf-8"))["initial"]
        self.assertEqual([".private/"], initial["ignored_paths"])
        self.assertNotIn(".private/local.md", initial["untracked_sha256"])
        self.git("add", "-f", ".private/local.md")
        result = self.run_scope("check", "--allow", ".private/local.md", expected=1)
        self.assertEqual([".private/local.md"], result["ambiguous_preexisting_paths"])


if __name__ == "__main__":
    unittest.main()
