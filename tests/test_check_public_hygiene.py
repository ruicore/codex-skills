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
    scan_history,
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
