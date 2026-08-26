from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

from tools import cpt_dist

from manager.product_os_manager.adapters.base import AdapterRegistry
from manager.product_os_manager.adapters.deterministic import DeterministicSelectorAdapter
from manager.product_os_manager.adapters.repository import (
    DirectoryTargetProvider,
    LocalGitTargetProvider,
)
from manager.product_os_manager.backup import resource_paths, snapshot_resources
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.doctor import (
    run_migration_doctor,
    validate_migration_doctor_report,
)
from manager.product_os_manager.inventory import detect_installation
from manager.product_os_manager.planning import build_adoption_plan
from manager.product_os_manager.registry import RegistryStore, receipt_entry
from manager.product_os_manager.state import (
    canonical_text_file_sha256,
    exclusive_lock,
    file_sha256,
)
from manager.product_os_manager.transaction import (
    AdoptionTransactionError,
    ConcurrentAdoptionChange,
    _transition,
    load_transaction,
    prepare_adoption,
    recover_adoption,
    rollback_adoption,
    switch_adoption,
    transaction_lock_path,
    validate_mutation_context,
)

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tools" / "cpt_dist.py"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def tree_snapshot(root: Path, *, exclude: tuple[Path, ...] = ()) -> dict[str, str]:
    excluded = {str(path.absolute()).casefold() for path in exclude}
    return {
        path.relative_to(root).as_posix(): file_sha256(path) or ""
        for path in sorted(root.rglob("*"))
        if path.is_file() and str(path.absolute()).casefold() not in excluded
    }


class AdversarialSelectorAdapter(DeterministicSelectorAdapter):
    mode: str | None = None
    drift_path: Path | None = None

    def _corrupt_unrelated(self) -> None:
        document = self._read_document()
        selectors = document["selectors"]
        for item in selectors:
            if item["selector"] == "external-tool@disabled":
                item["source_revision"] = "collateral-corruption"
        self._write_document(selectors, document["operations"])

    def prepare(self, *args, **kwargs):
        evidence = super().prepare(*args, **kwargs)
        if self.mode == "collateral_prepare":
            self._corrupt_unrelated()
            return self.inspect()
        return evidence

    def activate(self, *args, **kwargs):
        if self.mode == "resource_drift":
            assert self.drift_path is not None
            self.drift_path.write_text(
                "external concurrent edit\n", encoding="utf-8"
            )
            raise RuntimeError("Injected external resource drift")
        evidence = super().activate(*args, **kwargs)
        if self.mode == "collateral_activate":
            self._corrupt_unrelated()
            return self.inspect()
        return evidence


class ManagerTransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-transaction-"))
        self.home = self.tmp / "home"
        self.project = self.tmp / "project"
        self.codex_home = self.tmp / "codex-home"
        self.product_os_home = self.tmp / "product-os-home"
        self.home.mkdir()
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.env = os.environ.copy()
        self.env.update(
            {
                "HOME": str(self.home),
                "USERPROFILE": str(self.home),
                "CODEX_HOME": str(self.codex_home),
                "PRODUCT_OS_HOME": str(self.product_os_home),
            }
        )
        self.context = InstallationContext.from_environment(self.project, self.env)
        result = subprocess.run(
            [
                sys.executable,
                str(DIST),
                "install",
                "--project",
                str(self.project),
                "--mode",
                "local",
                "--plugin-scope",
                "personal",
                "--rules-profile",
                "none",
            ],
            cwd=ROOT,
            env=self.env,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        pack_result = subprocess.run(
            [
                sys.executable,
                str(DIST),
                "pack-add",
                "--name",
                "cpt-design-ui",
                "--scope",
                "personal",
                "--project",
                str(self.project),
            ],
            cwd=ROOT,
            env=self.env,
            text=True,
            capture_output=True,
        )
        if pack_result.returncode:
            raise AssertionError(pack_result.stdout + pack_result.stderr)
        self.initial_receipt = cpt_dist.load_receipt(self.project)
        self.initial_receipt_bytes = (self.project / ".cpt" / "install.json").read_bytes()
        self.selector = AdversarialSelectorAdapter(
            self.tmp / "selectors.json",
            [
                {
                    "name": "cpt-core",
                    "selector": "cpt-core@cpt-personal",
                    "marketplace_identity": "cpt-personal",
                    "enabled": True,
                    "source_revision": None,
                },
                {
                    "name": "cpt-design-ui",
                    "selector": "cpt-design-ui@cpt-personal",
                    "marketplace_identity": "cpt-personal",
                    "enabled": True,
                    "source_revision": None,
                },
                {
                    "name": "external-tool",
                    "selector": "external-tool@external",
                    "marketplace_identity": "external",
                    "enabled": True,
                    "source_revision": "external-1",
                },
                {
                    "name": "external-tool",
                    "selector": "external-tool@disabled",
                    "marketplace_identity": "external",
                    "enabled": False,
                    "source_revision": "external-0",
                },
            ],
        )
        self.initial_selectors = self.selector.inspect().copy_selectors()
        self.source = self._build_source_distribution()
        self.provider = DirectoryTargetProvider(
            self.source,
            self.context,
            resolved_commit="c" * 40,
            requested_ref="v4.1.0",
            repository="file:///isolated/product-os.git",
        )
        self.adapters = AdapterRegistry(
            target_providers=[self.provider],
            selector_adapters=[self.selector],
        )
        self.request = {
            "repository": self.provider.repository,
            "requested_ref": self.provider.requested_ref,
            "marketplace_identity": "product-os-git",
            "plugins": ["cpt-core", "cpt-design-ui"],
        }
        self.plan = self._plan()
        if self.plan["status"] != "ready":
            raise AssertionError(self.plan["blockers"])

    def tearDown(self) -> None:
        def remove_readonly(function, path, _error):
            os.chmod(path, stat.S_IWRITE)
            function(path)

        shutil.rmtree(self.tmp, onerror=remove_readonly)

    def _build_source_distribution(self) -> Path:
        source = self.tmp / "source-distribution"
        shutil.copytree(
            ROOT / "payload" / "repo-scaffold",
            source / "payload" / "repo-scaffold",
        )
        shutil.copytree(
            ROOT / "payload" / "marketplace-root" / "plugins" / "cpt-core",
            source / "payload" / "marketplace-root" / "plugins" / "cpt-core",
        )
        shutil.copytree(
            ROOT / "domain-packs" / "cpt-design-ui" / ".codex-plugin",
            source
            / "payload"
            / "marketplace-root"
            / "plugins"
            / "cpt-design-ui"
            / ".codex-plugin",
        )
        fixture_skills = (
            source
            / "payload"
            / "marketplace-root"
            / "plugins"
            / "cpt-design-ui"
            / "skills"
        )
        fixture_skills.mkdir()
        (fixture_skills / "README.md").write_text(
            "Minimal materialization fixture; selector semantics are under test.\n",
            encoding="utf-8",
        )
        write_json(
            source / ".agents" / "plugins" / "marketplace.json",
            {
                "name": "product-os-git",
                "plugins": [
                    {
                        "name": "cpt-core",
                        "source": {
                            "source": "local",
                            "path": "payload/marketplace-root/plugins/cpt-core",
                        },
                    },
                    {
                        "name": "cpt-design-ui",
                        "source": {
                            "source": "local",
                            "path": "payload/marketplace-root/plugins/cpt-design-ui",
                        },
                    },
                ],
            },
        )
        files = []
        for path in sorted(source.rglob("*")):
            if path.is_file():
                files.append(
                    {
                        "path": path.relative_to(source).as_posix(),
                        "sha256": canonical_text_file_sha256(path),
                    }
                )
        write_json(
            source / "MANIFEST.json",
            {
                "schema": "cpt-package-manifest-v10",
                "name": "codex-product-os",
                "version": "4.1.0",
                "file_count": len(files),
                "files": files,
            },
        )
        return source

    def _plan(self) -> dict:
        selector_evidence = self.selector.inspect()
        target_evidence = self.provider.resolve(self.request)
        detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=selector_evidence,
        )
        return build_adoption_plan(
            detection,
            target_evidence,
            context=self.context,
        )

    def _active_snapshot(self):
        receipt = cpt_dist.load_receipt(self.project)
        files, directories = resource_paths(self.context, receipt)
        return snapshot_resources(self.context, files, directories)

    def _prepare(self):
        return prepare_adoption(
            self.plan,
            confirmed_plan_hash=self.plan["plan_hash"],
            context=self.context,
            adapters=self.adapters,
        )

    def test_wrong_plan_confirmation_has_zero_writes(self) -> None:
        before = tree_snapshot(self.tmp)
        with self.assertRaisesRegex(AdoptionTransactionError, "plan_hash"):
            prepare_adoption(
                self.plan,
                confirmed_plan_hash="0" * 64,
                context=self.context,
                adapters=self.adapters,
            )
        self.assertEqual(tree_snapshot(self.tmp), before)

    def test_prepare_is_idempotent_and_keeps_legacy_active(self) -> None:
        before = self._active_snapshot()
        first = self._prepare()
        second = self._prepare()
        self.assertEqual(first["transaction_id"], second["transaction_id"])
        self.assertEqual(first["prepared_state_hash"], second["prepared_state_hash"])
        self.assertEqual(self._active_snapshot(), before)
        journal = load_transaction(self.context, first["transaction_id"])
        self.assertEqual(journal["state"], "prepared")
        self.assertIsNotNone(journal["backup"]["manifest_hash"])
        enabled = {
            item["selector"]
            for item in self.selector.inspect().selectors
            if item["enabled"]
        }
        self.assertEqual(
            enabled,
            {
                "cpt-core@cpt-personal",
                "cpt-design-ui@cpt-personal",
                "external-tool@external",
            },
        )
        target = next(
            item
            for item in self.selector.inspect().selectors
            if item["selector"] == "cpt-core@product-os-git"
        )
        self.assertFalse(target["enabled"])
        self.assertEqual(
            [
                item
                for item in self.selector.inspect().copy_selectors()
                if item["name"] == "external-tool"
            ],
            [item for item in self.initial_selectors if item["name"] == "external-tool"],
        )

    def test_wrong_switch_confirmation_has_zero_writes(self) -> None:
        prepared = self._prepare()
        before = tree_snapshot(self.tmp)
        with self.assertRaisesRegex(AdoptionTransactionError, "prepared-state"):
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash="0" * 64,
                context=self.context,
                adapters=self.adapters,
            )
        self.assertEqual(tree_snapshot(self.tmp), before)

    def test_switch_commits_git_lineage_then_rollback_restores_installation(self) -> None:
        prepared = self._prepare()
        result = switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        self.assertEqual(result["status"], "committed")
        self.assertEqual(result["doctor"]["status"], "PASS")
        self.assertEqual(
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                context=self.context,
                adapters=self.adapters,
            ),
            result,
        )
        receipt = cpt_dist.load_receipt(self.project)
        self.assertEqual(receipt["source_lineage"]["delivery_type"], "git_marketplace")
        self.assertEqual(receipt["source_lineage"]["commit_sha"], "c" * 40)
        self.assertEqual(receipt["manager"]["last_transaction_id"], prepared["transaction_id"])
        self.assertEqual(
            [item["selector"] for item in receipt["installed_plugins"]],
            [
                "cpt-core@product-os-git",
                "cpt-design-ui@product-os-git",
            ],
        )
        migration = receipt["applied_migrations"][-1]
        self.assertEqual(
            migration["superseded_local_state"]["packs"][0]["name"],
            "cpt-design-ui",
        )
        enabled = [
            item["selector"]
            for item in self.selector.inspect().selectors
            if item["enabled"]
        ]
        self.assertEqual(
            enabled,
            [
                "cpt-core@product-os-git",
                "cpt-design-ui@product-os-git",
                "external-tool@external",
            ],
        )
        rolled_back = rollback_adoption(
            prepared["transaction_id"],
            context=self.context,
            adapters=self.adapters,
        )
        self.assertEqual(rolled_back["status"], "rolled_back")
        self.assertEqual(
            (self.project / ".cpt" / "install.json").read_bytes(),
            self.initial_receipt_bytes,
        )
        self.assertEqual(
            self.selector.inspect().copy_selectors(),
            self.initial_selectors,
        )

    def test_partial_selector_activation_is_compensated(self) -> None:
        prepared = self._prepare()
        self.selector.faults.add("activate_after_first")
        with self.assertRaisesRegex(RuntimeError, "activate_after_first"):
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                context=self.context,
                adapters=self.adapters,
            )
        journal = load_transaction(self.context, prepared["transaction_id"])
        self.assertEqual(journal["state"], "rolled_back")
        self.assertEqual(
            (self.project / ".cpt" / "install.json").read_bytes(),
            self.initial_receipt_bytes,
        )
        self.assertEqual(self.selector.inspect().copy_selectors(), self.initial_selectors)

    def test_local_git_provider_completes_transactional_adoption(self) -> None:
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
                "user.name=Product OS Test",
                "-c",
                "user.email=product-os-test.invalid",
                "commit",
                "-q",
                "-m",
                "isolated 4.1 target",
            ],
            check=True,
        )
        provider = LocalGitTargetProvider(self.source, self.context)
        adapters = AdapterRegistry(
            target_providers=[provider],
            selector_adapters=[self.selector],
        )
        request = {
            "repository": provider.repository,
            "requested_ref": "release/4.1.0",
            "marketplace_identity": "product-os-git",
            "plugins": ["cpt-core", "cpt-design-ui"],
        }
        target = provider.resolve(request)
        plan = build_adoption_plan(
            detect_installation(
                self.project,
                context=self.context,
                selector_observation=self.selector.inspect(),
            ),
            target,
            context=self.context,
        )
        self.assertEqual(plan["status"], "ready")
        prepared = prepare_adoption(
            plan,
            confirmed_plan_hash=plan["plan_hash"],
            context=self.context,
            adapters=adapters,
        )
        result = switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=adapters,
        )
        self.assertEqual(result["status"], "committed")
        journal = load_transaction(self.context, prepared["transaction_id"])
        self.assertEqual(journal["adapters"]["target"]["adapter_id"], "local-git")
        receipt = cpt_dist.load_receipt(self.project)
        self.assertEqual(receipt["source_lineage"]["repository"], provider.repository)
        self.assertEqual(
            receipt["source_lineage"]["commit_sha"],
            subprocess.run(
                ["git", "-C", str(self.source), "rev-parse", "HEAD"],
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip(),
        )

    def test_receipt_and_registry_failures_compensate(self) -> None:
        for fault in ("after_receipt_write", "after_registry_write"):
            with self.subTest(fault=fault):
                if fault != "after_receipt_write":
                    self.tearDown()
                    self.setUp()
                prepared = self._prepare()
                with self.assertRaisesRegex(RuntimeError, fault):
                    switch_adoption(
                        prepared["transaction_id"],
                        confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                        context=self.context,
                        adapters=self.adapters,
                        faults={fault},
                    )
                journal = load_transaction(self.context, prepared["transaction_id"])
                self.assertEqual(journal["state"], "rolled_back")
                self.assertEqual(
                    (self.project / ".cpt" / "install.json").read_bytes(),
                    self.initial_receipt_bytes,
                )
                report = detect_installation(
                    self.project,
                    context=self.context,
                    selector_observation=self.selector.inspect(),
                )
                self.assertTrue(report["registry"]["entry_matches_receipt"])

    def test_selector_drift_blocks_switch_without_runtime_mutation(self) -> None:
        prepared = self._prepare()
        before = self._active_snapshot()
        state = json.loads(self.selector.state_path.read_text(encoding="utf-8"))
        state["selectors"].append(
            {
                "name": "unrelated",
                "selector": "unrelated@fixture",
                "marketplace_identity": "fixture",
                "enabled": True,
                "source_revision": None,
            }
        )
        write_json(self.selector.state_path, state)
        with self.assertRaisesRegex(ConcurrentAdoptionChange, "Selector state changed"):
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                context=self.context,
                adapters=self.adapters,
            )
        self.assertEqual(self._active_snapshot(), before)
        self.assertEqual(
            load_transaction(self.context, prepared["transaction_id"])["state"],
            "prepared",
        )

    def test_prepared_transaction_can_be_rolled_back(self) -> None:
        prepared = self._prepare()
        result = rollback_adoption(
            prepared["transaction_id"],
            context=self.context,
            adapters=self.adapters,
        )
        self.assertEqual(result["status"], "rolled_back")
        self.assertEqual(self.selector.inspect().copy_selectors(), self.initial_selectors)

    def test_default_nested_user_roots_are_valid(self) -> None:
        env = self.env.copy()
        env.pop("CODEX_HOME", None)
        env.pop("PRODUCT_OS_HOME", None)
        nested = InstallationContext.from_environment(self.project, env)
        self.assertEqual(nested.codex_home.parent, self.home)
        self.assertEqual(nested.product_os_home.parent, self.home)
        validate_mutation_context(nested)

    def test_prepare_collateral_selector_change_fails_closed(self) -> None:
        before_resources = self._active_snapshot()
        self.selector.mode = "collateral_prepare"
        with self.assertRaisesRegex(
            AdoptionTransactionError, "exact bounded target diff"
        ):
            self._prepare()
        journal_path = next(self.product_os_home.rglob("journal.json"))
        journal = load_transaction(self.context, journal_path.parent.name)
        self.assertEqual(journal["state"], "manual_recovery_required")
        self.assertEqual(self._active_snapshot(), before_resources)
        corrupted = next(
            item
            for item in self.selector.inspect().selectors
            if item["selector"] == "external-tool@disabled"
        )
        self.assertEqual(corrupted["source_revision"], "collateral-corruption")
        with self.assertRaisesRegex(AdoptionTransactionError, "unresolved"):
            self._prepare()

    def test_activate_collateral_selector_change_is_not_claimed_rolled_back(self) -> None:
        prepared = self._prepare()
        self.selector.mode = "collateral_activate"
        with self.assertRaisesRegex(
            AdoptionTransactionError, "exact bounded target diff"
        ):
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                context=self.context,
                adapters=self.adapters,
            )
        journal = load_transaction(self.context, prepared["transaction_id"])
        self.assertEqual(journal["state"], "manual_recovery_required")
        corrupted = next(
            item
            for item in self.selector.inspect().selectors
            if item["selector"] == "external-tool@disabled"
        )
        self.assertEqual(corrupted["source_revision"], "collateral-corruption")

    def test_concurrent_resource_drift_is_never_overwritten_by_compensation(self) -> None:
        prepared = self._prepare()
        drift_path = self.project / ".cpt" / "bin" / "cpt_runtime.py"
        self.selector.mode = "resource_drift"
        self.selector.drift_path = drift_path
        with self.assertRaisesRegex(RuntimeError, "external resource drift"):
            switch_adoption(
                prepared["transaction_id"],
                confirmed_prepared_state_hash=prepared["prepared_state_hash"],
                context=self.context,
                adapters=self.adapters,
            )
        self.assertEqual(
            drift_path.read_text(encoding="utf-8"), "external concurrent edit\n"
        )
        self.assertEqual(
            load_transaction(self.context, prepared["transaction_id"])["state"],
            "manual_recovery_required",
        )

    def test_owned_drift_blocks_explicit_rollback_before_any_restore(self) -> None:
        prepared = self._prepare()
        switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        drift_path = self.project / ".cpt" / "bin" / "cpt_runtime.py"
        drift_path.write_text("post-commit external edit\n", encoding="utf-8")
        selectors = self.selector.inspect().copy_selectors()
        with self.assertRaisesRegex(AdoptionTransactionError, "manual recovery"):
            rollback_adoption(
                prepared["transaction_id"],
                context=self.context,
                adapters=self.adapters,
            )
        self.assertEqual(
            drift_path.read_text(encoding="utf-8"), "post-commit external edit\n"
        )
        self.assertEqual(self.selector.inspect().copy_selectors(), selectors)

    def test_rollback_preserves_unrelated_selector_and_registry_changes(self) -> None:
        prepared = self._prepare()
        switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        document = self.selector._read_document()
        document["selectors"].append(
            {
                "name": "third-party",
                "selector": "third-party@external",
                "marketplace_identity": "external",
                "enabled": True,
                "source_revision": "third-party-1",
            }
        )
        self.selector._write_document(document["selectors"], document["operations"])
        store = RegistryStore(self.context)
        registry, digest = store.snapshot()
        other_receipt = json.loads(json.dumps(cpt_dist.load_receipt(self.project)))
        other_receipt["installation_id"] = str(uuid.uuid4())
        other_project = self.tmp / "other-project"
        other_entry = receipt_entry(other_project, other_receipt)
        registry["installations"][other_receipt["installation_id"]] = other_entry
        store.save(registry, expected_digest=digest)

        result = rollback_adoption(
            prepared["transaction_id"],
            context=self.context,
            adapters=self.adapters,
        )
        self.assertEqual(result["status"], "rolled_back")
        selectors = self.selector.inspect().copy_selectors()
        self.assertIn("third-party@external", [item["selector"] for item in selectors])
        for initial in self.initial_selectors:
            self.assertIn(initial, selectors)
        registry_after, _digest = store.snapshot()
        self.assertEqual(
            registry_after["installations"][other_receipt["installation_id"]],
            other_entry,
        )

    def test_public_migration_doctor_revalidates_committed_transaction(self) -> None:
        prepared = self._prepare()
        switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        report = run_migration_doctor(
            self.context,
            self.adapters,
            transaction_id=prepared["transaction_id"],
        )
        validate_migration_doctor_report(report)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["transaction_state"], "committed")
        self.assertEqual(
            run_migration_doctor(self.context, self.adapters)["transaction_id"],
            prepared["transaction_id"],
        )

    def test_public_migration_doctor_reports_owned_drift_without_repair(self) -> None:
        prepared = self._prepare()
        switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        drift_path = self.project / ".cpt" / "bin" / "cpt_runtime.py"
        drift_path.write_text("doctor-observed external drift\n", encoding="utf-8")
        before = tree_snapshot(self.tmp)
        report = run_migration_doctor(
            self.context,
            self.adapters,
            transaction_id=prepared["transaction_id"],
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            "MANAGED_FILES_HEALTHY",
            [item["code"] for item in report["checks"] if item["status"] == "FAIL"],
        )
        self.assertEqual(tree_snapshot(self.tmp), before)

    def test_public_migration_doctor_is_zero_write_while_transaction_is_active(self) -> None:
        prepared = self._prepare()
        switch_adoption(
            prepared["transaction_id"],
            confirmed_prepared_state_hash=prepared["prepared_state_hash"],
            context=self.context,
            adapters=self.adapters,
        )
        lock_path = transaction_lock_path(self.context)
        with exclusive_lock(lock_path):
            before = tree_snapshot(self.tmp, exclude=(lock_path,))
            report = run_migration_doctor(
                self.context,
                self.adapters,
                transaction_id=prepared["transaction_id"],
            )
            self.assertEqual(tree_snapshot(self.tmp, exclude=(lock_path,)), before)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(
            next(
                item["status"]
                for item in report["checks"]
                if item["code"] == "TRANSACTION_QUIESCENT"
            ),
            "FAIL",
        )

    def test_recover_orphaned_switch_intent_rolls_back_safely(self) -> None:
        prepared = self._prepare()
        journal = load_transaction(self.context, prepared["transaction_id"])
        _transition(self.context, journal, "refreshing_runtime")
        result = recover_adoption(
            prepared["transaction_id"],
            context=self.context,
            adapters=self.adapters,
        )
        self.assertEqual(result["status"], "rolled_back")
        self.assertEqual(
            (self.project / ".cpt" / "install.json").read_bytes(),
            self.initial_receipt_bytes,
        )
        self.assertEqual(self.selector.inspect().copy_selectors(), self.initial_selectors)


if __name__ == "__main__":
    unittest.main()
