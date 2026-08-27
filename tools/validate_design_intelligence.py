#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "evaluation" / "design-intelligence"


def fail(errors: list[str]) -> int:
    print("DESIGN INTELLIGENCE VALIDATION FAILED")
    for error in errors:
        print("ERROR:", error)
    return 1


def main() -> int:
    errors: list[str] = []
    rubric = json.loads((DIR / "rubric.json").read_text(encoding="utf-8"))
    cases = json.loads((DIR / "baseline-cases.json").read_text(encoding="utf-8"))

    if rubric.get("schema") != "cpt-design-intelligence-rubric-v1":
        errors.append("rubric schema mismatch")
    dimensions = rubric.get("dimensions", [])
    dimension_ids = [item.get("id") for item in dimensions]
    if len(dimension_ids) != 16 or len(set(dimension_ids)) != 16:
        errors.append("rubric must contain 16 unique dimensions")
    expected = {f"D{i}" for i in range(1, 17)}
    if set(dimension_ids) != expected:
        errors.append("dimension ids must be D1..D16")

    for profile, weights in rubric.get("profiles", {}).items():
        if set(weights) != expected:
            errors.append(f"profile {profile} does not cover every dimension")
        if any(not isinstance(value, (int, float)) or value <= 0 for value in weights.values()):
            errors.append(f"profile {profile} has invalid weight")

    if cases.get("schema") != "cpt-design-intelligence-cases-v1":
        errors.append("case schema mismatch")
    items = cases.get("cases", [])
    if cases.get("case_count") != len(items):
        errors.append("case_count mismatch")
    ids = [item.get("id") for item in items]
    if len(ids) != len(set(ids)) or len(items) < 10:
        errors.append("cases must contain at least 10 unique ids")

    profiles = set(rubric.get("profiles", {}))
    required_fields = {
        "id", "title", "type", "profile", "prompt", "context",
        "required_evidence", "expected_behaviors", "critical_errors", "target_dimensions"
    }
    for item in items:
        missing = required_fields - set(item)
        if missing:
            errors.append(f"{item.get('id')}: missing fields {sorted(missing)}")
        if item.get("profile") not in profiles:
            errors.append(f"{item.get('id')}: unknown profile")
        targets = set(item.get("target_dimensions", []))
        if not targets or not targets <= expected:
            errors.append(f"{item.get('id')}: invalid target dimensions")
        for field in ("required_evidence", "expected_behaviors", "critical_errors"):
            if not item.get(field):
                errors.append(f"{item.get('id')}: empty {field}")

    if errors:
        return fail(errors)
    print(f"DESIGN INTELLIGENCE VALIDATION PASSED: {len(dimensions)} dimensions, {len(items)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
