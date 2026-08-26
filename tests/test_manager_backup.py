from __future__ import annotations

import json
import os
import shutil
import stat
import tempfile
import unittest
import uuid
from pathlib import Path

from manager.product_os_manager.adapters.deterministic import DeterministicSelectorAdapter
from manager.product_os_manager.adapters.repository import DirectoryTargetProvider
from manager.product_os_manager.backup import (
    create_backup,
    resource_paths,
    restore_backup,
    snapshot_resources,
    verify_backup,
)
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.state import canonical_text_file_sha256


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class ManagerBackupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-backup-"))
        self.home = self.tmp / "home"
        self.project = self.tmp / "project"
        self.codex_home = self.tmp / "codex-home"
        self.product_os_home = self.tmp / "product-os-home"
        self.home.mkdir()
        self.project.mkdir()
        self.context = InstallationContext.from_environment(
            self.project,
            {
                "HOME": str(self.home),
                "USERPROFILE": str(self.home),
                "CODEX_HOME": str(self.codex_home),
                "PRODUCT_OS_HOME": str(self.product_os_home),
            },
        )
        self.installation_id = str(uuid.uuid4())
        self.transaction_id = f"TX-{uuid.uuid4()}"
        self.receipt = {
            "managed_files": {
                "AGENTS.md": {"sha256": "0" * 64},
                ".cpt/bin/custom.py": {"sha256": "0" * 64},
            },
            "rules": {"profile": "none", "status": "not_installed"},
        }
        write_json(self.project / ".cpt" / "install.json", {"before": True})
        (self.project / "AGENTS.md").write_text("before agents\n", encoding="utf-8")
        custom = self.project / ".cpt" / "bin" / "custom.py"
        custom.parent.mkdir(parents=True, exist_ok=True)
        custom.write_text("before custom\n", encoding="utf-8")
        write_json(self.context.registry_path, {
            "schema": "product-os-installation-registry-v1",
            "updated_at": "2026-01-01T00:00:00Z",
            "installations": {},
        })
        write_json(self.context.marketplace_registry, {"name": "user", "plugins": []})
        write_json(
            self.project / ".agents" / "plugins" / "marketplace.json",
            {"name": "repo", "plugins": []},
        )
        self.selector = DeterministicSelectorAdapter(
            self.tmp / "selectors.json",
            [
                {
                    "name": "cpt-core",
                    "selector": "cpt-core@legacy",
                    "marketplace_identity": "legacy",
                    "enabled": True,
                    "source_revision": None,
                }
            ],
        )

    def tearDown(self) -> None:
        def remove_readonly(function, path, _error):
            os.chmod(path, stat.S_IWRITE)
            function(path)

        shutil.rmtree(self.tmp, onerror=remove_readonly)

    def _backup(self):
        files, directories = resource_paths(self.context, self.receipt)
        before = snapshot_resources(self.context, files, directories)
        selector = self.selector.inspect()
        manifest = create_backup(
            self.context,
            transaction_id=self.transaction_id,
            plan_hash="a" * 64,
            installation_id=self.installation_id,
            files=files,
            directories=directories,
            selector_snapshot=selector,
        )
        return files, directories, before, selector, manifest

    def test_verified_backup_restores_exact_resources(self) -> None:
        files, directories, before, selector, manifest = self._backup()
        for path, _scope in files.values():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("after\n", encoding="utf-8")
        for path in directories.values():
            path.mkdir(parents=True, exist_ok=True)
        after = snapshot_resources(self.context, files, directories)
        restore_backup(
            self.context,
            manifest,
            files=files,
            directories=directories,
            expected_current=after,
        )
        self.assertEqual(snapshot_resources(self.context, files, directories), before)
        verified = verify_backup(
            self.context,
            Path(manifest["backup_root"]) / "backup-manifest.json",
            transaction_id=self.transaction_id,
            plan_hash="a" * 64,
            installation_id=self.installation_id,
            files=files,
            directories=directories,
            expected_selector_adapter=selector.adapter_id,
            expected_selector_state_token=selector.state_token,
        )
        self.assertEqual(verified["manifest_hash"], manifest["manifest_hash"])

    def test_concurrent_drift_refuses_before_any_restore(self) -> None:
        files, directories, _before, _selector, manifest = self._backup()
        for path, _scope in files.values():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("transaction-owned\n", encoding="utf-8")
        expected = snapshot_resources(self.context, files, directories)
        drift_key = sorted(files)[-1]
        files[drift_key][0].write_text("concurrent\n", encoding="utf-8")
        immediately_before = snapshot_resources(self.context, files, directories)
        with self.assertRaisesRegex(RuntimeError, "changed concurrently"):
            restore_backup(
                self.context,
                manifest,
                files=files,
                directories=directories,
                expected_current=expected,
            )
        self.assertEqual(
            snapshot_resources(self.context, files, directories),
            immediately_before,
        )

    def test_resource_aliases_are_deduplicated(self) -> None:
        files, _directories = resource_paths(self.context, self.receipt)
        agents = [key for key, (path, _scope) in files.items() if path == self.project / "AGENTS.md"]
        self.assertEqual(len(agents), 1)

    def test_selector_operations_are_idempotent_and_partial_fault_is_real(self) -> None:
        transaction = f"TX-{uuid.uuid4()}"
        targets = [
            {
                "name": "cpt-core",
                "selector": "cpt-core@target",
                "marketplace_identity": "target",
                "source_revision": "a" * 40,
            },
            {
                "name": "product-os-manager",
                "selector": "product-os-manager@target",
                "marketplace_identity": "target",
                "source_revision": "a" * 40,
            },
        ]
        original = self.selector.inspect()
        prepared = self.selector.prepare(
            targets,
            transaction_id=transaction,
            operation_id="prepare-selectors",
            expected_state_token=original.state_token,
        )
        replayed = self.selector.prepare(
            targets,
            transaction_id=transaction,
            operation_id="prepare-selectors",
            expected_state_token=original.state_token,
        )
        self.assertEqual(replayed.state_token, prepared.state_token)
        self.selector.faults.add("activate_after_first")
        with self.assertRaisesRegex(RuntimeError, "activate_after_first"):
            self.selector.activate(
                targets,
                transaction_id=transaction,
                operation_id="activate-selectors",
                expected_state_token=prepared.state_token,
            )
        partial = self.selector.inspect()
        enabled = {(item["name"], item["selector"]) for item in partial.selectors if item["enabled"]}
        self.assertIn(("cpt-core", "cpt-core@target"), enabled)
        self.assertNotIn(("product-os-manager", "product-os-manager@target"), enabled)
        self.selector.restore(
            original.selectors,
            transaction_id=transaction,
            operation_id="restore-selectors",
            expected_state_token=partial.state_token,
        )
        self.assertEqual(self.selector.inspect().copy_selectors(), original.copy_selectors())

    def test_directory_provider_materializes_only_verified_manifest_files(self) -> None:
        source = self.tmp / "source"
        marketplace = {
            "name": "product-os-git",
            "plugins": [
                {
                    "name": "cpt-core",
                    "source": {"source": "local", "path": ".hidden/cpt-core"},
                }
            ],
        }
        plugin = {"name": "cpt-core", "version": "4.1.0"}
        marketplace_path = source / ".agents" / "plugins" / "marketplace.json"
        plugin_path = source / ".hidden" / "cpt-core" / ".codex-plugin" / "plugin.json"
        write_json(marketplace_path, marketplace)
        write_json(plugin_path, plugin)
        files = [
            {"path": ".agents/plugins/marketplace.json", "sha256": canonical_text_file_sha256(marketplace_path)},
            {"path": ".hidden/cpt-core/.codex-plugin/plugin.json", "sha256": canonical_text_file_sha256(plugin_path)},
        ]
        write_json(source / "MANIFEST.json", {
            "schema": "cpt-package-manifest-v10",
            "name": "codex-product-os",
            "version": "4.1.0",
            "file_count": len(files),
            "files": files,
        })
        provider = DirectoryTargetProvider(
            source,
            self.context,
            resolved_commit="b" * 40,
        )
        request = {
            "repository": provider.repository,
            "requested_ref": provider.requested_ref,
            "marketplace_identity": "product-os-git",
            "plugins": ["cpt-core"],
        }
        evidence = provider.resolve(request)
        self.assertEqual(evidence.copy_descriptor()["plugins"][0]["relative_path"], ".hidden/cpt-core")
        destination = Path(evidence.copy_descriptor()["materialized_root"])
        provider.materialize(
            evidence,
            destination,
            transaction_id=self.transaction_id,
            operation_id="materialize-target",
        )
        self.assertTrue((destination / ".product-os-source.json").is_file())
        self.assertFalse((destination / ".git").exists())
        (destination / "extra.txt").write_text("tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "inventory is not closed"):
            provider.materialize(
                evidence,
                destination,
                transaction_id=self.transaction_id,
                operation_id="materialize-target",
            )


if __name__ == "__main__":
    unittest.main()
