#!/usr/bin/env python3
"""Evaluate a small, visible decision protocol; this is not an agent benchmark."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CASES = Path(__file__).with_name("cases.json")


def evaluate(cases: list[dict], answers: list[dict]) -> dict:
    if not isinstance(answers, list) or any(not isinstance(a, dict) for a in answers):
        raise ValueError("responses must be an array of objects")
    ids = [case["id"] for case in cases]
    if len(set(ids)) != len(ids):
        raise ValueError("case ids must be unique")
    seen: dict[str, dict] = {}
    errors: list[str] = []
    for answer in answers:
        key = answer.get("id")
        if not isinstance(key, str) or key not in ids:
            errors.append("unknown or missing response id")
        elif key in seen:
            errors.append("duplicate response id: " + key)
        else:
            seen[key] = answer
    results = []
    for case in cases:
        answer = seen.get(case["id"], {})
        preserved = answer.get("preserve", [])
        valid_preserve = isinstance(preserved, list) and all(isinstance(x, str) for x in preserved)
        rationale = answer.get("rationale")
        passed = (
            answer.get("action") == case["expected"]
            and valid_preserve
            and set(case["must_preserve"]).issubset(preserved)
            and isinstance(rationale, str) and bool(rationale.strip())
        )
        results.append({"id": case["id"], "pass": bool(passed)})
    return {"schema_version": 1, "passed": sum(r["pass"] for r in results),
            "total": len(cases), "errors": errors, "results": results,
            "pass": not errors and all(r["pass"] for r in results),
            "boundary": "Visible decision contract only; rationale needs human review. No live execution is proven."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--cases", type=Path, default=CASES)
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(args.cases.read_text(encoding="utf-8")),
                          json.loads(args.responses.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Invalid evaluation input: {exc}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
