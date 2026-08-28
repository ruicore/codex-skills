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
        self.assertIn("Automated checks do not replace", text)
        self.assertIn("- Reviewer:", text)
        self.assertIn("- Reviewed revision:", text)
        self.assertIn("The review outcome is `pass`", text)
        self.assertIn(
            "- Outcome: exactly one of `pass`, `rewrite-required`, `remove`, "
            "or `needs-public-source`",
            text,
        )

    def test_authoring_surfaces_preserve_the_clean_room_boundary(self) -> None:
        surfaces = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "repository-contract.md",
            REPO_ROOT / "docs" / "skill-taxonomy.md",
            REPO_ROOT / "docs" / "skill-authoring-guide.md",
            REPO_ROOT / "docs" / "side-effect-policy.md",
            REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-proposal.yml",
            REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-improvement.yml",
        ]

        for path in surfaces:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8").lower()
                self.assertIn("independently design", text)
                self.assertTrue(
                    "private practice" in text or "private source material" in text
                )

    def test_high_risk_identifier_only_guidance_does_not_return(self) -> None:
        paths = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "repository-contract.md",
            REPO_ROOT / "docs" / "skill-taxonomy.md",
            REPO_ROOT / "docs" / "skill-authoring-guide.md",
            REPO_ROOT / "docs" / "side-effect-policy.md",
            REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-proposal.yml",
            REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-improvement.yml",
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

        forbidden_guidance = [
            "Replace private customer, employer, project, issue, URL, dashboard, hostname,",
            "Do not remove specific practice-derived details only because they are local.",
            "Prefer placeholders and portability notes over private examples.",
            "Keep practice-derived material when it is useful and safe",
            "keep practice-derived safety rules when they are useful",
        ]
        for phrase in forbidden_guidance:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
