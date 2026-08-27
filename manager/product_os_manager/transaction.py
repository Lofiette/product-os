from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from tools import cpt_dist

from .adapters.base import (
    AdapterRegistry,
    SelectorAdapter,
    SelectorAdapterEvidence,
    TargetAdapterEvidence,
    TargetProvider,
)
from .backup import (
    assert_safe_ancestry,
    create_backup,
    resource_paths,
    restore_backup,
    snapshot_resources,
    verify_backup,
)
from .context import InstallationContext
from .inventory import detect_installation
from .planning import build_adoption_plan, inspect_target_descriptor, validate_adoption_plan
from .registry import RegistryStore, receipt_entry
from .state import (
    atomic_write_json,
    canonical_json_hash,
    exclusive_lock,
    file_sha256,
    read_json,
    utc_now,
)

TRANSACTION_SCHEMA = "product-os-adoption-transaction-v1"
PREPARED_SCHEMA = "product-os-prepared-state-v1"
_UNSET = object()
TRANSACTION_PATTERN = re.compile(
    r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
CLOSED_STATES = {
    "committed",
    "rolled_back",
    "failed_no_mutation",
}
ALLOWED_TRANSITIONS = {
    "created": {"backed_up", "failed_no_mutation", "rolled_back", "manual_recovery_required"},
    "backed_up": {"materializing", "failed_no_mutation", "rolled_back", "manual_recovery_required"},
    "materializing": {"target_verified", "failed_no_mutation", "rolled_back", "manual_recovery_required"},
    "target_verified": {"preparing_selectors", "failed_no_mutation", "rolled_back", "manual_recovery_required"},
    "preparing_selectors": {"prepared", "failed_no_mutation", "rolled_back", "manual_recovery_required"},
    "prepared": {"refreshing_runtime", "rolling_back", "manual_recovery_required"},
    "refreshing_runtime": {"runtime_refreshed", "rolling_back", "manual_recovery_required"},
    "runtime_refreshed": {"activating_selectors", "rolling_back", "manual_recovery_required"},
    "activating_selectors": {"selectors_activated", "rolling_back", "manual_recovery_required"},
    "selectors_activated": {"writing_receipt", "rolling_back", "manual_recovery_required"},
    "writing_receipt": {"receipt_written", "rolling_back", "manual_recovery_required"},
    "receipt_written": {"writing_registry", "rolling_back", "manual_recovery_required"},
    "writing_registry": {"registry_written", "rolling_back", "manual_recovery_required"},
    "registry_written": {"verifying", "rolling_back", "manual_recovery_required"},
    "verifying": {"committed", "rolling_back", "manual_recovery_required"},
    "committed": {"rolling_back", "manual_recovery_required"},
    "rolling_back": {"rolled_back", "manual_recovery_required"},
    "manual_recovery_required": {"rolling_back"},
}


class AdoptionTransactionError(RuntimeError):
    pass


class ConcurrentAdoptionChange(AdoptionTransactionError):
    pass


def transaction_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "adoption-transaction-v1.schema.json"


def _hashable_journal(journal: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(journal))
    value.pop("journal_hash", None)
    return value


def validate_transaction_journal(journal: dict[str, Any]) -> None:
    schema = read_json(transaction_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(journal),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise AdoptionTransactionError(f"Invalid adoption transaction journal: {details}")
    if journal.get("journal_hash") != canonical_json_hash(_hashable_journal(journal)):
        raise AdoptionTransactionError("Invalid adoption transaction journal: hash mismatch")
    validate_adoption_plan(journal["plan"])
    if journal["plan_hash"] != journal["plan"]["plan_hash"]:
        raise AdoptionTransactionError("Transaction plan binding does not match")
    if journal["project"] != journal["plan"]["project"]:
        raise AdoptionTransactionError("Transaction project binding does not match")
    prepared = journal.get("prepared")
    if isinstance(prepared, dict):
        hashable = copy.deepcopy(prepared)
        prepared_hash = hashable.pop("prepared_state_hash", None)
        if prepared_hash != canonical_json_hash(hashable):
            raise AdoptionTransactionError("Prepared-state hash does not match transaction content")


def _path_key(path: Path) -> str:
    value = str(path.resolve())
    return value.casefold() if os.name == "nt" else value


def _contains(left: Path, right: Path) -> bool:
    left = left.resolve()
    right = right.resolve()
    return left == right or left in right.parents or right in left.parents


def validate_mutation_context(context: InstallationContext) -> None:
    mutable_roots = {
        "project": context.project,
        "CODEX_HOME": context.codex_home,
        "PRODUCT_OS_HOME": context.product_os_home,
    }
    checked: set[tuple[str, str]] = set()
    for left_name, left in mutable_roots.items():
        if left.exists() and (
            left.is_symlink() or bool(getattr(left, "is_junction", lambda: False)())
        ):
            raise AdoptionTransactionError(f"Mutable root is link-like: {left_name}={left}")
        for right_name, right in mutable_roots.items():
            pair = tuple(sorted((left_name, right_name)))
            if left_name != right_name and pair not in checked:
                checked.add(pair)
                if _contains(left, right):
                    raise AdoptionTransactionError(
                        f"Mutable roots overlap: {left_name}={left} and {right_name}={right}"
                    )
    reserved = {
        _path_key(context.registry_path),
        _path_key(context.project / ".cpt" / "install.json"),
    }
    if _path_key(context.marketplace_registry) in reserved:
        raise AdoptionTransactionError("Marketplace registry collides with a managed receipt or registry")


def _project_bucket(context: InstallationContext) -> str:
    return hashlib.sha256(_path_key(context.project).encode("utf-8")).hexdigest()


def transaction_directory(context: InstallationContext, transaction_id: str) -> Path:
    if not TRANSACTION_PATTERN.fullmatch(transaction_id):
        raise AdoptionTransactionError("Transaction id is invalid")
    path = (
        context.product_os_home / "transactions" / _project_bucket(context) / transaction_id
    ).absolute()
    assert_safe_ancestry(path, context.product_os_home)
    return path


def transaction_lock_path(context: InstallationContext) -> Path:
    path = (
        context.product_os_home / "locks" / f"{_project_bucket(context)}.lock"
    ).absolute()
    assert_safe_ancestry(path, context.product_os_home)
    return path


def _journal_path(context: InstallationContext, transaction_id: str) -> Path:
    return transaction_directory(context, transaction_id) / "journal.json"


def load_transaction(context: InstallationContext, transaction_id: str) -> dict[str, Any]:
    journal = read_json(_journal_path(context, transaction_id))
    if not isinstance(journal, dict):
        raise AdoptionTransactionError(f"Adoption transaction does not exist: {transaction_id}")
    validate_transaction_journal(journal)
    if journal["context"] != context.as_dict() or journal["project"] != str(context.project):
        raise AdoptionTransactionError("Transaction context does not match the current installation roots")
    return journal


def _write_new_journal(context: InstallationContext, journal: dict[str, Any]) -> dict[str, Any]:
    directory = transaction_directory(context, journal["transaction_id"])
    directory.mkdir(parents=True, exist_ok=False)
    assert_safe_ancestry(directory, context.product_os_home)
    candidate = copy.deepcopy(journal)
    candidate["revision"] = 1
    candidate["previous_journal_hash"] = None
    candidate["journal_hash"] = canonical_json_hash(_hashable_journal(candidate))
    validate_transaction_journal(candidate)
    atomic_write_json(directory / "journal.json", candidate)
    return candidate


def _save_journal(context: InstallationContext, journal: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(journal)
    candidate["previous_journal_hash"] = journal["journal_hash"]
    candidate["revision"] = journal["revision"] + 1
    candidate["updated_at"] = utc_now()
    candidate["journal_hash"] = canonical_json_hash(_hashable_journal(candidate))
    validate_transaction_journal(candidate)
    atomic_write_json(_journal_path(context, candidate["transaction_id"]), candidate)
    return candidate


def _transition(
    context: InstallationContext,
    journal: dict[str, Any],
    state: str,
    **changes: Any,
) -> dict[str, Any]:
    current = journal["state"]
    if state not in ALLOWED_TRANSITIONS.get(current, set()):
        raise AdoptionTransactionError(
            f"Invalid adoption transaction transition: {current} -> {state}"
        )
    candidate = copy.deepcopy(journal)
    candidate["state"] = state
    for name, value in changes.items():
        candidate[name] = copy.deepcopy(value)
    return _save_journal(context, candidate)


def _existing_transactions(context: InstallationContext) -> list[dict[str, Any]]:
    root = context.product_os_home / "transactions" / _project_bucket(context)
    if not root.exists():
        return []
    result = []
    for path in sorted(root.glob("TX-*/journal.json")):
        if TRANSACTION_PATTERN.fullmatch(path.parent.name):
            result.append(load_transaction(context, path.parent.name))
    return result


def list_adoption_transactions(context: InstallationContext) -> dict[str, Any]:
    """Return a bounded, read-only index for crash recovery and diagnosis."""

    validate_mutation_context(context)
    entries = [
        {
            "transaction_id": journal["transaction_id"],
            "state": journal["state"],
            "created_at": journal["created_at"],
            "updated_at": journal["updated_at"],
            "revision": journal["revision"],
            "plan_hash": journal["plan_hash"],
            "journal_hash": journal["journal_hash"],
            "unresolved": journal["state"] not in CLOSED_STATES,
        }
        for journal in _existing_transactions(context)
    ]
    entries.sort(
        key=lambda item: (
            str(item["updated_at"]),
            int(item["revision"]),
            str(item["transaction_id"]),
        ),
        reverse=True,
    )
    return {
        "schema": "product-os-adoption-transaction-list-v1",
        "project": str(context.project),
        "transactions": entries,
        "unresolved_count": sum(1 for item in entries if item["unresolved"]),
    }


def _load_receipt_snapshot(
    context: InstallationContext,
) -> tuple[dict[str, Any], str]:
    path = context.project / ".cpt" / "install.json"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict) or value.get("schema") not in {
        cpt_dist.RECEIPT_SCHEMA_V1,
        cpt_dist.RECEIPT_SCHEMA_V2,
    }:
        raise AdoptionTransactionError("No valid Product OS installation receipt found")
    if value.get("schema") == cpt_dist.RECEIPT_SCHEMA_V2:
        cpt_dist.validate_receipt_v2(value)
    return value, digest


def target_request_from_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    target = plan["target"]
    return {
        "repository": target["repository"],
        "requested_ref": target["requested_ref"],
        "marketplace_identity": target["marketplace_identity"],
        "plugins": sorted(str(plugin["name"]) for plugin in target["plugins"]),
    }


def target_contract(target: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "provider": target.get("provider"),
        "repository": target.get("repository"),
        "marketplace_identity": target.get("marketplace_identity"),
        "requested_ref": target.get("requested_ref"),
        "resolved_commit": target.get("resolved_commit"),
        "product_version": target.get("product_version"),
        "package_manifest_sha256": target.get("package_manifest_sha256"),
        "resolution_evidence_sha256": target.get("resolution_evidence_sha256"),
        "plugin_evidence_sha256": target.get("plugin_evidence_sha256"),
        "materialized_root": target.get("materialized_root"),
        "evidence_adapter": target.get("evidence_adapter"),
        "evidence_adapter_version": target.get("evidence_adapter_version"),
        "evidence_capability_fingerprint": target.get("evidence_capability_fingerprint"),
        "plugins": [
            {
                "name": plugin.get("name"),
                "selector": plugin.get("selector"),
                "relative_path": plugin.get("relative_path"),
                "manifest_sha256": plugin.get("manifest_sha256"),
            }
            for plugin in target.get("plugins", [])
        ],
    }


def _selector_state(evidence: SelectorAdapterEvidence) -> dict[str, Any]:
    selectors = evidence.copy_selectors()
    return {
        "adapter_id": evidence.adapter_id,
        "adapter_version": evidence.adapter_version,
        "capability_fingerprint": evidence.capability_fingerprint,
        "state_token": evidence.state_token,
        "selectors": selectors,
        "selectors_sha256": canonical_json_hash(selectors),
    }


def _assert_adapter_binding(adapter: Any, expected: Mapping[str, Any], *, label: str) -> None:
    actual = AdapterRegistry.binding(adapter)
    if actual != dict(expected):
        raise AdoptionTransactionError(f"{label} adapter binding changed: {actual}")


def _assert_evidence_binding(
    evidence: TargetAdapterEvidence | SelectorAdapterEvidence,
    expected: Mapping[str, Any],
    *,
    label: str,
) -> None:
    actual = {
        "adapter_id": evidence.adapter_id,
        "adapter_version": evidence.adapter_version,
        "capability_fingerprint": evidence.capability_fingerprint,
    }
    if actual != dict(expected):
        raise AdoptionTransactionError(f"{label} evidence binding changed: {actual}")


def _target_plugins(target: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": plugin["name"],
            "selector": plugin["selector"],
            "marketplace_identity": target["marketplace_identity"],
            "source_revision": target["resolved_commit"],
        }
        for plugin in target["plugins"]
    ]


def _selector_target_entry(plugin: Mapping[str, Any], *, enabled: bool) -> dict[str, Any]:
    return {
        "name": plugin["name"],
        "selector": plugin["selector"],
        "marketplace_identity": plugin["marketplace_identity"],
        "enabled": enabled,
        "source_revision": plugin.get("source_revision"),
    }


def _expected_prepared_selectors(
    before: Sequence[Mapping[str, Any]],
    target_plugins: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_key = {
        (item["name"], item["selector"]): copy.deepcopy(dict(item))
        for item in before
    }
    for plugin in target_plugins:
        key = (plugin["name"], plugin["selector"])
        if key in by_key and by_key[key].get("enabled"):
            if by_key[key].get("source_revision") == plugin.get("source_revision"):
                raise AdoptionTransactionError("Target selector is active before prepare")
            # A Git marketplace update keeps the same selector identity while
            # prepare verifies and materializes a newer immutable revision.
            # The predecessor must remain active until the separately confirmed
            # switch phase retargets the marketplace.
            continue
        by_key[key] = _selector_target_entry(plugin, enabled=False)
    return sorted(by_key.values(), key=lambda item: (item["name"], item["selector"]))


def _expected_active_selectors(
    prepared: Sequence[Mapping[str, Any]],
    target_plugins: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    targets = {item["name"]: item for item in target_plugins}
    target_keys = {(item["name"], item["selector"]) for item in target_plugins}
    prepared_keys = {(item["name"], item["selector"]) for item in prepared}
    if not target_keys.issubset(prepared_keys):
        raise AdoptionTransactionError("Prepared selector document is missing a target")
    result: list[dict[str, Any]] = []
    for item in prepared:
        candidate = copy.deepcopy(dict(item))
        target = targets.get(candidate["name"])
        if target:
            candidate["enabled"] = candidate["selector"] == target["selector"]
            if candidate["enabled"]:
                candidate["marketplace_identity"] = target["marketplace_identity"]
                candidate["source_revision"] = target.get("source_revision")
        result.append(candidate)
    return sorted(result, key=lambda item: (item["name"], item["selector"]))


def _selector_groups(
    selectors: Sequence[Mapping[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in selectors:
        grouped.setdefault(str(item["name"]), []).append(copy.deepcopy(dict(item)))
    for values in grouped.values():
        values.sort(key=lambda item: item["selector"])
    return grouped


def _assert_selector_transition_state(
    current: Sequence[Mapping[str, Any]],
    before: Sequence[Mapping[str, Any]],
    after: Sequence[Mapping[str, Any]],
    target_plugins: Sequence[Mapping[str, Any]],
    *,
    allow_unrelated_drift: bool = False,
) -> None:
    _assert_selector_envelope(
        current,
        [before, after],
        target_plugins,
        allow_unrelated_drift=allow_unrelated_drift,
    )


def _assert_selector_envelope(
    current: Sequence[Mapping[str, Any]],
    variants: Sequence[Sequence[Mapping[str, Any]]],
    target_plugins: Sequence[Mapping[str, Any]],
    *,
    allow_unrelated_drift: bool = False,
) -> None:
    current_groups = _selector_groups(current)
    variant_groups = [_selector_groups(value) for value in variants]
    baseline_groups = variant_groups[0]
    target_names = {str(item["name"]) for item in target_plugins}
    if not allow_unrelated_drift:
        unrelated = (set(current_groups) | set(baseline_groups)) - target_names
        for name in unrelated:
            if current_groups.get(name, []) != baseline_groups.get(name, []):
                raise ConcurrentAdoptionChange(
                    f"Unrelated selector state changed during adoption: {name}"
                )
    for name in target_names:
        actual = current_groups.get(name, [])
        allowed = [grouped.get(name, []) for grouped in variant_groups]
        if actual not in allowed:
            raise ConcurrentAdoptionChange(
                f"Transaction-owned selector state is ambiguous: {name}"
            )


def _resolve_target(
    provider: TargetProvider,
    request: Mapping[str, Any],
    context: InstallationContext,
    expected_binding: Mapping[str, Any],
) -> tuple[TargetAdapterEvidence, dict[str, Any]]:
    evidence = provider.resolve(request)
    _assert_evidence_binding(evidence, expected_binding, label="target")
    return evidence, inspect_target_descriptor(evidence, context)


def _assert_target_contract(
    inspected: Mapping[str, Any],
    expected_hash: str,
    *,
    require_materialized: bool,
) -> None:
    if canonical_json_hash(target_contract(inspected)) != expected_hash:
        raise ConcurrentAdoptionChange("Target resolution changed after the approved plan")
    if require_materialized and (
        inspected.get("materialization_status") != "verified" or inspected.get("errors")
    ):
        raise ConcurrentAdoptionChange(
            f"Target materialization is not verified: {inspected.get('errors')}"
        )


def _assert_prepared_selectors(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    target_plugins: Sequence[Mapping[str, Any]],
) -> None:
    expected = _expected_prepared_selectors(before["selectors"], target_plugins)
    if after["selectors"] != expected:
        raise AdoptionTransactionError(
            "Selector prepare changed state outside the exact bounded target diff"
        )


def _assert_active_selectors(
    state: Mapping[str, Any],
    target_plugins: Sequence[Mapping[str, Any]],
    prepared_selectors: Sequence[Mapping[str, Any]],
) -> None:
    expected = _expected_active_selectors(prepared_selectors, target_plugins)
    if state["selectors"] != expected:
        raise AdoptionTransactionError(
            "Selector activation changed state outside the exact bounded target diff"
        )


def _merge_selector_restore(
    current: Sequence[Mapping[str, Any]],
    initial: Sequence[Mapping[str, Any]],
    target_plugins: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    owned_names = {str(item["name"]) for item in target_plugins}
    merged = [
        copy.deepcopy(dict(item))
        for item in current
        if item.get("name") not in owned_names
    ]
    merged.extend(
        copy.deepcopy(dict(item))
        for item in initial
        if item.get("name") in owned_names
    )
    return sorted(merged, key=lambda item: (item["name"], item["selector"]))


def _owned_resource_keys(
    files: Mapping[str, Any], directories: Mapping[str, Any]
) -> list[str]:
    return sorted(
        key for key in [*files, *directories] if str(key).startswith("project:")
    )


def _resource_envelope(journal: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    snapshots: list[Mapping[str, Any]] = [journal["initial"]["resources"]]
    switch = journal.get("switch") or {}
    for name in ("runtime_resources", "receipt_resources", "post_resources"):
        value = switch.get(name)
        if isinstance(value, dict):
            snapshots.append(value)
    return snapshots


def _assert_resource_envelope(
    current: Mapping[str, Any],
    allowed: Sequence[Mapping[str, Any]],
    keys: Sequence[str],
) -> None:
    for section in ("files", "directories"):
        for key, actual in current.get(section, {}).items():
            if key not in keys:
                continue
            candidates = [
                snapshot.get(section, {}).get(key) for snapshot in allowed
            ]
            if actual not in candidates:
                raise ConcurrentAdoptionChange(
                    f"Transaction-owned resource is outside its recovery envelope: {key}"
                )


def _json_resource_snapshot(
    base: Mapping[str, Any], key: str, value: Any
) -> dict[str, Any]:
    result = copy.deepcopy(dict(base))
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    entry = result["files"][key]
    entry["exists"] = True
    entry["sha256"] = hashlib.sha256(payload).hexdigest()
    entry["size"] = len(payload)
    return result


def _restore_selectors(
    selector: SelectorAdapter,
    journal: Mapping[str, Any],
    *,
    expected_current: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    current_evidence = selector.inspect()
    expected_binding = journal["adapters"]["selector"]
    _assert_evidence_binding(current_evidence, expected_binding, label="selector")
    current = _selector_state(current_evidence)
    if expected_current is not None and current != dict(expected_current):
        raise ConcurrentAdoptionChange("Selector state changed after rollback preflight")
    desired = _merge_selector_restore(
        current["selectors"],
        journal["initial"]["selector"]["selectors"],
        _target_plugins(journal["plan"]["target"]),
    )
    # Selector adapters may own host state that is intentionally opaque to the
    # normalized selector list (for example a prepared marketplace
    # registration). Always delegate restore so that hidden transaction-owned
    # state is compensated even when the visible selectors already match.
    restored = selector.restore(
        desired,
        transaction_id=journal["transaction_id"],
        operation_id=f"restore-{journal['revision']}",
        expected_state_token=current["state_token"],
    )
    _assert_evidence_binding(restored, expected_binding, label="selector")
    result = _selector_state(selector.inspect())
    if result["selectors_sha256"] != canonical_json_hash(desired):
        raise AdoptionTransactionError("Selector restore could not be verified")
    return result


def _journal_path_from_journal(journal: Mapping[str, Any]) -> Path:
    values = journal["context"]
    context = InstallationContext(
        project=Path(values["project"]),
        user_home=Path(values["user_home"]),
        codex_home=Path(values["codex_home"]),
        product_os_home=Path(values["product_os_home"]),
        marketplace_registry=Path(values["marketplace_registry"]),
    )
    return _journal_path(context, journal["transaction_id"])


def _prepared_result(journal: Mapping[str, Any]) -> dict[str, Any]:
    prepared = journal.get("prepared") or {}
    return {
        "status": "committed" if journal["state"] == "committed" else "prepared",
        "transaction_id": journal["transaction_id"],
        "plan_hash": journal["plan_hash"],
        "prepared_state_hash": prepared.get("prepared_state_hash"),
        "journal_path": str(_journal_path_from_journal(journal)),
        "state": journal["state"],
    }


def _fail(faults: set[str] | None, name: str) -> None:
    if faults and name in faults:
        raise RuntimeError(f"Injected adoption transaction failure: {name}")


def _prepare_failure(
    context: InstallationContext,
    journal: dict[str, Any],
    provider: TargetProvider,
    selector: SelectorAdapter,
    error: Exception,
) -> None:
    latest = load_transaction(context, journal["transaction_id"])
    error_record = {"phase": "prepare", "message": str(error)}
    try:
        files, directories = resource_paths(context, latest["initial"]["receipt"])
        current_resources = snapshot_resources(context, files, directories)
        _assert_resource_envelope(
            current_resources,
            [latest["initial"]["resources"]],
            _owned_resource_keys(files, directories),
        )
        before = _selector_state(selector.inspect())
        targets = _target_plugins(latest["plan"]["target"])
        expected_prepared = _expected_prepared_selectors(
            latest["initial"]["selector"]["selectors"], targets
        )
        _assert_selector_transition_state(
            before["selectors"],
            latest["initial"]["selector"]["selectors"],
            expected_prepared,
            targets,
        )
        restored = _restore_selectors(
            selector, latest, expected_current=before
        )
        if restored["selectors"] != latest["initial"]["selector"]["selectors"]:
            raise AdoptionTransactionError("Prepare selector rollback is not exact")
        provider.cleanup_created(
            Path(latest["plan"]["target"]["materialized_root"]),
            transaction_id=latest["transaction_id"],
            operation_id="recover-prepare-target",
        )
        state = (
            "failed_no_mutation"
            if before["selectors_sha256"] == restored["selectors_sha256"]
            else "rolled_back"
        )
        _transition(context, latest, state, last_error=error_record)
    except Exception as recovery_error:
        _transition(
            context,
            latest,
            "manual_recovery_required",
            last_error={**error_record, "recovery_error": str(recovery_error)},
        )


def prepare_adoption(
    plan: Mapping[str, Any],
    *,
    confirmed_plan_hash: str,
    context: InstallationContext,
    adapters: AdapterRegistry,
    faults: set[str] | None = None,
) -> dict[str, Any]:
    candidate_plan = copy.deepcopy(dict(plan))
    validate_mutation_context(context)
    validate_adoption_plan(candidate_plan)
    if candidate_plan["status"] != "ready":
        raise AdoptionTransactionError("Blocked adoption plan cannot be prepared")
    if confirmed_plan_hash != candidate_plan["plan_hash"]:
        raise AdoptionTransactionError("Exact plan_hash confirmation is required")
    if candidate_plan["project"] != str(context.project):
        raise AdoptionTransactionError("Adoption plan project does not match context")

    with exclusive_lock(transaction_lock_path(context)):
        transactions = _existing_transactions(context)
        unresolved = [
            item for item in transactions if item["state"] not in CLOSED_STATES
        ]
        if len(unresolved) == 1 and (
            unresolved[0]["plan_hash"] == candidate_plan["plan_hash"]
            and unresolved[0]["state"] == "prepared"
        ):
            return _prepared_result(unresolved[0])
        if unresolved:
            existing = unresolved[0]
            raise AdoptionTransactionError(
                "Another unresolved adoption transaction already exists: "
                f"{existing['transaction_id']} ({existing['state']})"
            )
        for existing in transactions:
            if (
                existing["plan_hash"] == candidate_plan["plan_hash"]
                and existing["state"] == "committed"
            ):
                return _prepared_result(existing)

        target_binding = {
            "adapter_id": candidate_plan["target"]["evidence_adapter"],
            "adapter_version": candidate_plan["target"]["evidence_adapter_version"],
            "capability_fingerprint": candidate_plan["target"][
                "evidence_capability_fingerprint"
            ],
        }
        selector_binding = candidate_plan["selector_adapter_binding"]
        if not isinstance(selector_binding, dict):
            raise AdoptionTransactionError(
                "Approved plan lacks authoritative selector adapter binding"
            )
        provider = adapters.target(target_binding["adapter_id"])
        selector = adapters.selector(selector_binding["adapter_id"])
        _assert_adapter_binding(provider, target_binding, label="target")
        _assert_adapter_binding(selector, selector_binding, label="selector")

        selector_evidence = selector.inspect()
        _assert_evidence_binding(selector_evidence, selector_binding, label="selector")
        request = target_request_from_plan(candidate_plan)
        target_evidence, inspected_target = _resolve_target(
            provider, request, context, target_binding
        )
        fresh_detection = detect_installation(
            context.project,
            context=context,
            selector_observation=selector_evidence,
        )
        fresh_plan = build_adoption_plan(
            fresh_detection,
            target_evidence,
            context=context,
        )
        if fresh_plan["plan_hash"] != candidate_plan["plan_hash"]:
            raise ConcurrentAdoptionChange(
                "Installation or target changed after the approved plan"
            )
        if inspected_target != fresh_plan["target"]:
            raise ConcurrentAdoptionChange("Fresh target inspection is inconsistent")

        receipt, receipt_digest = _load_receipt_snapshot(context)
        if receipt_digest != fresh_detection["receipt"]["sha256"]:
            raise ConcurrentAdoptionChange(
                "Installation receipt changed while the approved state was captured"
            )
        staged_receipt = cpt_dist.ensure_receipt_v2(
            context.project, copy.deepcopy(receipt)
        )
        if candidate_plan["target"]["product_version"] != cpt_dist.PACKAGE_VERSION:
            raise AdoptionTransactionError(
                "Target version differs from the running Manager distribution version"
            )
        cpt_dist.validate_receipt_v2(staged_receipt)
        installation_id = staged_receipt["installation_id"]
        registry_data, registry_digest = RegistryStore(context).snapshot()
        if registry_digest != fresh_detection["registry"]["sha256"]:
            raise ConcurrentAdoptionChange(
                "Installation registry changed while the approved state was captured"
            )
        files, directories = resource_paths(context, receipt)
        initial_resources = snapshot_resources(context, files, directories)
        initial_selector = _selector_state(selector_evidence)
        if initial_resources["files"]["project:receipt"]["sha256"] != receipt_digest:
            raise ConcurrentAdoptionChange(
                "Installation receipt changed during the initial resource snapshot"
            )
        confirmed_selector = _selector_state(selector.inspect())
        if confirmed_selector != initial_selector:
            raise ConcurrentAdoptionChange(
                "Selector state changed during the initial transaction snapshot"
            )
        _target_evidence, confirmed_target = _resolve_target(
            provider, request, context, target_binding
        )
        if confirmed_target != inspected_target:
            raise ConcurrentAdoptionChange(
                "Target resolution changed during the initial transaction snapshot"
            )
        target_contract_sha256 = canonical_json_hash(target_contract(inspected_target))
        transaction_id = f"TX-{uuid.uuid4()}"
        created_at = utc_now()
        journal: dict[str, Any] = {
            "schema": TRANSACTION_SCHEMA,
            "transaction_id": transaction_id,
            "revision": 0,
            "state": "created",
            "project": str(context.project),
            "project_path_key": _path_key(context.project),
            "installation_id": installation_id,
            "context": context.as_dict(),
            "plan_hash": candidate_plan["plan_hash"],
            "plan": candidate_plan,
            "adapters": {"target": target_binding, "selector": selector_binding},
            "target_request": request,
            "target_contract_sha256": target_contract_sha256,
            "target_existed_before": Path(inspected_target["materialized_root"]).exists(),
            "initial": {
                "detection_state_hash": fresh_detection["state_hash"],
                "receipt_sha256": receipt_digest,
                "receipt": receipt,
                "registry_sha256": registry_digest,
                "registry": registry_data,
                "resources": initial_resources,
                "resources_sha256": canonical_json_hash(initial_resources),
                "selector": initial_selector,
            },
            "backup": {"manifest_path": None, "manifest_hash": None},
            "prepared": None,
            "switch": {},
            "result": None,
            "last_error": None,
            "created_at": created_at,
            "updated_at": created_at,
            "previous_journal_hash": None,
            "journal_hash": "",
        }
        journal = _write_new_journal(context, journal)
        try:
            backup = create_backup(
                context,
                transaction_id=transaction_id,
                plan_hash=candidate_plan["plan_hash"],
                installation_id=installation_id,
                files=files,
                directories=directories,
                selector_snapshot=selector_evidence,
            )
            if snapshot_resources(context, files, directories) != initial_resources:
                raise ConcurrentAdoptionChange(
                    "Installation changed while the backup was created"
                )
            journal = _transition(
                context,
                journal,
                "backed_up",
                backup={
                    "manifest_path": str(
                        Path(backup["backup_root"]) / "backup-manifest.json"
                    ),
                    "manifest_hash": backup["manifest_hash"],
                },
            )
            _fail(faults, "after_backup")

            journal = _transition(context, journal, "materializing")
            provider.materialize(
                target_evidence,
                Path(inspected_target["materialized_root"]),
                transaction_id=transaction_id,
                operation_id="materialize-target",
            )
            _fail(faults, "after_target_materialize")
            _target_evidence, verified_target = _resolve_target(
                provider, request, context, target_binding
            )
            _assert_target_contract(
                verified_target,
                target_contract_sha256,
                require_materialized=True,
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["verified_target"] = verified_target
            journal = _transition(
                context,
                journal,
                "target_verified",
                switch=switch_state,
            )

            target_plugins = _target_plugins(verified_target)
            journal = _transition(context, journal, "preparing_selectors")
            selector.prepare(
                target_plugins,
                transaction_id=transaction_id,
                operation_id="prepare-selectors",
                expected_state_token=initial_selector["state_token"],
            )
            _fail(faults, "after_selector_prepare")
            prepared_evidence = selector.inspect()
            _assert_evidence_binding(prepared_evidence, selector_binding, label="selector")
            prepared_selector = _selector_state(prepared_evidence)
            _assert_prepared_selectors(initial_selector, prepared_selector, target_plugins)
            prepared_resources = snapshot_resources(context, files, directories)
            if prepared_resources != initial_resources:
                raise ConcurrentAdoptionChange(
                    "Prepare changed active installation resources"
                )
            prepared_state: dict[str, Any] = {
                "schema": PREPARED_SCHEMA,
                "transaction_id": transaction_id,
                "plan_hash": candidate_plan["plan_hash"],
                "backup_manifest_hash": backup["manifest_hash"],
                "target_contract_sha256": target_contract_sha256,
                "target_inventory_sha256": verified_target["package_inventory"][
                    "inventory_sha256"
                ],
                "target": verified_target,
                "resources": prepared_resources,
                "resources_sha256": canonical_json_hash(prepared_resources),
                "selector": prepared_selector,
                "staged_receipt": staged_receipt,
                "staged_receipt_sha256": canonical_json_hash(staged_receipt),
                "runtime_quiescent": not bool(
                    cpt_dist.active_runtime_reasons(context.project)
                ),
            }
            if not prepared_state["runtime_quiescent"]:
                raise ConcurrentAdoptionChange(
                    "Product OS runtime became active during prepare"
                )
            prepared_state["prepared_state_hash"] = canonical_json_hash(prepared_state)
            journal = _transition(
                context,
                journal,
                "prepared",
                prepared=prepared_state,
                result={
                    "status": "prepared",
                    "transaction_id": transaction_id,
                    "prepared_state_hash": prepared_state["prepared_state_hash"],
                },
            )
            return _prepared_result(journal)
        except Exception as exc:
            _prepare_failure(context, journal, provider, selector, exc)
            raise


def _build_final_receipt(
    journal: Mapping[str, Any],
    runtime_receipt: dict[str, Any],
) -> dict[str, Any]:
    target = journal["prepared"]["target"]
    root = Path(target["materialized_root"])
    receipt = copy.deepcopy(runtime_receipt)
    superseded = {
        "plugin_scope": receipt.get("plugin_scope"),
        "plugin": copy.deepcopy(receipt.get("plugin", {})),
        "packs": copy.deepcopy(receipt.get("packs", [])),
        "installed_plugins": copy.deepcopy(receipt.get("installed_plugins", [])),
    }
    receipt["version"] = target["product_version"]
    receipt["product"]["version"] = target["product_version"]
    receipt["source_lineage"] = {
        "delivery_type": "git_marketplace",
        "repository": target["repository"],
        "marketplace_identity": target["marketplace_identity"],
        "release": target["product_version"],
        "ref": target["requested_ref"],
        "commit_sha": target["resolved_commit"],
        "manifest_sha256": target["package_manifest_sha256"],
        "observed_from": "product-os-manager",
    }
    receipt["installed_plugins"] = [
        {
            "name": plugin["name"],
            "selector": plugin["selector"],
            "marketplace_identity": target["marketplace_identity"],
            "version": target["product_version"],
            "payload_path": str(root / plugin["relative_path"]),
            "manifest_sha256": plugin["manifest_sha256"],
            "status": "active",
        }
        for plugin in target["plugins"]
    ]
    migrations = [
        item
        for item in receipt.get("applied_migrations", [])
        if isinstance(item, dict) and item.get("id") != journal["transaction_id"]
    ]
    migrations.append(
        {
            "id": journal["transaction_id"],
            "kind": "local-to-git-marketplace-adoption",
            "status": "applied",
            "plan_hash": journal["plan_hash"],
            "prepared_state_hash": journal["prepared"]["prepared_state_hash"],
            "target_commit": target["resolved_commit"],
            "backup_manifest_hash": journal["backup"]["manifest_hash"],
            "superseded_local_state": superseded,
        }
    )
    receipt["applied_migrations"] = migrations
    receipt["manager"] = {
        "last_transaction_id": journal["transaction_id"],
        "last_backup_path": str(Path(journal["backup"]["manifest_path"]).parent),
    }
    previous_plugin = copy.deepcopy(receipt.get("plugin", {}))
    receipt["plugin_scope"] = "none"
    receipt["plugin"] = {
        "scope": "none",
        "status": "superseded_by_manager",
        "legacy": previous_plugin,
    }
    receipt["packs"] = []
    receipt["updated_at"] = utc_now()
    cpt_dist.validate_receipt_v2(receipt)
    return receipt


def _registry_candidate(
    journal: Mapping[str, Any],
    receipt: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(journal["initial"]["registry"])
    entry = receipt_entry(Path(journal["project"]), receipt)
    candidate.setdefault("installations", {})[entry["installation_id"]] = entry
    return candidate, entry


def _target_evidence_from_journal(journal: Mapping[str, Any]) -> TargetAdapterEvidence:
    target = journal["prepared"]["target"]
    descriptor = {
        key: copy.deepcopy(target[key])
        for key in (
            "provider",
            "repository",
            "marketplace_identity",
            "requested_ref",
            "resolved_commit",
            "product_version",
            "package_manifest_sha256",
            "resolution_evidence",
            "materialized_root",
        )
    }
    descriptor["plugins"] = [
        {
            "name": item["name"],
            "selector": item["selector"],
            "relative_path": item["relative_path"],
            "manifest_sha256": item["manifest_sha256"],
        }
        for item in target["plugins"]
    ]
    binding = journal["adapters"]["target"]
    return TargetAdapterEvidence(
        binding["adapter_id"],
        descriptor,
        binding["adapter_version"],
        binding["capability_fingerprint"],
    )


def _verify_commit_state(
    context: InstallationContext,
    journal: Mapping[str, Any],
    selector: SelectorAdapter,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(code: str, passed: bool, detail: str) -> None:
        checks.append(
            {"code": code, "status": "PASS" if passed else "FAIL", "detail": detail}
        )

    runtime_ok, runtime_output = cpt_dist.runtime_validate(context.project)
    check("RUNTIME_VALID", runtime_ok, runtime_output)
    files, directories = resource_paths(context, journal["initial"]["receipt"])
    try:
        backup = verify_backup(
            context,
            Path(journal["backup"]["manifest_path"]),
            transaction_id=journal["transaction_id"],
            plan_hash=journal["plan_hash"],
            installation_id=journal["installation_id"],
            files=files,
            directories=directories,
            expected_selector_adapter=journal["adapters"]["selector"]["adapter_id"],
            expected_selector_state_token=journal["initial"]["selector"]["state_token"],
        )
        backup_ok = backup["manifest_hash"] == journal["backup"]["manifest_hash"]
        backup_detail = backup["manifest_hash"]
    except Exception as exc:
        backup_ok = False
        backup_detail = str(exc)
    check("BACKUP_VERIFIED", backup_ok, backup_detail)
    selector_evidence = selector.inspect()
    _assert_evidence_binding(
        selector_evidence, journal["adapters"]["selector"], label="selector"
    )
    selector_state = _selector_state(selector_evidence)
    try:
        _assert_active_selectors(
            selector_state,
            _target_plugins(journal["prepared"]["target"]),
            journal["prepared"]["selector"]["selectors"],
        )
        selector_ok = True
        selector_detail = "target selectors are exclusively active"
    except Exception as exc:
        selector_ok = False
        selector_detail = str(exc)
    check("SELECTORS_ACTIVE", selector_ok, selector_detail)
    detection = detect_installation(
        context.project,
        context=context,
        selector_observation=selector_evidence,
    )
    check(
        "RECEIPT_VALID",
        detection["receipt"]["valid"],
        str(detection["receipt"]["error"]),
    )
    receipt = cpt_dist.load_receipt(context.project)
    target = journal["prepared"]["target"]
    expected_lineage = {
        "delivery_type": "git_marketplace",
        "repository": target["repository"],
        "marketplace_identity": target["marketplace_identity"],
        "release": target["product_version"],
        "ref": target["requested_ref"],
        "commit_sha": target["resolved_commit"],
        "manifest_sha256": target["package_manifest_sha256"],
        "observed_from": "product-os-manager",
    }
    migration = next(
        (
            item
            for item in receipt.get("applied_migrations", [])
            if isinstance(item, dict) and item.get("id") == journal["transaction_id"]
        ),
        None,
    )
    lineage_ok = (
        receipt.get("source_lineage") == expected_lineage
        and (receipt.get("manager") or {}).get("last_transaction_id")
        == journal["transaction_id"]
        and isinstance(migration, dict)
        and migration.get("status") == "applied"
    )
    check("LINEAGE_BOUND", lineage_ok, str(receipt.get("source_lineage")))
    root = Path(target["materialized_root"])
    expected_plugins = [
        {
            "name": plugin["name"],
            "selector": plugin["selector"],
            "marketplace_identity": target["marketplace_identity"],
            "version": target["product_version"],
            "payload_path": str(root / plugin["relative_path"]),
            "manifest_sha256": plugin["manifest_sha256"],
            "status": "active",
        }
        for plugin in target["plugins"]
    ]
    check(
        "RECEIPT_TARGET_PLUGINS_EXACT",
        receipt.get("installed_plugins") == expected_plugins,
        str(receipt.get("installed_plugins")),
    )
    expected_migration = {
        "id": journal["transaction_id"],
        "kind": "local-to-git-marketplace-adoption",
        "status": "applied",
        "plan_hash": journal["plan_hash"],
        "prepared_state_hash": journal["prepared"]["prepared_state_hash"],
        "target_commit": target["resolved_commit"],
        "backup_manifest_hash": journal["backup"]["manifest_hash"],
    }
    migration_ok = isinstance(migration, dict) and all(
        migration.get(key) == value for key, value in expected_migration.items()
    )
    check("MIGRATION_BOUND", migration_ok, str(migration))
    unhealthy_managed = [
        item["path"]
        for item in detection["managed_files"]["entries"]
        if item["status"] not in {"healthy", "mutable"}
    ]
    check("MANAGED_FILES_HEALTHY", not unhealthy_managed, str(unhealthy_managed))
    unhealthy_plugins = [
        f"{item['name']}:{item['status']}"
        for item in detection["plugins"]
        if item["status"] != "healthy"
    ]
    check("PLUGINS_HEALTHY", not unhealthy_plugins, str(unhealthy_plugins))
    check(
        "REGISTRY_CONSISTENT",
        detection["registry"]["entry_matches_receipt"] is True,
        str(detection["registry"].get("error")),
    )
    inspected = inspect_target_descriptor(_target_evidence_from_journal(journal), context)
    target_ok = (
        canonical_json_hash(target_contract(inspected))
        == journal["target_contract_sha256"]
        and inspected["materialization_status"] == "verified"
        and not inspected["errors"]
    )
    check("TARGET_VERIFIED", target_ok, str(inspected["errors"]))
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    return {
        "schema": "product-os-migration-doctor-report-v1",
        "status": status,
        "transaction_id": journal["transaction_id"],
        "checks": checks,
        "lifecycle": {"status": "unsupported", "adapter": None},
    }


def _scoped_registry_restore(
    context: InstallationContext,
    journal: Mapping[str, Any],
    *,
    force: bool,
    expected_digest: str | None | object = _UNSET,
) -> None:
    store = RegistryStore(context)
    current, digest = store.snapshot()
    if expected_digest is not _UNSET and digest != expected_digest:
        raise ConcurrentAdoptionChange("Registry changed after rollback preflight")
    initial = journal["initial"]["registry"]
    installation_id = journal["installation_id"]
    initial_entry = initial.get("installations", {}).get(installation_id)
    owned_entry = journal.get("switch", {}).get("registry_entry")
    current_entry = current.get("installations", {}).get(installation_id)
    if current_entry == initial_entry:
        return
    if current_entry != owned_entry and not force:
        raise ConcurrentAdoptionChange(
            "Registry installation entry changed after transaction commit"
        )
    candidate = copy.deepcopy(current)
    if initial_entry is None:
        candidate.setdefault("installations", {}).pop(installation_id, None)
    else:
        candidate.setdefault("installations", {})[installation_id] = copy.deepcopy(
            initial_entry
        )
    if journal["initial"]["registry_sha256"] is None and not candidate.get(
        "installations"
    ):
        with exclusive_lock(store.lock_path):
            if file_sha256(store.path) != digest:
                raise ConcurrentAdoptionChange("Registry changed during scoped rollback")
            if store.path.exists():
                store.path.unlink()
        return
    store.save(candidate, expected_digest=digest)


def _registry_recovery_snapshot(
    context: InstallationContext,
    journal: Mapping[str, Any],
    *,
    force: bool,
) -> tuple[dict[str, Any], str | None]:
    current, digest = RegistryStore(context).snapshot()
    installation_id = journal["installation_id"]
    current_entry = current.get("installations", {}).get(installation_id)
    initial_entry = (
        journal["initial"]["registry"].get("installations", {}).get(installation_id)
    )
    owned_entry = journal.get("switch", {}).get("registry_entry")
    allowed = [initial_entry]
    if owned_entry is not None:
        allowed.append(owned_entry)
    if current_entry not in allowed and not force:
        raise ConcurrentAdoptionChange(
            "Registry installation entry is outside its recovery envelope"
        )
    return current, digest


def _compensate_switch(
    context: InstallationContext,
    journal: dict[str, Any],
    selector: SelectorAdapter,
    *,
    error: Exception,
    force: bool = False,
    allow_unrelated_selector_drift: bool = False,
) -> dict[str, Any]:
    latest = load_transaction(context, journal["transaction_id"])
    error_record = {"phase": "switch", "message": str(error)}
    files, directories = resource_paths(context, latest["initial"]["receipt"])
    restore_keys = _owned_resource_keys(files, directories)
    try:
        recover_incomplete = getattr(selector, "recover_incomplete_activation", None)
        if callable(recover_incomplete):
            recover_incomplete(transaction_id=latest["transaction_id"])
        backup = verify_backup(
            context,
            Path(latest["backup"]["manifest_path"]),
            transaction_id=latest["transaction_id"],
            plan_hash=latest["plan_hash"],
            installation_id=latest["installation_id"],
            files=files,
            directories=directories,
            expected_selector_adapter=latest["adapters"]["selector"]["adapter_id"],
            expected_selector_state_token=latest["initial"]["selector"]["state_token"],
        )
        current_resources = snapshot_resources(context, files, directories)
        if not force:
            _assert_resource_envelope(
                current_resources,
                _resource_envelope(latest),
                restore_keys,
            )
        current_selector_evidence = selector.inspect()
        _assert_evidence_binding(
            current_selector_evidence,
            latest["adapters"]["selector"],
            label="selector",
        )
        current_selector = _selector_state(current_selector_evidence)
        targets = _target_plugins(latest["prepared"]["target"])
        prepared_selectors = latest["prepared"]["selector"]["selectors"]
        active_selectors = latest.get("switch", {}).get(
            "expected_active_selectors"
        ) or _expected_active_selectors(prepared_selectors, targets)
        if not force:
            _assert_selector_envelope(
                current_selector["selectors"],
                [
                    latest["initial"]["selector"]["selectors"],
                    prepared_selectors,
                    active_selectors,
                ],
                targets,
                allow_unrelated_drift=allow_unrelated_selector_drift,
            )
        _registry_data, registry_digest = _registry_recovery_snapshot(
            context, latest, force=force
        )
        preflight = {
            "resources_sha256": canonical_json_hash(current_resources),
            "selector_state_token": current_selector["state_token"],
            "selector_sha256": current_selector["selectors_sha256"],
            "registry_sha256": registry_digest,
        }
    except Exception as recovery_error:
        if latest["state"] == "manual_recovery_required":
            changed = copy.deepcopy(latest)
            changed["last_error"] = {
                **error_record,
                "recovery_error": str(recovery_error),
            }
            return _save_journal(context, changed)
        return _transition(
            context,
            latest,
            "manual_recovery_required",
            last_error={**error_record, "recovery_error": str(recovery_error)},
        )

    if latest["state"] != "rolling_back":
        switch_state = copy.deepcopy(latest.get("switch", {}))
        switch_state["rollback"] = {
            "origin_state": latest["state"],
            "force": force,
            "preflight": preflight,
            "preflight_sha256": canonical_json_hash(preflight),
            "completed_steps": [],
        }
        latest = _transition(
            context,
            latest,
            "rolling_back",
            last_error=error_record,
            switch=switch_state,
        )
    try:
        _restore_selectors(
            selector, latest, expected_current=current_selector
        )
        switch_state = copy.deepcopy(latest["switch"])
        switch_state["rollback"]["completed_steps"] = ["selectors"]
        changed = copy.deepcopy(latest)
        changed["switch"] = switch_state
        latest = _save_journal(context, changed)
        restore_backup(
            context,
            backup,
            files=files,
            directories=directories,
            expected_current=current_resources,
            keys=restore_keys,
        )
        switch_state = copy.deepcopy(latest["switch"])
        switch_state["rollback"]["completed_steps"] = ["selectors", "resources"]
        changed = copy.deepcopy(latest)
        changed["switch"] = switch_state
        latest = _save_journal(context, changed)
        _scoped_registry_restore(
            context,
            latest,
            force=force,
            expected_digest=registry_digest,
        )
        restored = snapshot_resources(context, files, directories)
        for section in ("files", "directories"):
            for key, expected in latest["initial"]["resources"][section].items():
                if key in restore_keys and restored[section][key] != expected:
                    raise AdoptionTransactionError(f"Rollback verification failed: {key}")
        restored_selector = _selector_state(selector.inspect())
        initial_groups = _selector_groups(
            latest["initial"]["selector"]["selectors"]
        )
        restored_groups = _selector_groups(restored_selector["selectors"])
        for target in targets:
            name = target["name"]
            if restored_groups.get(name, []) != initial_groups.get(name, []):
                raise AdoptionTransactionError(
                    f"Selector rollback verification failed: {name}"
                )
        _registry_recovery_snapshot(context, latest, force=False)
        return _transition(
            context,
            latest,
            "rolled_back",
            result={
                "status": "rolled_back",
                "transaction_id": latest["transaction_id"],
            },
        )
    except Exception as recovery_error:
        return _transition(
            context,
            latest,
            "manual_recovery_required",
            last_error={**error_record, "recovery_error": str(recovery_error)},
        )


def switch_adoption(
    transaction_id: str,
    *,
    confirmed_prepared_state_hash: str,
    context: InstallationContext,
    adapters: AdapterRegistry,
    faults: set[str] | None = None,
) -> dict[str, Any]:
    validate_mutation_context(context)
    observed = load_transaction(context, transaction_id)
    observed_prepared = observed.get("prepared") or {}
    if confirmed_prepared_state_hash != observed_prepared.get("prepared_state_hash"):
        raise AdoptionTransactionError(
            "Exact prepared-state hash confirmation is required"
        )
    with exclusive_lock(transaction_lock_path(context)):
        journal = load_transaction(context, transaction_id)
        prepared = journal.get("prepared") or {}
        if confirmed_prepared_state_hash != prepared.get("prepared_state_hash"):
            raise AdoptionTransactionError(
                "Exact prepared-state hash confirmation is required"
            )
        if journal["state"] == "committed":
            return copy.deepcopy(journal["result"])
        if journal["state"] != "prepared":
            raise AdoptionTransactionError(
                f"Transaction is not awaiting switch confirmation: {journal['state']}"
            )
        prepared = journal["prepared"]
        provider = adapters.target(journal["adapters"]["target"]["adapter_id"])
        selector = adapters.selector(journal["adapters"]["selector"]["adapter_id"])
        _assert_adapter_binding(
            provider, journal["adapters"]["target"], label="target"
        )
        _assert_adapter_binding(
            selector, journal["adapters"]["selector"], label="selector"
        )
        files, directories = resource_paths(context, journal["initial"]["receipt"])
        if snapshot_resources(context, files, directories) != prepared["resources"]:
            raise ConcurrentAdoptionChange("Installation resources changed after prepare")
        current_selector = _selector_state(selector.inspect())
        if current_selector != prepared["selector"]:
            raise ConcurrentAdoptionChange("Selector state changed after prepare")
        if cpt_dist.active_runtime_reasons(context.project):
            raise ConcurrentAdoptionChange("Product OS runtime became active after prepare")
        verify_backup(
            context,
            Path(journal["backup"]["manifest_path"]),
            transaction_id=transaction_id,
            plan_hash=journal["plan_hash"],
            installation_id=journal["installation_id"],
            files=files,
            directories=directories,
            expected_selector_adapter=journal["adapters"]["selector"]["adapter_id"],
            expected_selector_state_token=journal["initial"]["selector"]["state_token"],
        )
        _target_evidence, verified_target = _resolve_target(
            provider,
            journal["target_request"],
            context,
            journal["adapters"]["target"],
        )
        _assert_target_contract(
            verified_target,
            journal["target_contract_sha256"],
            require_materialized=True,
        )

        try:
            journal = _transition(context, journal, "refreshing_runtime")
            runtime_receipt = copy.deepcopy(prepared["staged_receipt"])
            cpt_dist.refresh_runtime_scaffold(
                context.project,
                runtime_receipt,
                distribution_root=Path(verified_target["materialized_root"]),
            )
            runtime_resources = snapshot_resources(context, files, directories)
            switch_state = copy.deepcopy(journal["switch"])
            switch_state.update(
                {
                    "runtime_resources": runtime_resources,
                    "runtime_resources_sha256": canonical_json_hash(runtime_resources),
                }
            )
            journal = _transition(
                context,
                journal,
                "runtime_refreshed",
                switch=switch_state,
            )
            final_receipt = _build_final_receipt(journal, runtime_receipt)
            receipt_resources = _json_resource_snapshot(
                runtime_resources, "project:receipt", final_receipt
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state.update(
                {
                    "receipt_candidate": final_receipt,
                    "receipt_candidate_sha256": canonical_json_hash(final_receipt),
                    "receipt_resources": receipt_resources,
                    "receipt_resources_sha256": canonical_json_hash(receipt_resources),
                }
            )
            changed = copy.deepcopy(journal)
            changed["switch"] = switch_state
            journal = _save_journal(context, changed)
            _fail(faults, "after_runtime_refresh")

            target_plugins = _target_plugins(verified_target)
            expected_active_selectors = _expected_active_selectors(
                prepared["selector"]["selectors"], target_plugins
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["expected_active_selectors"] = expected_active_selectors
            changed = copy.deepcopy(journal)
            changed["switch"] = switch_state
            journal = _save_journal(context, changed)
            journal = _transition(context, journal, "activating_selectors")
            selector.activate(
                target_plugins,
                transaction_id=transaction_id,
                operation_id="activate-selectors",
                expected_state_token=prepared["selector"]["state_token"],
            )
            active_evidence = selector.inspect()
            _assert_evidence_binding(
                active_evidence,
                journal["adapters"]["selector"],
                label="selector",
            )
            active_selector = _selector_state(active_evidence)
            _assert_active_selectors(
                active_selector,
                target_plugins,
                prepared["selector"]["selectors"],
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["active_selector"] = active_selector
            journal = _transition(
                context,
                journal,
                "selectors_activated",
                switch=switch_state,
            )
            _fail(faults, "after_selector_activate")

            receipt_path = context.project / ".cpt" / "install.json"
            if file_sha256(receipt_path) != journal["initial"]["receipt_sha256"]:
                raise ConcurrentAdoptionChange("Installation receipt changed before commit")
            journal = _transition(context, journal, "writing_receipt")
            atomic_write_json(receipt_path, final_receipt)
            committed_receipt = cpt_dist.load_receipt(context.project)
            if canonical_json_hash(committed_receipt) != canonical_json_hash(final_receipt):
                raise AdoptionTransactionError(
                    "Committed receipt does not match its transaction candidate"
                )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["receipt_after_sha256"] = file_sha256(receipt_path)
            written_resources = snapshot_resources(context, files, directories)
            if written_resources != journal["switch"]["receipt_resources"]:
                raise AdoptionTransactionError(
                    "Receipt write changed resources outside its declared intent"
                )
            journal = _transition(
                context,
                journal,
                "receipt_written",
                switch=switch_state,
            )
            _fail(faults, "after_receipt_write")

            _registry_data, registry_digest = RegistryStore(context).snapshot()
            if registry_digest != journal["initial"]["registry_sha256"]:
                raise ConcurrentAdoptionChange(
                    "Installation registry changed before commit"
                )
            registry_candidate, registry_entry_value = _registry_candidate(
                journal, final_receipt
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["registry_entry"] = registry_entry_value
            journal = _transition(
                context,
                journal,
                "writing_registry",
                switch=switch_state,
            )
            registry_after_sha256 = RegistryStore(context).save(
                registry_candidate,
                expected_digest=registry_digest,
            )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state.update(
                {
                    "registry_after_sha256": registry_after_sha256,
                }
            )
            journal = _transition(
                context,
                journal,
                "registry_written",
                switch=switch_state,
            )
            _fail(faults, "after_registry_write")

            journal = _transition(context, journal, "verifying")
            doctor = _verify_commit_state(context, journal, selector)
            _fail(faults, "after_doctor")
            if doctor["status"] != "PASS":
                raise AdoptionTransactionError(
                    "Migration doctor rejected the candidate committed state: "
                    + "; ".join(
                        f"{item['code']}={item['detail']}"
                        for item in doctor["checks"]
                        if item["status"] == "FAIL"
                    )
                )
            post_resources = snapshot_resources(context, files, directories)
            _assert_resource_envelope(
                post_resources,
                [journal["switch"]["receipt_resources"]],
                _owned_resource_keys(files, directories),
            )
            final_selector = _selector_state(selector.inspect())
            if final_selector != journal["switch"]["active_selector"]:
                raise ConcurrentAdoptionChange(
                    "Selector state changed after migration doctor verification"
                )
            final_registry, final_registry_digest = RegistryStore(context).snapshot()
            if final_registry_digest != journal["switch"]["registry_after_sha256"]:
                raise ConcurrentAdoptionChange(
                    "Registry changed after migration doctor verification"
                )
            if (
                final_registry.get("installations", {}).get(journal["installation_id"])
                != journal["switch"]["registry_entry"]
            ):
                raise ConcurrentAdoptionChange(
                    "Registry installation entry changed after migration doctor verification"
                )
            result = {
                "status": "committed",
                "transaction_id": transaction_id,
                "plan_hash": journal["plan_hash"],
                "prepared_state_hash": prepared["prepared_state_hash"],
                "doctor": doctor,
                "legacy_retirement": {
                    "status": "retained",
                    "reason": "registry completeness is not proven",
                },
            }
            switch_state = copy.deepcopy(journal["switch"])
            switch_state.update(
                {
                    "doctor_report_sha256": canonical_json_hash(doctor),
                    "post_resources": post_resources,
                    "post_resources_sha256": canonical_json_hash(post_resources),
                }
            )
            journal = _transition(
                context,
                journal,
                "committed",
                switch=switch_state,
                result=result,
            )
            return copy.deepcopy(journal["result"])
        except Exception as exc:
            recovery = _compensate_switch(
                context,
                journal,
                selector,
                error=exc,
            )
            if recovery["state"] == "manual_recovery_required":
                raise AdoptionTransactionError(
                    f"Switch failed and automatic recovery is incomplete: {exc}; "
                    f"{recovery['last_error'].get('recovery_error')}"
                ) from exc
            raise


def rollback_adoption(
    transaction_id: str,
    *,
    context: InstallationContext,
    adapters: AdapterRegistry,
    force: bool = False,
    confirmed_current_state_hash: str | None = None,
) -> dict[str, Any]:
    validate_mutation_context(context)
    with exclusive_lock(transaction_lock_path(context)):
        journal = load_transaction(context, transaction_id)
        if journal["state"] == "rolled_back":
            return copy.deepcopy(journal["result"])
        if journal["state"] not in {
            "prepared",
            "committed",
            "rolling_back",
            "manual_recovery_required",
        }:
            raise AdoptionTransactionError(
                f"Transaction cannot be rolled back from state: {journal['state']}"
            )
        selector = adapters.selector(journal["adapters"]["selector"]["adapter_id"])
        _assert_adapter_binding(
            selector, journal["adapters"]["selector"], label="selector"
        )
        files, directories = resource_paths(context, journal["initial"]["receipt"])
        if journal["state"] == "manual_recovery_required" and not force:
            raise AdoptionTransactionError(
                "Manual recovery requires force plus exact current-state confirmation"
            )
        emergency = None
        if force:
            current_resources = snapshot_resources(context, files, directories)
            current_selector = _selector_state(selector.inspect())
            current_registry, current_registry_digest = RegistryStore(context).snapshot()
            observed = {
                "resources": current_resources,
                "selector": current_selector,
                "registry_sha256": current_registry_digest,
                "registry_entry": current_registry.get("installations", {}).get(
                    journal["installation_id"]
                ),
            }
            observed_hash = canonical_json_hash(observed)
            if confirmed_current_state_hash != observed_hash:
                raise AdoptionTransactionError(
                    "Force rollback requires exact current-state hash confirmation: "
                    f"{observed_hash}"
                )
            emergency_id = f"TX-{uuid.uuid4()}"
            emergency = create_backup(
                context,
                transaction_id=emergency_id,
                plan_hash=journal["plan_hash"],
                installation_id=journal["installation_id"],
                files=files,
                directories=directories,
                selector_snapshot=selector.inspect(),
            )
            rechecked_registry, rechecked_registry_digest = RegistryStore(
                context
            ).snapshot()
            rechecked = {
                "resources": snapshot_resources(context, files, directories),
                "selector": _selector_state(selector.inspect()),
                "registry_sha256": rechecked_registry_digest,
                "registry_entry": rechecked_registry
                .get("installations", {})
                .get(journal["installation_id"]),
            }
            if canonical_json_hash(rechecked) != observed_hash:
                raise ConcurrentAdoptionChange(
                    "Adoption state changed while the emergency backup was created"
                )
            switch_state = copy.deepcopy(journal["switch"])
            switch_state["emergency_backup"] = {
                "transaction_id": emergency_id,
                "manifest_path": str(
                    Path(emergency["backup_root"]) / "backup-manifest.json"
                ),
                "manifest_hash": emergency["manifest_hash"],
            }
            changed = copy.deepcopy(journal)
            changed["switch"] = switch_state
            journal = _save_journal(context, changed)
        result = _compensate_switch(
            context,
            journal,
            selector,
            error=AdoptionTransactionError("User-requested rollback"),
            force=force,
            allow_unrelated_selector_drift=True,
        )
        if result["state"] != "rolled_back":
            raise AdoptionTransactionError(
                f"Rollback requires manual recovery: {result['last_error']}"
            )
        response = copy.deepcopy(result["result"])
        if emergency is not None:
            response["emergency_backup_manifest_hash"] = emergency["manifest_hash"]
        return response


def recover_adoption(
    transaction_id: str,
    *,
    context: InstallationContext,
    adapters: AdapterRegistry,
) -> dict[str, Any]:
    """Reconcile an orphaned journal without guessing through unknown drift."""

    validate_mutation_context(context)
    observed = load_transaction(context, transaction_id)
    if observed["state"] in CLOSED_STATES:
        return {
            "status": observed["state"],
            "transaction_id": transaction_id,
            "journal_hash": observed["journal_hash"],
        }
    if observed["state"] == "manual_recovery_required":
        return {
            "status": "manual_recovery_required",
            "transaction_id": transaction_id,
            "journal_hash": observed["journal_hash"],
            "last_error": copy.deepcopy(observed.get("last_error")),
        }

    with exclusive_lock(transaction_lock_path(context)):
        journal = load_transaction(context, transaction_id)
        if journal["state"] in CLOSED_STATES:
            return {
                "status": journal["state"],
                "transaction_id": transaction_id,
                "journal_hash": journal["journal_hash"],
            }
        if journal["state"] == "manual_recovery_required":
            return {
                "status": "manual_recovery_required",
                "transaction_id": transaction_id,
                "journal_hash": journal["journal_hash"],
                "last_error": copy.deepcopy(journal.get("last_error")),
            }
        if cpt_dist.active_runtime_reasons(context.project):
            return {
                "status": "blocked_runtime_active",
                "transaction_id": transaction_id,
                "state": journal["state"],
            }
        provider = adapters.target(journal["adapters"]["target"]["adapter_id"])
        selector = adapters.selector(journal["adapters"]["selector"]["adapter_id"])
        _assert_adapter_binding(
            provider, journal["adapters"]["target"], label="target"
        )
        _assert_adapter_binding(
            selector, journal["adapters"]["selector"], label="selector"
        )
        prepare_states = {
            "created",
            "backed_up",
            "materializing",
            "target_verified",
            "preparing_selectors",
        }
        if journal["state"] in prepare_states:
            _prepare_failure(
                context,
                journal,
                provider,
                selector,
                AdoptionTransactionError(
                    f"Recovered orphaned prepare state: {journal['state']}"
                ),
            )
            recovered = load_transaction(context, transaction_id)
            return {
                "status": recovered["state"],
                "transaction_id": transaction_id,
                "journal_hash": recovered["journal_hash"],
            }
        if journal["state"] == "prepared":
            try:
                files, directories = resource_paths(
                    context, journal["initial"]["receipt"]
                )
                current_resources = snapshot_resources(context, files, directories)
                _assert_resource_envelope(
                    current_resources,
                    [journal["prepared"]["resources"]],
                    _owned_resource_keys(files, directories),
                )
                current_selector = _selector_state(selector.inspect())
                if current_selector != journal["prepared"]["selector"]:
                    raise ConcurrentAdoptionChange(
                        "Prepared selector state changed before recovery"
                    )
                verify_backup(
                    context,
                    Path(journal["backup"]["manifest_path"]),
                    transaction_id=transaction_id,
                    plan_hash=journal["plan_hash"],
                    installation_id=journal["installation_id"],
                    files=files,
                    directories=directories,
                    expected_selector_adapter=journal["adapters"]["selector"][
                        "adapter_id"
                    ],
                    expected_selector_state_token=journal["initial"]["selector"][
                        "state_token"
                    ],
                )
                _target_evidence, target = _resolve_target(
                    provider,
                    journal["target_request"],
                    context,
                    journal["adapters"]["target"],
                )
                _assert_target_contract(
                    target,
                    journal["target_contract_sha256"],
                    require_materialized=True,
                )
                return _prepared_result(journal)
            except Exception as exc:
                changed = _transition(
                    context,
                    journal,
                    "manual_recovery_required",
                    last_error={"phase": "recover-prepared", "message": str(exc)},
                )
                return {
                    "status": changed["state"],
                    "transaction_id": transaction_id,
                    "journal_hash": changed["journal_hash"],
                    "last_error": copy.deepcopy(changed["last_error"]),
                }
        recovered = _compensate_switch(
            context,
            journal,
            selector,
            error=AdoptionTransactionError(
                f"Recovered orphaned switch state: {journal['state']}"
            ),
        )
        return {
            "status": recovered["state"],
            "transaction_id": transaction_id,
            "journal_hash": recovered["journal_hash"],
            "last_error": copy.deepcopy(recovered.get("last_error")),
        }


__all__ = [
    "AdoptionTransactionError",
    "ConcurrentAdoptionChange",
    "load_transaction",
    "prepare_adoption",
    "recover_adoption",
    "rollback_adoption",
    "switch_adoption",
    "target_contract",
    "target_request_from_plan",
    "transaction_directory",
    "validate_mutation_context",
    "validate_transaction_journal",
]
