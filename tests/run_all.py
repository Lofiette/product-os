#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run(command: list[str], *, timeout: int = 300) -> None:
    print("+", " ".join(map(str, command)), flush=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(command, cwd=ROOT, text=True, timeout=timeout, env=env)
    if completed.returncode:
        raise SystemExit(completed.returncode)


# Each case runs in an isolated interpreter. Temporary HOME/CODEX_HOME,
# installer state, mocks, and Python globals must not leak between tests.
suite = unittest.TestSuite(
    [
        unittest.defaultTestLoader.loadTestsFromName("tests.test_distribution"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_skills"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_roles"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_knowledge"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_enforcement"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_orchestration"),
        unittest.defaultTestLoader.loadTestsFromName("tests.test_evaluation"),
    ]
)
test_ids = [test.id() for test in flatten(suite)]
for test_id in test_ids:
    run([sys.executable, "-m", "unittest", "-v", test_id], timeout=360)

commands = [
    [sys.executable, str(ROOT / "tools" / "validate_orchestration.py")],
    [sys.executable, str(ROOT / "tools" / "eval_orchestration.py")],
    [sys.executable, str(ROOT / "tools" / "run_orchestration_integration.py")],
    [sys.executable, str(ROOT / "tools" / "validate_enforcement.py")],
    [sys.executable, str(ROOT / "tools" / "eval_enforcement.py")],
    [sys.executable, str(ROOT / "tools" / "validate_knowledge_assets.py")],
    [
        sys.executable,
        str(ROOT / "tools" / "validate_knowledge.py"),
        "--project",
        str(ROOT / "payload" / "repo-scaffold"),
    ],
    [sys.executable, str(ROOT / "tools" / "validate_roles.py"), "--root", str(ROOT)],
    [
        sys.executable,
        str(ROOT / "tools" / "eval_knowledge_lifecycle.py"),
        "--root",
        str(ROOT),
        "--write-report",
        str(ROOT / "evaluation" / "knowledge-lifecycle-eval-report.json"),
    ],
    [
        sys.executable,
        str(ROOT / "tools" / "eval_role_routing.py"),
        "--root",
        str(ROOT),
        "--write-report",
        str(ROOT / "evaluation" / "role-routing-eval-report.json"),
    ],
    [sys.executable, str(ROOT / "tools" / "validate_evaluation.py")],
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
    run(command, timeout=600)

# Generated reports live outside the immutable package tree. This both tests the
# executable plane and proves that validation does not self-pollute MANIFEST.json.
eval_tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha8-run-all-evals-"))
try:
    run(
        [
            sys.executable,
            str(ROOT / "tools" / "cpt_eval.py"),
            "run",
            "--suite",
            "offline-core",
            "--backend",
            "reference",
            "--report-dir",
            str(eval_tmp / "offline-core"),
        ],
        timeout=1800,
    )
    scorecard = eval_tmp / "offline-core" / "offline-core-reference-scorecard.json"
    run(
        [
            sys.executable,
            str(ROOT / "tools" / "cpt_eval.py"),
            "compare-baseline",
            "--current",
            str(scorecard),
            "--baseline",
            str(ROOT / "evaluation" / "executable" / "baselines" / "offline-core-alpha8.json"),
            "--output",
            str(eval_tmp / "baseline-comparison.json"),
        ],
        timeout=120,
    )
    run(
        [
            sys.executable,
            str(ROOT / "tools" / "cpt_eval.py"),
            "mutate",
            "--scorecard",
            str(scorecard),
            "--output",
            str(eval_tmp / "mutation-report.json"),
        ],
        timeout=120,
    )
    # Running the eval plane must not dirty or extend the immutable package tree.
    run([sys.executable, str(ROOT / "tools" / "validate_distribution.py")], timeout=300)
finally:
    shutil.rmtree(eval_tmp, ignore_errors=True)

print(f"ALPHA 8 COMPLETE TEST SUITE PASSED: {len(test_ids)} behavioral cases")
