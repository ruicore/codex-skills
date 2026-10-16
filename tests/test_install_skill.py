from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import install_skill


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install_skill.py"


class InstallSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "library"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copyfile(SCRIPT, self.repo / "scripts" / SCRIPT.name)
        entries = []
        for name in ("alpha", "beta"):
            package = self.repo / "skills" / name
            (package / "notes").mkdir(parents=True)
            (package / "empty").mkdir()
            (package / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
            (package / "notes" / "guide.md").write_text("supporting content\n", encoding="utf-8")
            entries.append({"name": name, "path": f"skills/{name}", "category": "sample"})
        (self.repo / "skills" / "index.json").write_text(json.dumps({"skills": entries}), encoding="utf-8")
        (self.repo / "README.md").write_text("repository-only material\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "Initial synthetic library")
        self.target = self.base / "installed"
        self.receipts = self.base / ".installed-install-receipts"

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def run_installer(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess:
        result = subprocess.run([sys.executable, str(self.repo / "scripts" / SCRIPT.name),
                                 *args, "--target", str(self.target)], capture_output=True, text=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_default_target_is_agents_directory(self) -> None:
        self.assertEqual(Path(install_skill.parse_args(["alpha"]).target), Path("~/.agents/skills"))

    def test_selected_package_copy_and_receipt_are_verified(self) -> None:
        self.run_installer("alpha")
        self.assertEqual({"alpha"}, {p.name for p in self.target.iterdir()})
        self.assertTrue((self.target / "alpha" / "empty").is_dir())
        self.assertEqual(install_skill.inventory(self.repo / "skills" / "alpha"),
                         install_skill.inventory(self.target / "alpha"))
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertEqual(self.git("rev-parse", "HEAD"), receipt["source"]["commit"])
        self.assertFalse(receipt["source"]["package_modified"])
        self.assertEqual(hashlib.sha256((self.repo / "skills" / "alpha" / "SKILL.md").read_bytes()).hexdigest(),
                         receipt["content"]["files"]["SKILL.md"])
        self.run_installer("alpha", "--verify")

    def test_dry_run_has_no_writes_and_multiple_selection_is_explicit(self) -> None:
        self.run_installer("alpha", "beta", "--dry-run")
        self.assertFalse(self.target.exists())
        self.assertFalse(self.receipts.exists())
        self.run_installer("alpha", "beta")
        self.assertEqual({"alpha", "beta"}, {p.name for p in self.target.iterdir()})

    def test_category_selection_and_unknown_selection(self) -> None:
        self.run_installer("unknown", expected=1)
        self.assertFalse(self.target.exists())
        self.run_installer("--category", "sample")
        self.assertTrue((self.target / "beta").is_dir())

    def test_overwrite_updates_unchanged_installation_but_protects_local_edits(self) -> None:
        self.run_installer("alpha")
        source = self.repo / "skills" / "alpha" / "SKILL.md"
        source.write_text("# revised alpha\n", encoding="utf-8")
        self.run_installer("alpha", expected=1)
        self.run_installer("alpha", "--verify", expected=1)
        self.run_installer("alpha", "--overwrite")
        self.run_installer("alpha", "--verify")
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["source"]["package_modified"])
        installed = self.target / "alpha" / "SKILL.md"
        installed.write_text("local customization\n", encoding="utf-8")
        self.run_installer("alpha", "--overwrite", expected=1)
        self.assertEqual("local customization\n", installed.read_text(encoding="utf-8"))

    def test_extra_local_file_is_not_erased(self) -> None:
        self.run_installer("alpha")
        extra = self.target / "alpha" / "local.md"
        extra.write_text("local note\n", encoding="utf-8")
        self.run_installer("alpha", "--verify", expected=1)
        self.run_installer("alpha", "--overwrite", expected=1)
        self.assertTrue(extra.exists())

    def test_python_runtime_caches_are_excluded_consistently(self) -> None:
        source = self.repo / "skills" / "alpha"
        cache = source / "scripts" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "generated.pyc").write_bytes(b"synthetic bytecode cache")
        (cache / "detail.txt").write_text("cache directory content\n", encoding="utf-8")
        (source / "old.pyc").write_bytes(b"synthetic bytecode cache")
        (source / "old.pyo").write_bytes(b"synthetic optimized cache")
        self.run_installer("alpha")
        installed = self.target / "alpha"
        self.assertFalse((installed / "scripts" / "__pycache__").exists())
        self.assertFalse((installed / "old.pyc").exists())
        self.assertFalse((installed / "old.pyo").exists())
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertFalse(receipt["source"]["package_modified"])
        installed_cache = installed / "__pycache__"
        installed_cache.mkdir()
        (installed_cache / "generated.pyc").write_bytes(b"local generated cache")
        (installed / "local.pyo").write_bytes(b"local optimized cache")
        self.run_installer("alpha", "--verify")
        self.run_installer("alpha", "--overwrite")
        (source / "extra.md").write_text("real source addition\n", encoding="utf-8")
        self.run_installer("alpha", "--overwrite")
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["source"]["package_modified"])

    def test_ignored_noncache_content_is_still_copied_and_audited(self) -> None:
        (self.repo / ".gitignore").write_text("*.local\n__pycache__/\n*.pyc\n*.pyo\n", encoding="utf-8")
        source = self.repo / "skills" / "alpha"
        (source / "ignored.pyc").write_bytes(b"synthetic ignored cache")
        self.run_installer("alpha")
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertFalse(receipt["source"]["package_modified"])
        (source / "extra.local").write_text("synthetic ignored package note\n", encoding="utf-8")
        self.run_installer("alpha", "--overwrite")
        self.assertTrue((self.target / "alpha" / "extra.local").is_file())
        self.assertFalse((self.target / "alpha" / "ignored.pyc").exists())
        receipt = json.loads((self.receipts / "alpha.json").read_text(encoding="utf-8"))
        self.assertTrue(receipt["source"]["package_modified"])
        (self.target / "alpha" / "local.local").write_text("local ignored addition\n", encoding="utf-8")
        self.run_installer("alpha", "--verify", expected=1)
        self.run_installer("alpha", "--overwrite", expected=1)

    def test_unknown_existing_directory_cannot_be_blindly_replaced(self) -> None:
        package = self.target / "alpha"
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text("custom\n", encoding="utf-8")
        self.run_installer("alpha", "--overwrite", expected=1)
        self.assertEqual("custom\n", (package / "SKILL.md").read_text(encoding="utf-8"))

    def test_preflight_all_packages_before_replacing_any(self) -> None:
        self.run_installer("alpha", "beta")
        (self.repo / "skills" / "alpha" / "SKILL.md").write_text("source update\n", encoding="utf-8")
        (self.target / "beta" / "SKILL.md").write_text("local edit\n", encoding="utf-8")
        self.run_installer("alpha", "beta", "--overwrite", expected=1)
        self.assertEqual("# alpha\n", (self.target / "alpha" / "SKILL.md").read_text(encoding="utf-8"))

    def test_receipts_inside_discovery_target_are_rejected(self) -> None:
        self.run_installer("alpha", "--receipt-dir", str(self.target / "audit"), expected=1)
        self.assertFalse(self.target.exists())

    def test_verify_missing_installation_does_not_write(self) -> None:
        self.run_installer("alpha", "--verify", expected=1)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.receipts.exists())

    def test_receipt_failure_restores_previous_installation(self) -> None:
        self.run_installer("alpha")
        original_receipt = (self.receipts / "alpha.json").read_bytes()
        (self.repo / "skills" / "alpha" / "SKILL.md").write_text("new source\n", encoding="utf-8")
        with patch.object(install_skill, "REPO_ROOT", self.repo), patch.object(
                install_skill, "receipt_path", side_effect=RuntimeError("receipt unavailable")):
            with self.assertRaisesRegex(RuntimeError, "receipt unavailable"):
                install_skill.install_one("alpha", self.repo / "skills" / "alpha",
                                          self.target / "alpha", self.target, self.receipts)
        self.assertEqual("# alpha\n", (self.target / "alpha" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(original_receipt, (self.receipts / "alpha.json").read_bytes())

    @unittest.skipUnless(sys.platform == "win32", "Windows read-only replacement semantics")
    def test_readonly_copy_and_real_receipt_write_failure_restore_previous_installation(self) -> None:
        self.run_installer("alpha")
        original_tree = install_skill.inventory(self.target / "alpha")
        receipt = self.receipts / "alpha.json"
        original_receipt = receipt.read_bytes()
        source = self.repo / "skills" / "alpha" / "SKILL.md"
        source.write_text("replacement with read-only source\n", encoding="utf-8")
        source.chmod(stat.S_IREAD)
        receipt.chmod(stat.S_IREAD)
        try:
            # Windows denies replacing the existing read-only receipt. The
            # new installation also contains a real copied read-only file.
            result = self.run_installer("alpha", "--overwrite", expected=1)
            self.assertIn("Error:", result.stderr)
            self.assertEqual(original_tree, install_skill.inventory(self.target / "alpha"))
            self.assertEqual(original_receipt, receipt.read_bytes())
            self.assertFalse(source.stat().st_mode & stat.S_IWRITE)
            self.assertFalse(list(self.base.glob(".skill-install-*")))
        finally:
            source.chmod(stat.S_IREAD | stat.S_IWRITE)
            receipt.chmod(stat.S_IREAD | stat.S_IWRITE)

    def test_failed_restore_keeps_original_backup_outside_automatic_cleanup(self) -> None:
        self.run_installer("alpha")
        original_tree = install_skill.inventory(self.target / "alpha")
        original_receipt = (self.receipts / "alpha.json").read_bytes()
        (self.repo / "skills" / "alpha" / "SKILL.md").write_text("new source\n", encoding="utf-8")
        original_rename = Path.rename

        def deny_restore(path: Path, destination: Path) -> Path:
            if path.name == "previous" and destination == self.target / "alpha":
                raise PermissionError("synthetic restore denied")
            return original_rename(path, destination)

        with patch.object(install_skill, "REPO_ROOT", self.repo), patch.object(
                install_skill, "receipt_path", side_effect=RuntimeError("receipt unavailable")), patch.object(
                Path, "rename", deny_restore):
            with self.assertRaisesRegex(RuntimeError, "previous installation preserved at") as raised:
                install_skill.install_one("alpha", self.repo / "skills" / "alpha",
                                          self.target / "alpha", self.target, self.receipts)
        retained = list(self.base.glob(".skill-install-*"))
        self.assertEqual(1, len(retained))
        self.assertIn(str(retained[0] / "previous"), str(raised.exception))
        self.assertEqual(original_tree, install_skill.inventory(retained[0] / "previous"))
        self.assertTrue((retained[0] / "failed" / "SKILL.md").is_file())
        self.assertEqual(original_receipt, (self.receipts / "alpha.json").read_bytes())

    def test_bad_registry_cannot_install_repository_root(self) -> None:
        index = self.repo / "skills" / "index.json"
        index.write_text(json.dumps({"skills": [{"name": "alpha", "path": "."}]}), encoding="utf-8")
        self.run_installer("alpha", expected=1)
        self.assertFalse(self.target.exists())

    def test_copy_corruption_is_detected_before_replacement(self) -> None:
        self.run_installer("alpha")
        original_copytree = shutil.copytree

        def corrupt_copy(source: Path, destination: Path, *args, **kwargs) -> None:
            original_copytree(source, destination, *args, **kwargs)
            skill_file = Path(destination) / "SKILL.md"
            if skill_file.exists():
                skill_file.write_text("corrupt\n", encoding="utf-8")

        with patch.object(install_skill, "REPO_ROOT", self.repo), patch.object(install_skill.shutil, "copytree", corrupt_copy):
            with self.assertRaisesRegex(RuntimeError, "verification failed"):
                install_skill.install_one("alpha", self.repo / "skills" / "alpha",
                                          self.target / "alpha", self.target, self.receipts)
        self.assertEqual("# alpha\n", (self.target / "alpha" / "SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
