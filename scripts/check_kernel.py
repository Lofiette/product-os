#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def validate_template(data_rel: str, schema_rel: str) -> list[str]:
    data_path = ROOT / data_rel
    schema_path = ROOT / schema_rel
    data = yaml.safe_load(data_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{data_rel}:{'.'.join(str(x) for x in error.path) or '<root>'}: {error.message}"
        for error in validator.iter_errors(data)
    ]


def main() -> int:
    failures: list[str] = []
    agents = ROOT / "AGENTS.md"
    size = agents.stat().st_size
    if size > 8192:
        failures.append(f"AGENTS.md too large for Alpha 1 target: {size} bytes")
    text = agents.read_text(encoding="utf-8")
    required = [
        "current_task: null",
        "Micro Change",
        "authorization lease",
        "checkpoint",
        "External services are optional",
    ]
    for phrase in required:
        if phrase not in text:
            failures.append(f"AGENTS.md missing invariant: {phrase}")

    template_pairs = [
        ("templates/task.template.yaml", "schemas/task.schema.json"),
        ("templates/authorization-lease.template.yaml", "schemas/authorization-lease.schema.json"),
        ("templates/checkpoint.template.yaml", "schemas/checkpoint.schema.json"),
        ("templates/micro-change.template.yaml", "schemas/micro-change.schema.json"),
        ("examples/TKT-000-system-intake.yaml", "schemas/task.schema.json"),
    ]
    for data_rel, schema_rel in template_pairs:
        failures.extend(validate_template(data_rel, schema_rel))

    # Project-specific terminology is checked by the release pipeline against an external denylist.
    # The universal core must not embed private project names in its own scanner configuration.
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cpt_runtime.py"), "--root", str(ROOT), "validate"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        failures.append(result.stdout + result.stderr)

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "simulate_compaction_recovery.py")],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        failures.append(result.stdout + result.stderr)

    if failures:
        print("KERNEL CHECK FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print(f"KERNEL CHECK PASSED: AGENTS.md={size} bytes; templates={len(template_pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
