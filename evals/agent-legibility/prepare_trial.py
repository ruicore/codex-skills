#!/usr/bin/env python3
"""Prepare fresh review packets and an operator-only assignment record; no model calls."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import random
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHORT_GUIDANCE = (
    "Consider whether a future coding agent could choose the wrong edit point, "
    "trust the wrong authority, or miss a related consumer. Check existing "
    "navigation before recommending a change."
)


def load_cases() -> list[dict]:
    cases = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))["cases"]
    for case in cases:
        for name, content in case["files"].items():
            path = PurePosixPath(name)
            if (path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name
                    or not isinstance(content, str)):
                raise ValueError("fixture requires safe relative paths and text contents")
    return cases


def prepare(output: Path, seed: int, repeats: int) -> dict:
    output = output.resolve()
    if output.is_relative_to(ROOT) or ROOT.is_relative_to(output):
        raise ValueError("trial output must be outside and must not contain the source repository")
    if output.exists():
        raise ValueError("trial output already exists; use a new directory")
    if repeats < 2:
        raise ValueError("use at least two attempts per case and condition")
    cases = load_cases()
    skill = ROOT / "skills/agent-legibility-review/SKILL.md"
    skill_bytes = skill.read_bytes()
    skill_text = skill_bytes.decode("utf-8")
    registry = json.loads((ROOT / "skills/index.json").read_text(encoding="utf-8"))
    entry = next(item for item in registry["skills"] if item["name"] == "agent-legibility-review")
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    assignments = [(case, arm, repetition) for case in cases for arm in ("A", "B", "C")
                   for repetition in range(1, repeats + 1)]
    random.Random(seed).shuffle(assignments)
    output.mkdir(parents=True)
    records = []
    for index, (case, arm, repetition) in enumerate(assignments, 1):
        run_id = f"run-{index:03d}"
        packet = output / "packets" / run_id
        workspace = packet / "workspace"
        workspace.mkdir(parents=True)
        for name, content in case["files"].items():
            path = workspace / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        guidance = {"A": "", "B": SHORT_GUIDANCE, "C": skill_text}[arm]
        prompt = case["task"] + "\n\nInspect only the supplied workspace. Keep it unchanged.\n"
        if guidance:
            prompt += "\nAdditional review guidance:\n\n" + guidance + "\n"
        prompt_bytes = prompt.encode("utf-8")
        (packet / "task.md").write_bytes(prompt_bytes)
        fixture_digest = hashlib.sha256(json.dumps(case["files"], sort_keys=True).encode("utf-8")).hexdigest()
        records.append({"run_id": run_id, "case": case["id"], "condition": arm,
                        "repetition": repetition, "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
                        "fixture_sha256": fixture_digest, "status": "not_run"})
    operator = output / "operator"
    operator.mkdir()
    (operator / "rubric.json").write_text(json.dumps(
        {case["id"]: case["grading"] for case in cases}, indent=2) + "\n", encoding="utf-8")
    plan = {"schema_version": 1, "status": "not_run", "seed": seed, "repeats": repeats,
            "source_commit": commit, "skill_version": entry["version"],
            "skill_sha256": hashlib.sha256(skill_bytes).hexdigest(), "runs": records}
    (operator / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return {"status": "prepared_not_run", "packet_count": len(records), "skill_sha256": plan["skill_sha256"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--repeats", type=int, default=2)
    args = parser.parse_args()
    try:
        result = prepare(args.output, args.seed, args.repeats)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
