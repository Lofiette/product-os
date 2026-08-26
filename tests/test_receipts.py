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

from tools import cpt_dist

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "cpt_dist.py"
V2_FIELDS = {
    "installation_id",
    "product",
    "source_lineage",
    "installed_plugins",
    "applied_migrations",
    "manager",
}


def run_tool(*args: str, env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if check and result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result


class InstallationReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-r-"))
        self.home = self.tmp / "home"
        self.codex_home = self.tmp / "codex-home"
        self.project = self.tmp / "project"
        self.home.mkdir()
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.home)
        self.env["USERPROFILE"] = str(self.home)
        self.env["CODEX_HOME"] = str(self.codex_home)

    def tearDown(self) -> None:
        def remove_readonly(function, path, _error):
            os.chmod(path, stat.S_IWRITE)
            function(path)

        shutil.rmtree(self.tmp, onerror=remove_readonly)

    @property
    def receipt_path(self) -> Path:
        return self.project / ".cpt" / "install.json"

    def install(self, *extra: str) -> dict:
        run_tool("install", "--project", str(self.project), "--mode", "local", *extra, env=self.env)
        return json.loads(self.receipt_path.read_text(encoding="utf-8"))

    def downgrade_to_v1(self, receipt: dict) -> dict:
        receipt = dict(receipt)
        receipt["schema"] = "cpt-install-receipt-v1"
        for field in V2_FIELDS:
            receipt.pop(field, None)
        self.receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        return receipt

    def test_fresh_install_writes_valid_v2_with_local_lineage(self) -> None:
        receipt = self.install()
        self.assertEqual(receipt["schema"], "cpt-install-receipt-v2")
        self.assertEqual(receipt["product"]["id"], "product-os")
        self.assertEqual(receipt["source_lineage"]["delivery_type"], "local_distribution")
        self.assertEqual(receipt["source_lineage"]["observed_from"], "installer")
        self.assertRegex(receipt["installation_id"], r"^[0-9a-f-]{36}$")
        core = next(item for item in receipt["installed_plugins"] if item["name"] == "cpt-core")
        self.assertEqual(core["marketplace_identity"], "cpt-personal")
        self.assertIsNone(core["selector"])
        registry = json.loads(
            (self.home / ".product-os" / "registry.json").read_text(encoding="utf-8")
        )
        self.assertIn(receipt["installation_id"], registry["installations"])

    def test_v1_read_is_backward_compatible_and_non_mutating(self) -> None:
        legacy = self.downgrade_to_v1(self.install("--plugin-scope", "none"))
        before = self.receipt_path.read_bytes()
        result = run_tool("status", "--project", str(self.project), "--json", env=self.env)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.receipt_path.read_bytes(), before)
        self.assertEqual(json.loads(before)["managed_files"], legacy["managed_files"])

    def test_v1_upgrades_on_update_without_losing_legacy_fields(self) -> None:
        legacy = self.downgrade_to_v1(self.install("--plugin-scope", "none"))
        run_tool("update", "--project", str(self.project), env=self.env)
        upgraded = json.loads(self.receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(upgraded["schema"], "cpt-install-receipt-v2")
        self.assertEqual(upgraded["source_lineage"]["delivery_type"], "unknown")
        self.assertEqual(upgraded["source_lineage"]["observed_from"], "v1_receipt")
        for field in ["mode", "plugin_scope", "mutable_files", "agents", "plugin", "packs", "workers"]:
            self.assertEqual(upgraded[field], legacy[field])
        self.assertTrue(set(legacy["managed_files"]).issubset(upgraded["managed_files"]))

    def test_installation_id_is_stable_and_invalid_v2_fails_closed(self) -> None:
        receipt = self.install("--plugin-scope", "none")
        installation_id = receipt["installation_id"]
        run_tool("update", "--project", str(self.project), env=self.env)
        updated = json.loads(self.receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(updated["installation_id"], installation_id)
        updated.pop("installation_id")
        self.receipt_path.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
        result = run_tool("status", "--project", str(self.project), "--json", env=self.env, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid CPT installation receipt v2", result.stderr)

    def test_git_managed_receipt_is_canonical_and_legacy_commands_fail_closed(self) -> None:
        receipt = self.install("--plugin-scope", "personal")
        target_payload = self.home / ".product-os" / "sources" / "product-os" / ("a" * 40) / "plugins" / "cpt-core"
        canonical_plugin = {
            "name": "cpt-core",
            "selector": "cpt-core@product-os",
            "marketplace_identity": "product-os",
            "version": "4.1.0",
            "payload_path": str(target_payload),
            "manifest_sha256": "b" * 64,
            "status": "active",
        }
        receipt["source_lineage"] = {
            "delivery_type": "git_marketplace",
            "repository": "https://example.invalid/product-os.git",
            "marketplace_identity": "product-os",
            "release": "4.1.0",
            "ref": "v4.1.0",
            "commit_sha": "a" * 40,
            "manifest_sha256": "c" * 64,
            "observed_from": "product-os-manager",
        }
        receipt["installed_plugins"] = [canonical_plugin]
        normalized = cpt_dist.ensure_receipt_v2(self.project, copy.deepcopy(receipt))
        cpt_dist.validate_receipt_v2(normalized)
        self.assertEqual(normalized["installed_plugins"], [canonical_plugin])

        invalid = copy.deepcopy(normalized)
        invalid["source_lineage"]["commit_sha"] = "a" * 41
        with self.assertRaisesRegex(RuntimeError, "Invalid CPT installation receipt v2"):
            cpt_dist.validate_receipt_v2(invalid)

        self.receipt_path.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
        before = self.receipt_path.read_bytes()
        for command in ("update", "uninstall"):
            result = run_tool(command, "--project", str(self.project), env=self.env, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("managed by a Git marketplace", result.stderr)
            self.assertEqual(self.receipt_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
