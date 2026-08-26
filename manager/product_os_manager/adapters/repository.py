from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
from typing import Any, Callable, Mapping, Sequence

from ..context import InstallationContext
from ..planning import SOURCE_MARKER, _is_link_like, _is_within
from ..state import (
    atomic_write_bytes,
    atomic_write_json,
    canonical_json_hash,
    canonical_text_file_sha256,
    read_json,
)
from .base import TargetAdapterEvidence

MAX_FILES = 20_000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
TRANSACTION_PATTERN = re.compile(
    r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


def _canonical_bytes(data: bytes) -> bytes:
    if b"\0" in data:
        return data
    return data.replace(b"\r\n", b"\n")


def _canonical_bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(_canonical_bytes(data)).hexdigest()


def _path_is_link_like(path: Path) -> bool:
    if path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)()):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise RuntimeError(f"Cannot inspect repository path safely: {path}: {exc}") from exc
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _strict_relative(value: Any) -> tuple[PurePosixPath, Path]:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or "\0" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise RuntimeError(f"Repository path is invalid: {value!r}")
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise RuntimeError(f"Repository path is not a normalized relative path: {value}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or len(value) > 240:
        raise RuntimeError(f"Repository path is unsafe or too long: {value}")
    for part in pure.parts:
        if ":" in part or part.endswith((".", " ")):
            raise RuntimeError(f"Repository path is not Windows-safe: {value}")
        if part.split(".", 1)[0].casefold() in WINDOWS_RESERVED:
            raise RuntimeError(f"Repository path uses a reserved Windows name: {value}")
    return pure, Path(*pure.parts)


def _safe_relative(value: Any) -> Path:
    return _strict_relative(value)[1]


def _safe_root(value: Path) -> Path:
    lexical = value.expanduser().absolute()
    if _path_is_link_like(lexical):
        raise RuntimeError("Repository source root is link-like")
    try:
        resolved = lexical.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(f"Repository source root is unavailable: {lexical}: {exc}") from exc
    if not resolved.is_dir() or _path_is_link_like(resolved):
        raise RuntimeError("Repository source root is missing or link-like")
    return resolved


def _manifest_specs(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries or manifest.get("file_count") != len(entries):
        raise RuntimeError("Repository package files inventory is invalid")
    if len(entries) > MAX_FILES:
        raise RuntimeError("Repository package exceeds the file-count limit")
    records: list[dict[str, Any]] = []
    exact: set[str] = set()
    folded: dict[str, str] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RuntimeError(f"Repository package file entry {index} is invalid")
        pure, relative = _strict_relative(entry.get("path"))
        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise RuntimeError(f"Repository package file digest is invalid: {pure}")
        declared_size = entry.get("size")
        if declared_size is not None and (
            not isinstance(declared_size, int)
            or isinstance(declared_size, bool)
            or declared_size < 0
            or declared_size > MAX_FILE_BYTES
        ):
            raise RuntimeError(f"Repository package file size is invalid: {pure}")
        key = pure.as_posix()
        collision = key.casefold()
        if key in exact or collision in folded:
            raise RuntimeError(f"Repository package paths collide: {folded.get(collision, key)} and {key}")
        exact.add(key)
        folded[collision] = key
        records.append(
            {
                "path": key,
                "relative": relative,
                "sha256": expected_hash,
                "declared_size": declared_size,
            }
        )
    return sorted(records, key=lambda item: item["path"])


def _walk_regular_files(root: Path) -> set[str]:
    files: set[str] = set()

    def visit(directory: Path, prefix: PurePosixPath | None = None) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name.casefold())
        except OSError as exc:
            raise RuntimeError(f"Cannot inspect repository directory: {directory}: {exc}") from exc
        for entry in entries:
            relative = PurePosixPath(entry.name) if prefix is None else prefix / entry.name
            path = Path(entry.path)
            if _path_is_link_like(path):
                raise RuntimeError(f"Repository contains a link or reparse point: {relative}")
            if prefix is None and entry.name == ".git":
                if not entry.is_dir(follow_symlinks=False):
                    raise RuntimeError("Repository .git entry is not a regular directory")
                continue
            if entry.is_dir(follow_symlinks=False):
                visit(path, relative)
            elif entry.is_file(follow_symlinks=False):
                files.add(relative.as_posix())
            else:
                raise RuntimeError(f"Repository contains an unsupported entry: {relative}")

    visit(root)
    return files


def _verified_manifest_records(root: Path, manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = _manifest_specs(manifest)
    total_size = 0
    for record in records:
        key = record["path"]
        relative = record["relative"]
        source = root / relative
        current = root
        for part in relative.parts:
            current = current / part
            if _path_is_link_like(current):
                raise RuntimeError(f"Repository package path is link-like: {key}")
        if not source.is_file():
            raise RuntimeError(f"Repository package file is missing: {key}")
        size = source.stat().st_size
        if size > MAX_FILE_BYTES:
            raise RuntimeError(f"Repository package file exceeds the size limit: {key}")
        total_size += size
        if total_size > MAX_TOTAL_BYTES:
            raise RuntimeError("Repository package exceeds the total-size limit")
        data = source.read_bytes()
        declared_size = record["declared_size"]
        if declared_size is not None and len(_canonical_bytes(data)) != declared_size:
            raise RuntimeError(f"Repository package file size mismatch: {key}")
        actual_hash = _canonical_bytes_sha256(data)
        if actual_hash != record["sha256"]:
            raise RuntimeError(f"Repository package file hash mismatch: {key}")
        record["size"] = size
    actual = _walk_regular_files(root)
    exact = {record["path"] for record in records}
    allowed = exact | {"MANIFEST.json", SOURCE_MARKER}
    extras = sorted(actual - allowed)
    missing = sorted(exact - actual)
    if extras or missing:
        raise RuntimeError(f"Repository package inventory is not closed: extras={extras[:3]} missing={missing[:3]}")
    return records


def build_repository_descriptor(
    source_root: Path,
    *,
    context: InstallationContext,
    provider: str,
    repository: str,
    requested_ref: str,
    resolved_commit: str,
    marketplace_identity: str,
    plugin_names: Sequence[str],
    method: str,
) -> dict[str, Any]:
    source_root = _safe_root(source_root)
    package_path = source_root / "MANIFEST.json"
    marketplace_path = source_root / ".agents" / "plugins" / "marketplace.json"
    package = read_json(package_path)
    marketplace = read_json(marketplace_path)
    if not isinstance(package, dict) or package.get("name") != "codex-product-os":
        raise RuntimeError("Repository package manifest identity is invalid")
    _verified_manifest_records(source_root, package)
    if not isinstance(marketplace, dict) or marketplace.get("name") != marketplace_identity:
        raise RuntimeError("Repository marketplace identity does not match requested identity")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        raise RuntimeError("Repository marketplace plugins inventory is invalid")
    by_name: dict[str, dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise RuntimeError("Repository marketplace plugin entry is invalid")
        if item["name"] in by_name:
            raise RuntimeError(f"Repository marketplace contains a duplicate plugin: {item['name']}")
        by_name[item["name"]] = item
    requested_plugins = sorted(set(plugin_names))
    if not requested_plugins or len(requested_plugins) != len(list(plugin_names)):
        raise RuntimeError("Target plugin selection must be non-empty and unique")
    plugins: list[dict[str, Any]] = []
    for name in requested_plugins:
        entry = by_name.get(name)
        if not entry:
            raise RuntimeError(f"Target plugin is absent from repository marketplace: {name}")
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            raise RuntimeError(f"Target plugin source is not a local repository path: {name}")
        relative = _safe_relative(source.get("path"))
        payload = (source_root / relative).resolve()
        if not _is_within(payload, source_root) or _is_link_like(payload):
            raise RuntimeError(f"Target plugin payload path is unsafe: {name}")
        manifest_path = payload / ".codex-plugin" / "plugin.json"
        manifest = read_json(manifest_path)
        if not isinstance(manifest, dict) or manifest.get("name") != name:
            raise RuntimeError(f"Target plugin manifest identity is invalid: {name}")
        if manifest.get("version") != package.get("version"):
            raise RuntimeError(f"Target plugin version does not match package version: {name}")
        plugins.append({
            "name": name,
            "selector": f"{name}@{marketplace_identity}",
            "relative_path": relative.as_posix(),
            "manifest_sha256": canonical_text_file_sha256(manifest_path),
        })
    plugins.sort(key=lambda item: (item["name"], item["selector"]))
    package_sha = canonical_text_file_sha256(package_path)
    descriptor: dict[str, Any] = {
        "provider": provider,
        "repository": repository,
        "marketplace_identity": marketplace_identity,
        "requested_ref": requested_ref,
        "resolved_commit": resolved_commit,
        "product_version": package.get("version"),
        "package_manifest_sha256": package_sha,
        "resolution_evidence": {
            "verified": True,
            "method": method,
            "provider": provider,
            "repository": repository,
            "requested_ref": requested_ref,
            "resolved_commit": resolved_commit,
            "product_version": package.get("version"),
            "package_manifest_sha256": package_sha,
            "plugins_sha256": canonical_json_hash(plugins),
        },
        "materialized_root": str(
            context.product_os_home / "sources" / marketplace_identity / resolved_commit
        ),
        "plugins": plugins,
    }
    return descriptor


def source_marker(descriptor: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema": "product-os-materialized-source-v1",
        "provider": descriptor.get("provider"),
        "repository": descriptor.get("repository"),
        "marketplace_identity": descriptor.get("marketplace_identity"),
        "requested_ref": descriptor.get("requested_ref"),
        "resolved_commit": descriptor.get("resolved_commit"),
        "product_version": descriptor.get("product_version"),
        "package_manifest_sha256": descriptor.get("package_manifest_sha256"),
    }


def _verify_materialized_root(
    destination: Path,
    evidence: TargetAdapterEvidence,
    context: InstallationContext,
) -> None:
    descriptor = evidence.copy_descriptor()
    actual = build_repository_descriptor(
        destination,
        context=context,
        provider=str(descriptor["provider"]),
        repository=str(descriptor["repository"]),
        requested_ref=str(descriptor["requested_ref"]),
        resolved_commit=str(descriptor["resolved_commit"]),
        marketplace_identity=str(descriptor["marketplace_identity"]),
        plugin_names=[str(item["name"]) for item in descriptor["plugins"]],
        method=str(descriptor["resolution_evidence"]["method"]),
    )
    marker = read_json(destination / SOURCE_MARKER)
    if marker != source_marker(actual):
        raise RuntimeError("Existing target source marker does not match resolved evidence")
    if canonical_json_hash(actual) != canonical_json_hash(descriptor):
        raise RuntimeError("Existing target does not match resolved evidence")


def _cleanup_provider_staging(
    context: InstallationContext,
    destination: Path,
    *,
    transaction_id: str,
    operation_id: str,
) -> None:
    if not TRANSACTION_PATTERN.fullmatch(transaction_id):
        raise RuntimeError("Transaction id is invalid")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", operation_id):
        raise RuntimeError("Target cleanup operation id is invalid")
    destination = destination.absolute()
    sources_root = (context.product_os_home / "sources").absolute()
    if not _is_within(destination, sources_root):
        raise RuntimeError("Provider cleanup destination escapes immutable sources")
    staging = destination.parent / f".{destination.name[:8]}.s-{transaction_id[-12:]}"
    if not staging.exists():
        return
    if not _is_within(staging, sources_root) or _path_is_link_like(staging):
        raise RuntimeError("Refusing to remove unsafe provider staging path")
    if not staging.is_dir():
        raise RuntimeError("Provider staging path is not a directory")
    shutil.rmtree(staging)
    # Published roots are immutable, content-addressed caches and may be shared.
    # Transaction rollback deliberately retains them for later verified reuse/GC.


class DirectoryTargetProvider:
    """Deterministic local-directory provider for tests and offline harnesses."""

    adapter_id = "deterministic-directory"
    adapter_version = "1"
    capability_fingerprint = "manifest-copy-immutable-target-v1"

    def __init__(
        self,
        source_root: Path,
        context: InstallationContext,
        *,
        resolved_commit: str,
        requested_ref: str = "fixture-v4.1.0",
        repository: str | None = None,
        faults: set[str] | None = None,
    ) -> None:
        self.source_root = _safe_root(source_root)
        self.context = context
        self.resolved_commit = resolved_commit
        self.requested_ref = requested_ref
        self.repository = repository or self.source_root.as_uri()
        self.faults = set(faults or set())

    def _fail(self, operation: str) -> None:
        if operation in self.faults:
            raise RuntimeError(f"Injected deterministic provider failure: {operation}")

    def resolve(self, request: Mapping[str, Any]) -> TargetAdapterEvidence:
        allowed = {"repository", "requested_ref", "marketplace_identity", "plugins"}
        if set(request) != allowed:
            raise RuntimeError("Directory target request fields are invalid")
        if request.get("repository") != self.repository or request.get("requested_ref") != self.requested_ref:
            raise RuntimeError("Directory target request does not match registered immutable source")
        plugins = request.get("plugins")
        if not isinstance(plugins, list) or not all(isinstance(item, str) for item in plugins):
            raise RuntimeError("Directory target request plugins are invalid")
        descriptor = build_repository_descriptor(
            self.source_root,
            context=self.context,
            provider="filesystem",
            repository=self.repository,
            requested_ref=self.requested_ref,
            resolved_commit=self.resolved_commit,
            marketplace_identity=str(request.get("marketplace_identity")),
            plugin_names=plugins,
            method="deterministic-directory-v1",
        )
        return TargetAdapterEvidence(
            self.adapter_id,
            descriptor,
            self.adapter_version,
            self.capability_fingerprint,
        )

    @staticmethod
    def _request(evidence: TargetAdapterEvidence) -> dict[str, Any]:
        descriptor = evidence.copy_descriptor()
        return {
            "repository": descriptor.get("repository"),
            "requested_ref": descriptor.get("requested_ref"),
            "marketplace_identity": descriptor.get("marketplace_identity"),
            "plugins": [item.get("name") for item in descriptor.get("plugins", [])],
        }

    def materialize(
        self,
        evidence: TargetAdapterEvidence,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> TargetAdapterEvidence:
        if not TRANSACTION_PATTERN.fullmatch(transaction_id):
            raise RuntimeError("Transaction id is invalid")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", operation_id):
            raise RuntimeError("Target operation id is invalid")
        if evidence.adapter_id != self.adapter_id:
            raise RuntimeError("Target evidence adapter does not match directory provider")
        if (
            evidence.adapter_version != self.adapter_version
            or evidence.capability_fingerprint != self.capability_fingerprint
        ):
            raise RuntimeError("Target evidence adapter binding changed")
        fresh = self.resolve(self._request(evidence))
        if canonical_json_hash(fresh.copy_descriptor()) != canonical_json_hash(evidence.copy_descriptor()):
            raise RuntimeError("Directory source changed after target resolution")
        expected = Path(fresh.copy_descriptor()["materialized_root"]).absolute()
        destination = destination.absolute()
        if str(destination).casefold() != str(expected).casefold():
            raise RuntimeError("Provider destination is not the manager-derived immutable target root")
        resolved_parent = destination.parent.resolve()
        if (
            resolved_parent == self.source_root
            or resolved_parent in self.source_root.parents
            or self.source_root in resolved_parent.parents
        ):
            raise RuntimeError("Repository source and target roots overlap")
        if destination.exists():
            self._verify_materialized(destination, fresh)
            return fresh
        self._fail("before_copy")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if _path_is_link_like(destination.parent):
            raise RuntimeError("Provider target parent is link-like")
        # Keep the sibling staging name short enough for legacy Windows MAX_PATH
        # environments while the full transaction id remains bound in the journal.
        staging = destination.parent / f".{destination.name[:8]}.s-{transaction_id[-12:]}"
        if staging.exists():
            raise RuntimeError(f"Provider staging path already exists: {staging}")
        try:
            staging.mkdir()
            package = read_json(self.source_root / "MANIFEST.json")
            if not isinstance(package, dict):
                raise RuntimeError("Repository package manifest is invalid")
            records = _verified_manifest_records(self.source_root, package)
            package_bytes = (self.source_root / "MANIFEST.json").read_bytes()
            atomic_write_bytes(staging / "MANIFEST.json", package_bytes)
            if canonical_text_file_sha256(staging / "MANIFEST.json") != fresh.copy_descriptor()["package_manifest_sha256"]:
                raise RuntimeError("Copied package manifest does not match resolved evidence")
            for record in records:
                source = self.source_root / record["relative"]
                if _path_is_link_like(source) or not source.is_file():
                    raise RuntimeError(f"Repository source changed during copy: {record['path']}")
                data = source.read_bytes()
                if len(data) != record["size"]:
                    raise RuntimeError(f"Repository source size changed during copy: {record['path']}")
                destination_file = staging / record["relative"]
                atomic_write_bytes(destination_file, data)
                if canonical_text_file_sha256(destination_file) != record["sha256"]:
                    raise RuntimeError(f"Copied repository file failed verification: {record['path']}")
            self._fail("after_copy")
            staged = build_repository_descriptor(
                staging,
                context=self.context,
                provider="filesystem",
                repository=self.repository,
                requested_ref=self.requested_ref,
                resolved_commit=self.resolved_commit,
                marketplace_identity=str(self._request(evidence)["marketplace_identity"]),
                plugin_names=list(self._request(evidence)["plugins"]),
                method="deterministic-directory-v1",
            )
            if canonical_json_hash(staged) != canonical_json_hash(fresh.copy_descriptor()):
                raise RuntimeError("Staged target differs from resolved evidence")
            atomic_write_json(staging / SOURCE_MARKER, source_marker(staged))
            self._fail("before_publish")
            try:
                os.rename(staging, destination)
            except FileExistsError:
                self._verify_materialized(destination, fresh)
        finally:
            if staging.exists():
                if _path_is_link_like(staging):
                    raise RuntimeError(f"Refusing to remove link-like provider staging path: {staging}")
                shutil.rmtree(staging)
        self._fail("after_publish")
        self._verify_materialized(destination, fresh)
        return fresh

    def _verify_materialized(
        self,
        destination: Path,
        evidence: TargetAdapterEvidence,
    ) -> None:
        _verify_materialized_root(destination, evidence, self.context)

    def cleanup_created(
        self,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> None:
        _cleanup_provider_staging(
            self.context,
            destination,
            transaction_id=transaction_id,
            operation_id=operation_id,
        )


class LocalGitTargetProvider:
    """Read and materialize an immutable commit from a user-selected local Git repo.

    The adapter never fetches, checks out, or executes repository hooks. All
    payload bytes come directly from the resolved commit's object database and
    are accepted only when covered by the package MANIFEST.json.
    """

    adapter_id = "local-git"
    adapter_version = "1"
    capability_fingerprint = "local-git-object-db-manifest-materialize-v1"
    method = "local-git-object-database-v1"

    def __init__(
        self,
        repository_root: Path,
        context: InstallationContext,
        *,
        git_executable: str = "git",
    ) -> None:
        self.source_root = _safe_root(repository_root)
        self.context = context
        dot_git = self.source_root / ".git"
        if not dot_git.is_dir() or _path_is_link_like(dot_git):
            raise RuntimeError("Local Git provider requires a non-linked, non-bare repository")
        executable = shutil.which(git_executable)
        if executable is None:
            candidate = Path(git_executable)
            if not candidate.is_file():
                raise RuntimeError(f"Git executable is unavailable: {git_executable}")
            executable = str(candidate.resolve())
        self.git_executable = executable
        top = self._git_text("rev-parse", "--show-toplevel")
        if str(Path(top).resolve()).casefold() != str(self.source_root).casefold():
            raise RuntimeError("Local Git provider root must be the repository top level")
        if self._git_text("rev-parse", "--is-inside-work-tree") != "true":
            raise RuntimeError("Local Git provider source is not a working-tree repository")
        self.repository = self.source_root.as_uri()

    def _git_environment(self) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_TERMINAL_PROMPT": "0",
                "GCM_INTERACTIVE": "Never",
                "LC_ALL": "C",
            }
        )
        return environment

    def _git(self, *arguments: str, input_bytes: bytes | None = None) -> bytes:
        try:
            completed = subprocess.run(
                [self.git_executable, "-C", str(self.source_root), *arguments],
                input=input_bytes,
                capture_output=True,
                check=False,
                env=self._git_environment(),
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"Local Git command failed safely: {arguments[0]}: {exc}") from exc
        if completed.returncode:
            detail = completed.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"Local Git command failed: {arguments[0]}: {detail}")
        return completed.stdout

    def _git_text(self, *arguments: str) -> str:
        try:
            return self._git(*arguments).decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"Local Git output is not UTF-8: {arguments[0]}") from exc

    @staticmethod
    def _validated_ref(value: Any) -> str:
        if (
            not isinstance(value, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,255}", value)
            or ".." in value
            or "//" in value
            or "@{" in value
            or value.endswith(("/", ".lock"))
        ):
            raise RuntimeError("Requested local Git ref is invalid")
        return value

    def _resolve_commit(self, requested_ref: str) -> str:
        resolved = self._git_text(
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{requested_ref}^{{commit}}",
        )
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", resolved):
            raise RuntimeError("Local Git ref did not resolve to a canonical commit id")
        if self._git_text("cat-file", "-t", resolved) != "commit":
            raise RuntimeError("Local Git ref does not resolve to a commit")
        return resolved

    def _tree(self, resolved_commit: str) -> dict[str, dict[str, Any]]:
        output = self._git(
            "ls-tree",
            "-r",
            "-z",
            "-l",
            "--full-tree",
            resolved_commit,
        )
        result: dict[str, dict[str, Any]] = {}
        folded: dict[str, str] = {}
        for raw in output.split(b"\0"):
            if not raw:
                continue
            try:
                metadata, encoded_path = raw.split(b"\t", 1)
                mode, object_type, object_id, size_text = metadata.decode("ascii").split()
                path = encoded_path.decode("utf-8")
            except (ValueError, UnicodeDecodeError) as exc:
                raise RuntimeError("Local Git tree contains an unsupported entry") from exc
            pure, _ = _strict_relative(path)
            key = pure.as_posix()
            collision = key.casefold()
            if key in result or collision in folded:
                raise RuntimeError(
                    f"Local Git tree paths collide: {folded.get(collision, key)} and {key}"
                )
            folded[collision] = key
            size = None if size_text == "-" else int(size_text)
            result[key] = {
                "path": key,
                "mode": mode,
                "type": object_type,
                "oid": object_id,
                "size": size,
            }
        return result

    def _blob(self, object_id: str) -> bytes:
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id):
            raise RuntimeError("Local Git object id is invalid")
        data = self._git("cat-file", "blob", object_id)
        if len(data) > MAX_FILE_BYTES:
            raise RuntimeError("Local Git blob exceeds the per-file size limit")
        return data

    @staticmethod
    def _read_exact(handle: Any, size: int) -> bytes:
        chunks: list[bytes] = []
        remaining = size
        while remaining:
            chunk = handle.read(remaining)
            if not chunk:
                raise RuntimeError("Local Git batch output ended unexpectedly")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def _consume_blobs(
        self,
        records: Sequence[Mapping[str, Any]],
        consumer: Callable[[Mapping[str, Any], bytes], None],
    ) -> None:
        process = subprocess.Popen(
            [self.git_executable, "-C", str(self.source_root), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self._git_environment(),
        )
        try:
            if process.stdin is None or process.stdout is None:
                raise RuntimeError("Local Git batch pipes are unavailable")
            for record in records:
                object_id = str(record["oid"])
                process.stdin.write(object_id.encode("ascii") + b"\n")
                process.stdin.flush()
                header = process.stdout.readline()
                try:
                    actual_id, object_type, size_text = header.decode("ascii").strip().split()
                    size = int(size_text)
                except (UnicodeDecodeError, ValueError) as exc:
                    raise RuntimeError("Local Git batch returned an invalid object header") from exc
                if actual_id != object_id or object_type != "blob" or size != record["size"]:
                    raise RuntimeError(f"Local Git object changed during read: {record['path']}")
                data = self._read_exact(process.stdout, size)
                if process.stdout.read(1) != b"\n":
                    raise RuntimeError("Local Git batch returned an invalid object boundary")
                consumer(record, data)
            process.stdin.close()
            stderr = process.stderr.read() if process.stderr is not None else b""
            return_code = process.wait(timeout=120)
            if return_code:
                raise RuntimeError(
                    "Local Git batch failed: "
                    + stderr.decode("utf-8", errors="replace").strip()
                )
        except Exception:
            process.kill()
            process.wait()
            raise
        finally:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None and not stream.closed:
                    stream.close()

    @staticmethod
    def _json_object(data: bytes, label: str) -> dict[str, Any]:
        try:
            value = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Local Git {label} is not valid UTF-8 JSON") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"Local Git {label} must be a JSON object")
        return value

    def _verified_snapshot(
        self,
        resolved_commit: str,
    ) -> tuple[dict[str, Any], bytes, list[dict[str, Any]], dict[str, bytes]]:
        tree = self._tree(resolved_commit)
        manifest_node = tree.get("MANIFEST.json")
        if not manifest_node or manifest_node["type"] != "blob" or manifest_node["mode"] not in {"100644", "100755"}:
            raise RuntimeError("Local Git commit lacks a regular MANIFEST.json")
        manifest_bytes = self._blob(str(manifest_node["oid"]))
        package = self._json_object(manifest_bytes, "package manifest")
        specs = _manifest_specs(package)
        records: list[dict[str, Any]] = []
        total_size = 0
        for spec in specs:
            node = tree.get(spec["path"])
            if not node:
                raise RuntimeError(f"Local Git package file is missing: {spec['path']}")
            if node["type"] != "blob" or node["mode"] not in {"100644", "100755"}:
                raise RuntimeError(f"Local Git package entry is not a regular file: {spec['path']}")
            size = node["size"]
            if not isinstance(size, int) or size < 0 or size > MAX_FILE_BYTES:
                raise RuntimeError(f"Local Git package file exceeds the size limit: {spec['path']}")
            total_size += size
            if total_size > MAX_TOTAL_BYTES:
                raise RuntimeError("Local Git package exceeds the total-size limit")
            records.append({**spec, **node})

        captured: dict[str, bytes] = {}

        def verify(record: Mapping[str, Any], data: bytes) -> None:
            canonical = _canonical_bytes(data)
            if record.get("declared_size") is not None and len(canonical) != record["declared_size"]:
                raise RuntimeError(f"Local Git package file size mismatch: {record['path']}")
            if hashlib.sha256(canonical).hexdigest() != record["sha256"]:
                raise RuntimeError(f"Local Git package file hash mismatch: {record['path']}")
            path = str(record["path"])
            if path == ".agents/plugins/marketplace.json" or path.endswith("/.codex-plugin/plugin.json"):
                captured[path] = data

        self._consume_blobs(records, verify)
        return package, manifest_bytes, records, captured

    def resolve(self, request: Mapping[str, Any]) -> TargetAdapterEvidence:
        allowed = {"repository", "requested_ref", "marketplace_identity", "plugins"}
        if set(request) != allowed:
            raise RuntimeError("Local Git target request fields are invalid")
        if request.get("repository") != self.repository:
            raise RuntimeError("Local Git target request does not match the registered repository")
        requested_ref = self._validated_ref(request.get("requested_ref"))
        marketplace_identity = request.get("marketplace_identity")
        if not isinstance(marketplace_identity, str):
            raise RuntimeError("Local Git marketplace identity is invalid")
        plugins_value = request.get("plugins")
        if not isinstance(plugins_value, list) or not all(isinstance(item, str) for item in plugins_value):
            raise RuntimeError("Local Git target request plugins are invalid")
        requested_plugins = sorted(set(plugins_value))
        if not requested_plugins or len(requested_plugins) != len(plugins_value):
            raise RuntimeError("Target plugin selection must be non-empty and unique")

        resolved_commit = self._resolve_commit(requested_ref)
        package, manifest_bytes, _records, captured = self._verified_snapshot(resolved_commit)
        if package.get("name") != "codex-product-os":
            raise RuntimeError("Local Git package manifest identity is invalid")
        marketplace_bytes = captured.get(".agents/plugins/marketplace.json")
        if marketplace_bytes is None:
            raise RuntimeError("Local Git package does not inventory its marketplace manifest")
        marketplace = self._json_object(marketplace_bytes, "marketplace manifest")
        if marketplace.get("name") != marketplace_identity:
            raise RuntimeError("Local Git marketplace identity does not match requested identity")
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            raise RuntimeError("Local Git marketplace plugins inventory is invalid")
        by_name: dict[str, dict[str, Any]] = {}
        for item in entries:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                raise RuntimeError("Local Git marketplace plugin entry is invalid")
            if item["name"] in by_name:
                raise RuntimeError(f"Local Git marketplace contains a duplicate plugin: {item['name']}")
            by_name[item["name"]] = item

        plugins: list[dict[str, Any]] = []
        for name in requested_plugins:
            entry = by_name.get(name)
            if not entry:
                raise RuntimeError(f"Target plugin is absent from local Git marketplace: {name}")
            source = entry.get("source")
            if not isinstance(source, dict) or source.get("source") != "local":
                raise RuntimeError(f"Target plugin source is not a local repository path: {name}")
            relative = _safe_relative(source.get("path"))
            manifest_key = (PurePosixPath(relative.as_posix()) / ".codex-plugin" / "plugin.json").as_posix()
            manifest_bytes_for_plugin = captured.get(manifest_key)
            if manifest_bytes_for_plugin is None:
                raise RuntimeError(f"Target plugin manifest is not package-inventoried: {name}")
            manifest = self._json_object(manifest_bytes_for_plugin, f"plugin manifest {name}")
            if manifest.get("name") != name:
                raise RuntimeError(f"Target plugin manifest identity is invalid: {name}")
            if manifest.get("version") != package.get("version"):
                raise RuntimeError(f"Target plugin version does not match package version: {name}")
            plugins.append(
                {
                    "name": name,
                    "selector": f"{name}@{marketplace_identity}",
                    "relative_path": relative.as_posix(),
                    "manifest_sha256": _canonical_bytes_sha256(manifest_bytes_for_plugin),
                }
            )
        plugins.sort(key=lambda item: (item["name"], item["selector"]))
        package_sha = _canonical_bytes_sha256(manifest_bytes)
        descriptor = {
            "provider": "git",
            "repository": self.repository,
            "marketplace_identity": marketplace_identity,
            "requested_ref": requested_ref,
            "resolved_commit": resolved_commit,
            "product_version": package.get("version"),
            "package_manifest_sha256": package_sha,
            "resolution_evidence": {
                "verified": True,
                "method": self.method,
                "provider": "git",
                "repository": self.repository,
                "requested_ref": requested_ref,
                "resolved_commit": resolved_commit,
                "product_version": package.get("version"),
                "package_manifest_sha256": package_sha,
                "plugins_sha256": canonical_json_hash(plugins),
            },
            "materialized_root": str(
                self.context.product_os_home
                / "sources"
                / marketplace_identity
                / resolved_commit
            ),
            "plugins": plugins,
        }
        return TargetAdapterEvidence(
            self.adapter_id,
            descriptor,
            self.adapter_version,
            self.capability_fingerprint,
        )

    @staticmethod
    def _request(evidence: TargetAdapterEvidence) -> dict[str, Any]:
        descriptor = evidence.copy_descriptor()
        return {
            "repository": descriptor.get("repository"),
            "requested_ref": descriptor.get("requested_ref"),
            "marketplace_identity": descriptor.get("marketplace_identity"),
            "plugins": [item.get("name") for item in descriptor.get("plugins", [])],
        }

    def materialize(
        self,
        evidence: TargetAdapterEvidence,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> TargetAdapterEvidence:
        if not TRANSACTION_PATTERN.fullmatch(transaction_id):
            raise RuntimeError("Transaction id is invalid")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", operation_id):
            raise RuntimeError("Target operation id is invalid")
        if evidence.adapter_id != self.adapter_id:
            raise RuntimeError("Target evidence adapter does not match local Git provider")
        if (
            evidence.adapter_version != self.adapter_version
            or evidence.capability_fingerprint != self.capability_fingerprint
        ):
            raise RuntimeError("Target evidence adapter binding changed")
        fresh = self.resolve(self._request(evidence))
        if canonical_json_hash(fresh.copy_descriptor()) != canonical_json_hash(evidence.copy_descriptor()):
            raise RuntimeError("Local Git ref or commit evidence changed after target resolution")
        descriptor = fresh.copy_descriptor()
        expected = Path(descriptor["materialized_root"]).absolute()
        destination = destination.absolute()
        if str(destination).casefold() != str(expected).casefold():
            raise RuntimeError("Provider destination is not the manager-derived immutable target root")
        sources_root = (self.context.product_os_home / "sources").absolute()
        if not _is_within(destination, sources_root):
            raise RuntimeError("Provider destination escapes immutable sources")
        if _path_is_link_like(destination):
            raise RuntimeError("Provider destination is link-like")
        resolved_parent = destination.parent.resolve()
        if (
            resolved_parent == self.source_root
            or resolved_parent in self.source_root.parents
            or self.source_root in resolved_parent.parents
        ):
            raise RuntimeError("Local Git source and target roots overlap")
        if destination.exists():
            if not destination.is_dir():
                raise RuntimeError("Existing immutable target is not a directory")
            _verify_materialized_root(destination, fresh, self.context)
            return fresh

        destination.parent.mkdir(parents=True, exist_ok=True)
        if _path_is_link_like(destination.parent):
            raise RuntimeError("Provider target parent is link-like")
        staging = destination.parent / f".{destination.name[:8]}.s-{transaction_id[-12:]}"
        if staging.exists() or _path_is_link_like(staging):
            raise RuntimeError(f"Provider staging path already exists or is link-like: {staging}")
        try:
            staging.mkdir()
            package, manifest_bytes, records, _captured = self._verified_snapshot(
                str(descriptor["resolved_commit"])
            )
            if _canonical_bytes_sha256(manifest_bytes) != descriptor["package_manifest_sha256"]:
                raise RuntimeError("Local Git package manifest changed during materialization")
            atomic_write_bytes(staging / "MANIFEST.json", manifest_bytes)

            def copy_blob(record: Mapping[str, Any], data: bytes) -> None:
                if _canonical_bytes_sha256(data) != record["sha256"]:
                    raise RuntimeError(f"Local Git blob failed copy verification: {record['path']}")
                destination_file = staging / Path(str(record["relative"]))
                atomic_write_bytes(destination_file, data)
                if record["mode"] == "100755" and os.name != "nt":
                    destination_file.chmod(destination_file.stat().st_mode | stat.S_IXUSR)
                if canonical_text_file_sha256(destination_file) != record["sha256"]:
                    raise RuntimeError(f"Copied local Git file failed verification: {record['path']}")

            self._consume_blobs(records, copy_blob)
            staged = build_repository_descriptor(
                staging,
                context=self.context,
                provider="git",
                repository=self.repository,
                requested_ref=str(descriptor["requested_ref"]),
                resolved_commit=str(descriptor["resolved_commit"]),
                marketplace_identity=str(descriptor["marketplace_identity"]),
                plugin_names=[str(item["name"]) for item in descriptor["plugins"]],
                method=self.method,
            )
            if package.get("version") != staged.get("product_version"):
                raise RuntimeError("Materialized local Git package version changed")
            if canonical_json_hash(staged) != canonical_json_hash(descriptor):
                raise RuntimeError("Staged local Git target differs from resolved evidence")
            atomic_write_json(staging / SOURCE_MARKER, source_marker(staged))
            try:
                os.rename(staging, destination)
            except FileExistsError:
                _verify_materialized_root(destination, fresh, self.context)
        finally:
            if staging.exists():
                if _path_is_link_like(staging):
                    raise RuntimeError(f"Refusing to remove link-like provider staging path: {staging}")
                shutil.rmtree(staging)
        _verify_materialized_root(destination, fresh, self.context)
        return fresh

    def cleanup_created(
        self,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> None:
        _cleanup_provider_staging(
            self.context,
            destination,
            transaction_id=transaction_id,
            operation_id=operation_id,
        )
