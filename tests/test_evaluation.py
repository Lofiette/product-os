from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import cpt_eval, build_manifest


ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation" / "executable"


class EvaluationPlaneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha8-eval-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_01_assets_validate_and_case_inventory(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_evaluation.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=120,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        cases = cpt_eval.all_cases()
        self.assertEqual(len(cases), 21)
        self.assertEqual(
            set(json.loads((EVAL / "SUITES.json").read_text())["suites"]),
            {"offline-core", "live-smoke", "live-readonly", "live-full"},
        )

    def test_02_reference_micro_case_passes(self) -> None:
        report = cpt_eval.run_reference_case(cpt_eval.load_case("micro_copy_change"), self.tmp)
        self.assertEqual(report["status"], "PASS", report.get("critical_failures"))
        self.assertLessEqual(report["metrics"]["writes"], 2)

    def test_03_reference_design_system_case_passes(self) -> None:
        report = cpt_eval.run_reference_case(
            cpt_eval.load_case("design_system_ui_implementation"), self.tmp
        )
        self.assertEqual(report["status"], "PASS", report.get("critical_failures"))
        self.assertIn("src/features/editor/EmptyState.tsx", report["changed_paths"])
        source = 'import { Button } from "x";\nfunction X() { return <Button>{task_id}</Button>; }\n'
        rendered = cpt_eval.deep_format(source, {"task_id": "TKT-123"})
        self.assertIn("import { Button }", rendered)
        self.assertIn("function X() {", rendered)
        self.assertIn(">TKT-123<", rendered)

    def test_04_live_backend_skips_when_cli_is_absent(self) -> None:
        case = cpt_eval.load_case("local_ignored_runtime_git_cleanliness")
        with patch.object(cpt_eval, "prepare_workspace") as prepare, patch.object(
            cpt_eval.shutil, "which", return_value=None
        ):
            workspace = self.tmp / "workspace"
            workspace.mkdir()
            prepare.return_value = (workspace, {"HOME": str(self.tmp), "CODEX_HOME": str(self.tmp / ".codex")})
            status, output, actual_workspace, _, meta = cpt_eval.run_live_case(case, self.tmp)
        self.assertEqual(status, "SKIPPED")
        self.assertIsNone(output)
        self.assertEqual(actual_workspace, workspace)
        self.assertIn("Codex CLI", meta["reason"])

    def test_05_live_nonzero_exit_is_failure_not_skip(self) -> None:
        case = cpt_eval.load_case("local_ignored_runtime_git_cleanliness")
        workspace = self.tmp / "workspace"
        workspace.mkdir()
        fake = subprocess.CompletedProcess(args=["codex"], returncode=2, stdout="", stderr="boom")
        with patch.object(cpt_eval, "prepare_workspace", return_value=(workspace, {})), patch.object(
            cpt_eval.shutil, "which", return_value="/usr/bin/codex"
        ), patch.object(cpt_eval, "run_process", return_value=fake):
            status, output, _, _, meta = cpt_eval.run_live_case(case, self.tmp)
        self.assertEqual(status, "FAIL")
        self.assertIsNone(output)
        self.assertEqual(meta["exit_code"], 2)

    def test_06_codex_jsonl_normalization(self) -> None:
        recorder = cpt_eval.TraceRecorder()
        stream = "\n".join(
            [
                json.dumps({"type": "thread.started", "thread_id": "test-thread"}),
                json.dumps(
                    {
                        "type": "item.started",
                        "item": {"id": "cmd-1", "type": "command_execution", "command": "rg --files src"},
                    }
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {"id": "cmd-1", "type": "command_execution", "exit_code": 0},
                    }
                ),
                json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {
                            "input_tokens": 100,
                            "cached_input_tokens": 40,
                            "output_tokens": 25,
                            "reasoning_output_tokens": 5,
                        },
                    }
                ),
            ]
        )
        cpt_eval.normalize_codex_jsonl(stream, recorder)
        self.assertEqual(cpt_eval.collect_commands(recorder.events), ["rg --files src"])
        self.assertEqual(cpt_eval.usage_totals(recorder.events)["input_tokens"], 100)
        self.assertTrue(
            any(
                event.get("type") == "codex_event"
                and event.get("codex_event_type") == "thread.started"
                for event in recorder.events
            )
        )
        fake = subprocess.CompletedProcess(args=["codex"], returncode=0, stdout="✓", stderr="")
        with patch.object(cpt_eval.subprocess, "run", return_value=fake) as runner:
            completed = cpt_eval.run_process(["codex", "--version"], cwd=ROOT)
        self.assertEqual(completed.stdout, "✓")
        self.assertEqual(runner.call_args.kwargs["encoding"], "utf-8")
        self.assertEqual(runner.call_args.kwargs["errors"], "replace")

    def test_07_structured_output_activity_is_marked_reported(self) -> None:
        recorder = cpt_eval.TraceRecorder()
        cpt_eval.augment_trace_from_structured_output(
            {"files_read": ["src/a.ts"], "files_changed": ["src/b.ts"]}, recorder
        )
        self.assertEqual(cpt_eval.collect_paths_from_trace(recorder.events, "file_read"), ["src/a.ts"])
        self.assertEqual(cpt_eval.collect_paths_from_trace(recorder.events, "file_write"), ["src/b.ts"])
        self.assertTrue(all(event.get("evidence_level") == "reported" for event in recorder.events))

    def test_08_baseline_comparison_pass_and_regression(self) -> None:
        base = {
            "cases": [
                {
                    "id": "x",
                    "status": "PASS",
                    "score": 100,
                    "metrics": {"input_tokens": 100, "output_tokens": 50, "tool_events": 4, "commands": 2, "writes": 1},
                }
            ]
        }
        baseline = self.tmp / "baseline.json"
        current = self.tmp / "current.json"
        cpt_eval.write_json(baseline, base)
        cpt_eval.write_json(current, base)
        self.assertEqual(cpt_eval.compare_baseline(current, baseline)["status"], "PASS")
        regressed = json.loads(json.dumps(base))
        regressed["cases"][0]["status"] = "FAIL"
        regressed["cases"][0]["score"] = 20
        cpt_eval.write_json(current, regressed)
        report = cpt_eval.compare_baseline(current, baseline)
        self.assertEqual(report["status"], "FAIL")
        self.assertGreaterEqual(report["regression_count"], 1)

    def test_09_mutation_checks_detect_all_four(self) -> None:
        scorecard = self.tmp / "scorecard.json"
        output = self.tmp / "mutations.json"
        case = cpt_eval.load_case("accessibility_review")
        cpt_eval.write_json(
            scorecard,
            {
                "cases": [
                    {
                        "id": case["id"],
                        "metrics": {"tool_events": 4},
                        "changed_paths": [],
                        "output": case["reference_output"],
                    }
                ]
            },
        )
        report = cpt_eval.mutate_and_check(scorecard, output)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["detected"], 4)
        self.assertEqual(report["total"], 4)

    def test_10_external_fixture_uses_isolated_codex_home(self) -> None:
        case = cpt_eval.load_case("local_ignored_runtime_git_cleanliness")
        out = self.tmp / "external"
        metadata = cpt_eval.prepare_external(case, out)
        self.assertTrue((out / "prompt.md").exists())
        self.assertTrue((out / "output-schema.json").exists())
        self.assertTrue(Path(metadata["codex_home"]).is_relative_to(out))
        self.assertTrue(Path(metadata["workspace"]).is_relative_to(out))

    def test_11_fixture_projects_only_selected_plugins_and_workers(self) -> None:
        case = cpt_eval.load_case("required_worker_timeout_quorum")
        workspace, env = cpt_eval.prepare_workspace(case, self.tmp)
        plugin_root = Path(env["CODEX_HOME"]) / "plugins"
        self.assertTrue((plugin_root / "cpt-core").exists())
        self.assertTrue((plugin_root / "cpt-engineering").exists())
        self.assertFalse((plugin_root / "cpt-design-ui").exists())
        # The case asks for workers, so their personal receipt and agents must be projected.
        worker_receipt = Path(env["HOME"]) / ".cpt-os" / "worker-packs" / "cpt-workers.json"
        self.assertTrue(worker_receipt.exists())
        self.assertTrue((Path(env["CODEX_HOME"]) / "agents").exists())
        self.assertTrue((workspace / ".cpt" / "runtime.yaml").exists())

    def test_12_scorecard_supports_mixed_live_suite(self) -> None:
        scorecard = cpt_eval.suite_scorecard(
            "live-smoke",
            "live",
            [
                {"id": "a", "status": "PASS", "score": 100, "metrics": {}},
                {"id": "b", "status": "SKIPPED", "score": 0, "metrics": {}},
            ],
        )
        self.assertEqual(scorecard["status"], "MIXED")
        self.assertEqual(scorecard["passed"], 1)
        self.assertEqual(scorecard["skipped"], 1)

    def test_13_generated_reports_are_excluded_from_manifest(self) -> None:
        report = EVAL / "reports" / "unit-test-runtime-report.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text("{}\n", encoding="utf-8")
        try:
            included = {
                path.relative_to(ROOT).as_posix()
                for path in build_manifest.included_files()
            }
            self.assertNotIn(
                "evaluation/executable/reports/unit-test-runtime-report.json",
                included,
            )
        finally:
            report.unlink(missing_ok=True)



if __name__ == "__main__":
    unittest.main()
