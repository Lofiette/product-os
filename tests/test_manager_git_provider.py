from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path

from manager.product_os_manager.adapters.repository import LocalGitTargetProvider
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.state import canonical_json_hash


def canonical_bytes(data: bytes) -> bytes:
    return data if b"\0" in data else data.replace(b"\r\n", b"\n")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


class LocalGitTargetProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="po41-local-git-"))
        self.repository_root = self.tmp / "repository"
        self.project = self.tmp / "project"
        self.home = self.tmp / "home"
        self.codex_home = self.tmp / "codex-home"
        self.product_os_home = self.tmp / "product-os-home"
        for path in (self.repository_root, self.project, self.home):
            path.mkdir()
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(self.home),
                "USERPROFILE": str(self.home),
                "CODEX_HOME": str(self.codex_home),
                "PRODUCT_OS_HOME": str(self.product_os_home),
            }
        )
        self.context = InstallationContext.from_environment(self.project, environment)
        self._git("init", "-q")
        self._git("symbolic-ref", "HEAD", "refs/heads/release/4.1.0")
        self._write_distribution("initial payload\n")
        self._commit("initial distribution")
        self.provider = LocalGitTargetProvider(self.repository_root, self.context)
        self.request = {
            "repository": self.provider.repository,
            "requested_ref": "release/4.1.0",
            "marketplace_identity": "product-os-git",
            "plugins": ["cpt-core"],
        }

    def tearDown(self) -> None:
        def remove_readonly(function, path, _error):
            os.chmod(path, stat.S_IWRITE)
            function(path)

        shutil.rmtree(self.tmp, onerror=remove_readonly)

    def _git(self, *arguments: str, input_bytes: bytes | None = None) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repository_root), *arguments],
            input=input_bytes,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise AssertionError(completed.stderr.decode("utf-8", errors="replace"))
        return completed.stdout.decode("utf-8").strip()

    def _write_distribution(self, payload: str) -> None:
        write_json(
            self.repository_root / ".agents" / "plugins" / "marketplace.json",
            {
                "name": "product-os-git",
                "plugins": [
                    {
                        "name": "cpt-core",
                        "source": {
                            "source": "local",
                            "path": "plugins/cpt-core",
                        },
                    }
                ],
            },
        )
        write_json(
            self.repository_root
            / "plugins"
            / "cpt-core"
            / ".codex-plugin"
            / "plugin.json",
            {"name": "cpt-core", "version": "4.1.0"},
        )
        payload_path = self.repository_root / "plugins" / "cpt-core" / "README.md"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload_path.write_text(payload, encoding="utf-8", newline="\n")
        self._rewrite_manifest()

    def _rewrite_manifest(self) -> None:
        files = []
        for path in sorted(self.repository_root.rglob("*")):
            if not path.is_file() or ".git" in path.parts or path.name == "MANIFEST.json":
                continue
            data = canonical_bytes(path.read_bytes())
            files.append(
                {
                    "path": path.relative_to(self.repository_root).as_posix(),
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        write_json(
            self.repository_root / "MANIFEST.json",
            {
                "schema": "cpt-package-manifest-v10",
                "name": "codex-product-os",
                "version": "4.1.0",
                "file_count": len(files),
                "files": files,
            },
        )

    def _commit(self, message: str) -> str:
        self._git("add", "--all")
        self._git(
            "-c",
            "user.name=Product OS Test",
            "-c",
            "user.email=product-os-test.invalid",
            "commit",
            "-q",
            "-m",
            message,
        )
        return self._git("rev-parse", "HEAD")

    def _transaction_id(self) -> str:
        return f"TX-{uuid.uuid4()}"

    def test_resolve_reads_immutable_commit_and_ignores_dirty_worktree(self) -> None:
        first = self.provider.resolve(self.request)
        expected_commit = self._git("rev-parse", "HEAD")
        (self.repository_root / "plugins" / "cpt-core" / "README.md").write_text(
            "dirty working tree\n", encoding="utf-8"
        )
        (self.repository_root / "untracked.txt").write_text("ignored\n", encoding="utf-8")
        second = self.provider.resolve(self.request)
        self.assertEqual(first.copy_descriptor()["resolved_commit"], expected_commit)
        self.assertEqual(
            canonical_json_hash(first.copy_descriptor()),
            canonical_json_hash(second.copy_descriptor()),
        )

    def test_materialize_is_verified_immutable_and_idempotent(self) -> None:
        evidence = self.provider.resolve(self.request)
        destination = Path(evidence.copy_descriptor()["materialized_root"])
        first = self.provider.materialize(
            evidence,
            destination,
            transaction_id=self._transaction_id(),
            operation_id="materialize-target",
        )
        second = self.provider.materialize(
            evidence,
            destination,
            transaction_id=self._transaction_id(),
            operation_id="materialize-target",
        )
        self.assertEqual(
            canonical_json_hash(first.copy_descriptor()),
            canonical_json_hash(second.copy_descriptor()),
        )
        self.assertTrue((destination / ".product-os-source.json").is_file())
        self.assertFalse((destination / ".git").exists())
        self.assertEqual(
            (destination / "plugins" / "cpt-core" / "README.md").read_text(encoding="utf-8"),
            "initial payload\n",
        )

    def test_existing_materialized_corruption_is_rejected(self) -> None:
        evidence = self.provider.resolve(self.request)
        destination = Path(evidence.copy_descriptor()["materialized_root"])
        self.provider.materialize(
            evidence,
            destination,
            transaction_id=self._transaction_id(),
            operation_id="materialize-target",
        )
        (destination / "plugins" / "cpt-core" / "README.md").write_text(
            "corrupt\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "(?:size|hash) mismatch"):
            self.provider.materialize(
                evidence,
                destination,
                transaction_id=self._transaction_id(),
                operation_id="materialize-target",
            )

    def test_ref_movement_invalidates_previously_resolved_evidence(self) -> None:
        evidence = self.provider.resolve(self.request)
        self._write_distribution("new commit\n")
        self._commit("move release ref")
        with self.assertRaisesRegex(RuntimeError, "changed after target resolution"):
            self.provider.materialize(
                evidence,
                Path(evidence.copy_descriptor()["materialized_root"]),
                transaction_id=self._transaction_id(),
                operation_id="materialize-target",
            )

    def test_manifest_hash_mismatch_is_rejected(self) -> None:
        manifest_path = self.repository_root / "MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"][0]["sha256"] = "0" * 64
        write_json(manifest_path, manifest)
        self._commit("tamper package inventory")
        with self.assertRaisesRegex(RuntimeError, "hash mismatch"):
            self.provider.resolve(self.request)

    def test_manifest_cannot_authorize_a_git_symlink(self) -> None:
        payload = b"plugins/cpt-core/README.md"
        object_id = self._git("hash-object", "-w", "--stdin", input_bytes=payload)
        manifest_path = self.repository_root / "MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["files"].append(
            {
                "path": "linked-readme",
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
        manifest["file_count"] = len(manifest["files"])
        write_json(manifest_path, manifest)
        self._git("add", "MANIFEST.json")
        self._git("update-index", "--add", "--cacheinfo", f"120000,{object_id},linked-readme")
        self._git(
            "-c",
            "user.name=Product OS Test",
            "-c",
            "user.email=product-os-test.invalid",
            "commit",
            "-q",
            "-m",
            "add forbidden symlink",
        )
        with self.assertRaisesRegex(RuntimeError, "not a regular file"):
            self.provider.resolve(self.request)

    def test_request_authority_is_bounded_to_registered_repo_and_safe_ref(self) -> None:
        wrong_repository = dict(self.request)
        wrong_repository["repository"] = (self.tmp / "other").as_uri()
        with self.assertRaisesRegex(RuntimeError, "registered repository"):
            self.provider.resolve(wrong_repository)
        invalid_ref = dict(self.request)
        invalid_ref["requested_ref"] = "--upload-pack=evil"
        with self.assertRaisesRegex(RuntimeError, "ref is invalid"):
            self.provider.resolve(invalid_ref)


if __name__ == "__main__":
    unittest.main()
