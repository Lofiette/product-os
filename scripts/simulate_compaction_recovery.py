#!/usr/bin/env python3
from __future__ import annotations

import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
CLI = PACKAGE / "scripts" / "cpt_runtime.py"


def run(root: Path, *args: str, expected=(0,)) -> subprocess.CompletedProcess:
    result = subprocess.run([sys.executable, str(CLI), "--root", str(root), *args], text=True, capture_output=True)
    if result.returncode not in expected:
        raise RuntimeError(f"command failed {args}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump(path: Path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="cpt-alpha1-recovery-") as tmp:
        root = Path(tmp) / "fixture"
        shutil.copytree(PACKAGE, root)
        run(root, "create-task", "--title", "Synthetic standard task", "--objective", "Verify checkpoint recovery", "--task-type", "validation", "--complexity", "standard", "--activate")
        run(root, "lease-create", "--task", "TKT-001", "--read", "src/example/**", "--write", "src/example/**", "--verify", "python -m unittest", "--rationale", "Synthetic recovery test")
        cp = run(root, "checkpoint", "--source", "synthetic", "--reason", "Before simulated compaction").stdout.strip()

        current_path = root / ".cpt" / "current.yaml"
        index_path = root / ".cpt" / "task-index.yaml"
        task_path = root / ".cpt" / "tasks" / "TKT-001.yaml"
        current = load(current_path)
        index = load(index_path)
        task = load(task_path)

        # Simulate loss of active context and task state.
        current["current_task"] = None
        current["current_lease"] = None
        current["runtime_status"] = "ready"
        current["next_operation"] = {"type": "await_user_task", "summary": "Incorrect compacted state"}
        current["state_revision"] += 1
        index["tasks"][0]["status"] = "proposed"
        task["status"] = "proposed"
        dump(current_path, current)
        dump(index_path, index)
        dump(task_path, task)
        run(root, "render-summary")

        mismatch = run(root, "recover", "--checkpoint", cp, "--verify-only", expected=(2,))
        if "CHECKPOINT MISMATCH" not in mismatch.stdout:
            raise RuntimeError("Expected mismatch was not detected")
        run(root, "recover", "--checkpoint", cp)
        run(root, "validate")

        restored = load(current_path)
        if restored["current_task"] != "TKT-001" or not restored["current_lease"]:
            raise RuntimeError("Recovery did not restore task/lease")
        print("SYNTHETIC COMPACTION RECOVERY PASSED")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
