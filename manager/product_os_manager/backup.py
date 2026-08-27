from __future__ import annotations

import copy
import os
import shutil
import stat
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from tools import cpt_dist

from .adapters.base import SelectorAdapterEvidence
from .context import InstallationContext
from .state import (
    atomic_write_bytes,
    atomic_write_json,
    canonical_json_hash,
    file_sha256,
    read_json,
    utc_now,
)

BACKUP_SCHEMA = "product-os-backup-manifest-v1"


def backup_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "backup-manifest-v1.schema.json"


def _hashable_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(manifest))
    value.pop("manifest_hash", None)
    return value


def validate_backup_manifest(manifest: dict[str, Any]) -> None:
    schema = read_json(backup_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Invalid Product OS backup manifest: {details}")
    if manifest.get("manifest_hash") != canonical_json_hash(_hashable_manifest(manifest)):
        raise RuntimeError("Invalid Product OS backup manifest: manifest_hash does not match content")
    path_keys: set[str] = set()
    for entry in manifest.get("entries", []):
        path_key = entry.get("path_key")
        if path_key in path_keys:
            raise RuntimeError("Invalid Product OS backup manifest: duplicate physical resource")
        path_keys.add(path_key)
        kind = entry.get("kind")
        existed = entry.get("existed")
        has_file_data = (
            entry.get("backup_file") is not None
            and entry.get("sha256") is not None
            and entry.get("size") is not None
        )
        if kind == "file" and (existed is not True or not has_file_data):
            raise RuntimeError("Invalid Product OS backup manifest: file entry is incomplete")
        if kind == "directory_marker" and (
            existed is not True
            or entry.get("backup_file") is not None
            or entry.get("sha256") is not None
            or entry.get("size") is not None
        ):
            raise RuntimeError("Invalid Product OS backup manifest: directory marker is inconsistent")
        if kind == "absent" and (
            existed is not False
            or entry.get("backup_file") is not None
            or entry.get("sha256") is not None
            or entry.get("size") is not None
        ):
            raise RuntimeError("Invalid Product OS backup manifest: absent entry carries data")


def _path_key(path: Path) -> str:
    value = str(path.absolute())
    return value.casefold() if os.name == "nt" else value


def _is_within(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    resolved_root = root.resolve()
    return resolved == resolved_root or resolved_root in resolved.parents


def _is_link_like(path: Path) -> bool:
    if path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)()):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise RuntimeError(f"Cannot inspect backup resource safely: {path}: {exc}") from exc
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _assert_safe_ancestry(path: Path, root: Path) -> None:
    path = path.expanduser().absolute()
    root = root.expanduser().absolute()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"Backup resource escapes approved root: {path}")
    current = root
    if _is_link_like(current):
        raise RuntimeError(f"Approved root is link-like: {current}")
    for part in relative.parts:
        current = current / part
        if _is_link_like(current):
            raise RuntimeError(f"Backup resource ancestry is link-like: {current}")
    if not _is_within(path, root):
        raise RuntimeError(f"Backup resource resolves outside approved root: {path}")


def assert_safe_ancestry(path: Path, root: Path) -> None:
    """Validate every existing component without following a link-like escape."""

    _assert_safe_ancestry(path, root)


def resource_paths(
    context: InstallationContext,
    receipt: Mapping[str, Any],
) -> tuple[dict[str, tuple[Path, str]], dict[str, Path]]:
    files: dict[str, tuple[Path, str]] = {
        "project:receipt": (context.project / ".cpt" / "install.json", "project"),
        "project:agents": (context.project / "AGENTS.md", "project"),
        "registry": (context.registry_path, "registry"),
        "marketplace:user": (context.marketplace_registry, "marketplace"),
        "marketplace:repo": (
            context.project / ".agents" / "plugins" / "marketplace.json",
            "marketplace",
        ),
    }
    managed = receipt.get("managed_files")
    if isinstance(managed, dict):
        for raw in managed:
            relative = Path(raw)
            if relative.is_absolute() or ".." in relative.parts:
                raise RuntimeError(f"Managed receipt path is unsafe: {raw}")
            files[f"project:{relative.as_posix()}"] = (context.project / relative, "project")
    for raw, _mutable in cpt_dist.core_scaffold_files():
        relative = Path(raw)
        files[f"project:{relative.as_posix()}"] = (context.project / relative, "project")
    rules = receipt.get("rules")
    if isinstance(rules, dict) and isinstance(rules.get("path"), str):
        relative = Path(rules["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Rules receipt path is unsafe: {relative}")
        files[f"project:{relative.as_posix()}"] = (context.project / relative, "project")
    directories = {
        "project:.cpt/orchestrations/contracts": context.project / ".cpt" / "orchestrations" / "contracts",
        "project:.cpt/orchestrations/results": context.project / ".cpt" / "orchestrations" / "results",
        "project:.cpt/worktrees": context.project / ".cpt" / "worktrees",
    }
    deduplicated: dict[str, tuple[Path, str]] = {}
    physical: dict[str, tuple[str, str]] = {}
    for key, (path, scope) in sorted(files.items()):
        path_key = _path_key(path)
        if path_key in physical:
            previous_key, previous_scope = physical[path_key]
            if previous_scope != scope:
                raise RuntimeError(
                    f"Backup resource aliases cross scopes: {previous_key} and {key}"
                )
            continue
        physical[path_key] = (key, scope)
        deduplicated[key] = (path, scope)
    return deduplicated, dict(sorted(directories.items()))


def _validate_resource_path(
    context: InstallationContext,
    key: str,
    path: Path,
    scope: str,
) -> None:
    path = path.absolute()
    if scope == "project":
        _assert_safe_ancestry(path, context.project)
    elif scope == "registry":
        if _path_key(path) != _path_key(context.registry_path):
            raise RuntimeError(f"Registry backup path is not canonical: {path}")
        _assert_safe_ancestry(path, context.product_os_home)
    elif scope == "marketplace":
        approved = {
            _path_key(context.marketplace_registry),
            _path_key(context.project / ".agents" / "plugins" / "marketplace.json"),
        }
        if _path_key(path) not in approved:
            raise RuntimeError(f"Marketplace backup path is not canonical: {path}")
        root = context.project if _is_within(path, context.project) else context.marketplace_registry.parent
        _assert_safe_ancestry(path, root)
    else:
        raise RuntimeError(f"Unsupported backup scope for {key}: {scope}")


def snapshot_resources(
    context: InstallationContext,
    files: Mapping[str, tuple[Path, str]],
    directories: Mapping[str, Path],
) -> dict[str, Any]:
    snapshot: dict[str, Any] = {"files": {}, "directories": {}}
    path_keys: set[str] = set()
    for key, (path, scope) in sorted(files.items()):
        path = path.absolute()
        _validate_resource_path(context, key, path, scope)
        if path.exists() and not path.is_file():
            raise RuntimeError(f"Expected a file or absent resource: {path}")
        path_key = _path_key(path)
        if path_key in path_keys:
            raise RuntimeError(f"Backup resource path is duplicated: {path}")
        path_keys.add(path_key)
        snapshot["files"][key] = {
            "path_key": path_key,
            "exists": path.is_file(),
            "sha256": file_sha256(path),
            "size": path.stat().st_size if path.is_file() else None,
        }
    for key, path in sorted(directories.items()):
        path = path.absolute()
        _assert_safe_ancestry(path, context.project)
        if path.exists() and not path.is_dir():
            raise RuntimeError(f"Expected a directory or absent resource: {path}")
        path_key = _path_key(path)
        if path_key in path_keys:
            raise RuntimeError(f"Backup directory path is duplicated: {path}")
        path_keys.add(path_key)
        snapshot["directories"][key] = {
            "path_key": path_key,
            "exists": path.is_dir(),
        }
    return snapshot


def create_backup(
    context: InstallationContext,
    *,
    transaction_id: str,
    plan_hash: str,
    installation_id: str,
    files: Mapping[str, tuple[Path, str]],
    directories: Mapping[str, Path],
    selector_snapshot: SelectorAdapterEvidence,
) -> dict[str, Any]:
    backup_root = (
        context.product_os_home / "backups" / installation_id / transaction_id
    ).absolute()
    _assert_safe_ancestry(backup_root, context.product_os_home)
    if backup_root.exists():
        raise RuntimeError(f"Backup already exists: {backup_root}")
    backup_root.mkdir(parents=True)
    _assert_safe_ancestry(backup_root, context.product_os_home)
    entries: list[dict[str, Any]] = []
    try:
        for index, (key, (path, scope)) in enumerate(sorted(files.items())):
            path = path.absolute()
            _validate_resource_path(context, key, path, scope)
            if path.exists() and not path.is_file():
                raise RuntimeError(f"Backup resource is not a regular file: {path}")
            backup_file = None
            digest = None
            size = None
            if path.is_file():
                backup_file = f"files/{index:04d}.bin"
                destination = backup_root / backup_file
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
                digest = file_sha256(path)
                size = path.stat().st_size
                if file_sha256(destination) != digest or destination.stat().st_size != size:
                    raise RuntimeError(f"Backup verification failed: {path}")
            entries.append({
                "key": key,
                "path": str(path),
                "path_key": _path_key(path),
                "scope": scope,
                "existed": path.is_file(),
                "kind": "file" if path.is_file() else "absent",
                "sha256": digest,
                "size": size,
                "backup_file": backup_file,
            })
        for key, path in sorted(directories.items()):
            path = path.absolute()
            _assert_safe_ancestry(path, context.project)
            if path.exists() and not path.is_dir():
                raise RuntimeError(f"Backup directory marker is not a directory: {path}")
            entries.append({
                "key": key,
                "path": str(path),
                "path_key": _path_key(path),
                "scope": "project",
                "existed": path.is_dir(),
                "kind": "directory_marker" if path.is_dir() else "absent",
                "sha256": None,
                "size": None,
                "backup_file": None,
            })
        selectors = selector_snapshot.copy_selectors()
        selector_record = {
            "adapter": selector_snapshot.adapter_id,
            "state_token": selector_snapshot.state_token,
            "selectors": selectors,
            "sha256": canonical_json_hash(selectors),
        }
        manifest: dict[str, Any] = {
            "schema": BACKUP_SCHEMA,
            "transaction_id": transaction_id,
            "plan_hash": plan_hash,
            "project": str(context.project),
            "installation_id": installation_id,
            "created_at": utc_now(),
            "backup_root": str(backup_root),
            "entries": entries,
            "selector_snapshot": selector_record,
            "manifest_hash": "",
        }
        manifest["manifest_hash"] = canonical_json_hash(_hashable_manifest(manifest))
        validate_backup_manifest(manifest)
        atomic_write_json(backup_root / "backup-manifest.json", manifest)
        return verify_backup(
            context,
            backup_root / "backup-manifest.json",
            transaction_id=transaction_id,
            plan_hash=plan_hash,
            installation_id=installation_id,
            files=files,
            directories=directories,
            expected_selector_adapter=selector_snapshot.adapter_id,
            expected_selector_state_token=selector_snapshot.state_token,
        )
    except Exception:
        # This directory is transaction-owned and no active resource has been changed yet.
        if backup_root.exists() and not _is_link_like(backup_root):
            shutil.rmtree(backup_root)
        raise


def verify_backup(
    context: InstallationContext,
    manifest_path: Path,
    *,
    transaction_id: str,
    plan_hash: str,
    installation_id: str,
    files: Mapping[str, tuple[Path, str]],
    directories: Mapping[str, Path],
    expected_selector_adapter: str | None = None,
    expected_selector_state_token: str | None = None,
) -> dict[str, Any]:
    manifest_path = manifest_path.absolute()
    expected_root = (
        context.product_os_home / "backups" / installation_id / transaction_id
    ).absolute()
    if _path_key(manifest_path) != _path_key(expected_root / "backup-manifest.json"):
        raise RuntimeError("Backup manifest path is not the derived transaction path")
    _assert_safe_ancestry(manifest_path, context.product_os_home)
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise RuntimeError("Backup manifest is missing")
    validate_backup_manifest(manifest)
    if (
        manifest["transaction_id"] != transaction_id
        or manifest["plan_hash"] != plan_hash
        or manifest["installation_id"] != installation_id
        or manifest["project"] != str(context.project)
        or _path_key(Path(manifest["backup_root"])) != _path_key(expected_root)
    ):
        raise RuntimeError("Backup manifest binding does not match the transaction")
    expected_entries: dict[str, tuple[Path, str, bool]] = {
        key: (path.absolute(), scope, False) for key, (path, scope) in files.items()
    }
    expected_entries.update({
        key: (path.absolute(), "project", True) for key, path in directories.items()
    })
    seen: set[str] = set()
    for entry in manifest["entries"]:
        key = entry["key"]
        if key in seen or key not in expected_entries:
            raise RuntimeError(f"Backup manifest contains an unknown or duplicate resource: {key}")
        seen.add(key)
        expected_path, expected_scope, directory_marker = expected_entries[key]
        if (
            entry["path_key"] != _path_key(expected_path)
            or _path_key(Path(entry["path"])) != _path_key(expected_path)
            or entry["scope"] != expected_scope
        ):
            raise RuntimeError(f"Backup manifest resource binding is invalid: {key}")
        _validate_resource_path(context, key, expected_path, expected_scope)
        if directory_marker:
            if entry["kind"] not in {"directory_marker", "absent"} or entry["backup_file"] is not None:
                raise RuntimeError(f"Backup directory marker is invalid: {key}")
            continue
        if entry["existed"]:
            relative = Path(str(entry["backup_file"]))
            backup_file = (expected_root / relative).absolute()
            if relative.is_absolute() or ".." in relative.parts or not _is_within(backup_file, expected_root):
                raise RuntimeError(f"Backup file path is unsafe: {key}")
            if not backup_file.is_file() or _is_link_like(backup_file):
                raise RuntimeError(f"Backup file is missing or unsafe: {key}")
            if file_sha256(backup_file) != entry["sha256"] or backup_file.stat().st_size != entry["size"]:
                raise RuntimeError(f"Backup file integrity check failed: {key}")
        elif entry["backup_file"] is not None or entry["sha256"] is not None:
            raise RuntimeError(f"Absent backup resource carries file data: {key}")
    if seen != set(expected_entries):
        raise RuntimeError("Backup manifest does not cover the complete mutation set")
    selectors = manifest["selector_snapshot"]
    if selectors["sha256"] != canonical_json_hash(selectors["selectors"]):
        raise RuntimeError("Backup selector snapshot hash does not match")
    if expected_selector_adapter is not None and selectors["adapter"] != expected_selector_adapter:
        raise RuntimeError("Backup selector adapter binding does not match")
    if (
        expected_selector_state_token is not None
        and selectors["state_token"] != expected_selector_state_token
    ):
        raise RuntimeError("Backup selector state token binding does not match")
    return manifest


def restore_backup(
    context: InstallationContext,
    manifest: dict[str, Any],
    *,
    files: Mapping[str, tuple[Path, str]],
    directories: Mapping[str, Path],
    expected_current: Mapping[str, Any] | None = None,
    keys: Sequence[str] | None = None,
) -> None:
    verified = verify_backup(
        context,
        Path(manifest["backup_root"]) / "backup-manifest.json",
        transaction_id=manifest["transaction_id"],
        plan_hash=manifest["plan_hash"],
        installation_id=manifest["installation_id"],
        files=files,
        directories=directories,
    )
    by_key = {entry["key"]: entry for entry in verified["entries"]}
    selected = set(keys) if keys is not None else set(by_key)
    unknown = selected - set(by_key)
    if unknown:
        raise RuntimeError(f"Unknown backup restore resources: {sorted(unknown)}")
    if expected_current is not None:
        current = snapshot_resources(context, files, directories)
        for section in ("files", "directories"):
            for key, expected in expected_current.get(section, {}).items():
                if key in selected and current.get(section, {}).get(key) != expected:
                    raise RuntimeError(f"Rollback resource changed concurrently: {key}")
    for key, (path, scope) in sorted(files.items()):
        if key not in selected:
            continue
        path = path.absolute()
        _validate_resource_path(context, key, path, scope)
        if expected_current is not None:
            current_file = snapshot_resources(context, {key: (path, scope)}, {})["files"][key]
            if current_file != expected_current["files"][key]:
                raise RuntimeError(f"Rollback resource changed during restore: {key}")
        entry = by_key[key]
        if entry["existed"]:
            source = Path(verified["backup_root"]) / entry["backup_file"]
            atomic_write_bytes(path, source.read_bytes())
            if file_sha256(path) != entry["sha256"]:
                raise RuntimeError(f"Restored file verification failed: {key}")
        elif path.exists():
            if not path.is_file() or _is_link_like(path):
                raise RuntimeError(f"Refusing to remove non-file rollback resource: {path}")
            path.unlink()
    for key, path in sorted(directories.items(), reverse=True):
        if key not in selected:
            continue
        if expected_current is not None:
            current_directory = snapshot_resources(context, {}, {key: path})["directories"][key]
            if current_directory != expected_current["directories"][key]:
                raise RuntimeError(f"Rollback directory changed during restore: {key}")
        entry = by_key[key]
        if not entry["existed"] and path.exists():
            if not path.is_dir() or _is_link_like(path):
                raise RuntimeError(f"Refusing to remove unsafe rollback directory: {path}")
            try:
                path.rmdir()
            except OSError as exc:
                raise RuntimeError(f"Rollback directory is not empty: {path}") from exc
