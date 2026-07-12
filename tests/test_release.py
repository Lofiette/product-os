from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "cpt_release.py"


class ReleasePlaneTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, capture_output=True)
        if check and proc.returncode:
            self.fail(proc.stdout + proc.stderr)
        return proc

    def test_gate_registry_has_nine_unique_gates(self):
        data = json.loads((ROOT / "release" / "GATES.json").read_text())
        ids = [x["id"] for x in data["gates"]]
        self.assertEqual(len(ids), 9)
        self.assertEqual(len(set(ids)), 9)

    def test_trial_registry_has_thirty_three_unique_tracks(self):
        data = json.loads((ROOT / "release" / "TRIALS.json").read_text())
        ids = [x["id"] for x in data["tracks"]]
        self.assertEqual(len(ids), 33)
        self.assertEqual(len(set(ids)), 33)

    def test_offline_assessment_is_beta_ready(self):
        data = json.loads(self.run_cli("assess", "--scope", "offline").stdout)
        self.assertEqual(data["status"], "BETA_READY")
        self.assertEqual(data["summary"]["blocked"], 0)

    def test_rc_assessment_is_blocked_without_live_evidence(self):
        proc = self.run_cli("assess", "--scope", "rc", check=False)
        self.assertNotEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "BLOCKED")
        self.assertGreaterEqual(data["summary"]["pending"], 3)

    def test_offline_readiness_counts_release_assets(self):
        data = json.loads(self.run_cli("readiness", "--scope", "offline").stdout)
        self.assertEqual(data["status"], "BETA_READY")
        self.assertEqual(data["offline_cases"], 21)
        self.assertEqual(data["release_tracks"], 33)
        self.assertEqual(data["release_gates"], 9)

    def test_scorecard_round_trip_validation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "scorecard.json"
            self.run_cli("assess", "--scope", "offline", "--output", str(path))
            self.run_cli("validate-scorecard", str(path))

    def test_invalid_scorecard_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.json"
            path.write_text('{"schema_version":"wrong"}\n')
            proc = self.run_cli("validate-scorecard", str(path), check=False)
            self.assertNotEqual(proc.returncode, 0)

    def test_beta_limits_are_explicit(self):
        text = (ROOT / "BETA1_LIMITATIONS.md").read_text()
        self.assertIn("offline-certified", text)
        self.assertIn("live Codex", text)

    def test_external_services_are_not_beta_requirements(self):
        gates = json.loads((ROOT / "release" / "GATES.json").read_text())["gates"]
        evidence = " ".join(" ".join(x.get("evidence", [])) for x in gates).lower()
        for service in ["chroma", "langfuse", "postgres", "langgraph"]:
            self.assertNotIn(service, evidence)

    def test_release_validator_passes(self):
        proc = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_release.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
