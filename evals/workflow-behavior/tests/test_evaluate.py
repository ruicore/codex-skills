import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow_evaluate", ROOT / "evaluate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DecisionEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))
        self.answers = [{"id": c["id"], "action": c["expected"],
                         "preserve": c["must_preserve"], "rationale": "Synthetic protocol fixture."}
                        for c in self.cases]

    def test_complete_contract_passes(self):
        self.assertTrue(module.evaluate(self.cases, self.answers)["pass"])

    def test_missing_and_duplicate_answers_fail(self):
        self.assertFalse(module.evaluate(self.cases, self.answers[:-1])["pass"])
        self.assertFalse(module.evaluate(self.cases, self.answers + self.answers[:1])["pass"])

    def test_wrong_action_and_boundary_fail(self):
        self.answers[0]["action"] = "publish"
        self.answers[1]["preserve"] = []
        report = module.evaluate(self.cases, self.answers)
        self.assertFalse(report["pass"])
        self.assertEqual(report["passed"], len(self.cases) - 2)

    def test_unknown_response_cannot_hide_extra_action(self):
        self.answers.append({"id": "unsolicited-operation"})
        self.assertFalse(module.evaluate(self.cases, self.answers)["pass"])

    def test_malformed_input_is_rejected(self):
        with self.assertRaises(ValueError):
            module.evaluate(self.cases, {})


if __name__ == "__main__":
    unittest.main()
