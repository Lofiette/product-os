from __future__ import annotations

import copy
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
from typing import Any, Mapping, Sequence

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
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
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
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries or manifest.get("file_count") != len(entries):
        raise RuntimeError("Repository package files inventory is invalid")
    if len(entries) > MAX_FILES:
        raise RuntimeError("Repository package exceeds the file-count limit")
    records: list[dict[str, Any]] = []
    exact: set[str] = set()
    folded: dict[str, str] = {}
    total_size = 0
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RuntimeError(f"Repository package file entry {index} is invalid")
        pure, relative = _strict_relative(entry.get("path"))
        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise RuntimeError(f"Repository package file digest is invalid: {pure}")
        key = pure.as_posix()
        collision = key.casefold()
        if key in exact or collision in folded:
            raise RuntimeError(f"Repository package paths collide: {folded.get(collision, key)} and {key}")
        exact.add(key)
        folded[collision] = key
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
        actual_hash = canonical_text_file_sha256(source)
        if actual_hash != expected_hash:
            raise RuntimeError(f"Repository package file hash mismatch: {key}")
        records.append({"path": key, "relative": relative, "sha256": expected_hash, "size": size})
    actual = _walk_regular_files(root)
    allowed = exact | {"MANIFEST.json", SOURCE_MARKER}
    extras = sorted(actual - allowed)
    missing = sorted(exact - actual)
    if extras or missing:
        raise RuntimeError(f"Repository package inventory is not closed: extras={extras[:3]} missing={missing[:3]}")
    return sorted(records, key=lambda item: item["path"])


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
        descriptor = evidence.copy_descriptor()
        actual = build_repository_descriptor(
            destination,
            context=self.context,
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

    def cleanup_created(
        self,
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
        sources_root = (self.context.product_os_home / "sources").absolute()
        if not _is_within(destination, [sources_root]):
            raise RuntimeError("Provider cleanup destination escapes immutable sources")
        staging = destination.parent / f".{destination.name[:8]}.s-{transaction_id[-12:]}"
        if not staging.exists():
            return
        if not _is_within(staging, [sources_root]) or _path_is_link_like(staging):
            raise RuntimeError("Refusing to remove unsafe provider staging path")
        if not staging.is_dir():
            raise RuntimeError("Provider staging path is not a directory")
        shutil.rmtree(staging)
        # Published roots are immutable, content-addressed caches and may be shared.
        # Transaction rollback deliberately retains them for later verified reuse/GC.
