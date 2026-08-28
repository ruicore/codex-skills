from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicAuthoringContractTests(unittest.TestCase):
    def test_private_extraction_note_is_never_a_public_artifact(self) -> None:
        text = (REPO_ROOT / "templates" / "skill-extraction-note.md").read_text(encoding="utf-8")

        self.assertIn(".manifest/skill-intake/", text)
        self.assertIn("Never commit a completed copy", text)
        self.assertIn("Private practice is not", text)
        self.assertIn("source material for public prose", text)

    def test_public_proposal_requires_clean_room_design(self) -> None:
        text = (REPO_ROOT / "templates" / "skill-proposal.md").read_text(encoding="utf-8")

        self.assertIn("## Clean-Room Design Declaration", text)
        self.assertIn("## Independent Public Problem Domain", text)
        self.assertNotIn("## Practice-Derived Details To Keep", text)

    def test_public_issue_does_not_request_private_practice_evidence(self) -> None:
        text = (
            REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-proposal.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("label: Clean-room declaration", text)
        self.assertIn("label: Abstract capability and public need", text)
        self.assertNotIn("label: Real practice or repeated workflow evidence", text)

    def test_pull_request_requires_protected_clean_room_gate(self) -> None:
        text = (REPO_ROOT / ".github" / "pull_request_template.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/clean-room-review.md", text)
        self.assertIn("--require-denylist", text)
        self.assertIn("not an authoritative approval", text)


if __name__ == "__main__":
    unittest.main()
