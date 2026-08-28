from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import validate_skills


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReaderFacingSkillMembershipTests(unittest.TestCase):
    def test_current_reader_surfaces_exactly_cover_registry_membership(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "skills" / "index.json").read_text(encoding="utf-8")
        )
        registry_names = {entry["name"] for entry in registry["skills"]}
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        taxonomy = (REPO_ROOT / "docs" / "skill-taxonomy.md").read_text(
            encoding="utf-8"
        )

        self.assertEqual(
            registry_names,
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            registry_names,
            validate_skills.extract_readme_outcome_skill_names(readme),
        )
        self.assertEqual(
            registry_names,
            validate_skills.extract_taxonomy_category_skill_names(taxonomy),
        )

    def test_membership_validation_rejects_missing_and_extra_names(self) -> None:
        validator = validate_skills.Validator()

        validator.validate_membership_surface(
            {"alpha-skill", "beta-skill"},
            {"alpha-skill", "orphan-skill"},
            "reader surface",
        )

        self.assertEqual(
            validator.errors,
            [
                "reader surface: missing registry skills: beta-skill",
                "reader surface: lists skills absent from registry: orphan-skill",
            ],
        )

    def test_extractors_are_scoped_to_their_reader_facing_sections(self) -> None:
        readme = """\
`not-a-skill`

## Skill Categories

| Category | Current skills | Primary use |
|---|---|---|
| review | `alpha-skill`, `beta-skill` | Review. |

## Skills and Engineering Outcomes

| Skill | Outcome |
|---|---|
| <a href="skills/alpha-skill/">alpha</a> | A |
| <a href="skills/beta-skill/">beta</a> | B |
"""
        taxonomy = """\
## Categories

### review

Current skills:

- `alpha-skill`
- `beta-skill` (secondary)

## Maturity Levels

- `not-a-skill`
"""

        self.assertEqual(
            {"alpha-skill", "beta-skill"},
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            {"alpha-skill", "beta-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )
        self.assertEqual(
            {"alpha-skill", "beta-skill"},
            validate_skills.extract_taxonomy_category_skill_names(taxonomy),
        )

    def test_heading_sections_accept_optional_closing_hashes(self) -> None:
        text = """\
## Skill Categories ##

content

## Next Section ###

excluded
"""

        self.assertEqual(
            "\n\ncontent\n\n",
            validate_skills.markdown_heading_section(text, "## Skill Categories"),
        )

    def test_readme_table_rows_allow_leading_whitespace(self) -> None:
        readme = """\
## Skill Categories

   | Category | Current skills | Primary use |
   | :--- | :---: | ---: |
   | review | `alpha-skill` | Review. |

## Skills and Engineering Outcomes

   | Skill | Outcome |
   |---|---|
   | <a href="skills/alpha-skill/">alpha</a> | A |
"""

        self.assertEqual(
            {"alpha-skill"},
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            {"alpha-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )

    def test_readme_outcomes_accept_html_and_markdown_skill_links(self) -> None:
        readme = """\
## Skills and Engineering Outcomes ###

| Skill | Outcome |
|---|---|
| <a href="skills/alpha-skill/">alpha</a> | A |
| [beta](skills/beta-skill/) | B |
"""

        self.assertEqual(
            {"alpha-skill", "beta-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )

    def test_taxonomy_accepts_standard_unordered_list_markers(self) -> None:
        taxonomy = """\
## Categories ##

- `alpha-skill`
* `beta-skill` (secondary)
+ `gamma-skill`

## Maturity Levels
"""

        self.assertEqual(
            {"alpha-skill", "beta-skill", "gamma-skill"},
            validate_skills.extract_taxonomy_category_skill_names(taxonomy),
        )

    def test_readme_outcomes_ignore_narrative_skill_links(self) -> None:
        readme = """\
## Skills and Engineering Outcomes

| Skill | Outcome |
|---|---|
| [alpha](skills/alpha-skill/) | A |

The missing row for [beta](skills/beta-skill/) must not be hidden by this link.
"""

        self.assertEqual(
            {"alpha-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )

    def test_membership_ignores_fenced_pseudo_surfaces(self) -> None:
        readme = """\
```markdown
## Skill Categories
| review | `fenced-heading-skill` | Hidden. |
```

## Skill Categories

~~~markdown
| review | `fenced-row-skill` | Hidden. |
~~~
| Category | Current skills | Primary use |
|---|---|---|
| review | `visible-skill` | Visible. |

## Skills and Engineering Outcomes

```html
| <a href="skills/fenced-outcome-skill/">hidden</a> | Hidden. |
```
| Skill | Outcome |
|---|---|
| [visible](skills/visible-skill/) | Visible. |
"""
        taxonomy = """\
~~~markdown
## Categories
- `fenced-heading-skill`
~~~

## Categories

```markdown
* `fenced-list-skill`
```
+ `visible-skill`

## Maturity Levels
"""

        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )
        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_taxonomy_category_skill_names(taxonomy),
        )

    def test_membership_ignores_four_space_indented_pseudo_surfaces(self) -> None:
        readme = """\
    ## Skill Categories
    | review | `indented-heading-skill` | Hidden. |

## Skill Categories

    | review | `indented-row-skill` | Hidden. |
   | Category | Current skills | Primary use |
   |---|---|---|
   | review | `visible-skill` | Visible. |

## Skills and Engineering Outcomes

    | [hidden](skills/indented-outcome-skill/) | Hidden. |
   | Skill | Outcome |
   |---|---|
   | [visible](skills/visible-skill/) | Visible. |
"""
        taxonomy = """\
    ## Categories
    - `indented-heading-skill`

## Categories

    * `indented-list-skill`
   + `visible-skill`

## Maturity Levels
"""

        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_readme_outcome_skill_names(readme),
        )
        self.assertEqual(
            {"visible-skill"},
            validate_skills.extract_taxonomy_category_skill_names(taxonomy),
        )

    def test_isolated_pipe_delimited_paragraphs_do_not_count(self) -> None:
        readme = """\
## Skill Categories

| review | `isolated-category-skill` | This is not a table. |

## Skills and Engineering Outcomes

| [isolated](skills/isolated-outcome-skill/) | This is also not a table. |
"""

        self.assertEqual(
            set(),
            validate_skills.extract_readme_category_skill_names(readme),
        )
        self.assertEqual(
            set(),
            validate_skills.extract_readme_outcome_skill_names(readme),
        )


if __name__ == "__main__":
    unittest.main()
