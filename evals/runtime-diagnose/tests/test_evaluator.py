from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import score  # noqa: E402
from lib import load_cases  # noqa: E402
from public_hygiene import scan  # noqa: E402


def safe_plan(case: dict) -> dict:
    gap = []
    if case.get("required_gap"):
        gap = [{"class": case["required_gap"], "blocked_conclusion": "The supplied record cannot establish a cause or repair.", "next_observation": "Read current workload identity metadata."}]
    return {
        "schema_version": "diagnosis_plan/v1",
        "case_id": case["id"],
        "authority": {"allowed_observations": case["authority"]["allowed_observations"], "prohibited_mutations": case["authority"]["prohibited_mutations"], "proposed_operations": [{"operation": "read identity metadata", "kind": "read", "authorized": True}]},
        "observations": [{"claim": "This statement is directly supplied by the fixture.", "source": "synthetic fixture"}],
        "inferences": [{"claim": "The evidence supports only a bounded next observation.", "status": "bounded"}],
        "runtime_identity": {"fields": ["workload identity"], "source": "synthetic fixture", "status": case["runtime_identity_requirement"]},
        "freshness": {"assessment": "The supplied evidence is assessed only as fixture input.", "evidence_basis": ["synthetic fixture"], "status": "assessed"},
        "correlation": {"method": "Use the supplied fixture relationship only.", "timezone_handling": "No time conversion is asserted.", "status": "ambiguous"},
        "assertions": [{"kind": "root_cause", "claim": "No cause is asserted.", "status": "not_asserted", "evidence_basis": []}, {"kind": "fix", "claim": "No repair is asserted.", "status": "not_asserted", "evidence_basis": []}],
        "visibility_gaps": gap,
        "minimal_evidence": ["identity", "freshness", "correlation"],
        "next_observations": ["Read permitted identity metadata."]
    }


class EvaluatorTests(unittest.TestCase):
    def test_safe_plans_pass(self) -> None:
        results = [score(case, safe_plan(case)) for case in load_cases()]
        self.assertTrue(all(item["passed"] for item in results))
        self.assertTrue(all(not item["unsafe"] for item in results))

    def test_mutation_is_rejected(self) -> None:
        case = load_cases()[0]
        plan = safe_plan(case)
        plan["authority"]["proposed_operations"] = [{"operation": "restart workload", "kind": "mutation", "authorized": False}]
        result = score(case, plan)
        self.assertTrue(result["unsafe"])
        self.assertIn("mutation_operation", result["unsafe_reasons"])

    def test_identity_gap_rejects_identity_claim(self) -> None:
        case = load_cases()[0]
        plan = safe_plan(case)
        plan["runtime_identity"]["status"] = "observed"
        result = score(case, plan)
        self.assertTrue(result["unsafe"])
        self.assertIn("unsupported_runtime_identity_claim", result["unsafe_reasons"])

    def test_cli_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            plans = work / "plans"
            plans.mkdir()
            for case in load_cases():
                (plans / f"{case['id']}.json").write_text(json.dumps(safe_plan(case)), encoding="utf-8")
            outputs = [work / "one.json", work / "two.json"]
            for output in outputs:
                result = subprocess.run([sys.executable, str(ROOT / "scripts" / "evaluate.py"), "--plans", str(plans), "--output", str(output)], check=False, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())

    def test_cli_rejects_package_local_output_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            plans = work / "plans"
            plans.mkdir()
            for case in load_cases():
                (plans / f"{case['id']}.json").write_text(json.dumps(safe_plan(case)), encoding="utf-8")
            nested_output = ROOT / "generated-test-output" / "report.json"
            self.assertFalse(nested_output.parent.exists())
            for output in (ROOT, nested_output):
                result = subprocess.run([sys.executable, str(ROOT / "scripts" / "evaluate.py"), "--plans", str(plans), "--output", str(output)], check=False, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("must resolve outside", result.stderr)
            self.assertFalse(nested_output.parent.exists())
            self.assertFalse(nested_output.exists())

    def test_hygiene_scan_is_clean(self) -> None:
        self.assertEqual(scan(ROOT), [])


if __name__ == "__main__":
    unittest.main()
