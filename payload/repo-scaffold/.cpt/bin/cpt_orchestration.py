#!/usr/bin/env python3
from __future__ import annotations

import copy
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import fastjsonschema
import yaml

SCHEMA_VERSION = "4.0-alpha7"
TERMINAL_CONTRACT_STATUSES = {
    "completed",
    "partial",
    "failed",
    "insufficient_evidence",
    "cancelled",
    "timed_out",
    "skipped",
}
ACTIVE_CONTRACT_STATUSES = {"active", "returned", "cancel_requested", "needs_reconcile"}
SUCCESS_RESULT_STATUS = "success"
RESULT_STATUSES = {"success", "partial", "failure", "insufficient_evidence", "cancelled"}
WRITE_PERMISSION_MODES = {"workspace_write"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def atomic_write_yaml(path: Path, data: Any) -> None:
    atomic_write_text(path, dump_yaml(data))


def canonical_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=True, allow_unicode=True)


def digest(data: Any) -> str | None:
    if data is None:
        return None
    return hashlib.sha256(canonical_yaml(data).encode("utf-8")).hexdigest()


@contextmanager
def orchestration_lock(root: Path, timeout: float = 10.0):
    lock = root / ".cpt" / ".orchestration.lock"
    deadline = time.time() + timeout
    fd = None
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()}\ncreated_at={utc_now()}\n".encode())
        except FileExistsError:
            if time.time() >= deadline:
                raise RuntimeError(f"Orchestration lock timeout: {lock}")
            time.sleep(0.1)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def cpt_paths(root: Path) -> dict[str, Path]:
    cpt = root / ".cpt"
    orch = cpt / "orchestrations"
    return {
        "cpt": cpt,
        "current": cpt / "current.yaml",
        "task_index": cpt / "task-index.yaml",
        "leases": cpt / "leases",
        "workers": cpt / "workers",
        "worker_archetypes": cpt / "worker-archetypes.json",
        "orchestrations": orch,
        "contracts": orch / "contracts",
        "results": orch / "results",
        "worktrees": cpt / "worktrees",
        "schema_bundle": cpt / "schema-bundle.json",
    }


def ensure_dirs(root: Path) -> None:
    p = cpt_paths(root)
    for key in ("orchestrations", "contracts", "results", "worktrees", "workers"):
        p[key].mkdir(parents=True, exist_ok=True)


def run_path(root: Path, run_id: str) -> Path:
    return cpt_paths(root)["orchestrations"] / f"{run_id}.yaml"


def contract_path(root: Path, contract_id: str) -> Path:
    return cpt_paths(root)["contracts"] / f"{contract_id}.yaml"


def result_path(root: Path, contract_id: str) -> Path:
    return cpt_paths(root)["results"] / f"{contract_id}.yaml"


def worktree_path(root: Path, contract_id: str) -> Path:
    return cpt_paths(root)["worktrees"] / f"{contract_id}.yaml"


def worker_record_path(root: Path, agent_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", agent_id)
    return cpt_paths(root)["workers"] / f"{safe}.yaml"


def schema_bundle(root: Path) -> dict[str, Any]:
    return json.loads(cpt_paths(root)["schema_bundle"].read_text(encoding="utf-8"))


_VALIDATORS: dict[tuple[str, str], Any] = {}


def validate_schema(root: Path, data: Any, schema_name: str, label: str) -> list[str]:
    key = (str(cpt_paths(root)["schema_bundle"]), schema_name)
    try:
        validator = _VALIDATORS.get(key)
        if validator is None:
            validator = fastjsonschema.compile(schema_bundle(root)[schema_name], use_default=False)
            _VALIDATORS[key] = validator
        validator(data)
        return []
    except fastjsonschema.JsonSchemaException as exc:
        return [f"{label}:{exc.path or '<root>'}: {exc.message}"]


def load_registry(root: Path) -> dict[str, dict]:
    path = cpt_paths(root)["worker_archetypes"]
    data = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data.get("archetypes", [])}


def next_id(existing: Iterable[str], prefix: str) -> str:
    rx = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    maximum = 0
    for value in existing:
        match = rx.match(value)
        if match:
            maximum = max(maximum, int(match.group(1)))
    return f"{prefix}-{maximum + 1:03d}"


def next_run_id(root: Path) -> str:
    return next_id((p.stem for p in cpt_paths(root)["orchestrations"].glob("ORC-*.yaml")), "ORC")


def next_contract_id(root: Path, run_id: str) -> str:
    values = []
    rx = re.compile(rf"^{re.escape(run_id)}-W(\d+)$")
    maximum = 0
    for path in cpt_paths(root)["contracts"].glob(f"{run_id}-W*.yaml"):
        match = rx.match(path.stem)
        if match:
            maximum = max(maximum, int(match.group(1)))
    return f"{run_id}-W{maximum + 1:02d}"


def next_worktree_id(root: Path) -> str:
    return next_id((p.stem for p in cpt_paths(root)["worktrees"].glob("WT-*.yaml")), "WT")


def load_run(root: Path, run_id: str) -> dict:
    path = run_path(root, run_id)
    if not path.exists():
        raise RuntimeError(f"Orchestration run not found: {run_id}")
    return load_yaml(path)


def load_contract(root: Path, contract_id: str) -> dict:
    path = contract_path(root, contract_id)
    if not path.exists():
        raise RuntimeError(f"Worker contract not found: {contract_id}")
    return load_yaml(path)


def load_result(root: Path, contract_id: str, required: bool = False) -> dict | None:
    path = result_path(root, contract_id)
    if not path.exists():
        if required:
            raise RuntimeError(f"Worker result not found: {contract_id}")
        return None
    return load_yaml(path)


def contracts_for_run(root: Path, run_id: str) -> list[dict]:
    run = load_run(root, run_id)
    return [load_contract(root, cid) for cid in run.get("contract_ids", [])]


def results_for_run(root: Path, run_id: str) -> list[dict]:
    result = []
    for contract in contracts_for_run(root, run_id):
        item = load_result(root, contract["id"], required=False)
        if item is not None:
            result.append(item)
    return result


def worktrees_for_run(root: Path, run_id: str) -> list[dict]:
    result = []
    for path in sorted(cpt_paths(root)["worktrees"].glob("WT-*.yaml")):
        try:
            item = load_yaml(path)
        except Exception:
            continue
        if item.get("orchestration_id") == run_id:
            result.append(item)
    return result


def current_orchestration(root: Path) -> str | None:
    current = load_yaml(cpt_paths(root)["current"])
    return current.get("current_orchestration")


def current_task_and_lease(root: Path) -> tuple[str | None, str | None]:
    current = load_yaml(cpt_paths(root)["current"])
    return current.get("current_task"), current.get("current_lease")


def active_lease(root: Path, lease_id: str | None = None) -> dict | None:
    _, current_lease = current_task_and_lease(root)
    lease_id = lease_id or current_lease
    if not lease_id:
        return None
    path = cpt_paths(root)["leases"] / f"{lease_id}.yaml"
    if not path.exists():
        return None
    lease = load_yaml(path)
    return lease if lease.get("status") == "active" else None


def matches_scope(path: str, scopes: list[str]) -> bool:
    value = Path(path).as_posix().lstrip("./")
    for pattern in scopes:
        normalized = Path(pattern).as_posix().lstrip("./")
        if normalized in {".", "**", "**/*"}:
            return True
        if fnmatch.fnmatch(value, normalized):
            return True
        prefix = normalized[:-3] if normalized.endswith("/**") else None
        if prefix and (value == prefix.rstrip("/") or value.startswith(prefix)):
            return True
    return False


def save_run(root: Path, run: dict) -> None:
    run["updated_at"] = utc_now()
    errors = validate_schema(root, run, "orchestration-run.schema.json", run["id"])
    if errors:
        raise RuntimeError("; ".join(errors))
    atomic_write_yaml(run_path(root, run["id"]), run)


def save_contract(root: Path, contract: dict) -> None:
    contract["updated_at"] = utc_now()
    errors = validate_schema(root, contract, "worker-contract.schema.json", contract["id"])
    if errors:
        raise RuntimeError("; ".join(errors))
    atomic_write_yaml(contract_path(root, contract["id"]), contract)


def save_result(root: Path, result: dict) -> None:
    errors = validate_schema(root, result, "worker-result.schema.json", result["id"])
    if errors:
        raise RuntimeError("; ".join(errors))
    atomic_write_yaml(result_path(root, result["contract_id"]), result)


def save_worktree(root: Path, record: dict) -> None:
    record["updated_at"] = utc_now()
    errors = validate_schema(root, record, "worktree-record.schema.json", record["id"])
    if errors:
        raise RuntimeError("; ".join(errors))
    atomic_write_yaml(worktree_path(root, record["contract_id"]), record)


def update_current_pointer(root: Path, run_id: str | None) -> None:
    path = cpt_paths(root)["current"]
    current = load_yaml(path)
    current["current_orchestration"] = run_id
    current["state_revision"] = int(current.get("state_revision", 0)) + 1
    current["updated_at"] = utc_now()
    atomic_write_yaml(path, current)


def validate_contract_semantics(root: Path, contract: dict, run: dict | None = None) -> list[str]:
    errors: list[str] = []
    registry = load_registry(root)
    archetype = registry.get(contract.get("archetype"))
    if archetype is None:
        errors.append(f"{contract.get('id')}: unknown worker archetype {contract.get('archetype')}")
        return errors
    invalid_roles = sorted(set(contract.get("role_lenses", [])) - set(archetype.get("allowed_role_lenses", [])))
    if invalid_roles:
        errors.append(f"{contract['id']}: role lenses not allowed for {contract['archetype']}: {invalid_roles}")
    if contract.get("permission_mode") == "read_only" and contract.get("write_scope"):
        errors.append(f"{contract['id']}: read_only contract cannot have write_scope")
    if contract.get("permission_mode") == "workspace_write" and not contract.get("write_scope"):
        errors.append(f"{contract['id']}: workspace_write contract requires write_scope")
    if contract.get("isolation") == "worktree" and contract.get("permission_mode") != "workspace_write":
        errors.append(f"{contract['id']}: worktree isolation is only valid for workspace_write contracts")
    if run is not None:
        if contract.get("orchestration_id") != run.get("id"):
            errors.append(f"{contract['id']}: orchestration pointer mismatch")
        if contract.get("task_id") != run.get("task_id"):
            errors.append(f"{contract['id']}: task pointer mismatch")
        if contract.get("lease_id") != run.get("lease_id"):
            errors.append(f"{contract['id']}: lease pointer mismatch")
        strategy = run.get("write_strategy")
        if contract.get("permission_mode") == "workspace_write":
            if strategy == "read_only":
                errors.append(f"{contract['id']}: writable contract not allowed in read_only run")
            if strategy == "parallel_worktree" and contract.get("isolation") != "worktree":
                errors.append(f"{contract['id']}: parallel_worktree run requires worktree isolation")
            if strategy == "sequential_direct" and contract.get("isolation") != "direct":
                errors.append(f"{contract['id']}: sequential_direct run requires direct isolation")
    return errors


def successful_contract_ids(root: Path, run: dict) -> set[str]:
    success: set[str] = set()
    for cid in run.get("contract_ids", []):
        result = load_result(root, cid, required=False)
        if result and result.get("status") == SUCCESS_RESULT_STATUS:
            success.add(cid)
    return success


def quorum_state(root: Path, run: dict) -> dict[str, Any]:
    contracts = contracts_for_run(root, run["id"])
    success = successful_contract_ids(root, run)
    required_ids = {item["id"] for item in contracts if item.get("required")}
    all_ids = {item["id"] for item in contracts}
    terminal_non_success = {
        item["id"]
        for item in contracts
        if item.get("status") in TERMINAL_CONTRACT_STATUSES and item["id"] not in success
    }
    required_failed = sorted(required_ids & terminal_non_success)
    required_ok = required_ids <= success
    mode = run.get("quorum", {}).get("mode", "all_required")
    n = run.get("quorum", {}).get("n")
    if mode == "all_required":
        satisfied = required_ok
    elif mode == "all":
        satisfied = all_ids <= success
    elif mode == "n_of_m":
        satisfied = required_ok and len(success) >= int(n or 0)
    else:
        satisfied = False
    possible = not required_failed
    if mode == "all":
        possible = possible and not terminal_non_success
    if mode == "n_of_m":
        remaining = sum(1 for item in contracts if item.get("status") not in TERMINAL_CONTRACT_STATUSES)
        possible = possible and len(success) + remaining >= int(n or 0)
    return {
        "mode": mode,
        "n": n,
        "satisfied": satisfied,
        "possible": possible,
        "successful_contracts": sorted(success),
        "required_contracts": sorted(required_ids),
        "required_failed": required_failed,
        "terminal_non_success": sorted(terminal_non_success),
    }


def recalculate_run(root: Path, run: dict) -> dict:
    state = quorum_state(root, run)
    contracts = contracts_for_run(root, run["id"])
    statuses = {item.get("status") for item in contracts}
    if run.get("status") in {"completed", "cancelled"}:
        return run
    if run.get("cancellation", {}).get("requested"):
        run["status"] = "cancelling"
    elif run.get("approval", {}).get("status") != "approved":
        # Draft runs are still collecting contracts. A quorum that is not yet
        # numerically possible must not block the run before the user approves
        # the final contract set.
        run["status"] = "proposed"
    elif not state["possible"]:
        run["status"] = "blocked"
    elif run.get("integration", {}).get("status") == "applied":
        run["status"] = "integrated"
    elif run.get("integration", {}).get("status") == "planned":
        run["status"] = "integrating"
    elif state["satisfied"]:
        run["status"] = "satisfied"
    elif statuses & ACTIVE_CONTRACT_STATUSES:
        run["status"] = "active"
    else:
        run["status"] = "approved"
    run["quorum_state"] = state
    return run


def create_run(root: Path, *, title: str, purpose: str, task_id: str | None, lease_id: str | None,
               write_strategy: str, quorum_mode: str, quorum_n: int | None) -> dict:
    ensure_dirs(root)
    current_task, current_lease = current_task_and_lease(root)
    task_id = task_id or current_task
    lease_id = lease_id or current_lease
    if not task_id:
        raise RuntimeError("Orchestration requires an active Standard Task")
    if not lease_id:
        raise RuntimeError("Orchestration requires an active authorization lease")
    lease = active_lease(root, lease_id)
    if lease is None or lease.get("task_id") != task_id:
        raise RuntimeError("Active lease does not belong to the orchestration task")
    if not lease.get("delegation", {}).get("allowed"):
        raise RuntimeError("Active lease does not allow delegation")
    if current_orchestration(root):
        active = load_run(root, current_orchestration(root))
        if active.get("status") not in {"completed", "cancelled", "failed"}:
            raise RuntimeError(f"Another orchestration is current: {active['id']}")
    run_id = next_run_id(root)
    run = {
        "schema_version": SCHEMA_VERSION,
        "id": run_id,
        "title": title,
        "purpose": purpose,
        "task_id": task_id,
        "lease_id": lease_id,
        "status": "proposed",
        "write_strategy": write_strategy,
        "approval": {"status": "proposed", "approved_by": None, "approved_at": None},
        "quorum": {"mode": quorum_mode, "n": quorum_n},
        "quorum_state": {
            "mode": quorum_mode,
            "n": quorum_n,
            "satisfied": False,
            "possible": True,
            "successful_contracts": [],
            "required_contracts": [],
            "required_failed": [],
            "terminal_non_success": [],
        },
        "contract_ids": [],
        "integration": {"status": "not_started", "owner": "main_thread", "summary": None, "plan": [], "applied_at": None},
        "cancellation": {"requested": False, "reason": None, "requested_at": None},
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "completed_at": None,
    }
    if quorum_mode == "n_of_m" and (quorum_n is None or quorum_n < 1):
        raise RuntimeError("n_of_m quorum requires --quorum-n >= 1")
    save_run(root, run)
    update_current_pointer(root, run_id)
    return run


def add_contract(root: Path, run_id: str, *, archetype: str, purpose: str, required: bool,
                 role_lenses: list[str], skills: list[str], read_scope: list[str], write_scope: list[str],
                 permission_mode: str, isolation: str, timeout_seconds: int, output_fields: list[str],
                 stop_conditions: list[str], fallback: str | None) -> dict:
    ensure_dirs(root)
    run = load_run(root, run_id)
    if run.get("status") not in {"proposed", "approved"}:
        raise RuntimeError(f"Cannot add contracts to run in status {run.get('status')}")
    if archetype in {item.get("archetype") for item in contracts_for_run(root, run_id)}:
        raise RuntimeError(f"Duplicate worker archetype in one orchestration run is not allowed: {archetype}")
    registry = load_registry(root)
    if archetype not in registry:
        raise RuntimeError(f"Unknown worker archetype: {archetype}")
    lease = active_lease(root, run.get("lease_id"))
    if lease is None:
        raise RuntimeError("Orchestration lease is not active")
    delegation = lease.get("delegation", {})
    if archetype not in delegation.get("allowed_worker_archetypes", []):
        raise RuntimeError(f"Lease does not allow worker archetype: {archetype}")
    if delegation.get("read_only") and permission_mode != "read_only":
        raise RuntimeError("Lease permits read-only workers only")
    if len(run.get("contract_ids", [])) >= int(delegation.get("max_workers", 0)):
        raise RuntimeError("Worker contract count would exceed lease max_workers")
    contract_id = next_contract_id(root, run_id)
    contract = {
        "schema_version": SCHEMA_VERSION,
        "id": contract_id,
        "orchestration_id": run_id,
        "task_id": run["task_id"],
        "lease_id": run["lease_id"],
        "archetype": archetype,
        "purpose": purpose,
        "required": required,
        "status": "proposed",
        "role_lenses": sorted(set(role_lenses)),
        "skills": sorted(set(skills)),
        "read_scope": read_scope,
        "write_scope": write_scope,
        "permission_mode": permission_mode,
        "isolation": isolation,
        "timeout_seconds": timeout_seconds,
        "output_contract": {
            "required_fields": sorted(set(output_fields or registry[archetype].get("required_output_fields", []))),
            "format": "cpt-worker-result-v1",
        },
        "stop_conditions": stop_conditions,
        "fallback": fallback,
        "native_agent_id": None,
        "worktree_id": None,
        "created_at": utc_now(),
        "approved_at": None,
        "started_at": None,
        "returned_at": None,
        "completed_at": None,
        "updated_at": utc_now(),
    }
    errors = validate_contract_semantics(root, contract, run)
    if errors:
        raise RuntimeError("; ".join(errors))
    save_contract(root, contract)
    run["contract_ids"].append(contract_id)
    # Persist the contract pointer before quorum calculation. quorum_state()
    # deliberately reloads contracts through the on-disk run record so a
    # half-written contract cannot satisfy or block quorum.
    save_run(root, run)
    run = recalculate_run(root, load_run(root, run_id))
    save_run(root, run)
    return contract


def approve_run(root: Path, run_id: str, approved_by: str = "user") -> dict:
    run = load_run(root, run_id)
    if not run.get("contract_ids"):
        raise RuntimeError("Cannot approve orchestration without worker contracts")
    contracts = contracts_for_run(root, run_id)
    if len({c["archetype"] for c in contracts}) != len(contracts):
        raise RuntimeError("Duplicate archetypes make native worker binding ambiguous")
    writable = [c for c in contracts if c.get("permission_mode") in WRITE_PERMISSION_MODES]
    if len(writable) > 1 and run.get("write_strategy") != "parallel_worktree":
        raise RuntimeError("Multiple writable workers require parallel_worktree strategy")
    for contract in contracts:
        errors = validate_contract_semantics(root, contract, run)
        if errors:
            raise RuntimeError("; ".join(errors))
        contract["status"] = "approved"
        contract["approved_at"] = utc_now()
        save_contract(root, contract)
    run["approval"] = {"status": "approved", "approved_by": approved_by, "approved_at": utc_now()}
    run = recalculate_run(root, run)
    save_run(root, run)
    return run


def activate_run(root: Path, run_id: str) -> dict:
    run = load_run(root, run_id)
    if run.get("approval", {}).get("status") != "approved":
        raise RuntimeError("Orchestration must be approved before activation")
    if run.get("status") not in {"approved", "satisfied", "active"}:
        raise RuntimeError(f"Cannot activate orchestration in status {run.get('status')}")
    run["status"] = "active"
    save_run(root, run)
    return run


def find_contract_for_native_start(root: Path, archetype: str) -> dict | None:
    run_id = current_orchestration(root)
    if not run_id:
        return None
    run = load_run(root, run_id)
    if run.get("status") not in {"approved", "active", "satisfied"}:
        return None
    candidates = [
        contract
        for contract in contracts_for_run(root, run_id)
        if contract.get("archetype") == archetype
        and contract.get("status") == "approved"
        and not contract.get("native_agent_id")
    ]
    if len(candidates) > 1:
        raise RuntimeError(f"Ambiguous worker binding for archetype {archetype}")
    return candidates[0] if candidates else None


def bind_native_worker(root: Path, payload: dict) -> dict | None:
    archetype = payload.get("agent_type") or payload.get("name") or "unknown"
    contract = find_contract_for_native_start(root, archetype)
    if contract is None:
        return None
    run = load_run(root, contract["orchestration_id"])
    if contract.get("permission_mode") == "workspace_write" and contract.get("isolation") == "worktree" and not contract.get("worktree_id"):
        raise RuntimeError(f"Writable worktree contract {contract['id']} has no managed worktree")
    contract["native_agent_id"] = payload.get("agent_id") or "unknown"
    contract["status"] = "active"
    contract["started_at"] = utc_now()
    save_contract(root, contract)
    run["status"] = "active"
    save_run(root, run)
    return contract


def native_worker_returned(root: Path, payload: dict) -> dict | None:
    agent_id = payload.get("agent_id") or "unknown"
    for path in sorted(cpt_paths(root)["contracts"].glob("ORC-*-W*.yaml")):
        contract = load_yaml(path)
        if contract.get("native_agent_id") == agent_id and contract.get("status") in {"active", "cancel_requested", "needs_reconcile"}:
            contract["status"] = "returned"
            contract["returned_at"] = utc_now()
            save_contract(root, contract)
            run = recalculate_run(root, load_run(root, contract["orchestration_id"]))
            save_run(root, run)
            return contract
    return None


def submit_result(root: Path, contract_id: str, *, status: str, summary: str, evidence: list[str], blockers: list[str],
                  confidence: str, touched_paths: list[str], verification: list[str], recommendations: list[str]) -> dict:
    if status not in RESULT_STATUSES:
        raise RuntimeError(f"Invalid worker result status: {status}")
    contract = load_contract(root, contract_id)
    if contract.get("status") not in {"approved", "returned", "active", "cancel_requested", "needs_reconcile"}:
        raise RuntimeError(f"Cannot submit result for contract in status {contract.get('status')}")
    # Manual fallback: when lifecycle hooks are disabled or unavailable, the
    # parent may submit a bounded structured result directly for an approved
    # contract. Hook-backed runs still record native agent identity and timing.
    if contract.get("status") == "approved" and not contract.get("started_at"):
        contract["started_at"] = utc_now()
    required_fields = contract.get("output_contract", {}).get("required_fields", [])
    values = {
        "summary": summary,
        "evidence": evidence,
        "blockers": blockers,
        "confidence": confidence,
        "touched_paths": touched_paths,
        "verification": verification,
        "recommendations": recommendations,
    }
    missing = []
    for field in required_fields:
        if field not in values:
            missing.append(field)
            continue
        value = values[field]
        # Required means structurally present. Some valid result fields, such as
        # blockers or touched_paths, may intentionally be empty. Narrative and
        # evidentiary fields must still contain meaningful content.
        if field in {"summary", "confidence"} and not str(value).strip():
            missing.append(field)
        elif field == "evidence" and not value:
            missing.append(field)
    if missing:
        raise RuntimeError(f"Worker result is missing required fields: {missing}")
    if status == "success" and contract.get("permission_mode") == "workspace_write":
        if not verification:
            raise RuntimeError("Successful workspace-write worker result requires verification evidence")
    if contract.get("permission_mode") == "read_only" and touched_paths:
        raise RuntimeError("Read-only worker result cannot report touched paths")
    invalid_touched = [path for path in touched_paths if not matches_scope(path, contract.get("write_scope", []))]
    if invalid_touched:
        raise RuntimeError(f"Worker result reports paths outside contract write_scope: {invalid_touched}")
    result = {
        "schema_version": SCHEMA_VERSION,
        "id": f"RES-{contract_id}",
        "orchestration_id": contract["orchestration_id"],
        "contract_id": contract_id,
        "worker_archetype": contract["archetype"],
        "status": status,
        "summary": summary,
        "evidence": [{"reference": item} for item in evidence],
        "blockers": blockers,
        "confidence": confidence,
        "touched_paths": touched_paths,
        "verification": verification,
        "recommendations": recommendations,
        "submitted_at": utc_now(),
    }
    save_result(root, result)
    mapping = {
        "success": "completed",
        "partial": "partial",
        "failure": "failed",
        "insufficient_evidence": "insufficient_evidence",
        "cancelled": "cancelled",
    }
    contract["status"] = mapping[status]
    contract["completed_at"] = utc_now()
    save_contract(root, contract)
    run = recalculate_run(root, load_run(root, contract["orchestration_id"]))
    save_run(root, run)
    return result


def request_cancel(root: Path, *, run_id: str | None = None, contract_id: str | None = None, reason: str) -> dict:
    if contract_id:
        contract = load_contract(root, contract_id)
        if contract.get("status") in TERMINAL_CONTRACT_STATUSES:
            return contract
        contract["status"] = "cancel_requested"
        contract["fallback"] = (contract.get("fallback") or "") + f" Cancellation requested: {reason}"
        save_contract(root, contract)
        run = load_run(root, contract["orchestration_id"])
        # Cancelling one contract is not equivalent to cancelling the whole
        # orchestration. The parent/host must still stop the native worker and
        # the run is recalculated from contract states and quorum policy.
        run = recalculate_run(root, run)
        save_run(root, run)
        return contract
    if not run_id:
        raise RuntimeError("Provide run_id or contract_id")
    run = load_run(root, run_id)
    run["cancellation"] = {"requested": True, "reason": reason, "requested_at": utc_now()}
    for contract in contracts_for_run(root, run_id):
        if contract.get("status") not in TERMINAL_CONTRACT_STATUSES:
            contract["status"] = "cancel_requested"
            save_contract(root, contract)
    run = recalculate_run(root, run)
    save_run(root, run)
    return run


def skip_contract(root: Path, contract_id: str, reason: str) -> dict:
    contract = load_contract(root, contract_id)
    if contract.get("required"):
        raise RuntimeError("Required worker contracts cannot be skipped")
    if contract.get("status") not in {"proposed", "approved"}:
        raise RuntimeError(f"Cannot skip contract in status {contract.get('status')}")
    contract["status"] = "skipped"
    contract["completed_at"] = utc_now()
    contract["fallback"] = reason
    save_contract(root, contract)
    run = recalculate_run(root, load_run(root, contract["orchestration_id"]))
    save_run(root, run)
    return contract


def reconcile(root: Path, run_id: str, *, now_epoch: float | None = None) -> dict:
    now_epoch = now_epoch or time.time()
    run = load_run(root, run_id)
    worker_records: dict[str, dict] = {}
    for path in cpt_paths(root)["workers"].glob("*.yaml"):
        try:
            item = load_yaml(path)
        except Exception:
            continue
        if item.get("agent_id"):
            worker_records[item["agent_id"]] = item
    for contract in contracts_for_run(root, run_id):
        status = contract.get("status")
        agent_id = contract.get("native_agent_id")
        if status in {"active", "cancel_requested"}:
            started = contract.get("started_at")
            if started:
                started_epoch = datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp()
                if now_epoch - started_epoch > int(contract.get("timeout_seconds", 900)):
                    contract["status"] = "timed_out"
                    contract["completed_at"] = utc_now()
                    save_contract(root, contract)
                    continue
            if not agent_id or agent_id not in worker_records:
                contract["status"] = "needs_reconcile"
                save_contract(root, contract)
            elif worker_records[agent_id].get("status") in {"completed", "interrupted", "failed", "unknown"} and status == "active":
                contract["status"] = "returned" if worker_records[agent_id].get("status") == "completed" else "needs_reconcile"
                contract["returned_at"] = utc_now()
                save_contract(root, contract)
        elif status == "returned" and load_result(root, contract["id"], required=False) is None:
            # Returned is a valid intermediate state. It becomes needs_reconcile only if the host record disappeared.
            if agent_id and agent_id not in worker_records:
                contract["status"] = "needs_reconcile"
                save_contract(root, contract)
    run = recalculate_run(root, run)
    save_run(root, run)
    return run


def integration_update(root: Path, run_id: str, *, summary: str, plan: list[str], apply: bool) -> dict:
    run = recalculate_run(root, load_run(root, run_id))
    if not run.get("quorum_state", {}).get("satisfied"):
        raise RuntimeError("Cannot integrate before quorum is satisfied")
    active = [c["id"] for c in contracts_for_run(root, run_id) if c.get("status") in ACTIVE_CONTRACT_STATUSES]
    if active:
        raise RuntimeError(f"Cannot integrate while workers are active or unresolved: {active}")
    run["integration"] = {
        "status": "applied" if apply else "planned",
        "owner": "main_thread",
        "summary": summary,
        "plan": plan,
        "applied_at": utc_now() if apply else None,
    }
    run = recalculate_run(root, run)
    save_run(root, run)
    return run


def complete_run(root: Path, run_id: str) -> dict:
    run = recalculate_run(root, load_run(root, run_id))
    if not run.get("quorum_state", {}).get("satisfied"):
        raise RuntimeError("Cannot complete orchestration before quorum is satisfied")
    if run.get("integration", {}).get("status") != "applied":
        raise RuntimeError("Cannot complete orchestration before main-thread integration is applied")
    unresolved = [c["id"] for c in contracts_for_run(root, run_id) if c.get("status") not in TERMINAL_CONTRACT_STATUSES]
    if unresolved:
        raise RuntimeError(f"Cannot complete orchestration with unresolved contracts: {unresolved}")
    dirty_worktrees = [w["id"] for w in worktrees_for_run(root, run_id) if w.get("status") in {"active", "dirty", "blocked"}]
    if dirty_worktrees:
        raise RuntimeError(f"Cannot complete orchestration with active/dirty worktrees: {dirty_worktrees}")
    run["status"] = "completed"
    run["completed_at"] = utc_now()
    save_run(root, run)
    if current_orchestration(root) == run_id:
        update_current_pointer(root, None)
    return run


def bundle_for_checkpoint(root: Path, run_id: str | None) -> dict | None:
    if not run_id:
        return None
    run = load_run(root, run_id)
    return {
        "run": copy.deepcopy(run),
        "contracts": copy.deepcopy(contracts_for_run(root, run_id)),
        "results": copy.deepcopy(results_for_run(root, run_id)),
        "worktrees": copy.deepcopy(worktrees_for_run(root, run_id)),
    }


def bundle_diff(root: Path, bundle: dict | None) -> list[str]:
    if bundle is None:
        return []
    run = bundle.get("run")
    if not run:
        return ["orchestration checkpoint bundle has no run"]
    run_id = run["id"]
    try:
        live = bundle_for_checkpoint(root, run_id)
    except Exception as exc:
        return [f"active orchestration unavailable: {exc}"]
    # Worker lifecycle may legitimately progress after checkpoint. Compare durable contract/result/run pointers separately in PostCompact reconciliation.
    if live == bundle:
        return []
    return ["active orchestration state differs"]


def restore_bundle(root: Path, bundle: dict | None) -> None:
    if bundle is None:
        return
    run = bundle["run"]
    save_run(root, run)
    for contract in bundle.get("contracts", []):
        save_contract(root, contract)
    for result in bundle.get("results", []):
        save_result(root, result)
    for worktree in bundle.get("worktrees", []):
        save_worktree(root, worktree)


def managed_compaction_issues(root: Path, run_id: str | None) -> list[str]:
    if not run_id:
        return []
    issues: list[str] = []
    run = load_run(root, run_id)
    for contract in contracts_for_run(root, run_id):
        if contract.get("status") in ACTIVE_CONTRACT_STATUSES:
            if contract.get("permission_mode") != "read_only":
                issues.append(f"write worker {contract['id']} is active during compaction")
            if not contract.get("native_agent_id"):
                issues.append(f"managed worker {contract['id']} has no native binding")
    if run.get("status") == "needs_reconcile":
        issues.append(f"orchestration {run_id} requires reconciliation")
    return issues


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result


def git_root(root: Path) -> Path:
    result = git(root, "rev-parse", "--show-toplevel")
    return Path(result.stdout.strip()).resolve()


def git_head(root: Path) -> str:
    return git(root, "rev-parse", "HEAD").stdout.strip()


def git_status_paths(root: Path) -> list[str]:
    result = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    found: list[str] = []
    for item in result.stdout.split("\x00"):
        if not item:
            continue
        value = item[3:] if len(item) >= 4 else item
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        found.append(Path(value).as_posix())
    return sorted(set(found))


def registered_worktrees(root: Path) -> list[dict[str, str]]:
    result = git(root, "worktree", "list", "--porcelain")
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            if current:
                records.append(current); current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        records.append(current)
    return records


def create_worktree(root: Path, contract_id: str, target: str | None = None, allow_dirty_base: bool = False) -> dict:
    contract = load_contract(root, contract_id)
    if contract.get("permission_mode") != "workspace_write" or contract.get("isolation") != "worktree":
        raise RuntimeError("Managed worktree requires a workspace_write contract with worktree isolation")
    if contract.get("worktree_id"):
        return load_yaml(worktree_path(root, contract_id))
    repo = git_root(root)
    dirty = git_status_paths(repo)
    runtime_only = [path for path in dirty if not path.startswith(".cpt/")]
    if runtime_only and not allow_dirty_base:
        raise RuntimeError(f"Main repository is dirty; refusing worktree creation: {runtime_only[:10]}")
    run = load_run(root, contract["orchestration_id"])
    base = git_head(repo)
    branch = f"cpt/{run['id'].lower()}/{contract_id.lower()}"
    worktree_id = next_worktree_id(root)
    target_path = Path(target).expanduser().resolve() if target else (repo.parent / ".cpt-worktrees" / repo.name / run["id"] / contract_id).resolve()
    if target_path == repo or repo in target_path.parents:
        raise RuntimeError("Managed worktree target must be outside the main repository")
    if target_path.exists() and any(target_path.iterdir()):
        raise RuntimeError(f"Worktree target is not empty: {target_path}")
    existing_branch = git(repo, "show-ref", "--verify", f"refs/heads/{branch}", check=False)
    if existing_branch.returncode == 0:
        raise RuntimeError(f"Managed worktree branch already exists: {branch}")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    git(repo, "worktree", "add", "-b", branch, str(target_path), base)
    record = {
        "schema_version": SCHEMA_VERSION,
        "id": worktree_id,
        "orchestration_id": run["id"],
        "contract_id": contract_id,
        "repo_root": str(repo),
        "path": str(target_path),
        "branch": branch,
        "base_revision": base,
        "status": "active",
        "write_scope": contract.get("write_scope", []),
        "changed_paths": [],
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "removed_at": None,
    }
    save_worktree(root, record)
    contract["worktree_id"] = worktree_id
    save_contract(root, contract)
    return record


def validate_worktree_record(root: Path, contract_id: str) -> tuple[dict, dict]:
    record = load_yaml(worktree_path(root, contract_id))
    contract = load_contract(root, contract_id)
    if record.get("contract_id") != contract_id or record.get("orchestration_id") != contract.get("orchestration_id"):
        raise RuntimeError("Worktree record does not match managed contract")
    expected_branch = f"cpt/{contract['orchestration_id'].lower()}/{contract_id.lower()}"
    if record.get("branch") != expected_branch:
        raise RuntimeError("Worktree record branch does not match managed naming convention")
    repo = Path(record.get("repo_root", "")).resolve()
    target = Path(record.get("path", "")).resolve()
    if repo == target or repo in target.parents:
        raise RuntimeError("Worktree record points inside the main repository")
    registered = {Path(item.get("worktree", "")).resolve(): item for item in registered_worktrees(repo)}
    item = registered.get(target)
    if not item:
        raise RuntimeError("Worktree path is not registered with Git")
    branch_ref = item.get("branch", "")
    if branch_ref and branch_ref != f"refs/heads/{record['branch']}":
        raise RuntimeError("Registered Git branch does not match worktree record")
    return record, contract


def inspect_worktree(root: Path, contract_id: str) -> dict:
    record, contract = validate_worktree_record(root, contract_id)
    target = Path(record["path"])
    changed = git_status_paths(target)
    invalid = [path for path in changed if not matches_scope(path, contract.get("write_scope", []))]
    record["changed_paths"] = changed
    record["status"] = "blocked" if invalid else ("dirty" if changed else "clean")
    save_worktree(root, record)
    return {"record": record, "invalid_paths": invalid}


def integration_plan_for_worktree(root: Path, contract_id: str) -> dict:
    inspected = inspect_worktree(root, contract_id)
    record = inspected["record"]
    if inspected["invalid_paths"]:
        raise RuntimeError(f"Worktree contains changes outside contract write_scope: {inspected['invalid_paths']}")
    result = load_result(root, contract_id, required=False)
    if result is not None:
        reported = sorted(set(result.get("touched_paths", [])))
        actual = sorted(set(record.get("changed_paths", [])))
        if reported != actual:
            raise RuntimeError(f"Worker-reported touched paths do not match Git changes: reported={reported}, actual={actual}")
    return {
        "contract_id": contract_id,
        "worktree_id": record["id"],
        "path": record["path"],
        "branch": record["branch"],
        "base_revision": record["base_revision"],
        "changed_paths": record["changed_paths"],
        "merge_policy": "review_only_no_automatic_merge",
    }


def remove_worktree(root: Path, contract_id: str, discard: bool = False) -> dict:
    record, contract = validate_worktree_record(root, contract_id)
    inspected = inspect_worktree(root, contract_id)
    record = inspected["record"]
    if record.get("changed_paths") and not discard:
        raise RuntimeError("Worktree is dirty; review/integrate it or pass --discard explicitly")
    repo = Path(record["repo_root"])
    target = Path(record["path"])
    args = ["worktree", "remove"]
    if discard:
        args.append("--force")
    args.append(str(target))
    git(repo, *args)
    branch = record["branch"]
    if discard:
        git(repo, "branch", "-D", branch)
    else:
        merged = git(repo, "merge-base", "--is-ancestor", branch, "HEAD", check=False).returncode == 0
        if merged:
            git(repo, "branch", "-d", branch)
    record["status"] = "removed"
    record["removed_at"] = utc_now()
    record["changed_paths"] = []
    save_worktree(root, record)
    contract["worktree_id"] = None
    save_contract(root, contract)
    return record


def validate_all(root: Path) -> tuple[list[str], list[str]]:
    ensure_dirs(root)
    errors: list[str] = []
    warnings: list[str] = []
    registry = load_registry(root)
    if len(registry) != 10:
        errors.append(f"worker archetype registry must contain 10 entries; found {len(registry)}")
    seen_names: set[str] = set()
    for run_file in sorted(cpt_paths(root)["orchestrations"].glob("ORC-*.yaml")):
        run = load_yaml(run_file)
        errors += validate_schema(root, run, "orchestration-run.schema.json", str(run_file.relative_to(root)))
        contract_ids = run.get("contract_ids", [])
        if len(contract_ids) != len(set(contract_ids)):
            errors.append(f"{run['id']}: duplicate contract IDs")
        archetypes: list[str] = []
        for cid in contract_ids:
            path = contract_path(root, cid)
            if not path.exists():
                errors.append(f"{run['id']}: missing contract {cid}")
                continue
            contract = load_yaml(path)
            errors += validate_schema(root, contract, "worker-contract.schema.json", str(path.relative_to(root)))
            errors += validate_contract_semantics(root, contract, run)
            archetypes.append(contract.get("archetype"))
            result = load_result(root, cid, required=False)
            if result is not None:
                errors += validate_schema(root, result, "worker-result.schema.json", str(result_path(root, cid).relative_to(root)))
                if result.get("contract_id") != cid or result.get("orchestration_id") != run.get("id"):
                    errors.append(f"{cid}: worker result pointers do not match")
        if len(archetypes) != len(set(archetypes)):
            errors.append(f"{run['id']}: duplicate worker archetypes are not allowed")
        computed = quorum_state(root, run) if all(contract_path(root, cid).exists() for cid in contract_ids) else None
        if computed and run.get("quorum_state") != computed:
            warnings.append(f"{run['id']}: stored quorum_state differs from computed state; run orchestration-reconcile")
    known_contracts = {cid for path in cpt_paths(root)["orchestrations"].glob("ORC-*.yaml") for cid in load_yaml(path).get("contract_ids", [])}
    for path in cpt_paths(root)["contracts"].glob("ORC-*-W*.yaml"):
        if path.stem not in known_contracts:
            warnings.append(f"orphan worker contract: {path.relative_to(root)}")
    for path in cpt_paths(root)["results"].glob("ORC-*-W*.yaml"):
        if path.stem not in known_contracts:
            warnings.append(f"orphan worker result: {path.relative_to(root)}")
    for path in cpt_paths(root)["worktrees"].glob("WT-*.yaml"):
        record = load_yaml(path)
        errors += validate_schema(root, record, "worktree-record.schema.json", str(path.relative_to(root)))
        if record.get("status") not in {"removed"}:
            try:
                validate_worktree_record(root, record["contract_id"])
            except Exception as exc:
                warnings.append(f"{record.get('id')}: worktree needs reconciliation: {exc}")
    current = load_yaml(cpt_paths(root)["current"])
    run_id = current.get("current_orchestration")
    if run_id:
        path = run_path(root, run_id)
        if not path.exists():
            errors.append(f"current orchestration missing: {run_id}")
        elif load_yaml(path).get("status") in {"completed", "cancelled"}:
            warnings.append(f"current orchestration {run_id} is terminal; clear the pointer")
    return errors, warnings


def status_payload(root: Path, run_id: str | None = None) -> dict:
    run_id = run_id or current_orchestration(root)
    if not run_id:
        return {"current_orchestration": None, "status": "none"}
    run = recalculate_run(root, load_run(root, run_id))
    contracts = contracts_for_run(root, run_id)
    return {
        "current_orchestration": run_id,
        "status": run.get("status"),
        "approval": run.get("approval"),
        "quorum": run.get("quorum_state"),
        "integration": run.get("integration"),
        "contracts": [
            {
                "id": c["id"],
                "archetype": c["archetype"],
                "required": c["required"],
                "status": c["status"],
                "native_agent_id": c.get("native_agent_id"),
                "worktree_id": c.get("worktree_id"),
            }
            for c in contracts
        ],
    }
