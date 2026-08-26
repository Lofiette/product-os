from __future__ import annotations

import copy
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from tools import cpt_dist

from .adapters.base import SelectorAdapterEvidence
from .context import InstallationContext
from .registry import RegistryStore
from .state import canonical_json_hash, file_sha256, read_json, utc_now

DETECTION_SCHEMA = "product-os-detection-report-v1"


def detection_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "detection-report-v1.schema.json"


def validate_detection_report(report: dict[str, Any]) -> None:
    schema = read_json(detection_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(report),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Invalid Product OS detection report: {details}")
    expected_hash = canonical_json_hash(_hashable_report(report))
    if report.get("state_hash") != expected_hash:
        raise RuntimeError("Invalid Product OS detection report: state_hash does not match content")


def _is_within(path: Path, roots: list[Path]) -> bool:
    resolved = path.resolve()
    return any(resolved == root.resolve() or root.resolve() in resolved.parents for root in roots)


def _safe_project_path(project: Path, value: str) -> tuple[Path | None, str | None]:
    candidate = Path(value)
    if candidate.is_absolute():
        return None, "managed path must be project-relative"
    resolved = (project / candidate).resolve()
    if not _is_within(resolved, [project]):
        return None, "managed path escapes the project root"
    return resolved, None


def _safe_payload_path(
    context: InstallationContext,
    receipt: dict[str, Any] | None,
    value: str | None,
) -> tuple[Path | None, str | None]:
    if not value:
        return None, "payload path is not recorded"
    raw = Path(value)
    resolved = raw.resolve() if raw.is_absolute() else (context.project / raw).resolve()
    allowed_roots = [context.project, context.codex_home]
    lineage = (receipt or {}).get("source_lineage") or {}
    marketplace = lineage.get("marketplace_identity")
    commit = lineage.get("commit_sha")
    if (
        lineage.get("delivery_type") == "git_marketplace"
        and isinstance(marketplace, str)
        and re.fullmatch(r"[a-z][a-z0-9-]*", marketplace)
        and isinstance(commit, str)
        and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit)
    ):
        allowed_roots.append(context.product_os_home / "sources" / marketplace / commit)
    if not _is_within(resolved, allowed_roots):
        return None, "payload path is outside the project, CODEX_HOME, and verified Product OS source roots"
    return resolved, None


def _load_yaml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        return None, str(exc)
    if not isinstance(value, dict):
        return None, "document is not a mapping"
    return value, None


def _receipt_inventory(context: InstallationContext) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = context.project / ".cpt" / "install.json"
    safe_path = _is_within(path, [context.project])
    result: dict[str, Any] = {
        "path": str(path.absolute()),
        "exists": safe_path and path.exists(),
        "valid": False,
        "schema": None,
        "installation_id": None,
        "version": None,
        "mode": None,
        "plugin_scope": None,
        "sha256": file_sha256(path) if safe_path else None,
        "semantic_sha256": None,
        "source_lineage": None,
        "packs": [],
        "claim_issues": [],
        "error": None,
    }
    if not safe_path:
        result["error"] = "installation receipt path escapes the project root"
        return result, None
    if not path.exists():
        result["error"] = "installation receipt is missing"
        return result, None
    try:
        receipt = cpt_dist.load_receipt(context.project)
    except Exception as exc:
        result["error"] = str(exc)
        try:
            parsed = read_json(path)
            if isinstance(parsed, dict):
                result["schema"] = parsed.get("schema")
        except Exception:
            pass
        return result, None
    result.update({
        "valid": True,
        "schema": receipt.get("schema"),
        "installation_id": receipt.get("installation_id"),
        "version": receipt.get("version"),
        "mode": receipt.get("mode"),
        "plugin_scope": receipt.get("plugin_scope"),
        "semantic_sha256": canonical_json_hash(receipt),
        "source_lineage": copy.deepcopy(receipt.get("source_lineage")),
        "packs": copy.deepcopy(receipt.get("packs", [])),
    })
    claim_issues = []
    for condition, message in (
        (not isinstance(receipt.get("version"), str) or not receipt.get("version"), "version is missing"),
        (receipt.get("mode") not in {"local", "team"}, "mode is invalid"),
        (receipt.get("plugin_scope") not in {"none", "personal", "repo"}, "plugin_scope is invalid"),
        (not isinstance(receipt.get("managed_files"), dict), "managed_files is not an object"),
        (not isinstance(receipt.get("mutable_files"), list), "mutable_files is not an array"),
        (not isinstance(receipt.get("plugin"), dict), "plugin is not an object"),
        (not isinstance(receipt.get("packs"), list), "packs is not an array"),
    ):
        if condition:
            claim_issues.append(message)
    result["claim_issues"] = claim_issues
    if claim_issues:
        result["valid"] = False
        result["error"] = "invalid receipt claims: " + "; ".join(claim_issues)
        return result, None
    return result, receipt


def _managed_inventory(context: InstallationContext, receipt: dict[str, Any] | None) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    if receipt:
        managed = receipt.get("managed_files", {})
        if not isinstance(managed, dict):
            managed = {}
        for relative, metadata in sorted(managed.items()):
            item: dict[str, Any] = {
                "path": relative,
                "expected_sha256": metadata.get("sha256") if isinstance(metadata, dict) else None,
                "actual_sha256": None,
                "status": "unsafe",
                "error": None,
            }
            target, error = _safe_project_path(context.project, relative)
            if not isinstance(metadata, dict):
                item["error"] = "managed file metadata is not an object"
            elif error:
                item["error"] = error
            elif item["expected_sha256"] is not None and not (
                isinstance(item["expected_sha256"], str)
                and re.fullmatch(r"[0-9a-f]{64}", item["expected_sha256"])
            ):
                item["error"] = "managed file digest claim is invalid"
            elif target is None or not target.exists():
                item["status"] = "missing"
            elif not target.is_file():
                item["status"] = "invalid_type"
                item["error"] = "managed path is not a file"
            else:
                item["actual_sha256"] = file_sha256(target)
                expected = item["expected_sha256"]
                if not expected:
                    item["status"] = "unverified"
                elif item["actual_sha256"] == expected:
                    item["status"] = "healthy"
                else:
                    item["status"] = "modified"
            entries.append(item)
    counts = {
        status: sum(item["status"] == status for item in entries)
        for status in ("healthy", "modified", "missing", "unverified", "unsafe", "invalid_type")
    }
    return {"total": len(entries), "counts": counts, "entries": entries}


def _receipt_plugin_records(receipt: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not receipt:
        return []
    if receipt.get("schema") == cpt_dist.RECEIPT_SCHEMA_V2:
        plugins = receipt.get("installed_plugins", [])
        return [copy.deepcopy(item) for item in plugins if isinstance(item, dict)]
    result: list[dict[str, Any]] = []
    plugin = receipt.get("plugin", {}) if isinstance(receipt.get("plugin"), dict) else {}
    scope = plugin.get("scope", receipt.get("plugin_scope"))
    if scope in {"personal", "repo"}:
        result.append({
            "name": "cpt-core",
            "selector": None,
            "marketplace_identity": "cpt-personal" if scope == "personal" else "cpt-repo",
            "version": receipt.get("version"),
            "payload_path": plugin.get("plugin_path"),
            "manifest_sha256": None,
            "status": plugin.get("status", "unknown"),
        })
    for pack in receipt.get("packs", []):
        if not isinstance(pack, dict) or not pack.get("name"):
            continue
        pack_scope = pack.get("scope")
        result.append({
            "name": pack["name"],
            "selector": None,
            "marketplace_identity": (
                "cpt-personal" if pack_scope == "personal" else "cpt-repo" if pack_scope == "repo" else None
            ),
            "version": pack.get("version"),
            "payload_path": pack.get("path"),
            "manifest_sha256": None,
            "status": pack.get("status", "unknown"),
        })
    return result


def _plugin_inventory(context: InstallationContext, receipt: dict[str, Any] | None) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for recorded in sorted(_receipt_plugin_records(receipt), key=lambda item: str(item.get("name"))):
        item = {
            "name": recorded.get("name"),
            "selector": recorded.get("selector"),
            "marketplace_identity": recorded.get("marketplace_identity"),
            "version": recorded.get("version"),
            "payload_path": recorded.get("payload_path"),
            "expected_manifest_sha256": recorded.get("manifest_sha256"),
            "actual_manifest_sha256": None,
            "materialized": False,
            "status": "unsafe_path",
            "error": None,
        }
        payload, error = _safe_payload_path(context, receipt, recorded.get("payload_path"))
        if error:
            item["error"] = error
            item["status"] = "unobserved" if not recorded.get("payload_path") else "unsafe_path"
            result.append(item)
            continue
        manifest_path = payload / ".codex-plugin" / "plugin.json"
        if not payload.exists():
            item["status"] = "missing_payload"
        elif not manifest_path.exists():
            item["materialized"] = True
            item["status"] = "missing_manifest"
        else:
            if not _is_within(manifest_path, [payload]):
                item["status"] = "unsafe_path"
                item["error"] = "plugin manifest resolves outside its approved payload root"
                result.append(item)
                continue
            item["materialized"] = True
            item["actual_manifest_sha256"] = file_sha256(manifest_path)
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if not isinstance(manifest, dict):
                    raise ValueError("plugin manifest is not an object")
                if manifest.get("name") != item["name"]:
                    item["status"] = "name_mismatch"
                    item["error"] = f"manifest name is {manifest.get('name')!r}"
                elif item["expected_manifest_sha256"] is None:
                    item["status"] = "present_unverified"
                elif item["actual_manifest_sha256"] != item["expected_manifest_sha256"]:
                    item["status"] = "hash_mismatch"
                else:
                    item["status"] = "healthy"
            except Exception as exc:
                item["status"] = "invalid_manifest"
                item["error"] = str(exc)
        result.append(item)
    return result


def _marketplace_inventory(
    label: str,
    path: Path,
    *,
    allowed_root: Path | None = None,
) -> dict[str, Any]:
    path_safe = allowed_root is None or _is_within(path, [allowed_root])
    result: dict[str, Any] = {
        "label": label,
        "path": str(path.resolve()),
        "exists": path_safe and path.exists(),
        "valid": True,
        "sha256": file_sha256(path) if path_safe else None,
        "name": None,
        "plugins": [],
        "error": None,
    }
    if not path_safe:
        result["exists"] = False
        result["valid"] = False
        result["sha256"] = None
        result["error"] = "marketplace path escapes its approved root"
        return result
    if not path.exists():
        return result
    try:
        data = read_json(path)
        if not isinstance(data, dict) or not isinstance(data.get("plugins", []), list):
            raise ValueError("marketplace document must be an object with a plugins array")
        plugins = []
        for entry in data.get("plugins", []):
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
                raise ValueError("marketplace plugin entry is invalid")
            plugins.append({
                "name": entry["name"],
                "source": copy.deepcopy(entry.get("source")),
            })
        result["name"] = data.get("name")
        result["plugins"] = sorted(plugins, key=lambda item: item["name"])
    except Exception as exc:
        result["valid"] = False
        result["error"] = str(exc)
    return result


def _runtime_inventory(context: InstallationContext) -> dict[str, Any]:
    runtime_path = context.project / ".cpt" / "runtime.yaml"
    current_path = context.project / ".cpt" / "current.yaml"
    runtime_safe = _is_within(runtime_path, [context.project])
    current_safe = _is_within(current_path, [context.project])
    runtime, runtime_error = _load_yaml(runtime_path) if runtime_safe else (None, "runtime path escapes project root")
    current, current_error = _load_yaml(current_path) if current_safe else (None, "current path escapes project root")
    errors = [error for error in (runtime_error, current_error) if error]
    reasons: list[str] = []
    current = current or {}
    for field in ("current_task", "current_micro_change", "current_lease", "current_orchestration"):
        if current.get(field):
            reasons.append(f"{field}={current[field]}")
    for directory, pattern, active_states, label in (
        (context.project / ".cpt" / "workers", "*.yaml", {"running", "cancel_requested", "needs_reconcile"}, "worker"),
        (context.project / ".cpt" / "worktrees", "WT-*.yaml", {"active", "dirty", "blocked"}, "worktree"),
    ):
        if not directory.exists():
            continue
        if not _is_within(directory, [context.project]):
            errors.append(f"{label} directory escapes project root")
            continue
        for path in sorted(directory.glob(pattern)):
            if not path.is_file() or not _is_within(path, [directory]):
                errors.append(f"unsafe {label} record: {path.name}")
                continue
            record, record_error = _load_yaml(path)
            if record_error:
                errors.append(f"invalid {label} record {path.name}: {record_error}")
            elif record and record.get("status") in active_states:
                identity = record.get("agent_id") if label == "worker" else record.get("id")
                reasons.append(f"{label} {identity} is {record.get('status')}")
    latest_checkpoint = current.get("latest_checkpoint")
    checkpoint_valid = None
    if latest_checkpoint:
        checkpoint_root = context.project / ".cpt" / "checkpoints"
        checkpoint_path = checkpoint_root / f"{latest_checkpoint}.yaml"
        checkpoint_valid = _is_within(checkpoint_path, [checkpoint_root]) and checkpoint_path.is_file()
        if not checkpoint_valid:
            errors.append(f"latest checkpoint does not exist: {latest_checkpoint}")
    return {
        "exists": runtime is not None,
        "valid": not errors and runtime is not None,
        "schema_version": (runtime or {}).get("schema_version"),
        "runtime_status": current.get("runtime_status"),
        "current_task": current.get("current_task"),
        "current_micro_change": current.get("current_micro_change"),
        "current_lease": current.get("current_lease"),
        "current_orchestration": current.get("current_orchestration"),
        "latest_checkpoint": latest_checkpoint,
        "checkpoint_valid": checkpoint_valid,
        "state_revision": current.get("state_revision"),
        "file_sha256": {
            "runtime": file_sha256(runtime_path) if runtime_safe else None,
            "current": file_sha256(current_path) if current_safe else None,
        },
        "active_reasons": reasons,
        "errors": errors,
    }


def _registry_inventory(
    context: InstallationContext,
    receipt: dict[str, Any] | None,
) -> dict[str, Any]:
    registry_safe = _is_within(context.registry_path, [context.product_os_home])
    result: dict[str, Any] = {
        "path": str(context.registry_path),
        "exists": registry_safe and context.registry_path.exists(),
        "valid": True,
        "busy": registry_safe and context.product_os_home.joinpath("registry.lock").exists(),
        "sha256": file_sha256(context.registry_path) if registry_safe else None,
        "entry_present": False,
        "entry_matches_receipt": None,
        "installation_count": None,
        "identity_collisions": [],
        "error": None,
    }
    if not registry_safe:
        result["exists"] = False
        result["valid"] = False
        result["busy"] = False
        result["sha256"] = None
        result["error"] = "registry path escapes PRODUCT_OS_HOME"
        return result
    if not context.registry_path.exists():
        return result
    try:
        data, _ = RegistryStore(context).snapshot()
        installations = data.get("installations", {})
        result["installation_count"] = len(installations)
        installation_id = receipt.get("installation_id") if receipt else None
        current_project = str(context.project)
        result["identity_collisions"] = sorted(
            candidate_id
            for candidate_id, candidate in installations.items()
            if isinstance(candidate, dict)
            and candidate.get("project") == current_project
            and candidate_id != installation_id
        )
        if installation_id:
            entry = installations.get(installation_id)
            result["entry_present"] = entry is not None
            if entry:
                result["entry_matches_receipt"] = bool(
                    entry.get("project") == str(context.project)
                    and entry.get("receipt_sha256") == canonical_json_hash(receipt)
                )
    except Exception as exc:
        result["valid"] = False
        result["error"] = str(exc)
    return result


def _selector_inventory(
    observation: SelectorAdapterEvidence | dict[str, Any] | None,
) -> dict[str, Any]:
    if observation is None:
        return {
            "status": "unavailable",
            "adapter": None,
            "authoritative": False,
            "selectors": [],
            "sha256": None,
            "error": "no selector adapter observation was supplied",
        }
    evidence_from_adapter = isinstance(observation, SelectorAdapterEvidence)
    if evidence_from_adapter:
        candidate = {
            "status": "observed",
            "adapter": observation.adapter_id,
            "selectors": observation.copy_selectors(),
        }
    else:
        candidate = copy.deepcopy(observation)
    if not isinstance(candidate, dict):
        return {
            "status": "invalid",
            "adapter": None,
            "authoritative": False,
            "selectors": [],
            "sha256": canonical_json_hash(candidate),
            "error": "selector observation must be an object",
        }
    selectors = candidate.get("selectors")
    if candidate.get("status") != "observed" or not isinstance(selectors, list):
        return {
            "status": "invalid",
            "adapter": candidate.get("adapter"),
            "authoritative": False,
            "selectors": [],
            "sha256": canonical_json_hash(candidate),
            "error": "selector observation must have status=observed and a selectors array",
        }
    normalized = []
    for item in selectors:
        if not isinstance(item, dict) or not item.get("name") or not item.get("selector"):
            return {
                "status": "invalid",
                "adapter": candidate.get("adapter"),
                "authoritative": False,
                "selectors": [],
                "sha256": canonical_json_hash(candidate),
                "error": "selector entries require name and selector",
            }
        enabled = item.get("enabled", True)
        if not isinstance(enabled, bool):
            return {
                "status": "invalid",
                "adapter": candidate.get("adapter"),
                "authoritative": False,
                "selectors": [],
                "sha256": canonical_json_hash(candidate),
                "error": "selector enabled state must be a JSON boolean",
            }
        normalized.append({
            "name": item["name"],
            "selector": item["selector"],
            "enabled": enabled,
            "marketplace_identity": item.get("marketplace_identity"),
            "source_revision": item.get("source_revision"),
        })
    normalized.sort(key=lambda item: (item["name"], item["selector"]))
    enabled_names = [item["name"] for item in normalized if item["enabled"]]
    ambiguous = sorted({name for name in enabled_names if enabled_names.count(name) > 1})
    if ambiguous:
        return {
            "status": "invalid",
            "adapter": candidate.get("adapter"),
            "authoritative": False,
            "selectors": normalized,
            "sha256": canonical_json_hash(normalized),
            "error": f"multiple enabled selectors were observed for: {', '.join(ambiguous)}",
        }
    authoritative = evidence_from_adapter
    normalized_observation = {
        "status": "observed" if evidence_from_adapter else "untrusted",
        "adapter": candidate.get("adapter"),
        "authoritative": authoritative,
        "selectors": normalized,
        "error": None if evidence_from_adapter else "external JSON cannot establish selector authority",
    }
    normalized_observation["sha256"] = canonical_json_hash(normalized_observation)
    return normalized_observation


def _hashable_report(report: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(report)
    value.pop("detected_at", None)
    value.pop("state_hash", None)
    return value


def detect_installation(
    project: str | Path,
    *,
    context: InstallationContext | None = None,
    selector_observation: SelectorAdapterEvidence | dict[str, Any] | None = None,
) -> dict[str, Any]:
    context = context or InstallationContext.from_environment(project)
    receipt_inventory, receipt = _receipt_inventory(context)
    report: dict[str, Any] = {
        "schema": DETECTION_SCHEMA,
        "detected_at": utc_now(),
        "read_only": True,
        "project": str(context.project),
        "project_path_key": str(context.project).casefold() if os.name == "nt" else str(context.project),
        "context": context.as_dict(),
        "receipt": receipt_inventory,
        "runtime": _runtime_inventory(context),
        "managed_files": _managed_inventory(context, receipt),
        "plugins": _plugin_inventory(context, receipt),
        "marketplaces": {
            "user": _marketplace_inventory("user", context.marketplace_registry),
            "repo": _marketplace_inventory(
                "repo",
                context.project / ".agents" / "plugins" / "marketplace.json",
                allowed_root=context.project,
            ),
        },
        "selectors": _selector_inventory(selector_observation),
        "registry": _registry_inventory(context, receipt),
        "state_hash": "",
    }
    report["state_hash"] = canonical_json_hash(_hashable_report(report))
    validate_detection_report(report)
    return report
