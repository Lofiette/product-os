from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .adapters.base import AdapterRegistry
from .context import InstallationContext
from .state import lock_is_held, read_json, utc_now
from .transaction import (
    AdoptionTransactionError,
    _assert_adapter_binding,
    _existing_transactions,
    _verify_commit_state,
    load_transaction,
    transaction_lock_path,
    validate_mutation_context,
)

DOCTOR_SCHEMA = "product-os-migration-doctor-report-v1"


def migration_doctor_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "migration-doctor-report-v1.schema.json"


def validate_migration_doctor_report(report: dict[str, Any]) -> None:
    schema = read_json(migration_doctor_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(report),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise AdoptionTransactionError(f"Invalid migration doctor report: {details}")
    expected = "PASS" if all(item.get("status") == "PASS" for item in report["checks"]) else "FAIL"
    if report.get("status") != expected:
        raise AdoptionTransactionError("Invalid migration doctor report: status does not match checks")


def _latest_transaction(context: InstallationContext) -> dict[str, Any]:
    transactions = _existing_transactions(context)
    if not transactions:
        raise AdoptionTransactionError("No Product OS adoption transaction exists for this project")
    return max(
        transactions,
        key=lambda item: (
            str(item.get("updated_at", "")),
            int(item.get("revision", 0)),
            str(item.get("transaction_id", "")),
        ),
    )


def run_migration_doctor(
    context: InstallationContext,
    adapters: AdapterRegistry,
    *,
    transaction_id: str | None = None,
) -> dict[str, Any]:
    """Revalidate a committed adoption without mutating installation state."""

    validate_mutation_context(context)
    journal = (
        load_transaction(context, transaction_id)
        if transaction_id is not None
        else _latest_transaction(context)
    )
    checks: list[dict[str, str]] = []

    def check(code: str, passed: bool, detail: str) -> None:
        checks.append(
            {"code": code, "status": "PASS" if passed else "FAIL", "detail": detail}
        )

    lock_path = transaction_lock_path(context)
    busy = lock_is_held(lock_path)
    check(
        "TRANSACTION_QUIESCENT",
        not busy,
        "no adoption transaction lock is held" if not busy else "an adoption transaction is active",
    )
    committed = journal["state"] == "committed"
    check(
        "TRANSACTION_COMMITTED",
        committed,
        f"transaction state is {journal['state']}",
    )

    selector = None
    adapters_ok = False
    try:
        provider = adapters.target(journal["adapters"]["target"]["adapter_id"])
        selector = adapters.selector(journal["adapters"]["selector"]["adapter_id"])
        _assert_adapter_binding(provider, journal["adapters"]["target"], label="target")
        _assert_adapter_binding(selector, journal["adapters"]["selector"], label="selector")
        adapters_ok = True
        adapter_detail = "target and selector adapters match the committed journal"
    except Exception as exc:
        adapter_detail = str(exc)
    check("ADAPTER_BINDINGS", adapters_ok, adapter_detail)

    lifecycle: dict[str, Any] = {"status": "unsupported", "adapter": None}
    if not busy and committed and adapters_ok and selector is not None:
        try:
            internal = _verify_commit_state(context, journal, selector)
            checks.extend(internal["checks"])
            lifecycle = internal["lifecycle"]
        except Exception as exc:
            check("DOCTOR_EXECUTION", False, str(exc))

    stable = False
    stable_detail = "transaction changed while doctor was running"
    if not lock_is_held(lock_path):
        try:
            latest = load_transaction(context, journal["transaction_id"])
            stable = latest["journal_hash"] == journal["journal_hash"]
            if stable:
                stable_detail = "journal hash remained stable during readback"
        except Exception as exc:
            stable_detail = str(exc)
    check("JOURNAL_STABLE", stable, stable_detail)

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    report = {
        "schema": DOCTOR_SCHEMA,
        "status": status,
        "transaction_id": journal["transaction_id"],
        "transaction_state": journal["state"],
        "journal_hash": journal["journal_hash"],
        "observed_at": utc_now(),
        "checks": checks,
        "lifecycle": lifecycle,
    }
    validate_migration_doctor_report(report)
    return report


__all__ = [
    "DOCTOR_SCHEMA",
    "migration_doctor_schema_path",
    "run_migration_doctor",
    "validate_migration_doctor_report",
]
