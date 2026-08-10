#!/usr/bin/env python3
"""Conservative content check for files intended for publication."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def patterns() -> dict[str, str]:
    return {
        "absolute_windows_path": r"(?i)\b[a-z]:\\",
        "absolute_posix_path": r"(?m)(?<![\w.])/(?:users|home|var|opt)/",
        "url": r"(?i)\b(?:https?|ftp)://",
        "loopback": r"(?i)\b(?:local" + r"host|127\.0\.0\.1)\b",
        "endpoint_with_number": r"\b[a-z][a-z0-9_-]*:[0-9]{2,5}\b",
        "timestamp": r"\b20[0-9]{2}-[0-9]{2}-[0-9]{2}",
        "credential": r"(?i)\b(?:api[_-]?key|password|secret|token)\s*[:=]",
        "local_provenance": r"(?i)(?:up" + r"load-control-plane|c" + r"odex-runtime-evidence|\.man" + r"ifest|hid" + r"den|pri" + r"vate|author-" + r"plan)",
        "process_material": r"(?i)(?:re" + r"view)",
    }


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file() and "__pycache__" not in item.parts):
        data = path.read_text(encoding="utf-8")
        for name, expression in patterns().items():
            if re.search(expression, data):
                findings.append(f"{path.relative_to(root)}: {name}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    findings = scan(args.root)
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
