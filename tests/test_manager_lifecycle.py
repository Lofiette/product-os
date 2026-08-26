from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from manager.product_os_manager.adapters.base import AdapterRegistry
from manager.product_os_manager.adapters.codex_lifecycle import (
    CodexSessionLifecycleAdapter,
    project_bucket,
)
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.state import (
    canonical_json_hash,
    canonical_text_file_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
HOOK_HELPER = (
    ROOT
    / "payload"
    / "marketplace-root"
    / "plugins"
    / "cpt-core"
    / "hooks"
    / "product_os_lifecycle.py"
)
PLUGIN_ROOT = HOOK_HELPER.parents[1]
TRANSACTION_ID = "TX-00000000-0000-4000-8000-000000000001"
INSTALLATION_ID = "00000000-0000-4000-8000-000000000001"
OBSERVED_AT = "2026-08-26T12:00:00Z"


def load_hook_helper():
    spec = importlib.util.spec_from_file_location("product_os_lifecycle_test", HOOK_HELPER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodexLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-lifecycle-"))
        self.home = self.tmp / "home"
        self.project = self.tmp / "project"
        self.codex_home = self.tmp / "codex-home"
        self.product_os_home = self.tmp / "product-os-home"
        for path in (self.home, self.project, self.codex_home, self.product_os_home):
            path.mkdir(parents=True)
        self.context = InstallationContext(
            project=self.project.resolve(),
            user_home=self.home.resolve(),
            codex_home=self.codex_home.resolve(),
            product_os_home=self.product_os_home.resolve(),
            marketplace_registry=(self.home / ".agents" / "plugins" / "marketplace.json").resolve(),
        )
        target_plugin = (
            self.product_os_home
            / "sources"
            / "product-os-git"
            / ("c" * 40)
            / "payload"
            / "marketplace-root"
            / "plugins"
            / "cpt-core"
        )
        target_plugin.parent.mkdir(parents=True)
        shutil.copytree(PLUGIN_ROOT, target_plugin)
        plugin_hash = canonical_text_file_sha256(
            target_plugin / ".codex-plugin" / "plugin.json"
        )
        receipt = {
            "schema": "cpt-install-receipt-v2",
            "installation_id": INSTALLATION_ID,
            "manager": {
                "last_transaction_id": TRANSACTION_ID,
                "last_backup_path": str(self.product_os_home / "backups" / TRANSACTION_ID),
            },
            "source_lineage": {
                "delivery_type": "git_marketplace",
                "observed_from": "product-os-manager",
            },
            "installed_plugins": [
                {
                    "name": "cpt-core",
                    "payload_path": str(target_plugin),
                    "manifest_sha256": plugin_hash,
                }
            ],
        }
        receipt_path = self.project / ".cpt" / "install.json"
        receipt_path.parent.mkdir(parents=True)
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        self.receipt = receipt
        self.journal = {
            "schema": "product-os-adoption-transaction-v1",
            "transaction_id": TRANSACTION_ID,
            "state": "committed",
            "installation_id": INSTALLATION_ID,
            "project": str(self.context.project),
            "context": self.context.as_dict(),
            "revision": 1,
        }
        self.journal["journal_hash"] = canonical_json_hash(self.journal)
        journal_path = (
            self.product_os_home
            / "transactions"
            / project_bucket(self.project)
            / TRANSACTION_ID
            / "journal.json"
        )
        journal_path.parent.mkdir(parents=True)
        journal_path.write_text(json.dumps(self.journal, indent=2) + "\n", encoding="utf-8")
        self.env = {
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "CODEX_HOME": str(self.codex_home),
            "PRODUCT_OS_HOME": str(self.product_os_home),
        }
        self.hook = load_hook_helper()
        self.adapter = CodexSessionLifecycleAdapter(self.context)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def _record(self, event: str, *, session: str, source: str | None = None) -> bool:
        payload = {
            "hook_event_name": event,
            "session_id": session,
            "cwd": str(self.project),
            "transcript_path": str(self.tmp / "private-transcript.jsonl"),
            "model": "private-model-name",
        }
        if source is not None:
            payload["source"] = source
        return self.hook.record_lifecycle_event(
            self.project,
            PLUGIN_ROOT,
            payload,
            env=self.env,
            observed_at=OBSERVED_AT,
        )

    def _event_files(self) -> list[Path]:
        root = self.product_os_home / "lifecycle"
        return sorted(root.rglob("*.json")) if root.exists() else []

    def test_resume_and_compact_do_not_satisfy_new_session_gate(self) -> None:
        self.assertTrue(self._record("SessionStart", session="secret-session", source="resume"))
        self.assertEqual(self.adapter.inspect(self.journal).status, "pending")
        self.assertTrue(self._record("SessionStart", session="secret-session", source="compact"))
        self.assertEqual(self.adapter.inspect(self.journal).status, "pending")

    def test_matching_startup_passes_without_persisting_private_fields(self) -> None:
        session = "raw-secret-session-id"
        self.assertTrue(self._record("SessionStart", session=session, source="startup"))
        evidence = self.adapter.inspect(self.journal)
        self.assertEqual(evidence.status, "PASS")
        self.assertEqual(evidence.evidence["startup_observed_at"], OBSERVED_AT)
        raw = b"\n".join(path.read_bytes() for path in self._event_files())
        for forbidden in (
            session.encode(),
            str(self.project).encode(),
            b"private-transcript",
            b"private-model-name",
        ):
            self.assertNotIn(forbidden, raw)
        for index in range(self.hook.MAX_EVENT_FILES + 6):
            self.assertTrue(
                self._record(
                    "SessionStart",
                    session=f"bounded-session-{index}",
                    source="startup",
                )
            )
        self.assertLessEqual(len(self._event_files()), self.hook.MAX_EVENT_FILES)
        self.assertEqual(self.adapter.inspect(self.journal).status, "PASS")
        lock_files = list((self.product_os_home / "lifecycle").rglob("*.lock"))
        self.assertEqual(len(lock_files), 1)
        for index in range(self.hook.MAX_EVENT_FILES + 6):
            self.assertTrue(self._record("SessionEnd", session=f"end-only-{index}"))
        self.assertLessEqual(len(self._event_files()), self.hook.MAX_EVENT_FILES)
        self.assertEqual(self.adapter.inspect(self.journal).status, "PASS")

    def test_session_end_only_remains_pending(self) -> None:
        self.assertTrue(self._record("SessionEnd", session="end-only"))
        self.assertEqual(self.adapter.inspect(self.journal).status, "pending")

    def test_non_manager_lineage_and_wrong_plugin_root_make_zero_writes(self) -> None:
        receipt_path = self.project / ".cpt" / "install.json"
        local = dict(self.receipt)
        local["source_lineage"] = {
            "delivery_type": "local_distribution",
            "observed_from": "installer",
        }
        receipt_path.write_text(json.dumps(local) + "\n", encoding="utf-8")
        self.assertFalse(self._record("SessionStart", session="local", source="startup"))
        self.assertEqual(self._event_files(), [])

        receipt_path.write_text(json.dumps(self.receipt, indent=2) + "\n", encoding="utf-8")
        wrong_root = self.tmp / "wrong-plugin"
        (wrong_root / ".codex-plugin").mkdir(parents=True)
        (wrong_root / ".codex-plugin" / "plugin.json").write_text("{}\n", encoding="utf-8")
        payload = {
            "hook_event_name": "SessionStart",
            "session_id": "wrong-root",
            "source": "startup",
        }
        self.assertFalse(
            self.hook.record_lifecycle_event(
                self.project,
                wrong_root,
                payload,
                env=self.env,
                observed_at=OBSERVED_AT,
            )
        )
        self.assertEqual(self._event_files(), [])

    def test_tampered_evidence_fails_closed(self) -> None:
        self.assertTrue(self._record("SessionStart", session="tamper", source="startup"))
        event_path = self._event_files()[0]
        event = json.loads(event_path.read_text(encoding="utf-8"))
        event["last_event"] = "SessionEnd"
        event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
        self.assertEqual(self.adapter.inspect(self.journal).status, "FAIL")

    def test_registry_accepts_optional_lifecycle_adapter_and_rejects_duplicate(self) -> None:
        registry = AdapterRegistry(lifecycle_adapters=[self.adapter])
        self.assertIs(registry.lifecycle(self.adapter.adapter_id), self.adapter)
        with self.assertRaisesRegex(RuntimeError, "already registered"):
            registry.register_lifecycle(CodexSessionLifecycleAdapter(self.context))


if __name__ == "__main__":
    unittest.main()
