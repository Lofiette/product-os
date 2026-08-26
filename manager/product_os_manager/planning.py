from __future__ import annotations

import copy
import re
import stat
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .adapters.base import TargetAdapterEvidence
from .context import InstallationContext
from .inventory import validate_detection_report
from .state import (
    atomic_write_json,
    canonical_json_hash,
    canonical_text_file_sha256,
    read_json,
    utc_now,
)

PLAN_SCHEMA = "product-os-adoption-plan-v1"
COMMIT_PATTERN = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
IDENTITY_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
TARGET_FIELDS = {
    "provider",
    "repository",
    "marketplace_identity",
    "requested_ref",
    "resolved_commit",
    "product_version",
    "package_manifest_sha256",
    "resolution_evidence",
    "materialized_root",
    "plugins",
}
EVIDENCE_FIELDS = {
    "verified",
    "method",
    "provider",
    "repository",
    "requested_ref",
    "resolved_commit",
    "product_version",
    "package_manifest_sha256",
    "plugins_sha256",
}
PLUGIN_FIELDS = {"name", "selector", "relative_path", "manifest_sha256"}
SOURCE_MARKER = ".product-os-source.json"


def adoption_plan_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "adoption-plan-v1.schema.json"


def validate_adoption_plan(plan: dict[str, Any]) -> None:
    schema = read_json(adoption_plan_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(plan),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Invalid Product OS adoption plan: {details}")
    expected_hash = canonical_json_hash(_hashable_plan(plan))
    if plan.get("plan_hash") != expected_hash:
        raise RuntimeError("Invalid Product OS adoption plan: plan_hash does not match content")
    expected_status = "blocked" if plan.get("blockers") else "ready"
    if plan.get("status") != expected_status:
        raise RuntimeError("Invalid Product OS adoption plan: status does not match blockers")


def _is_within(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    root = root.resolve()
    return resolved == root or root in resolved.parents


def _same_path(left: Path, right: Path) -> bool:
    return str(left.absolute()).casefold() == str(right.absolute()).casefold()


def _is_link_like(path: Path) -> bool:
    if path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)()):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _target_root(
    context: InstallationContext,
    marketplace_identity: str | None,
    resolved_commit: str | None,
    configured: str | None,
) -> tuple[Path | None, str | None]:
    if not marketplace_identity or not resolved_commit:
        return None, "target root cannot be derived without marketplace identity and commit"
    sources_root = context.product_os_home / "sources"
    expected = sources_root / marketplace_identity / resolved_commit
    if configured:
        configured_path = Path(configured).expanduser()
        if not configured_path.is_absolute() or not _same_path(configured_path, expected):
            return None, "target root must equal PRODUCT_OS_HOME/sources/<marketplace>/<commit>"
    for candidate in (sources_root, expected.parent, expected):
        if candidate.exists() and _is_link_like(candidate):
            return None, "target root hierarchy cannot contain links or junctions"
    if not _is_within(expected, sources_root):
        return None, "target root escapes the managed sources directory"
    return expected.absolute(), None


def _safe_relative_path(value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


def _verify_package_inventory(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    declared: dict[str, str] = {}
    entries = manifest.get("files")
    if not isinstance(entries, list):
        entries = []
        errors.append({"code": "TARGET_PACKAGE_INVENTORY_INVALID", "message": "package files inventory is missing"})
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append({"code": "TARGET_PACKAGE_INVENTORY_INVALID", "message": f"file entry {index} is not an object"})
            continue
        relative = _safe_relative_path(entry.get("path"))
        expected_hash = entry.get("sha256")
        if relative is None or not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            errors.append({"code": "TARGET_PACKAGE_INVENTORY_INVALID", "message": f"file entry {index} has unsafe path or digest"})
            continue
        key = relative.as_posix()
        if key in declared:
            errors.append({"code": "TARGET_PACKAGE_INVENTORY_INVALID", "message": f"duplicate package path: {key}"})
            continue
        declared[key] = expected_hash
    if manifest.get("file_count") != len(entries):
        errors.append({"code": "TARGET_PACKAGE_INVENTORY_INVALID", "message": "file_count does not match files inventory"})

    verified: list[dict[str, str]] = []
    for relative, expected_hash in sorted(declared.items()):
        path = root / Path(relative)
        if not _is_within(path, root) or _is_link_like(path):
            errors.append({"code": "TARGET_PACKAGE_PATH_UNSAFE", "message": f"declared path is unsafe: {relative}"})
        elif not path.is_file():
            errors.append({"code": "TARGET_PACKAGE_FILE_MISSING", "message": f"declared file is missing: {relative}"})
        else:
            actual_hash = canonical_text_file_sha256(path)
            verified.append({"path": relative, "sha256": actual_hash or ""})
            if actual_hash != expected_hash:
                errors.append({"code": "TARGET_PACKAGE_FILE_HASH_MISMATCH", "message": f"declared file hash mismatch: {relative}"})

    allowed_extras = {"MANIFEST.json", SOURCE_MARKER}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if _is_link_like(path):
            errors.append({"code": "TARGET_PACKAGE_PATH_UNSAFE", "message": f"target contains a link or junction: {relative}"})
            continue
        if path.is_file() and relative not in declared and relative not in allowed_extras:
            errors.append({"code": "TARGET_PACKAGE_FILE_UNDECLARED", "message": f"target contains an undeclared file: {relative}"})
    return {
        "status": "verified" if not errors and declared else "invalid",
        "declared_count": len(declared),
        "verified_count": len(verified),
        "inventory_sha256": canonical_json_hash(verified),
        "declared_paths": sorted(declared),
        "errors": errors,
    }


def inspect_target_descriptor(
    descriptor: TargetAdapterEvidence | dict[str, Any],
    context: InstallationContext,
) -> dict[str, Any]:
    evidence_authoritative = isinstance(descriptor, TargetAdapterEvidence)
    evidence_adapter = descriptor.adapter_id if evidence_authoritative else None
    descriptor = descriptor.copy_descriptor() if evidence_authoritative else copy.deepcopy(descriptor)
    if not isinstance(descriptor, dict):
        descriptor = {}
    provider = descriptor.get("provider")
    repository = descriptor.get("repository")
    marketplace_identity = descriptor.get("marketplace_identity")
    requested_ref = descriptor.get("requested_ref")
    resolved_commit = descriptor.get("resolved_commit")
    product_version = descriptor.get("product_version")
    package_manifest_sha256 = descriptor.get("package_manifest_sha256")
    errors: list[dict[str, str]] = []

    def error(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    unknown_target_fields = sorted(set(descriptor) - TARGET_FIELDS)
    if unknown_target_fields:
        error("TARGET_FIELDS_INVALID", f"unsupported target fields: {unknown_target_fields}")

    if not isinstance(provider, str) or not IDENTITY_PATTERN.fullmatch(provider):
        error("TARGET_PROVIDER_INVALID", "provider must be a kebab-case identity")
    if not isinstance(repository, str) or not repository.strip():
        error("TARGET_REPOSITORY_MISSING", "repository is required")
    elif any(character in repository for character in ("\0", "\r", "\n")):
        error("TARGET_REPOSITORY_INVALID", "repository contains control characters")
    if not isinstance(marketplace_identity, str) or not IDENTITY_PATTERN.fullmatch(marketplace_identity):
        error("TARGET_MARKETPLACE_INVALID", "marketplace identity must be kebab-case")
    if not isinstance(requested_ref, str) or not requested_ref.strip():
        error("TARGET_REF_MISSING", "requested ref is required")
    elif (
        requested_ref.startswith("-")
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", requested_ref)
        or ".." in requested_ref
        or requested_ref.endswith(("/", "."))
    ):
        error("TARGET_REF_INVALID", "requested ref is not a safe immutable-resolution input")
    if not isinstance(resolved_commit, str) or not COMMIT_PATTERN.fullmatch(resolved_commit):
        error("TARGET_COMMIT_INVALID", "resolved commit must be a 40 or 64 character lowercase hex digest")
    if not isinstance(product_version, str) or not product_version:
        error("TARGET_VERSION_MISSING", "target product version is required")
    if not isinstance(package_manifest_sha256, str) or not re.fullmatch(
        r"[0-9a-f]{64}", package_manifest_sha256
    ):
        error("TARGET_PACKAGE_MANIFEST_INVALID", "package manifest SHA-256 is required")

    evidence = descriptor.get("resolution_evidence")
    unknown_evidence_fields = sorted(set(evidence) - EVIDENCE_FIELDS) if isinstance(evidence, dict) else []
    if unknown_evidence_fields:
        error("TARGET_EVIDENCE_FIELDS_INVALID", f"unsupported resolution evidence fields: {unknown_evidence_fields}")
    normalized_evidence = (
        {field: copy.deepcopy(evidence.get(field)) for field in sorted(EVIDENCE_FIELDS)}
        if isinstance(evidence, dict)
        else None
    )
    evidence_base_matches = bool(
        isinstance(normalized_evidence, dict)
        and normalized_evidence.get("verified") is True
        and normalized_evidence.get("provider") == provider
        and normalized_evidence.get("repository") == repository
        and normalized_evidence.get("requested_ref") == requested_ref
        and normalized_evidence.get("resolved_commit") == resolved_commit
        and normalized_evidence.get("product_version") == product_version
        and normalized_evidence.get("package_manifest_sha256") == package_manifest_sha256
        and isinstance(normalized_evidence.get("method"), str)
        and normalized_evidence.get("method")
        and not unknown_evidence_fields
    )

    root, root_error = _target_root(
        context,
        marketplace_identity if isinstance(marketplace_identity, str) else None,
        resolved_commit if isinstance(resolved_commit, str) else None,
        descriptor.get("materialized_root"),
    )
    if root_error:
        error("TARGET_ROOT_UNSAFE", root_error)

    raw_plugins = descriptor.get("plugins")
    if not isinstance(raw_plugins, list) or not raw_plugins:
        error("TARGET_PLUGINS_MISSING", "at least one target plugin is required")
        raw_plugins = []
    raw_plugins = sorted(
        raw_plugins,
        key=lambda item: (
            str(item.get("name")) if isinstance(item, dict) else "",
            str(item.get("selector")) if isinstance(item, dict) else "",
        ),
    )
    plugins: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_selectors: set[str] = set()
    for index, raw in enumerate(raw_plugins):
        if not isinstance(raw, dict):
            error("TARGET_PLUGIN_INVALID", f"plugin {index} is not an object")
            continue
        unknown_plugin_fields = sorted(set(raw) - PLUGIN_FIELDS)
        if unknown_plugin_fields:
            error("TARGET_PLUGIN_FIELDS_INVALID", f"plugin {index} has unsupported fields: {unknown_plugin_fields}")
        name = raw.get("name")
        selector = raw.get("selector")
        relative_path = raw.get("relative_path")
        expected_hash = raw.get("manifest_sha256")
        plugin_errors: list[str] = []
        if not isinstance(name, str) or not IDENTITY_PATTERN.fullmatch(name):
            plugin_errors.append("name must be kebab-case")
        elif name in seen_names:
            plugin_errors.append("name is duplicated")
        else:
            seen_names.add(name)
        if not isinstance(selector, str) or not selector:
            plugin_errors.append("selector is required")
        elif isinstance(name, str) and isinstance(marketplace_identity, str) and selector != f"{name}@{marketplace_identity}":
            plugin_errors.append("selector must bind plugin name to target marketplace identity")
        elif selector in seen_selectors:
            plugin_errors.append("selector is duplicated")
        else:
            seen_selectors.add(selector)
        relative = Path(relative_path) if isinstance(relative_path, str) else None
        if relative is None or relative.is_absolute() or ".." in relative.parts:
            plugin_errors.append("relative_path must remain inside the target root")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            plugin_errors.append("manifest_sha256 must be a lowercase SHA-256 digest")

        manifest_path: Path | None = None
        actual_hash: str | None = None
        status = "not_materialized"
        if root and relative and not relative.is_absolute() and ".." not in relative.parts:
            payload_path = (root / relative).resolve()
            if not _is_within(payload_path, root):
                plugin_errors.append("resolved plugin path escapes the target root")
            else:
                manifest_path = payload_path / ".codex-plugin" / "plugin.json"
                if root.exists():
                    if not _is_within(manifest_path, root):
                        status = "unsafe_path"
                        plugin_errors.append("materialized plugin manifest escapes the target root")
                    elif not manifest_path.exists():
                        status = "missing_manifest"
                        plugin_errors.append("materialized plugin manifest is missing")
                    else:
                        actual_hash = canonical_text_file_sha256(manifest_path)
                        try:
                            manifest = read_json(manifest_path)
                            if not isinstance(manifest, dict) or manifest.get("name") != name:
                                status = "name_mismatch"
                                plugin_errors.append("materialized manifest name does not match")
                            elif manifest.get("version") != product_version:
                                status = "version_mismatch"
                                plugin_errors.append("materialized manifest version does not match target product version")
                            elif actual_hash != expected_hash:
                                status = "hash_mismatch"
                                plugin_errors.append("materialized manifest hash does not match")
                            else:
                                status = "verified"
                                for resource_name, expected_type in (("skills", "directory"), ("hooks", "file")):
                                    reference = manifest.get(resource_name)
                                    if reference is None:
                                        continue
                                    relative_resource = _safe_relative_path(reference)
                                    resource_path = payload_path / relative_resource if relative_resource else None
                                    valid_type = bool(
                                        resource_path
                                        and _is_within(resource_path, payload_path)
                                        and not _is_link_like(resource_path)
                                        and (
                                            resource_path.is_dir()
                                            if expected_type == "directory"
                                            else resource_path.is_file()
                                        )
                                    )
                                    if not valid_type:
                                        status = "invalid_resource"
                                        plugin_errors.append(
                                            f"declared {resource_name} resource is missing, unsafe, or wrong type"
                                        )
                        except Exception as exc:
                            status = "invalid_manifest"
                            plugin_errors.append(f"materialized manifest is invalid: {exc}")
        if plugin_errors:
            error("TARGET_PLUGIN_INVALID", f"{name or index}: {'; '.join(plugin_errors)}")
        plugins.append({
            "name": name,
            "selector": selector,
            "relative_path": relative_path,
            "manifest_sha256": expected_hash,
            "actual_manifest_sha256": actual_hash,
            "status": status,
        })

    plugin_evidence = [
        {
            "name": item.get("name"),
            "selector": item.get("selector"),
            "relative_path": item.get("relative_path"),
            "manifest_sha256": item.get("manifest_sha256"),
        }
        for item in raw_plugins
        if isinstance(item, dict)
    ]
    plugin_evidence_sha256 = canonical_json_hash(plugin_evidence)
    evidence_verified = bool(
        evidence_base_matches
        and isinstance(normalized_evidence, dict)
        and normalized_evidence.get("plugins_sha256") == plugin_evidence_sha256
    )
    if not evidence_verified:
        error(
            "TARGET_RESOLUTION_UNVERIFIED",
            "resolution evidence does not bind provider, repository, ref, commit, package, and plugins",
        )

    package_manifest_actual_sha256: str | None = None
    package_manifest_status = "not_materialized"
    package_inventory: dict[str, Any] = {
        "status": "not_materialized",
        "declared_count": 0,
        "verified_count": 0,
        "inventory_sha256": None,
        "declared_paths": [],
        "errors": [],
    }
    source_marker_status = "not_materialized"
    if root and root.exists():
        package_manifest_path = root / "MANIFEST.json"
        if not _is_within(package_manifest_path, root):
            package_manifest_status = "unsafe_path"
            error("TARGET_PACKAGE_MANIFEST_UNSAFE", "materialized package manifest escapes the target root")
        elif not package_manifest_path.exists():
            package_manifest_status = "missing"
            error("TARGET_PACKAGE_MANIFEST_MISSING", "materialized target MANIFEST.json is missing")
        else:
            package_manifest_actual_sha256 = canonical_text_file_sha256(package_manifest_path)
            try:
                package_manifest = read_json(package_manifest_path)
                if not isinstance(package_manifest, dict):
                    raise ValueError("package manifest is not an object")
                if package_manifest.get("name") != "codex-product-os":
                    package_manifest_status = "identity_mismatch"
                    error("TARGET_PACKAGE_IDENTITY_MISMATCH", "materialized package name is not codex-product-os")
                elif package_manifest.get("version") != product_version:
                    package_manifest_status = "version_mismatch"
                    error("TARGET_PACKAGE_VERSION_MISMATCH", "materialized package version does not match evidence")
                elif package_manifest_actual_sha256 != package_manifest_sha256:
                    package_manifest_status = "hash_mismatch"
                    error("TARGET_PACKAGE_HASH_MISMATCH", "materialized package manifest hash does not match evidence")
                else:
                    package_manifest_status = "verified"
                    package_inventory = _verify_package_inventory(root, package_manifest)
                    for inventory_error in package_inventory["errors"]:
                        error(inventory_error["code"], inventory_error["message"])
            except Exception as exc:
                package_manifest_status = "invalid"
                error("TARGET_PACKAGE_MANIFEST_INVALID", f"materialized package manifest is invalid: {exc}")

        marker_path = root / SOURCE_MARKER
        if not _is_within(marker_path, root) or _is_link_like(marker_path):
            source_marker_status = "unsafe"
            error("TARGET_SOURCE_MARKER_UNSAFE", "materialized source marker is unsafe")
        elif not marker_path.is_file():
            source_marker_status = "missing"
            error("TARGET_SOURCE_MARKER_MISSING", "materialized source marker is missing")
        else:
            try:
                marker = read_json(marker_path)
                expected_marker = {
                    "schema": "product-os-materialized-source-v1",
                    "provider": provider,
                    "repository": repository,
                    "marketplace_identity": marketplace_identity,
                    "requested_ref": requested_ref,
                    "resolved_commit": resolved_commit,
                    "product_version": product_version,
                    "package_manifest_sha256": package_manifest_sha256,
                }
                if marker != expected_marker:
                    source_marker_status = "mismatch"
                    error("TARGET_SOURCE_MARKER_MISMATCH", "materialized source marker does not match target evidence")
                else:
                    source_marker_status = "verified"
            except Exception as exc:
                source_marker_status = "invalid"
                error("TARGET_SOURCE_MARKER_INVALID", f"materialized source marker is invalid: {exc}")

        declared_paths = set(package_inventory.get("declared_paths", []))
        for plugin in plugins:
            plugin_manifest_relative = (
                Path(str(plugin["relative_path"])) / ".codex-plugin" / "plugin.json"
            ).as_posix()
            if plugin_manifest_relative not in declared_paths:
                plugin["status"] = "undeclared_manifest"
                error(
                    "TARGET_PLUGIN_UNDECLARED",
                    f"plugin manifest is absent from package inventory: {plugin_manifest_relative}",
                )

    materialization_status = "not_materialized"
    if root and root.exists():
        materialization_status = (
            "verified"
            if package_manifest_status == "verified"
            and package_inventory["status"] == "verified"
            and source_marker_status == "verified"
            and plugins
            and all(item["status"] == "verified" for item in plugins)
            else "invalid"
        )
    return {
        "provider": provider,
        "repository": repository,
        "marketplace_identity": marketplace_identity,
        "requested_ref": requested_ref,
        "resolved_commit": resolved_commit,
        "product_version": product_version,
        "package_manifest_sha256": package_manifest_sha256,
        "package_manifest_actual_sha256": package_manifest_actual_sha256,
        "package_manifest_status": package_manifest_status,
        "package_inventory": package_inventory,
        "source_marker_status": source_marker_status,
        "resolution_evidence": normalized_evidence,
        "resolution_evidence_sha256": canonical_json_hash(normalized_evidence) if isinstance(normalized_evidence, dict) else None,
        "plugin_evidence_sha256": plugin_evidence_sha256,
        "resolution_verified": evidence_verified,
        "evidence_authoritative": evidence_authoritative,
        "evidence_adapter": evidence_adapter,
        "materialized_root": str(root) if root else None,
        "materialization_status": materialization_status,
        "plugins": plugins,
        "errors": errors,
    }


def _issue(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, "details": details}


def _append_unique(collection: list[dict[str, Any]], item: dict[str, Any]) -> None:
    if item["code"] not in {existing["code"] for existing in collection}:
        collection.append(item)


def _hashable_plan(plan: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(plan)
    value.pop("generated_at", None)
    value.pop("plan_hash", None)
    return value


def _actions(receipt_schema: str | None) -> list[dict[str, Any]]:
    actions = [
        {
            "id": "create_transaction_journal",
            "phase": "prepare",
            "mutation": "manager_state",
            "approval": "apply",
            "conditional": False,
            "description": "Create a durable transaction journal bound to the confirmed plan hash.",
        },
        {
            "id": "backup_current_state",
            "phase": "prepare",
            "mutation": "backup",
            "approval": "apply",
            "conditional": False,
            "description": "Capture and verify project, receipt, registry, marketplace, and selector pre-state.",
        },
        {
            "id": "materialize_target",
            "phase": "prepare",
            "mutation": "provider_target",
            "approval": "apply",
            "conditional": False,
            "description": "Materialize the resolved target revision outside the active selector path.",
        },
        {
            "id": "verify_target",
            "phase": "prepare",
            "mutation": "none",
            "approval": "apply",
            "conditional": False,
            "description": "Verify target revision, plugin manifests, names, and expected hashes.",
        },
        {
            "id": "refresh_runtime_scaffold",
            "phase": "prepare",
            "mutation": "project",
            "approval": "apply",
            "conditional": False,
            "description": "Refresh Product OS runtime-owned files without touching legacy selectors.",
        },
    ]
    if receipt_schema == "cpt-install-receipt-v1":
        actions.append({
            "id": "upgrade_installation_receipt_v2",
            "phase": "prepare",
            "mutation": "project",
            "approval": "apply",
            "conditional": False,
            "description": "Upgrade the receipt on an approved write while preserving v1 compatibility fields.",
        })
    actions.extend([
        {
            "id": "prepare_target_selectors",
            "phase": "prepare",
            "mutation": "selector",
            "approval": "apply",
            "conditional": False,
            "description": "Prepare target selectors alongside the legacy selectors without activation.",
        },
        {
            "id": "await_switch_confirmation",
            "phase": "switch",
            "mutation": "none",
            "approval": "switch",
            "conditional": False,
            "description": "Stop after preparation and require confirmation of the prepared-state hash.",
        },
        {
            "id": "activate_target_selectors",
            "phase": "switch",
            "mutation": "selector",
            "approval": "switch",
            "conditional": False,
            "description": "Activate the verified target selectors through the selected adapter.",
        },
        {
            "id": "verify_active_selectors",
            "phase": "switch",
            "mutation": "none",
            "approval": "switch",
            "conditional": False,
            "description": "Read back authoritative selector state and reject hybrid activation.",
        },
        {
            "id": "commit_receipt_and_registry",
            "phase": "commit",
            "mutation": "project_and_registry",
            "approval": "switch",
            "conditional": False,
            "description": "Commit source lineage, installed selectors, migration receipt, and registry entry.",
        },
        {
            "id": "run_migration_doctor",
            "phase": "commit",
            "mutation": "none",
            "approval": "switch",
            "conditional": False,
            "description": "Verify runtime, lineage, registry, target materialization, selectors, and journal state.",
        },
        {
            "id": "retire_legacy_selector_if_unreferenced",
            "phase": "finalize",
            "mutation": "selector",
            "approval": "switch",
            "conditional": True,
            "description": "Retire a legacy selector only after registry and adapter evidence prove it is unreferenced.",
        },
    ])
    return actions


def build_adoption_plan(
    detection: dict[str, Any],
    target_descriptor: TargetAdapterEvidence | dict[str, Any],
    *,
    context: InstallationContext | None = None,
) -> dict[str, Any]:
    validate_detection_report(detection)
    context = context or InstallationContext.from_environment(detection["project"])
    if context.as_dict() != detection["context"]:
        raise RuntimeError("Detection report roots do not match the planning context")
    target = inspect_target_descriptor(target_descriptor, context)
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    receipt = detection["receipt"]
    if not receipt["valid"]:
        _append_unique(blockers, _issue("RECEIPT_INVALID", "A valid v1 or v2 receipt is required", error=receipt["error"]))
    runtime = detection["runtime"]
    if not runtime["valid"]:
        _append_unique(blockers, _issue("RUNTIME_INVALID", "Runtime inventory is invalid", errors=runtime["errors"]))
    if runtime["active_reasons"]:
        _append_unique(
            blockers,
            _issue("RUNTIME_ACTIVE", "Adoption cannot apply while Product OS runtime work is active", reasons=runtime["active_reasons"]),
        )

    managed = detection["managed_files"]
    for status, code in (
        ("modified", "MANAGED_FILES_MODIFIED"),
        ("unsafe", "MANAGED_PATH_UNSAFE"),
        ("invalid_type", "MANAGED_PATH_INVALID"),
    ):
        paths = [item["path"] for item in managed["entries"] if item["status"] == status]
        if paths:
            _append_unique(blockers, _issue(code, f"Managed files are {status}", paths=paths))
    missing_managed = [item["path"] for item in managed["entries"] if item["status"] == "missing"]
    if missing_managed:
        _append_unique(
            warnings,
            _issue(
                "MANAGED_FILES_MISSING_REPAIRABLE",
                "Missing runtime-owned files can be restored from the verified target",
                paths=missing_managed,
            ),
        )
    unverified = [item["path"] for item in managed["entries"] if item["status"] == "unverified"]
    if unverified:
        _append_unique(warnings, _issue("MANAGED_FILES_UNVERIFIED", "Managed files lack expected hashes", paths=unverified))

    invalid_plugin_statuses = {
        "unsafe_path",
        "missing_payload",
        "missing_manifest",
        "invalid_manifest",
        "name_mismatch",
        "hash_mismatch",
    }
    invalid_plugins = [
        {"name": item["name"], "status": item["status"]}
        for item in detection["plugins"]
        if item["status"] in invalid_plugin_statuses
    ]
    if invalid_plugins:
        _append_unique(blockers, _issue("CURRENT_PLUGIN_INVALID", "Current plugin materialization is invalid", plugins=invalid_plugins))
    unverified_plugins = [item["name"] for item in detection["plugins"] if item["status"] in {"unobserved", "present_unverified"}]
    if unverified_plugins:
        _append_unique(warnings, _issue("CURRENT_PLUGIN_UNVERIFIED", "Current plugin provenance is incomplete", plugins=unverified_plugins))

    for label, marketplace in detection["marketplaces"].items():
        if marketplace["exists"] and not marketplace["valid"]:
            _append_unique(
                blockers,
                _issue("MARKETPLACE_INVALID", "A marketplace registry is invalid", marketplace=label, error=marketplace["error"]),
            )

    selectors = detection["selectors"]
    if selectors["status"] != "observed" or not selectors["authoritative"]:
        _append_unique(
            blockers,
            _issue("SELECTOR_STATE_UNOBSERVED", "Authoritative selector state is required before apply", status=selectors["status"]),
        )
    else:
        observed_by_name = {item["name"]: item for item in selectors["selectors"] if item.get("enabled")}
        current_with_payload = [item for item in detection["plugins"] if item["materialized"]]
        missing = [item["name"] for item in current_with_payload if item["name"] not in observed_by_name]
        if missing:
            _append_unique(
                blockers,
                _issue("CURRENT_SELECTOR_UNOBSERVED", "Materialized current plugins are absent from selector state", plugins=missing),
            )
        mismatched = [
            item["name"]
            for item in current_with_payload
            if item.get("selector")
            and item["name"] in observed_by_name
            and observed_by_name[item["name"]]["selector"] != item["selector"]
        ]
        if mismatched:
            _append_unique(
                blockers,
                _issue("SELECTOR_RECEIPT_MISMATCH", "Observed selectors differ from receipt selectors", plugins=mismatched),
            )

    registry = detection["registry"]
    if registry["busy"]:
        _append_unique(blockers, _issue("REGISTRY_BUSY", "The installation registry lock is already held"))
    if registry["exists"] and not registry["valid"]:
        _append_unique(blockers, _issue("REGISTRY_INVALID", "The user installation registry is invalid", error=registry["error"]))
    elif registry["identity_collisions"]:
        _append_unique(
            blockers,
            _issue(
                "REGISTRY_IDENTITY_COLLISION",
                "Another installation id already claims this project path",
                installation_ids=registry["identity_collisions"],
            ),
        )
    elif registry["entry_present"] and registry["entry_matches_receipt"] is False:
        _append_unique(blockers, _issue("REGISTRY_ENTRY_STALE", "Registry entry does not match the project receipt"))
    elif not registry["exists"] or not registry["entry_present"]:
        _append_unique(
            warnings,
            _issue("REGISTRY_INCOMPLETE", "Registry can be rebuilt for this installation but cannot prove global selector ownership"),
        )

    for target_error in target["errors"]:
        _append_unique(blockers, _issue(target_error["code"], target_error["message"]))
    if not target["evidence_authoritative"]:
        _append_unique(
            blockers,
            _issue(
                "TARGET_EVIDENCE_UNTRUSTED",
                "Target evidence must come from an in-process bounded provider adapter",
            ),
        )

    if receipt.get("source_lineage") is None or (receipt.get("source_lineage") or {}).get("delivery_type") == "unknown":
        _append_unique(warnings, _issue("SOURCE_LINEAGE_UNKNOWN", "Legacy source lineage remains unknown until approved adoption"))

    retirement_policy = "retain_until_proven_unreferenced"
    retirement_reasons = [
        "retirement requires post-switch authoritative selector readback",
        "retirement requires a valid complete registry reference check",
    ]
    preconditions = {
        "detection_state_hash": detection["state_hash"],
        "receipt_sha256": receipt["sha256"],
        "receipt_semantic_sha256": receipt["semantic_sha256"],
        "registry_sha256": registry["sha256"],
        "marketplace_sha256": {
            name: value["sha256"] for name, value in sorted(detection["marketplaces"].items())
        },
        "managed_state_sha256": canonical_json_hash(managed["entries"]),
        "selector_state_sha256": selectors["sha256"],
        "active_reasons": copy.deepcopy(runtime["active_reasons"]),
        "target_resolution_evidence_sha256": target["resolution_evidence_sha256"],
        "target_materialization_status": target["materialization_status"],
    }
    plan: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "generated_at": utc_now(),
        "project": detection["project"],
        "status": "blocked" if blockers else "ready",
        "dry_run": True,
        "plan_hash": "",
        "detection_state_hash": detection["state_hash"],
        "target": target,
        "preconditions": preconditions,
        "blockers": blockers,
        "warnings": warnings,
        "actions": _actions(receipt["schema"]),
        "approval": {
            "apply": {
                "required": True,
                "confirmation": "exact plan_hash",
                "scope": "backup, target materialization, runtime refresh, receipt/registry staging, selector preparation",
            },
            "switch": {
                "required": True,
                "confirmation": "transaction id plus prepared-state hash",
                "scope": "selector activation, readback verification, durable commit, conditional legacy retirement",
            },
        },
        "rollback": {
            "automatic_on_failure": True,
            "concurrent_change_policy": "refuse_without_emergency_backup",
            "legacy_selector_policy": retirement_policy,
            "legacy_selector_reasons": retirement_reasons,
        },
    }
    plan["plan_hash"] = canonical_json_hash(_hashable_plan(plan))
    validate_adoption_plan(plan)
    return plan


def write_adoption_plan(path: Path, plan: dict[str, Any]) -> None:
    validate_adoption_plan(plan)
    atomic_write_json(path.resolve(), plan)
