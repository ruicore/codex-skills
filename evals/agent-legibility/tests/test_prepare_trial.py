import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / "prepare_trial.py"))


class TrialPreparationTests(unittest.TestCase):
    def test_equal_fixtures_distinct_treatments_no_answers_in_packets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "trial"
            result = MODULE["prepare"](output, 17, 2)
            self.assertEqual(result["packet_count"], 18)
            self.assertEqual(result["status"], "prepared_not_run")
            plan = json.loads((output / "operator/plan.json").read_text(encoding="utf-8"))
            cases = {case["id"]: case for case in MODULE["load_cases"]()}
            combinations = set()
            for run in plan["runs"]:
                combinations.add((run["case"], run["condition"], run["repetition"]))
                self.assertEqual(run["status"], "not_run")
                packet = output / "packets" / run["run_id"]
                self.assertEqual({path.name for path in packet.iterdir()}, {"task.md", "workspace"})
                prompt = (packet / "task.md").read_bytes()
                self.assertEqual(hashlib.sha256(prompt).hexdigest(), run["prompt_sha256"])
                workspace = packet / "workspace"
                observed = {path.relative_to(workspace).as_posix(): path.read_text(encoding="utf-8")
                            for path in workspace.rglob("*") if path.is_file()}
                self.assertEqual(observed, cases[run["case"]]["files"])
                text = prompt.decode("utf-8")
                self.assertEqual(MODULE["SHORT_GUIDANCE"] in text, run["condition"] == "B")
                self.assertEqual("# Agent Legibility Review" in text, run["condition"] == "C")
            self.assertEqual(len(combinations), 18)
            with self.assertRaisesRegex(ValueError, "already exists"):
                MODULE["prepare"](output, 17, 2)

    def test_source_destination_and_single_attempt_rejected_before_write(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            MODULE["prepare"](MODULE["ROOT"] / "trial-output", 17, 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "trial"
            with self.assertRaisesRegex(ValueError, "two attempts"):
                MODULE["prepare"](output, 17, 1)
            self.assertFalse(output.exists())

    def test_fixture_source_is_executable(self):
        for case in MODULE["load_cases"]():
            with self.subTest(case=case["id"]):
                with tempfile.TemporaryDirectory() as directory:
                    workspace = Path(directory)
                    for name, content in case["files"].items():
                        path = workspace / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(content, encoding="utf-8")
                    result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover"],
                                            cwd=workspace, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
