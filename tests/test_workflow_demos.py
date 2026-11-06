import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowDemoTests(unittest.TestCase):
    def test_independent_demos_report_only_public_summary(self):
        for demo, section in (("install", "installation"), ("scope", "commit_scope")):
            with self.subTest(demo=demo):
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / "scripts/demo_workflow_tools.py"), "--demo", demo],
                    capture_output=True, text=True, check=True,
                )
                output = json.loads(result.stdout)
                self.assertEqual(set(output), {section})
                self.assertNotIn(str(ROOT), result.stdout)
                checks = {key: value for key, value in output[section].items()
                          if key not in {"skill", "version"}}
                self.assertTrue(checks)
                self.assertTrue(all(value is True for value in checks.values()))

    def test_repository_and_index_overrides_cannot_change_another_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "protected"
            repo.mkdir()
            # Fixture setup must not itself inherit the developer's Git context.
            environment = {name: value for name, value in os.environ.items()
                           if not name.upper().startswith("GIT_")}
            environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_SYSTEM=os.devnull,
                               GIT_CONFIG_GLOBAL=os.devnull)

            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], env=environment,
                               capture_output=True, text=True, check=True)

            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.invalid")
            for name in ("existing.txt", "task.txt"):
                (repo / name).write_text("protected baseline\n", encoding="utf-8")
            git("add", "existing.txt", "task.txt")
            git("-c", "core.hooksPath=", "-c", "commit.gpgsign=false",
                "commit", "-qm", "fixture baseline")
            (repo / "existing.txt").write_text("protected staged edit\n", encoding="utf-8")
            git("add", "existing.txt")
            (repo / "task.txt").write_text("protected unstaged edit\n", encoding="utf-8")

            def fingerprint():
                return {path.relative_to(repo).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in repo.rglob("*") if path.is_file()}

            before = fingerprint()
            index_override = {"GIT_INDEX_FILE": str(repo / ".git/index")}
            redirected = dict(index_override, GIT_DIR=str(repo / ".git"), GIT_WORK_TREE=str(repo))
            for demo, overrides in (("scope", index_override), ("scope", redirected),
                                    ("install", redirected)):
                with self.subTest(demo=demo, overrides=sorted(overrides)):
                    result = subprocess.run(
                        [sys.executable, "-B", str(ROOT / "scripts/demo_workflow_tools.py"), "--demo", demo],
                        env=dict(os.environ, **overrides), capture_output=True, text=True,
                    )
                    self.assertEqual(fingerprint(), before,
                                     "the protected repository configuration, index, or files changed")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("installation" if demo == "install" else "commit_scope",
                                  json.loads(result.stdout))

    def test_external_signing_and_hooks_config_is_not_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            hooks = base / "hooks"
            hooks.mkdir()
            hook = hooks / "pre-commit"
            hook.write_text("#!/bin/sh\nexit 97\n", encoding="utf-8")
            hook.chmod(0o755)
            config = base / "external.gitconfig"
            config.write_text(
                '[commit]\n    gpgsign = true\n[gpg]\n    program = unavailable-demo-signer\n'
                f'[core]\n    hooksPath = "{hooks.as_posix()}"\n', encoding="utf-8",
            )
            environment = dict(os.environ, GIT_CONFIG_GLOBAL=str(config), GIT_CONFIG_SYSTEM=str(config),
                               GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="commit.gpgsign",
                               GIT_CONFIG_VALUE_0="true")
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "scripts/demo_workflow_tools.py"), "--demo", "scope"],
                env=environment, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["commit_scope"]["narrowed_scope_passed"])


if __name__ == "__main__":
    unittest.main()
