from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
CLI = PACKAGE / "scripts" / "cpt_runtime.py"


class RuntimeKernelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cpt-alpha1-test-")
        self.root = Path(self.tmp.name) / "fixture"
        shutil.copytree(PACKAGE, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, msg=f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        return result

    def load(self, rel):
        return yaml.safe_load((self.root / rel).read_text(encoding="utf-8"))

    def test_no_active_task_is_valid(self):
        self.run_cli("validate")
        current = self.load(".cpt/current.yaml")
        self.assertIsNone(current["current_task"])
        self.assertEqual(current["runtime_status"], "ready")

    def test_standard_task_lifecycle(self):
        out = self.run_cli("create-task", "--title", "Example", "--objective", "Deliver example", "--activate").stdout.strip()
        self.assertEqual(out, "TKT-001")
        self.run_cli("lease-create", "--task", "TKT-001", "--read", "src/**", "--write", "src/example.py", "--verify", "python -m unittest")
        self.run_cli("validate")
        self.run_cli("complete-task")
        self.run_cli("validate")
        current = self.load(".cpt/current.yaml")
        self.assertIsNone(current["current_task"])
        self.assertEqual(current["runtime_status"], "ready")

    def test_micro_change_without_full_ticket(self):
        out = self.run_cli("micro-start", "--title", "Copy fix", "--intent", "Correct one label", "--target", "src/ui.tsx", "--verify", "python -m unittest", "--confirm-eligible").stdout.strip()
        self.assertEqual(out, "MC-001")
        current = self.load(".cpt/current.yaml")
        self.assertEqual(current["current_micro_change"], "MC-001")
        self.assertEqual(self.load(".cpt/task-index.yaml")["tasks"], [])
        self.run_cli("micro-complete")
        self.run_cli("validate")

    def test_checkpoint_detects_and_recovers_mismatch(self):
        self.run_cli("create-task", "--title", "Recovery", "--objective", "Test recovery", "--activate")
        cp = self.run_cli("checkpoint", "--source", "synthetic", "--reason", "test").stdout.strip()
        current_path = self.root / ".cpt/current.yaml"
        current = self.load(".cpt/current.yaml")
        current["current_task"] = None
        current["runtime_status"] = "ready"
        current["state_revision"] += 1
        current_path.write_text(yaml.safe_dump(current, sort_keys=False), encoding="utf-8")
        self.run_cli("render-summary")
        self.run_cli("recover", "--checkpoint", cp, "--verify-only", expected=2)
        self.run_cli("recover", "--checkpoint", cp)
        self.run_cli("validate")
        self.assertEqual(self.load(".cpt/current.yaml")["current_task"], "TKT-001")


    def test_micro_change_can_escalate(self):
        self.run_cli("micro-start", "--title", "Potentially systemic change", "--intent", "Start locally, then escalate", "--target", "src/ui.tsx", "--verify", "python -m unittest", "--confirm-eligible")
        self.run_cli("micro-escalate", "--reason", "Shared pattern discovered")
        current = self.load(".cpt/current.yaml")
        micro = self.load(".cpt/micro-changes/MC-001.yaml")
        self.assertIsNone(current["current_micro_change"])
        self.assertEqual(current["next_operation"]["type"], "intake")
        self.assertEqual(micro["status"], "escalated")
        self.assertEqual(micro["escalation_reason"], "Shared pattern discovered")
        self.run_cli("validate")

    def test_invalid_current_task_is_rejected(self):
        current_path = self.root / ".cpt/current.yaml"
        current = self.load(".cpt/current.yaml")
        current["runtime_status"] = "active"
        current["current_task"] = "TKT-999"
        current["state_revision"] += 1
        current_path.write_text(yaml.safe_dump(current, sort_keys=False), encoding="utf-8")
        self.run_cli("render-summary")
        result = self.run_cli("validate", expected=1)
        self.assertIn("not in task index", result.stdout)

    def test_checkpoint_tamper_is_rejected(self):
        self.run_cli("create-task", "--title", "Tamper test", "--objective", "Detect modified checkpoint", "--activate")
        cp_id = self.run_cli("checkpoint", "--source", "synthetic", "--reason", "tamper test").stdout.strip()
        cp_path = self.root / ".cpt/checkpoints" / f"{cp_id}.yaml"
        cp = self.load(cp_path.relative_to(self.root))
        cp["snapshot"]["current"]["runtime_status"] = "blocked"
        cp_path.write_text(yaml.safe_dump(cp, sort_keys=False), encoding="utf-8")
        result = self.run_cli("recover", "--checkpoint", cp_id, "--verify-only", expected=1)
        self.assertIn("integrity mismatch", result.stderr)

    def test_tkt_000_is_optional_not_current(self):
        self.run_cli("validate")
        self.assertFalse((self.root / ".cpt/tasks/TKT-000.yaml").exists())
        self.assertTrue((self.root / "examples/TKT-000-system-intake.yaml").exists())


if __name__ == "__main__":
    unittest.main()
