from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("prepare_feishu_publish.py")
SPEC = importlib.util.spec_from_file_location("prepare_feishu_publish", MODULE_PATH)
assert SPEC and SPEC.loader
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class PublicationPreflightTests(unittest.TestCase):
    def test_table_inventory_and_widths_are_content_aware(self) -> None:
        source = """\
| 阶段 | 执行位置 | 主要能力 | 平台记录 |
| --- | --- | --- | --- |
| 一期 | Edge Uploader 端侧 | 参数下发、端侧执行、对象级精简结果、Dataset 入库血缘 | 模板、不可变 profile、对象及 Dataset 的 ingest 结果 |
| 二期 | 平台 Worker | 对已上传 Dataset 重检、集中统计、审计和算法演进 | quality_run 与 quality_run_item 历史 |
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


if __name__ == "__main__":
    unittest.main()
