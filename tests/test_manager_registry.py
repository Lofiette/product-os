from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.registry import (
    ConcurrentRegistryChange,
    RegistryStore,
    empty_registry,
)
from manager.product_os_manager.state import exclusive_lock, file_sha256


def receipt(project: Path, *, selector: str | None = None) -> dict:
    return {
        "schema": "cpt-install-receipt-v2",
        "installation_id": str(uuid.uuid4()),
        "version": "4.1.0",
        "product": {
            "id": "product-os",
            "version": "4.1.0",
            "runtime_schema": "4.0-alpha8",
        },
        "source_lineage": {
            "delivery_type": "local_distribution",
            "repository": None,
            "marketplace_identity": None,
            "release": "4.1.0",
            "ref": None,
            "commit_sha": None,
            "manifest_sha256": "a" * 64,
            "observed_from": "test",
        },
        "installed_plugins": [
            {
                "name": "cpt-core",
                "selector": selector,
                "marketplace_identity": "fixture",
                "version": "4.1.0",
                "payload_path": str(project / "plugins" / "cpt-core"),
                "manifest_sha256": "b" * 64,
                "status": "healthy",
            }
        ],
    }


class ManagerRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-reg-"))
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.home = self.tmp / "home"
        self.codex_home = self.tmp / "codex"
        self.manager_home = self.tmp / "manager"
        self.env = os.environ.copy()
        self.env.update({
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "CODEX_HOME": str(self.codex_home),
            "PRODUCT_OS_HOME": str(self.manager_home),
        })
        self.context = InstallationContext.from_environment(self.project, self.env)
        self.store = RegistryStore(self.context)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_context_keeps_home_codex_and_manager_roots_distinct(self) -> None:
        self.assertEqual(self.context.user_home, self.home.resolve())
        self.assertEqual(self.context.codex_home, self.codex_home.resolve())
        self.assertEqual(self.context.product_os_home, self.manager_home.resolve())
        self.assertEqual(
            self.context.registry_path,
            (self.manager_home / "registry.json").resolve(),
        )

    def test_upsert_preserves_unrelated_installations_and_selector_references(self) -> None:
        first = receipt(self.project, selector="cpt-core@legacy")
        self.store.upsert(self.project, first)
        other_project = self.tmp / "other"
        other_project.mkdir()
        second = receipt(other_project, selector="cpt-core@git")
        self.store.upsert(other_project, second)
        data, _ = self.store.snapshot()
        self.assertEqual(
            set(data["installations"]),
            {first["installation_id"], second["installation_id"]},
        )
        self.assertEqual(
            self.store.selector_references("cpt-core@legacy"),
            [first["installation_id"]],
        )

    def test_compare_and_swap_rejects_concurrent_registry_change(self) -> None:
        data, digest = self.store.snapshot()
        self.store.upsert(self.project, receipt(self.project))
        with self.assertRaises(ConcurrentRegistryChange):
            self.store.save(data, expected_digest=digest)

    def test_stale_lock_file_does_not_block_writer(self) -> None:
        self.manager_home.mkdir(parents=True)
        self.store.lock_path.write_text("stale-owner\n", encoding="utf-8")
        digest = self.store.save(empty_registry(), expected_digest=None)
        self.assertEqual(digest, file_sha256(self.store.path))

    def test_live_lock_fails_closed_without_overwrite(self) -> None:
        with exclusive_lock(self.store.lock_path):
            with self.assertRaisesRegex(RuntimeError, "lock is already held"):
                self.store.save(empty_registry(), expected_digest=None)
        self.assertFalse(self.store.path.exists())

    def test_os_releases_lock_after_hard_process_exit(self) -> None:
        script = """
import os
import sys
from pathlib import Path
from manager.product_os_manager.state import exclusive_lock
with exclusive_lock(Path(sys.argv[1])):
    os._exit(0)
"""
        result = subprocess.run(
            [sys.executable, "-c", script, str(self.store.lock_path)],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(self.store.lock_path.exists())
        with exclusive_lock(self.store.lock_path):
            self.assertTrue(self.store.lock_path.exists())

    def test_rebuild_uses_only_explicit_v2_receipts(self) -> None:
        valid = receipt(self.project, selector="cpt-core@git")
        legacy = {"schema": "cpt-install-receipt-v1", "version": "4.0.0"}
        data, warnings = self.store.rebuild([
            (self.project, valid),
            (self.tmp / "legacy", legacy),
        ])
        self.assertEqual(list(data["installations"]), [valid["installation_id"]])
        self.assertEqual(len(warnings), 1)
        on_disk = json.loads(self.store.path.read_text(encoding="utf-8"))
        self.assertEqual(on_disk, data)
