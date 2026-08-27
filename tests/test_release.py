from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import cpt_release

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "cpt_release.py"


class ReleasePlaneTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run([sys.executable, str(CLI), *args], cwd=ROOT, text=True, capture_output=True)
        if check and proc.returncode:
            self.fail(proc.stdout + proc.stderr)
        return proc

    def test_gate_registry_has_eleven_unique_gates(self):
        data = json.loads((ROOT / "release" / "GATES.json").read_text())
        ids = [x["id"] for x in data["gates"]]
        self.assertEqual(len(ids), 11)
        self.assertEqual(len(set(ids)), 11)
        self.assertIn("manager_adoption", ids)
        self.assertIn("isolated_codex_adoption", ids)

    def test_trial_registry_has_thirty_five_unique_tracks(self):
        data = json.loads((ROOT / "release" / "TRIALS.json").read_text())
        ids = [x["id"] for x in data["tracks"]]
        self.assertEqual(len(ids), 35)
        self.assertEqual(len(set(ids)), 35)

    def test_offline_assessment_is_beta_ready(self):
        data = json.loads(self.run_cli("assess", "--scope", "offline").stdout)
        self.assertEqual(data["status"], "BETA_READY")
        self.assertEqual(data["summary"]["blocked"], 0)

    def test_rc_assessment_is_blocked_without_live_evidence(self):
        with mock.patch.object(
            cpt_release,
            "reviewed_release_evidence",
            return_value=({}, []),
        ):
            data = cpt_release.assess("rc")
            with mock.patch.object(
                sys,
                "argv",
                [str(CLI), "assess", "--scope", "rc"],
            ), mock.patch("builtins.print"):
                cli_result = cpt_release.main()
        self.assertEqual(data["status"], "BLOCKED")
        self.assertGreaterEqual(data["summary"]["pending"], 3)
        self.assertEqual(cli_result, 1)

    def test_reviewed_isolated_codex_acceptance_is_ingested(self):
        data = json.loads(self.run_cli("assess", "--scope", "offline").stdout)
        gates = {item["id"]: item for item in data["gates"]}
        self.assertEqual(gates["isolated_codex_adoption"]["status"], "PASS")
        self.assertIn("TX-679ec9c6-317e-486f-9142-43209a40ceb2", " ".join(gates["isolated_codex_adoption"]["evidence"]))
        self.assertEqual(gates["platform_matrix"]["status"], "PASS")
        self.assertIn("WSL", " ".join(gates["platform_matrix"]["evidence"]))
        self.assertEqual(gates["live_model_trials"]["status"], "PASS")
        self.assertEqual(gates["rc_mega_audit"]["status"], "PASS")

    def test_invalid_reviewed_evidence_fails_package_integrity_closed(self):
        with mock.patch.object(
            cpt_release,
            "reviewed_release_evidence",
            return_value=({}, ["fixture evidence error"]),
        ):
            evidence = cpt_release.offline_evidence()
        self.assertFalse(evidence["package_integrity"][0])

    def test_reviewed_evidence_is_bound_to_exact_candidate(self):
        document = json.loads((ROOT / "release" / "EVIDENCE.json").read_text())
        self.assertEqual(
            document["candidate_manifest_digest"],
            cpt_release.candidate_manifest_digest(),
        )
        with mock.patch.object(
            cpt_release,
            "candidate_manifest_digest",
            return_value="0" * 64,
        ):
            reviewed, errors = cpt_release.reviewed_release_evidence()
        self.assertEqual(reviewed, {})
        self.assertTrue(any("candidate digest mismatch" in item for item in errors))

    def test_offline_readiness_counts_release_assets(self):
        data = json.loads(self.run_cli("readiness", "--scope", "offline").stdout)
        self.assertEqual(data["status"], "BETA_READY")
        self.assertEqual(data["offline_cases"], 21)
        self.assertEqual(data["release_tracks"], 35)
        self.assertEqual(data["release_gates"], 11)
        facts = cpt_release.package_facts()
        facts["behavior"] = dict(facts["behavior"])
        facts["behavior"]["total"] -= 1
        with mock.patch.object(cpt_release, "package_facts", return_value=facts):
            self.assertFalse(cpt_release.offline_evidence()["offline_regression"][0])

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
        text = (ROOT / "KNOWN_LIMITATIONS.md").read_text()
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
