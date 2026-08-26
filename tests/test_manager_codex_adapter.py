from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Mapping
from unittest import mock

from manager.product_os_manager.adapters.codex import (
    CodexCliSelectorAdapter,
    SubprocessCodexPluginClient,
)
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.state import canonical_text_file_sha256


TRANSACTION_ID = "TX-00000000-0000-4000-8000-000000000001"
TARGET_REVISION = "c" * 40


class FakeCodexPluginClient:
    """Deterministic model of the documented Codex plugin JSON surface."""

    def __init__(self, target_root: Path) -> None:
        self.target_root = target_root.resolve()
        self.marketplaces: dict[str, str] = {
            "cpt-personal": str((target_root.parent / "legacy-marketplace").resolve()),
            "external": str((target_root.parent / "external-marketplace").resolve()),
        }
        self.catalogs: dict[str, dict[str, str]] = {
            "cpt-personal": {
                "cpt-core": "4.0.0",
                "cpt-design-ui": "4.0.0",
            },
            "external": {
                "external-tool": "1.0.0",
                "unused-external": "1.0.0",
            },
            "product-os-git": {
                "cpt-core": "4.1.0",
                "cpt-design-ui": "4.1.0",
            },
        }
        self.installed: dict[str, str] = {
            "cpt-core": "cpt-core@cpt-personal",
            "cpt-design-ui": "cpt-design-ui@cpt-personal",
            "external-tool": "external-tool@external",
        }
        self.calls: list[tuple[str, str]] = []
        self.fail_target_add_after: int | None = None
        self.marketplace_already_added_response = False
        self._target_adds = 0

    def _entry(
        self,
        name: str,
        marketplace: str,
        *,
        installed: bool,
    ) -> dict[str, Any]:
        root = Path(self.marketplaces[marketplace])
        relative = (
            f"payload/marketplace-root/plugins/{name}"
            if marketplace == "product-os-git"
            else f"plugins/{name}"
        )
        return {
            "pluginId": f"{name}@{marketplace}",
            "name": name,
            "marketplaceName": marketplace,
            "version": self.catalogs[marketplace][name],
            "installed": installed,
            "enabled": installed,
            "source": {"source": "local", "path": str(root / relative)},
            "marketplaceSource": {"sourceType": "local", "source": str(root)},
        }

    def list_plugins(self) -> Mapping[str, Any]:
        installed = []
        available = []
        for marketplace in sorted(self.marketplaces):
            for name in sorted(self.catalogs[marketplace]):
                selector = f"{name}@{marketplace}"
                active = self.installed.get(name) == selector
                entry = self._entry(name, marketplace, installed=active)
                (installed if active else available).append(entry)
        return {"installed": installed, "available": available}

    def list_marketplaces(self) -> Mapping[str, Any]:
        return {
            "marketplaces": [
                {"name": name, "root": root}
                for name, root in sorted(self.marketplaces.items())
            ]
        }

    def add_marketplace(self, source: Path) -> Mapping[str, Any]:
        self.calls.append(("marketplace-add", str(source.resolve())))
        if source.resolve() != self.target_root:
            raise RuntimeError("unexpected fake marketplace root")
        self.marketplaces["product-os-git"] = str(self.target_root)
        return {
            "marketplaceName": "product-os-git",
            "alreadyAdded": self.marketplace_already_added_response,
        }

    def remove_marketplace(self, marketplace: str) -> Mapping[str, Any]:
        self.calls.append(("marketplace-remove", marketplace))
        if any(value.endswith(f"@{marketplace}") for value in self.installed.values()):
            raise RuntimeError("cannot remove a marketplace with installed plugins")
        self.marketplaces.pop(marketplace, None)
        return {"marketplaceName": marketplace, "removed": True}

    def add_plugin(self, selector: str) -> Mapping[str, Any]:
        self.calls.append(("plugin-add", selector))
        name, marketplace = selector.split("@", 1)
        if marketplace not in self.marketplaces or name not in self.catalogs[marketplace]:
            raise RuntimeError("unknown fake plugin selector")
        self.installed[name] = selector
        if marketplace == "product-os-git":
            self._target_adds += 1
            if self.fail_target_add_after == self._target_adds:
                raise RuntimeError("injected partial Codex plugin activation")
        return {"pluginId": selector, "installed": True}

    def remove_plugin(self, selector: str) -> Mapping[str, Any]:
        self.calls.append(("plugin-remove", selector))
        name, _marketplace = selector.split("@", 1)
        if self.installed.get(name) == selector:
            del self.installed[name]
        return {"pluginId": selector, "removed": True}


class CodexCliSelectorAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-codex-adapter-"))
        self.home = self.tmp / "home"
        self.project = self.tmp / "project"
        self.codex_home = self.tmp / "codex-home"
        self.product_os_home = self.tmp / "product-os-home"
        self.target_root = (
            self.product_os_home
            / "sources"
            / "product-os-git"
            / TARGET_REVISION
        )
        for path in (self.home, self.project, self.codex_home, self.target_root):
            path.mkdir(parents=True, exist_ok=True)
        self.target_descriptors = []
        marketplace_plugins = []
        for name in ("cpt-core", "cpt-design-ui"):
            relative = f"payload/marketplace-root/plugins/{name}"
            plugin_manifest = self.target_root / relative / ".codex-plugin" / "plugin.json"
            plugin_manifest.parent.mkdir(parents=True)
            plugin_manifest.write_text(
                json.dumps({"name": name, "version": "4.1.0"}, indent=2) + "\n",
                encoding="utf-8",
            )
            self.target_descriptors.append(
                {
                    "name": name,
                    "selector": f"{name}@product-os-git",
                    "relative_path": relative,
                    "manifest_sha256": canonical_text_file_sha256(plugin_manifest),
                }
            )
            marketplace_plugins.append(
                {"name": name, "source": {"source": "local", "path": relative}}
            )
        marketplace = self.target_root / ".agents" / "plugins" / "marketplace.json"
        marketplace.parent.mkdir(parents=True)
        marketplace.write_text(
            json.dumps(
                {"name": "product-os-git", "plugins": marketplace_plugins},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        package_files = []
        for path in sorted(self.target_root.rglob("*")):
            if path.is_file():
                package_files.append(
                    {
                        "path": path.relative_to(self.target_root).as_posix(),
                        "sha256": canonical_text_file_sha256(path),
                    }
                )
        package_manifest = self.target_root / "MANIFEST.json"
        package_manifest.write_text(
            json.dumps(
                {
                    "schema": "cpt-package-manifest-v10",
                    "name": "codex-product-os",
                    "version": "4.1.0",
                    "file_count": len(package_files),
                    "files": package_files,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        self.target_manifest_sha256 = canonical_text_file_sha256(package_manifest)
        self.context = InstallationContext(
            project=self.project.resolve(),
            user_home=self.home.resolve(),
            codex_home=self.codex_home.resolve(),
            product_os_home=self.product_os_home.resolve(),
            marketplace_registry=(self.home / ".agents" / "plugins" / "marketplace.json").resolve(),
        )
        self.client = FakeCodexPluginClient(self.target_root)
        self.adapter = self._adapter()
        self.targets = [
            {
                "name": name,
                "selector": f"{name}@product-os-git",
                "marketplace_identity": "product-os-git",
                "source_revision": TARGET_REVISION,
            }
            for name in ("cpt-core", "cpt-design-ui")
        ]

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def _adapter(self) -> CodexCliSelectorAdapter:
        return CodexCliSelectorAdapter(
            self.context,
            target_root=self.target_root,
            marketplace_identity="product-os-git",
            target_revision=TARGET_REVISION,
            target_product_version="4.1.0",
            target_manifest_sha256=self.target_manifest_sha256,
            target_plugins=self.target_descriptors,
            legacy_selector_revisions={
                "cpt-core@cpt-personal": "4.0.0",
                "cpt-design-ui@cpt-personal": "4.0.0",
            },
            client=self.client,
        )

    @staticmethod
    def _enabled(evidence) -> set[str]:
        return {
            str(item["selector"])
            for item in evidence.selectors
            if item.get("enabled")
        }

    def test_inspect_is_read_only_and_ignores_untracked_available_plugins(self) -> None:
        evidence = self.adapter.inspect()
        self.assertEqual(self.client.calls, [])
        self.assertFalse(self.adapter.state_path.exists())
        self.assertNotIn(
            "unused-external@external",
            {item["selector"] for item in evidence.selectors},
        )
        self.assertEqual(
            self._enabled(evidence),
            {
                "cpt-core@cpt-personal",
                "cpt-design-ui@cpt-personal",
                "external-tool@external",
            },
        )

    def test_prepare_registers_disabled_targets_without_switching(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        self.assertEqual(self._enabled(prepared), self._enabled(initial))
        target_entries = [
            item for item in prepared.selectors if item["marketplace_identity"] == "product-os-git"
        ]
        self.assertEqual(len(target_entries), 2)
        self.assertTrue(all(not item["enabled"] for item in target_entries))
        self.assertIn("product-os-git", self.client.marketplaces)

    def test_activate_switches_two_plugins_and_preserves_unrelated_state(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        activated = self.adapter.activate(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="activate-selectors",
            expected_state_token=prepared.state_token,
        )
        self.assertEqual(
            self._enabled(activated),
            {
                "cpt-core@product-os-git",
                "cpt-design-ui@product-os-git",
                "external-tool@external",
            },
        )
        external = [item for item in activated.selectors if item["name"] == "external-tool"]
        self.assertEqual(external, [item for item in initial.selectors if item["name"] == "external-tool"])

    def test_restore_after_prepare_removes_transaction_owned_marketplace(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        restored = self.adapter.restore(
            initial.copy_selectors(),
            transaction_id=TRANSACTION_ID,
            operation_id="restore-selectors",
            expected_state_token=prepared.state_token,
        )
        self.assertEqual(restored.copy_selectors(), initial.copy_selectors())
        self.assertNotIn("product-os-git", self.client.marketplaces)

    def test_partial_activation_can_be_restored_exactly(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        self.client.fail_target_add_after = 1
        with self.assertRaisesRegex(RuntimeError, "partial Codex plugin activation"):
            self.adapter.activate(
                self.targets,
                transaction_id=TRANSACTION_ID,
                operation_id="activate-selectors",
                expected_state_token=prepared.state_token,
            )
        partial = self.adapter.inspect()
        self.client.fail_target_add_after = None
        restored = self.adapter.restore(
            initial.copy_selectors(),
            transaction_id=TRANSACTION_ID,
            operation_id="restore-selectors",
            expected_state_token=partial.state_token,
        )
        self.assertEqual(restored.copy_selectors(), initial.copy_selectors())
        self.assertNotIn("product-os-git", self.client.marketplaces)

    def test_restore_rejects_stale_token_without_mutation(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        self.client.catalogs["external"]["external-tool"] = "2.0.0"
        before_calls = copy.deepcopy(self.client.calls)
        with self.assertRaisesRegex(RuntimeError, "changed after rollback preflight"):
            self.adapter.restore(
                initial.copy_selectors(),
                transaction_id=TRANSACTION_ID,
                operation_id="restore-selectors",
                expected_state_token=prepared.state_token,
            )
        self.assertEqual(self.client.calls, before_calls)

    def test_reconstructed_adapter_uses_durable_prepare_ownership(self) -> None:
        initial = self.adapter.inspect()
        prepared = self.adapter.prepare(
            self.targets,
            transaction_id=TRANSACTION_ID,
            operation_id="prepare-selectors",
            expected_state_token=initial.state_token,
        )
        reconstructed = self._adapter()
        restored = reconstructed.restore(
            initial.copy_selectors(),
            transaction_id=TRANSACTION_ID,
            operation_id="restore-after-restart",
            expected_state_token=prepared.state_token,
        )
        self.assertEqual(restored.copy_selectors(), initial.copy_selectors())
        self.assertNotIn("product-os-git", self.client.marketplaces)

    def test_subprocess_client_does_not_create_missing_codex_home(self) -> None:
        missing = self.tmp / "missing-codex-home"
        context = InstallationContext(
            project=self.context.project,
            user_home=self.context.user_home,
            codex_home=missing.resolve(),
            product_os_home=self.context.product_os_home,
            marketplace_registry=self.context.marketplace_registry,
        )
        with self.assertRaisesRegex(RuntimeError, "existing explicit CODEX_HOME"):
            SubprocessCodexPluginClient(context, executable=sys.executable)
        self.assertFalse(missing.exists())

    def test_subprocess_wire_contract_and_descriptor_path_boundary(self) -> None:
        executable = str((self.tmp / "codex.exe").resolve())
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=b'{"installed":[],"available":[]}', stderr=b""
        )
        with mock.patch(
            "manager.product_os_manager.adapters.codex.shutil.which",
            return_value=executable,
        ), mock.patch(
            "manager.product_os_manager.adapters.codex.subprocess.run",
            return_value=completed,
        ) as run:
            client = SubprocessCodexPluginClient(self.context, executable="codex")
            self.assertEqual(client.list_plugins(), {"installed": [], "available": []})
            argv = run.call_args.args[0]
            kwargs = run.call_args.kwargs
            self.assertEqual(argv, [executable, "plugin", "list", "--available", "--json"])
            self.assertFalse(kwargs["check"])
            self.assertEqual(kwargs["timeout"], 120)
            self.assertEqual(kwargs["env"]["HOME"], str(self.home.resolve()))
            self.assertEqual(kwargs["env"]["USERPROFILE"], str(self.home.resolve()))
            self.assertEqual(kwargs["env"]["CODEX_HOME"], str(self.codex_home.resolve()))

        failures = [
            (
                subprocess.CompletedProcess([], 7, stdout=b"", stderr=b"denied"),
                "Codex plugin command failed: list: denied",
            ),
            (
                subprocess.CompletedProcess([], 0, stdout=b"\xff", stderr=b""),
                "returned invalid JSON",
            ),
            (
                subprocess.CompletedProcess([], 0, stdout=b"[]", stderr=b""),
                "did not return a JSON object",
            ),
        ]
        for result, expected in failures:
            with self.subTest(expected=expected), mock.patch(
                "manager.product_os_manager.adapters.codex.shutil.which",
                return_value=executable,
            ), mock.patch(
                "manager.product_os_manager.adapters.codex.subprocess.run",
                return_value=result,
            ):
                client = SubprocessCodexPluginClient(self.context, executable="codex")
                with self.assertRaisesRegex(RuntimeError, expected):
                    client.list_plugins()
        with mock.patch(
            "manager.product_os_manager.adapters.codex.shutil.which",
            return_value=executable,
        ), mock.patch(
            "manager.product_os_manager.adapters.codex.subprocess.run",
            side_effect=subprocess.TimeoutExpired("codex", 120),
        ):
            client = SubprocessCodexPluginClient(self.context, executable="codex")
            with self.assertRaisesRegex(RuntimeError, "failed safely"):
                client.list_plugins()

        for escaped in (r"C:\outside\plugin", r"\\server\share\plugin"):
            descriptors = copy.deepcopy(self.target_descriptors)
            descriptors[0]["relative_path"] = escaped
            with self.subTest(relative_path=escaped), self.assertRaisesRegex(
                RuntimeError, "descriptor is invalid"
            ):
                CodexCliSelectorAdapter(
                    self.context,
                    target_root=self.target_root,
                    marketplace_identity="product-os-git",
                    target_revision=TARGET_REVISION,
                    target_product_version="4.1.0",
                    target_manifest_sha256=self.target_manifest_sha256,
                    target_plugins=descriptors,
                    client=self.client,
                )

    def test_all_bindings_share_one_codex_home_lock(self) -> None:
        reconstructed = self._adapter()
        self.assertEqual(reconstructed.lock_path, self.adapter.lock_path)
        self.assertEqual(
            reconstructed.lock_path,
            (self.codex_home / ".product-os-manager.lock").resolve(),
        )

    def test_wrong_preexisting_marketplace_root_fails_without_mutation(self) -> None:
        self.client.marketplaces["product-os-git"] = str(self.tmp / "wrong-root")
        before = copy.deepcopy(self.client.calls)
        with self.assertRaisesRegex(RuntimeError, "bound to another root"):
            self.adapter.inspect()
        self.assertEqual(self.client.calls, before)

    def test_unproven_marketplace_ownership_fails_closed(self) -> None:
        initial = self.adapter.inspect()
        self.client.marketplace_already_added_response = True
        with self.assertRaisesRegex(RuntimeError, "did not prove transaction ownership"):
            self.adapter.prepare(
                self.targets,
                transaction_id=TRANSACTION_ID,
                operation_id="prepare-selectors",
                expected_state_token=initial.state_token,
            )
        current = self.adapter.inspect()
        with self.assertRaisesRegex(RuntimeError, "ownership is ambiguous"):
            self.adapter.restore(
                initial.copy_selectors(),
                transaction_id=TRANSACTION_ID,
                operation_id="restore-selectors",
                expected_state_token=current.state_token,
            )
        self.assertIn("product-os-git", self.client.marketplaces)
        self.assertNotIn(
            ("marketplace-remove", "product-os-git"),
            self.client.calls,
        )

    def test_retirement_is_explicitly_unsupported_and_zero_mutation(self) -> None:
        initial = self.adapter.inspect()
        before = copy.deepcopy(self.client.calls)
        with self.assertRaisesRegex(RuntimeError, "retirement is unsupported"):
            self.adapter.retire(
                ["cpt-core@product-os-git"],
                transaction_id=TRANSACTION_ID,
                operation_id="retire-selectors",
                expected_state_token=initial.state_token,
            )
        self.assertEqual(self.client.calls, before)


if __name__ == "__main__":
    unittest.main()
