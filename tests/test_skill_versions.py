from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import unittest

from scripts import list_skills, validate_skills


class SkillVersionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entry = json.loads(validate_skills.INDEX_PATH.read_text(encoding="utf-8"))["skills"][0]
        self.enums = validate_skills.Validator().load_registry_schema_enums()

    def test_validator_accepts_independent_normal_versions(self) -> None:
        for version in ("0.1.0", "0.12.3", "1.0.0", "12.34.56"):
            with self.subTest(version=version):
                entry = copy.deepcopy(self.entry)
                entry["version"] = version
                validator = validate_skills.Validator()
                context = validator.validate_registry_entry(0, entry, set(), self.enums)
                self.assertIsNotNone(context)
                self.assertEqual([], validator.errors)

    def test_validator_rejects_missing_or_invalid_versions(self) -> None:
        missing = copy.deepcopy(self.entry)
        del missing["version"]
        validator = validate_skills.Validator()
        self.assertIsNone(validator.validate_registry_entry(0, missing, set(), self.enums))
        self.assertTrue(any("missing required field 'version'" in error for error in validator.errors))

        for version in (None, 1, True, "", " ", "1.2", "01.2.3", "1.02.3", "1.2.03",
                        "-1.2.3", "1.2.3-rc.1", "1.2.3+build", "1.2.3\n"):
            with self.subTest(version=version):
                entry = copy.deepcopy(self.entry)
                entry["version"] = version
                validator = validate_skills.Validator()
                validator.validate_registry_entry(0, entry, set(), self.enums)
                self.assertTrue(any(".version:" in error for error in validator.errors))

    def test_listing_shows_each_skill_version_with_optional_categories(self) -> None:
        entries = [
            {"name": "alpha", "version": "0.2.1", "category": "review",
             "secondary_categories": ["planning"]},
            {"name": "beta", "version": "1.0.0", "category": "review"},
        ]
        for show_secondary in (False, True):
            with self.subTest(show_secondary=show_secondary):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    list_skills.render_table(entries, show_secondary=show_secondary)
                lines = output.getvalue().splitlines()
                self.assertIn("version", lines[0].split())
                alpha = next(line for line in lines if line.startswith("alpha"))
                beta = next(line for line in lines if line.startswith("beta"))
                self.assertIn("0.2.1", alpha)
                self.assertIn("1.0.0", beta)
                if show_secondary:
                    self.assertIn("planning", alpha)

    def test_schema_and_validator_agree_on_version_boundaries(self) -> None:
        schema = json.loads(validate_skills.REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
        pattern = schema["definitions"]["skill"]["properties"]["version"]["pattern"]
        for version, expected in (("0.1.0", True), ("12.34.56", True), ("01.2.3", False),
                                  ("1.2.3-rc.1", False), ("1.2.3+build", False),
                                  ("1.2.3\n", False), ("1.2.3\r\n", False)):
            with self.subTest(version=version):
                self.assertEqual(expected, re.search(pattern, version) is not None)
                entry = copy.deepcopy(self.entry)
                entry["version"] = version
                validator = validate_skills.Validator()
                validator.validate_registry_entry(0, entry, set(), self.enums)
                self.assertEqual(expected, not validator.errors)


if __name__ == "__main__":
    unittest.main()
