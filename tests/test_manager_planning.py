from __future__ import annotations

import copy
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from manager.product_os_manager.adapters.deterministic import DeterministicFixtureAdapter
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.inventory import detect_installation
from manager.product_os_manager.planning import build_adoption_plan, validate_adoption_plan
from manager.product_os_manager.state import (
    canonical_json_hash,
    canonical_text_file_sha256,
    file_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tools" / "cpt_dist.py"
MANAGER = ROOT / "tools" / "product_os_manager.py"
V2_FIELDS = {
    "installation_id",
    "product",
    "source_lineage",
    "installed_plugins",
    "applied_migrations",
    "manager",
}


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): file_sha256(path) or ""
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class ManagerPlanningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-plan-"))
        self.home = self.tmp / "home"
        self.codex_home = self.tmp / "codex-home"
        self.manager_home = self.tmp / "manager-home"
        self.project = self.tmp / "project"
        self.home.mkdir()
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.env = os.environ.copy()
        self.env.update({
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "CODEX_HOME": str(self.codex_home),
            "PRODUCT_OS_HOME": str(self.manager_home),
        })
        self.context = InstallationContext.from_environment(self.project, self.env)
        self.adapter = DeterministicFixtureAdapter()

    def tearDown(self) -> None:
        def remove_readonly(function, path, _error):
            os.chmod(path, stat.S_IWRITE)
            function(path)

        shutil.rmtree(self.tmp, onerror=remove_readonly)

    @property
    def receipt_path(self) -> Path:
        return self.project / ".cpt" / "install.json"

    def install(self, scope: str = "none") -> dict:
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
                scope,
            ],
            cwd=ROOT,
            env=self.env,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return json.loads(self.receipt_path.read_text(encoding="utf-8"))

    def selector_claim(self, *selectors: tuple[str, str]) -> dict:
        return {
            "status": "observed",
            "adapter": "deterministic-fixture",
            "authoritative": True,
            "selectors": [
                {
                    "name": name,
                    "selector": selector,
                    "marketplace_identity": selector.split("@", 1)[-1],
                    "enabled": True,
                    "source_revision": None,
                }
                for name, selector in selectors
            ],
        }

    def selector_observation(self, *selectors: tuple[str, str]):
        return self.adapter.selectors(self.selector_claim(*selectors)["selectors"])

    def target_descriptor(self, *, materialized: bool, plugin_version: str = "4.1.0") -> dict:
        commit = "a" * 40
        root = self.manager_home / "sources" / "product-os-git" / commit
        evidence_root = self.tmp / "target-evidence"
        plugin_specs = [
            ("cpt-core", "plugins/cpt-core"),
            ("product-os-manager", "plugins/product-os-manager"),
        ]
        declared_files = []
        plugins = []
        for name, relative in plugin_specs:
            manifest = {"name": name, "version": plugin_version, "description": "fixture"}
            evidence_manifest = evidence_root / relative / ".codex-plugin" / "plugin.json"
            write_json(evidence_manifest, manifest)
            manifest_hash = canonical_text_file_sha256(evidence_manifest)
            declared_files.append({
                "path": f"{relative}/.codex-plugin/plugin.json",
                "sha256": manifest_hash,
            })
            plugins.append({
                "name": name,
                "selector": f"{name}@product-os-git",
                "relative_path": relative,
                "manifest_sha256": manifest_hash,
            })
            if materialized:
                write_json(root / relative / ".codex-plugin" / "plugin.json", manifest)
        runtime_asset = evidence_root / "tools" / "runtime.txt"
        runtime_asset.parent.mkdir(parents=True, exist_ok=True)
        runtime_asset.write_text("runtime\n", encoding="utf-8")
        declared_files.append({
            "path": "tools/runtime.txt",
            "sha256": canonical_text_file_sha256(runtime_asset),
        })
        if materialized:
            target_runtime = root / "tools" / "runtime.txt"
            target_runtime.parent.mkdir(parents=True, exist_ok=True)
            target_runtime.write_text("runtime\n", encoding="utf-8")
        declared_files.sort(key=lambda item: item["path"])
        package_manifest = {
            "schema": "cpt-package-manifest-v10",
            "name": "codex-product-os",
            "version": "4.1.0",
            "file_count": len(declared_files),
            "files": declared_files,
        }
        package_path = evidence_root / "MANIFEST.json"
        write_json(package_path, package_manifest)
        package_hash = canonical_text_file_sha256(package_path)
        if materialized:
            write_json(root / "MANIFEST.json", package_manifest)
            write_json(root / ".product-os-source.json", {
                "schema": "product-os-materialized-source-v1",
                "provider": "filesystem-git",
                "repository": "file:///fixture/product-os.git",
                "marketplace_identity": "product-os-git",
                "requested_ref": "v4.1.0",
                "resolved_commit": commit,
                "product_version": "4.1.0",
                "package_manifest_sha256": package_hash,
            })
        descriptor = {
            "provider": "filesystem-git",
            "repository": "file:///fixture/product-os.git",
            "marketplace_identity": "product-os-git",
            "requested_ref": "v4.1.0",
            "resolved_commit": commit,
            "product_version": "4.1.0",
            "package_manifest_sha256": package_hash,
            "resolution_evidence": {
                "verified": True,
                "method": "filesystem-fixture",
                "provider": "filesystem-git",
                "repository": "file:///fixture/product-os.git",
                "requested_ref": "v4.1.0",
                "resolved_commit": commit,
                "product_version": "4.1.0",
                "package_manifest_sha256": package_hash,
            },
            "plugins": plugins,
        }
        descriptor["resolution_evidence"]["plugins_sha256"] = canonical_json_hash(
            sorted(descriptor["plugins"], key=lambda item: (item["name"], item["selector"]))
        )
        if materialized:
            descriptor["materialized_root"] = str(root)
        return descriptor

    def test_detect_v1_is_non_mutating_and_rejects_unsafe_payload_claim(self) -> None:
        receipt = self.install("personal")
        receipt["schema"] = "cpt-install-receipt-v1"
        for field in V2_FIELDS:
            receipt.pop(field, None)
        receipt["plugin"]["plugin_path"] = str((self.tmp.parent / "outside-plugin").resolve())
        write_json(self.receipt_path, receipt)
        before = self.receipt_path.read_bytes()
        report = detect_installation(self.project, context=self.context)
        self.assertEqual(report["receipt"]["schema"], "cpt-install-receipt-v1")
        self.assertIsNone(report["receipt"]["installation_id"])
        self.assertEqual(report["plugins"][0]["status"], "unsafe_path")
        self.assertEqual(self.receipt_path.read_bytes(), before)

    def test_detect_reports_active_lease_and_valid_checkpoint(self) -> None:
        self.install()
        current_path = self.project / ".cpt" / "current.yaml"
        current = yaml.safe_load(current_path.read_text(encoding="utf-8"))
        current["current_lease"] = "LEASE-fixture"
        current["latest_checkpoint"] = "CP-fixture"
        current_path.write_text(yaml.safe_dump(current, sort_keys=False), encoding="utf-8")
        (self.project / ".cpt" / "checkpoints" / "CP-fixture.yaml").write_text(
            "schema_version: 4.0-alpha8\n",
            encoding="utf-8",
        )
        report = detect_installation(self.project, context=self.context)
        self.assertTrue(report["runtime"]["checkpoint_valid"])
        self.assertIn("current_lease=LEASE-fixture", report["runtime"]["active_reasons"])

    def test_detect_distinguishes_modified_and_missing_managed_files(self) -> None:
        receipt = self.install()
        candidates = [path for path in sorted(receipt["managed_files"]) if path not in {".cpt/current.yaml", ".cpt/runtime.yaml"}]
        modified, missing = candidates[:2]
        (self.project / modified).write_text("modified\n", encoding="utf-8")
        (self.project / missing).unlink()
        report = detect_installation(self.project, context=self.context)
        states = {item["path"]: item["status"] for item in report["managed_files"]["entries"]}
        self.assertEqual(states[modified], "modified")
        self.assertEqual(states[missing], "missing")

    def test_detect_finds_plugin_manifest_hash_mismatch(self) -> None:
        receipt = self.install("personal")
        plugin = next(item for item in receipt["installed_plugins"] if item["name"] == "cpt-core")
        manifest_path = Path(plugin["payload_path"]) / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["description"] += " changed"
        write_json(manifest_path, manifest)
        report = detect_installation(self.project, context=self.context)
        core = next(item for item in report["plugins"] if item["name"] == "cpt-core")
        self.assertEqual(core["status"], "hash_mismatch")

    def test_materialized_plan_hash_is_stable_and_planning_writes_nothing(self) -> None:
        self.install()
        target_descriptor = self.target_descriptor(materialized=True)
        target = self.adapter.target(target_descriptor)
        before = tree_snapshot(self.tmp)
        first_detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(),
        )
        first = build_adoption_plan(first_detection, target, context=self.context)
        second_detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(),
        )
        second = build_adoption_plan(second_detection, target, context=self.context)
        self.assertEqual(first["status"], "ready")
        self.assertEqual(first_detection["state_hash"], second_detection["state_hash"])
        self.assertEqual(first["plan_hash"], second["plan_hash"])
        self.assertEqual(first["target"]["materialization_status"], "verified")
        permuted = copy.deepcopy(target_descriptor)
        permuted["plugins"].reverse()
        permuted_plan = build_adoption_plan(
            second_detection,
            self.adapter.target(permuted),
            context=self.context,
        )
        self.assertEqual(first["plan_hash"], permuted_plan["plan_hash"])
        runtime_asset = Path(first["target"]["materialized_root"]) / "tools" / "runtime.txt"
        runtime_asset.write_text("tampered\n", encoding="utf-8")
        payload_tamper_plan = build_adoption_plan(
            second_detection,
            self.adapter.target(target_descriptor),
            context=self.context,
        )
        self.assertIn(
            "TARGET_PACKAGE_FILE_HASH_MISMATCH",
            {item["code"] for item in payload_tamper_plan["blockers"]},
        )
        runtime_asset.write_text("runtime\n", encoding="utf-8")
        self.assertEqual(tree_snapshot(self.tmp), before)
        tampered_plan = copy.deepcopy(first)
        tampered_plan["actions"].pop()
        with self.assertRaisesRegex(RuntimeError, "plan_hash does not match"):
            validate_adoption_plan(tampered_plan)
        tampered_detection = copy.deepcopy(first_detection)
        tampered_detection["project_path_key"] += "-tampered"
        with self.assertRaisesRegex(RuntimeError, "state_hash does not match"):
            build_adoption_plan(tampered_detection, target, context=self.context)

        stale_plugin_plan = build_adoption_plan(
            second_detection,
            self.adapter.target(self.target_descriptor(materialized=True, plugin_version="4.0.0")),
            context=self.context,
        )
        self.assertEqual(stale_plugin_plan["target"]["materialization_status"], "invalid")
        self.assertIn(
            "version_mismatch",
            {item["status"] for item in stale_plugin_plan["target"]["plugins"]},
        )

    def test_exact_unmaterialized_target_produces_ready_prepare_plan(self) -> None:
        self.install()
        detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(),
        )
        plan = build_adoption_plan(
            detection,
            self.adapter.target(self.target_descriptor(materialized=False)),
            context=self.context,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(plan["target"]["materialization_status"], "not_materialized")
        self.assertIn("materialize_target", [action["id"] for action in plan["actions"]])

    def test_unverified_target_and_missing_selector_authority_block_apply(self) -> None:
        self.install("personal")
        target = self.target_descriptor(materialized=False)
        target["plugins"][0]["manifest_sha256"] = "f" * 64
        detection = detect_installation(self.project, context=self.context)
        plan = build_adoption_plan(detection, self.adapter.target(target), context=self.context)
        codes = {item["code"] for item in plan["blockers"]}
        self.assertEqual(plan["status"], "blocked")
        self.assertIn("TARGET_RESOLUTION_UNVERIFIED", codes)
        self.assertIn("SELECTOR_STATE_UNOBSERVED", codes)
        invalid_commit = self.target_descriptor(materialized=False)
        invalid_commit["resolved_commit"] = "a" * 41
        invalid_commit_plan = build_adoption_plan(
            detect_installation(
                self.project,
                context=self.context,
                selector_observation=self.selector_observation(),
            ),
            self.adapter.target(invalid_commit),
            context=self.context,
        )
        self.assertIn(
            "TARGET_COMMIT_INVALID",
            {item["code"] for item in invalid_commit_plan["blockers"]},
        )
        reserved_root = self.target_descriptor(materialized=False)
        reserved_root["materialized_root"] = str(self.manager_home / "backups")
        reserved_plan = build_adoption_plan(
            detect_installation(
                self.project,
                context=self.context,
                selector_observation=self.selector_observation(),
            ),
            self.adapter.target(reserved_root),
            context=self.context,
        )
        self.assertIn(
            "TARGET_ROOT_UNSAFE",
            {item["code"] for item in reserved_plan["blockers"]},
        )
        volatile_evidence = self.target_descriptor(materialized=False)
        volatile_evidence["resolution_evidence"]["observed_at"] = "volatile"
        volatile_plan = build_adoption_plan(
            detect_installation(
                self.project,
                context=self.context,
                selector_observation=self.selector_observation(),
            ),
            self.adapter.target(volatile_evidence),
            context=self.context,
        )
        self.assertIn(
            "TARGET_EVIDENCE_FIELDS_INVALID",
            {item["code"] for item in volatile_plan["blockers"]},
        )
        invalid_selector_claim = self.selector_claim(("cpt-core", "cpt-core@legacy"))
        invalid_selector_claim["selectors"][0]["enabled"] = "false"
        invalid_selector_detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=invalid_selector_claim,
        )
        self.assertEqual(invalid_selector_detection["selectors"]["status"], "invalid")

        incomplete_target = self.target_descriptor(materialized=False)
        incomplete_target["plugins"] = [
            item for item in incomplete_target["plugins"] if item["name"] != "cpt-core"
        ]
        incomplete_target["resolution_evidence"]["plugins_sha256"] = canonical_json_hash(
            incomplete_target["plugins"]
        )
        coverage_plan = build_adoption_plan(
            detect_installation(
                self.project,
                context=self.context,
                selector_observation=self.selector_observation(
                    ("cpt-core", "cpt-core@cpt-personal")
                ),
            ),
            self.adapter.target(incomplete_target),
            context=self.context,
        )
        self.assertIn(
            "TARGET_PLUGIN_COVERAGE_INCOMPLETE",
            {item["code"] for item in coverage_plan["blockers"]},
        )

    def test_missing_registry_is_repairable_but_never_authorizes_retirement(self) -> None:
        self.install()
        self.context.registry_path.unlink()
        detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(),
        )
        plan = build_adoption_plan(
            detection,
            self.adapter.target(self.target_descriptor(materialized=False)),
            context=self.context,
        )
        self.assertEqual(plan["status"], "ready")
        self.assertIn("REGISTRY_INCOMPLETE", {item["code"] for item in plan["warnings"]})
        self.assertEqual(plan["rollback"]["legacy_selector_policy"], "retain_until_proven_unreferenced")

    def test_recorded_unmaterialized_plugin_must_be_covered_by_target(self) -> None:
        receipt = self.install("personal")
        receipt["installed_plugins"].append(
            {
                "name": "recorded-pack",
                "selector": "recorded-pack@cpt-personal",
                "marketplace_identity": "cpt-personal",
                "version": "4.0.0",
                "payload_path": None,
                "manifest_sha256": None,
                "status": "unobserved",
            }
        )
        write_json(self.receipt_path, receipt)
        detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(
                ("cpt-core", "cpt-core@cpt-personal"),
                ("recorded-pack", "recorded-pack@cpt-personal"),
            ),
        )
        plan = build_adoption_plan(
            detection,
            self.adapter.target(self.target_descriptor(materialized=False)),
            context=self.context,
        )
        blocker = next(
            item
            for item in plan["blockers"]
            if item["code"] == "TARGET_PLUGIN_COVERAGE_INCOMPLETE"
        )
        self.assertEqual(blocker["details"]["plugins"], ["recorded-pack"])

    def test_corrupt_registry_and_marketplace_block_plan(self) -> None:
        self.install()
        self.context.registry_path.write_text("{broken", encoding="utf-8")
        self.context.marketplace_registry.parent.mkdir(parents=True, exist_ok=True)
        self.context.marketplace_registry.write_text("{broken", encoding="utf-8")
        detection = detect_installation(
            self.project,
            context=self.context,
            selector_observation=self.selector_observation(),
        )
        plan = build_adoption_plan(
            detection,
            self.adapter.target(self.target_descriptor(materialized=False)),
            context=self.context,
        )
        codes = {item["code"] for item in plan["blockers"]}
        self.assertIn("REGISTRY_INVALID", codes)
        self.assertIn("MARKETPLACE_INVALID", codes)

    def test_cli_plan_without_output_is_stdout_only(self) -> None:
        self.install()
        target_path = self.tmp / "target.json"
        selectors_path = self.tmp / "selectors.json"
        write_json(target_path, self.target_descriptor(materialized=True))
        write_json(selectors_path, self.selector_claim())
        before = tree_snapshot(self.tmp)
        result = subprocess.run(
            [
                sys.executable,
                str(MANAGER),
                "plan",
                "--project",
                str(self.project),
                "--target",
                str(target_path),
                "--selector-state",
                str(selectors_path),
            ],
            cwd=ROOT,
            env=self.env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        cli_plan = json.loads(result.stdout)
        self.assertEqual(cli_plan["status"], "blocked")
        codes = {item["code"] for item in cli_plan["blockers"]}
        self.assertIn("TARGET_EVIDENCE_UNTRUSTED", codes)
        self.assertIn("SELECTOR_STATE_UNOBSERVED", codes)
        self.assertEqual(tree_snapshot(self.tmp), before)


if __name__ == "__main__":
    unittest.main()
