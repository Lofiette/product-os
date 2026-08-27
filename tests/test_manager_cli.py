from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from tools import cpt_dist
from tools import product_os_manager as cli

from manager.product_os_manager.transaction import load_transaction
from tests.test_manager_codex_adapter import FakeCodexPluginClient
from tests import test_manager_lifecycle as lifecycle_tests
from tests import test_manager_transaction as transaction_tests


class ManagerCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = transaction_tests.ManagerTransactionTests(methodName="runTest")
        self.fixture.setUp()
        self.source = self.fixture.source
        subprocess.run(["git", "init", "-q", str(self.source)], check=True)
        subprocess.run(
            ["git", "-C", str(self.source), "symbolic-ref", "HEAD", "refs/heads/release/4.1.0"],
            check=True,
        )
        subprocess.run(["git", "-C", str(self.source), "add", "--all"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(self.source),
                "-c",
                "user.name=Product OS CLI Test",
                "-c",
                "user.email=product-os-cli-test.invalid",
                "commit",
                "-q",
                "-m",
                "isolated CLI target",
            ],
            check=True,
        )
        self.commit = subprocess.run(
            ["git", "-C", str(self.source), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        target_root = (
            self.fixture.product_os_home
            / "sources"
            / "product-os-git"
            / self.commit
        )
        self.fake = FakeCodexPluginClient(target_root)
        self.plan_path = self.fixture.tmp / "approved-plan.json"

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def _args(self, **extra) -> argparse.Namespace:
        values = {
            "project": str(self.fixture.project),
            "user_home": str(self.fixture.home),
            "codex_home": str(self.fixture.codex_home),
            "product_os_home": str(self.fixture.product_os_home),
            "marketplace_registry": str(self.fixture.context.marketplace_registry),
            "confirmed_active_codex_home": None,
            "repository_root": str(self.source),
            "git_executable": "git",
            "codex_executable": "codex-test-double",
        }
        values.update(extra)
        return argparse.Namespace(**values)

    @staticmethod
    def _invoke(function, args) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = function(args)
        return code, json.loads(output.getvalue())

    def test_trusted_cli_runs_two_phase_local_git_flow_without_real_codex(self) -> None:
        with mock.patch.object(
            cli,
            "SubprocessCodexPluginClient",
            return_value=self.fake,
        ):
            plan_code, plan = self._invoke(
                cli.command_plan_local_git,
                self._args(
                    requested_ref="release/4.1.0",
                    marketplace_identity="product-os-git",
                    plugin=["cpt-core", "cpt-design-ui"],
                    output=str(self.plan_path),
                ),
            )
            self.assertEqual(plan_code, 0)
            self.assertEqual(plan["status"], "ready")
            self.assertEqual(plan["target"]["evidence_adapter"], "local-git")
            self.assertEqual(
                plan["selector_adapter_binding"]["adapter_id"],
                "codex-cli-selector",
            )
            self.assertTrue(self.plan_path.is_file())

            prepare_code, prepared = self._invoke(
                cli.command_prepare,
                self._args(
                    plan=str(self.plan_path),
                    confirmed_plan_hash=plan["plan_hash"],
                ),
            )
            self.assertEqual(prepare_code, 0)
            self.assertEqual(prepared["status"], "prepared")
            transactions_code, transactions = self._invoke(
                cli.command_transactions,
                self._args(),
            )
            self.assertEqual(transactions_code, 0)
            self.assertEqual(transactions["unresolved_count"], 1)
            self.assertEqual(
                transactions["transactions"][0]["transaction_id"],
                prepared["transaction_id"],
            )
            enabled_after_prepare = set(self.fake.installed)
            self.assertIn("cpt-core@cpt-personal", enabled_after_prepare)
            self.assertIn("cpt-design-ui@cpt-personal", enabled_after_prepare)

            switch_code, committed = self._invoke(
                cli.command_switch,
                self._args(
                    transaction_id=prepared["transaction_id"],
                    confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                ),
            )
            self.assertEqual(switch_code, 0)
            self.assertEqual(committed["status"], "committed")
            self.assertEqual(
                {
                    selector
                    for selector in self.fake.installed
                    if selector.startswith(("cpt-core@", "cpt-design-ui@"))
                },
                {
                    "cpt-core@product-os-git",
                    "cpt-design-ui@product-os-git",
                },
            )
            receipt = cpt_dist.load_receipt(self.fixture.project)
            self.assertEqual(receipt["source_lineage"]["commit_sha"], self.commit)

            doctor_code, doctor = self._invoke(
                cli.command_doctor,
                self._args(
                    transaction_id=prepared["transaction_id"],
                    require_codex_lifecycle=False,
                ),
            )
            self.assertEqual(doctor_code, 0)
            self.assertEqual(doctor["status"], "PASS")
            self.assertEqual(doctor["lifecycle"]["status"], "unsupported")

            with mock.patch.dict(
                os.environ,
                {"PRODUCT_OS_HOME": str(self.fixture.product_os_home)},
                clear=False,
            ):
                lifecycle_code, lifecycle_doctor = self._invoke(
                    cli.command_doctor,
                    self._args(
                        transaction_id=prepared["transaction_id"],
                        require_codex_lifecycle=True,
                    ),
                )
            self.assertEqual(lifecycle_code, 1)
            self.assertEqual(lifecycle_doctor["status"], "PASS")
            self.assertEqual(lifecycle_doctor["lifecycle"]["status"], "pending")

            lifecycle_hook = lifecycle_tests.load_hook_helper()
            core_payload = next(
                item for item in receipt["installed_plugins"] if item["name"] == "cpt-core"
            )
            self.assertTrue(
                lifecycle_hook.record_lifecycle_event(
                    self.fixture.project,
                    Path(core_payload["payload_path"]),
                    {
                        "hook_event_name": "SessionStart",
                        "session_id": "isolated-cli-session",
                        "source": "startup",
                    },
                    env=self.fixture.env,
                    observed_at="2026-08-26T12:00:00Z",
                )
            )
            with mock.patch.dict(
                os.environ,
                {"PRODUCT_OS_HOME": str(self.fixture.product_os_home)},
                clear=False,
            ):
                lifecycle_code, lifecycle_doctor = self._invoke(
                    cli.command_doctor,
                    self._args(
                        transaction_id=prepared["transaction_id"],
                        require_codex_lifecycle=True,
                    ),
                )
            self.assertEqual(lifecycle_code, 0)
            self.assertEqual(lifecycle_doctor["lifecycle"]["status"], "PASS")

            rollback_code, rolled_back = self._invoke(
                cli.command_rollback,
                self._args(
                    transaction_id=prepared["transaction_id"],
                    force=False,
                    confirmed_current_state_hash=None,
                ),
            )
            self.assertEqual(rollback_code, 0)
            self.assertEqual(rolled_back["status"], "rolled_back")
            self.assertEqual(
                {
                    selector
                    for selector in self.fake.installed
                    if selector.startswith(("cpt-core@", "cpt-design-ui@"))
                },
                {
                    "cpt-core@cpt-personal",
                    "cpt-design-ui@cpt-personal",
                },
            )
            self.assertNotIn("product-os-git", self.fake.marketplaces)
            journal = load_transaction(
                self.fixture.context,
                prepared["transaction_id"],
            )
            self.assertEqual(journal["state"], "rolled_back")

    def test_explicit_context_refuses_ambient_codex_home_without_exact_confirmation(self) -> None:
        sentinel = self.fixture.codex_home / "active-sentinel.txt"
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("unchanged\n", encoding="utf-8")
        args = self._args()
        with mock.patch.dict(
            os.environ,
            {
                "HOME": str(self.fixture.home),
                "USERPROFILE": str(self.fixture.home),
                "CODEX_HOME": str(self.fixture.codex_home),
            },
            clear=False,
        ):
            with self.assertRaisesRegex(RuntimeError, "process-active CODEX_HOME"):
                cli._explicit_context(args)
            args.confirmed_active_codex_home = str(self.fixture.codex_home)
            context = cli._explicit_context(args)
        self.assertEqual(context.codex_home, self.fixture.codex_home.resolve())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged\n")

    def test_trusted_context_requires_all_explicit_roots(self) -> None:
        args = self._args(product_os_home=None)
        with self.assertRaisesRegex(RuntimeError, "explicit roots"):
            cli._explicit_context(args)
        parsed = cli.parser().parse_args(
            [
                "doctor",
                "--project", str(self.fixture.project),
                "--user-home", str(self.fixture.home),
                "--codex-home", str(self.fixture.codex_home),
                "--product-os-home", str(self.fixture.product_os_home),
                "--transaction-id", "TX-00000000-0000-4000-8000-000000000001",
            ]
        )
        self.assertFalse(hasattr(parsed, "repository_root"))
        self.assertEqual(parsed.handler, cli.command_doctor)
        with mock.patch.object(
            sys,
            "argv",
            [
                "product_os_manager.py",
                "transactions",
                "--project", str(self.fixture.project),
                "--user-home", str(self.fixture.home),
                "--codex-home", str(self.fixture.codex_home),
                "--product-os-home", str(self.fixture.product_os_home),
            ],
        ), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(), 0)
        self.assertEqual(json.loads(output.getvalue())["transactions"], [])
        with mock.patch.object(
            sys,
            "argv",
            [
                "product_os_manager.py",
                "transactions",
                "--project", str(self.fixture.project),
                "--user-home", str(self.fixture.home),
                "--codex-home", str(self.fixture.codex_home),
                "--product-os-home", str(self.fixture.tmp / "missing"),
            ],
        ), contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(cli.main(), 2)
        self.assertEqual(json.loads(error.getvalue())["status"], "error")


if __name__ == "__main__":
    unittest.main()
