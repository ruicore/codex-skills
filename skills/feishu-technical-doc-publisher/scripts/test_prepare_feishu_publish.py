from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("prepare_feishu_publish.py")
SPEC = importlib.util.spec_from_file_location("prepare_feishu_publish", MODULE_PATH)
assert SPEC and SPEC.loader
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class PublicationPreflightTests(unittest.TestCase):
    def test_diagram_placeholder_is_generic_and_manifest_addressable(self) -> None:
        placeholder = publisher.diagram_placeholder(1)

        self.assertEqual(publisher.diagram_slot_id(1), "diagram-01")
        self.assertEqual(placeholder, "【图位 01｜发布占位】")
        self.assertNotIn(".puml", placeholder)
        self.assertNotIn("请在飞书中插入", placeholder)
        self.assertNotIn("完成后删除", placeholder)

    def test_plantuml_extraction_maps_placeholder_to_dsl(self) -> None:
        source = """\
# Flow

```plantuml
@startuml
Alice -> Bob
@enduml
```
"""
        publish_text, diagrams = publisher.extract_plantuml_diagrams(
            source, Path("generated/diagrams")
        )

        self.assertIn("【图位 01｜发布占位】", publish_text)
        self.assertNotIn("请在飞书中插入", publish_text)
        self.assertEqual(diagrams[0]["slot_id"], "diagram-01")
        self.assertEqual(diagrams[0]["placeholder"], "【图位 01｜发布占位】")
        self.assertTrue(str(diagrams[0]["path"]).endswith("diagram-01.puml"))

    def test_table_inventory_and_widths_are_content_aware(self) -> None:
        source = """\
| 季节 | 活动地点 | 观察重点 | 随身物品 |
| --- | --- | --- | --- |
| 春季 | 城市公园 | 记录开花时间、花瓣颜色与授粉昆虫的活动 | 放大镜、素描本和可重复使用的水杯 |
| 秋季 | 湖边步道 | 比较迁徙鸟类的停留时段与觅食方式 | 双筒望远镜、铅笔和轻便雨衣 |
"""
        tables = publisher.extract_markdown_tables(source)

        self.assertEqual(len(tables), 1)
        widths = tables[0]["suggested_width_percent"]
        self.assertEqual(sum(widths), 100)
        self.assertLess(widths[0], widths[2])
        self.assertLess(widths[1], widths[3])
        self.assertEqual(tables[0]["feishu_layout_status"], "required")

    def test_tables_inside_code_fences_are_ignored(self) -> None:
        source = """\
```text
| not | a table |
| --- | --- |
```
"""
        self.assertEqual(publisher.extract_markdown_tables(source), [])

    def test_standalone_diamond_is_flagged_for_feishu(self) -> None:
        diagram = """\
@startuml
rectangle "start" as Start
diamond "continue?" as Decision
@enduml
"""
        warnings = publisher.plantuml_compatibility_warnings(diagram)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["line"], 3)
        self.assertIn("if/then/else/endif", warnings[0]["message"])

    def test_standard_activity_decision_is_not_flagged(self) -> None:
        diagram = """\
@startuml
start
if (continue?) then (yes)
  :upload;
else (no)
  stop
endif
@enduml
"""
        self.assertEqual(publisher.plantuml_compatibility_warnings(diagram), [])

    def test_final_payload_does_not_count_code_comments_or_extracted_diagrams(self) -> None:
        source = """\
# Example

```python
# A code comment
print("hello")
```

```plantuml
@startuml
Alice -> Bob: hello
@enduml
```
"""
        body, diagrams = publisher.extract_plantuml_diagrams(source, Path("generated/diagrams"))
        structure = publisher.publication_structure(publisher.markdown_to_html(body))

        self.assertEqual(structure["headings"], [{"ordinal": 1, "level": 1, "text": "Example"}])
        self.assertEqual(len(structure["code_blocks"]), 1)
        self.assertEqual(structure["code_blocks"][0]["language"], "python")
        self.assertEqual(len(diagrams), 1)

    def test_rendered_headings_tables_and_indented_code_drive_the_ledger(self) -> None:
        source = """\
Overview
========

## Fish &amp; **birds**

    # This remains code
    a = "<example>"

~~~text
| example | only |
| --- | --- |
~~~

<table><tr><th>Kind</th><th>Note</th></tr><tr><td>Bird</td><td>Wetland &amp; coast</td></tr></table>
"""
        structure = publisher.publication_structure(publisher.markdown_to_html(source))

        self.assertEqual(structure["headings_by_level"], {"h1": 1, "h2": 1, "h3": 0, "h4": 0, "h5": 0, "h6": 0})
        self.assertEqual(structure["headings"][1]["text"], "Fish & birds")
        self.assertEqual(len(structure["code_blocks"]), 2)
        self.assertEqual(len(structure["tables"]), 1)
        self.assertEqual(structure["tables"][0]["headers"], ["Kind", "Note"])
        self.assertEqual(structure["tables"][0]["data_rows"], 1)

    def test_fenced_plantuml_example_is_preserved_and_tilde_diagram_is_extracted(self) -> None:
        source = """\
````text
```plantuml
@startuml
Example -> Example
@enduml
```
````

~~~plantuml
@startuml
Reader -> Guide
@enduml
~~~
"""
        body, diagrams = publisher.extract_plantuml_diagrams(source, Path("generated/diagrams"))
        structure = publisher.publication_structure(publisher.markdown_to_html(body))

        self.assertEqual(len(diagrams), 1)
        self.assertIn("Reader -> Guide", diagrams[0]["content"])
        self.assertIn("Example -> Example", body)
        self.assertEqual(len(structure["code_blocks"]), 1)

    def test_long_code_has_searchable_tail_and_closing_lines(self) -> None:
        body = '```json\n{\n  "items": [\n    "sunrise",\n    "moon & stars"\n  ]\n}\n```\n'
        structure = publisher.publication_structure(publisher.markdown_to_html(body), long_code_lines=4)
        block = structure["code_blocks"][0]

        self.assertEqual(block["line_count"], 6)
        self.assertTrue(block["requires_tail_check"])
        self.assertEqual(block["tail_marker"], '    "moon & stars"')
        self.assertEqual(block["tail_lines"], ['    "moon & stars"', '  ]', '}'])
        self.assertEqual(len(block["sha256"]), 64)

    def test_cli_dry_run_and_written_manifest_share_final_structure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "guide.md"
            output = root / "package"
            source.write_text("# Guide\n\n```python\n# comment\nprint('done')\n```\n", encoding="utf-8")
            command = [str(MODULE_PATH), str(source), "--output-dir", str(output), "--long-code-lines", "2"]
            preview = io.StringIO()
            with patch.object(sys, "argv", command + ["--dry-run"]), redirect_stdout(preview):
                publisher.main()
            self.assertFalse(output.exists())
            with patch.object(sys, "argv", command), redirect_stdout(io.StringIO()):
                publisher.main()
            manifest = json.loads((output / "publish-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 3)
            self.assertEqual(manifest["inventory"], json.loads(preview.getvalue())["inventory"])
            self.assertEqual(manifest["inventory"]["headings"], 1)
            self.assertEqual(manifest["inventory"]["code_blocks"], 1)
            self.assertEqual(manifest["inventory"]["fenced_code_blocks"], 1)
            self.assertEqual(manifest["inventory"]["long_code_blocks"], 1)
            self.assertEqual(manifest["outputs"]["publish_html_sha256"], publisher.sha256_bytes((output / "guide.publish.html").read_bytes()))


if __name__ == "__main__":
    unittest.main()
