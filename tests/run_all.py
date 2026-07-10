#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run(command: list[str], *, timeout: int = 120) -> None:
    print("+", " ".join(map(str, command)), flush=True)
    completed = subprocess.run(command, cwd=ROOT, text=True, timeout=timeout)
    if completed.returncode:
        raise SystemExit(completed.returncode)


# Run each distribution case in an isolated interpreter. This keeps temporary
# HOME/CODEX_HOME state and installer subprocesses from leaking across cases.
suite = unittest.defaultTestLoader.loadTestsFromName("tests.test_distribution")
test_ids = [test.id() for test in flatten(suite)]
for test_id in test_ids:
    run([sys.executable, "-m", "unittest", "-v", test_id], timeout=120)

commands = [
    [sys.executable, str(ROOT / "tools" / "validate_distribution.py")],
    [sys.executable, str(ROOT / "tools" / "validate_skills.py"), "--root", str(ROOT)],
    [
        sys.executable,
        str(ROOT / "tools" / "eval_skill_triggers.py"),
        "--root",
        str(ROOT),
        "--write-report",
        str(ROOT / "evaluation" / "trigger-eval-report.json"),
    ],
    [sys.executable, str(ROOT / "tools" / "measure_all_skill_metadata.py")],
]
for command in commands:
    run(command, timeout=180)

print(f"ALPHA 3 COMPLETE TEST SUITE PASSED: {len(test_ids)} distribution cases")
