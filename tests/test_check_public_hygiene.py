from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from check_public_hygiene import (  # noqa: E402
    parse_denylist,
    scan_blob,
    scan_history,
    scan_worktree,
    scan_value,
)


class PublicHygieneTests(unittest.TestCase):
    def test_private_identifier_is_normalized_and_not_echoed(self) -> None:
        denylist = parse_denylist("InternalWidget\n")
        findings = scan_value(
            "internal-widget",
            scope="worktree",
            location="example.md",
            line=4,
            denylist=denylist,
        )

        self.assertEqual([finding.category for finding in findings], ["private_identifier"])
        self.assertNotIn("InternalWidget", findings[0].render())
        self.assertNotIn("internal-widget", findings[0].render())

    def test_private_identifier_split_across_lines_is_rejected(self) -> None:
        findings = scan_blob(
            b"Internal\nWidget\n",
            scope="worktree",
            location="example.md",
            denylist=parse_denylist("InternalWidget\n"),
        )

        self.assertIn("private_identifier", [finding.category for finding in findings])

    def test_generic_private_ip_is_rejected(self) -> None:
        findings = scan_value(
            "Connect to " + "192." + "168.40.12 before running the job.",
            scope="worktree",
            location="example.md",
            line=1,
            denylist=(),
        )

        self.assertIn("private_ipv4_address", [finding.category for finding in findings])

    def test_short_private_identifier_is_rejected_as_configuration(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "at least four"):
            parse_denylist("abc\n")

    def test_binary_and_non_utf8_content_is_rejected(self) -> None:
        binary = scan_blob(
            b"image\x00payload",
            scope="worktree",
            location="skills/example/image.png",
            denylist=(),
        )
        non_utf8 = scan_blob(
            b"\xff\xfe\xfd",
            scope="worktree",
            location="skills/example/note.txt",
            denylist=(),
        )

        self.assertIn("binary_or_non_utf8_content", [item.category for item in binary])
        self.assertIn("binary_or_non_utf8_content", [item.category for item in non_utf8])

    def test_tracked_manifest_path_is_rejected(self) -> None:
        findings = scan_blob(
            b"private intake\n",
            scope="worktree",
            location=".manifest/skill-intake/example.md",
            denylist=(),
        )

        self.assertIn("forbidden_private_storage_path", [item.category for item in findings])

    def test_history_scan_catches_an_intermediate_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_git(root, "init", "--initial-branch=main")
            self.run_git(root, "config", "user.name", "Hygiene Test")
            self.run_git(root, "config", "user.email", "hygiene@example.com")

            sample = root / "sample.md"
            sample.write_text("safe baseline\n", encoding="utf-8")
            self.run_git(root, "add", "sample.md")
            self.run_git(root, "commit", "-m", "safe baseline")
            base = self.run_git(root, "rev-parse", "HEAD").strip()

            sample.write_text("InternalWidget implementation detail\n", encoding="utf-8")
            self.run_git(root, "commit", "-am", "temporary private example")
            sample.write_text("neutral synthetic example\n", encoding="utf-8")
            self.run_git(root, "commit", "-am", "remove private example")

            result = scan_history(root, f"{base}..HEAD", parse_denylist("InternalWidget\n"))

            self.assertEqual(result.commits_scanned, 2)
            self.assertTrue(any(item.category == "private_identifier" for item in result.findings))
            self.assertNotIn("InternalWidget", "\n".join(item.render() for item in result.findings))

    def test_history_scan_catches_author_identity_without_echoing_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repo(root)
            base = self.run_git(root, "rev-parse", "HEAD").strip()
            self.run_git(root, "config", "user.name", "InternalWidget")
            sample = root / "sample.md"
            sample.write_text("second safe revision\n", encoding="utf-8")
            self.run_git(root, "commit", "-am", "safe public change")

            result = scan_history(root, f"{base}..HEAD", parse_denylist("InternalWidget\n"))
            rendered = "\n".join(item.render() for item in result.findings)

            self.assertTrue(any(item.category == "private_identifier" for item in result.findings))
            self.assertNotIn("InternalWidget", rendered)

    def test_history_scan_rejects_tracked_symlink_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repo(root)
            base = self.run_git(root, "rev-parse", "HEAD").strip()
            target = root / "link-target.txt"
            target.write_text("synthetic-target\n", encoding="utf-8")
            blob = self.run_git(root, "hash-object", "-w", "link-target.txt").strip()
            self.run_git(root, "update-index", "--add", "--cacheinfo", f"120000,{blob},link")
            self.run_git(root, "commit", "-m", "add synthetic link")

            result = scan_history(root, f"{base}..HEAD", ())

            self.assertIn("tracked_symlink", [item.category for item in result.findings])

    def test_worktree_scan_catches_ref_and_tag_annotation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repo(root)
            self.run_git(root, "tag", "internal-widget-release")
            self.run_git(root, "tag", "-a", "safe-release", "-m", "InternalWidget annotation")

            result = scan_worktree(root, parse_denylist("InternalWidget\n"))

            self.assertTrue(any(item.category == "private_identifier" for item in result.findings))

    def test_protected_mode_requires_private_denylist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repo(root)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "check_public_hygiene.py"),
                    "--repo-root",
                    str(root),
                    "--mode",
                    "protected",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 2)
            self.assertNotIn("InternalWidget", completed.stdout + completed.stderr)

    @classmethod
    def initialize_repo(cls, root: Path) -> None:
        cls.run_git(root, "init", "--initial-branch=main")
        cls.run_git(root, "config", "user.name", "Hygiene Test")
        cls.run_git(root, "config", "user.email", "hygiene@example.com")
        sample = root / "sample.md"
        sample.write_text("safe baseline\n", encoding="utf-8")
        cls.run_git(root, "add", "sample.md")
        cls.run_git(root, "commit", "-m", "safe baseline")

    @staticmethod
    def run_git(root: Path, *args: str) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout


if __name__ == "__main__":
    unittest.main()
