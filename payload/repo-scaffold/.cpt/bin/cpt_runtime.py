#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit(
        "Missing runtime dependencies. Install PyYAML and jsonschema using the CPT package requirements."
    ) from exc

SCHEMA_VERSION = "4.0-alpha2"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=True, allow_unicode=True)


def digest(data: Any) -> str | None:
    if data is None:
        return None
    return hashlib.sha256(canonical_yaml(data).encode("utf-8")).hexdigest()


def normalize_scalars(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize_scalars(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_scalars(item) for key, item in value.items()}
    return value


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return normalize_scalars(yaml.safe_load(handle))


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


@contextmanager
def runtime_lock(root: Path, timeout: float = 10.0):
    lock = root / ".cpt" / ".runtime.lock"
    deadline = time.time() + timeout
    fd = None
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()}\ncreated_at={utc_now()}\n".encode())
        except FileExistsError:
            if time.time() >= deadline:
                raise RuntimeError(f"Runtime lock timeout: {lock}")
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


def find_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".cpt" / "runtime.yaml").exists():
            return candidate
    raise RuntimeError("No CPT runtime found. Expected .cpt/runtime.yaml in this directory or a parent.")


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def paths(root: Path) -> dict[str, Path]:
    cpt = root / ".cpt"
    return {
        "cpt": cpt,
        "runtime": cpt / "runtime.yaml",
        "current": cpt / "current.yaml",
        "task_index": cpt / "task-index.yaml",
        "summary": cpt / "runtime-summary.md",
        "tasks": cpt / "tasks",
        "micro_changes": cpt / "micro-changes",
        "leases": cpt / "leases",
        "checkpoints": cpt / "checkpoints",
    }


_SCHEMA_BUNDLE: dict[str, Any] | None = None


def schema_bundle() -> dict[str, Any]:
    global _SCHEMA_BUNDLE
    if _SCHEMA_BUNDLE is None:
        _SCHEMA_BUNDLE = json.loads((package_root() / "schema-bundle.json").read_text(encoding="utf-8"))
    return _SCHEMA_BUNDLE


def validate_schema(data: Any, name: str, label: str) -> list[str]:
    schema = schema_bundle()[name]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{loc}: {error.message}")
    return errors


def task_file(root: Path, task_id: str) -> Path:
    return paths(root)["tasks"] / f"{task_id}.yaml"


def micro_file(root: Path, micro_id: str) -> Path:
    return paths(root)["micro_changes"] / f"{micro_id}.yaml"


def lease_file(root: Path, lease_id: str) -> Path:
    return paths(root)["leases"] / f"{lease_id}.yaml"


def checkpoint_file(root: Path, checkpoint_id: str) -> Path:
    return paths(root)["checkpoints"] / f"{checkpoint_id}.yaml"


def next_numeric_id(existing: Iterable[str], prefix: str) -> str:
    max_n = 0
    rx = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for value in existing:
        match = rx.match(value)
        if match:
            max_n = max(max_n, int(match.group(1)))
    return f"{prefix}-{max_n + 1:03d}"


def load_state(root: Path) -> tuple[dict, dict, dict]:
    p = paths(root)
    return load_yaml(p["runtime"]), load_yaml(p["current"]), load_yaml(p["task_index"])


def bump(current: dict) -> None:
    current["state_revision"] = int(current.get("state_revision", 0)) + 1
    current["updated_at"] = utc_now()


def render_summary(root: Path, current: dict | None = None, index: dict | None = None) -> str:
    p = paths(root)
    current = current or load_yaml(p["current"])
    index = index or load_yaml(p["task_index"])
    by_id = {entry["id"]: entry for entry in index.get("tasks", [])}

    task_label = "none"
    if current.get("current_task"):
        entry = by_id.get(current["current_task"])
        task_label = f"`{current['current_task']}`"
        if entry:
            task_label += f" — {entry['title']} ({entry['status']})"

    micro_label = current.get("current_micro_change") or "none"
    lease_label = current.get("current_lease") or "none"
    checkpoint_label = current.get("latest_checkpoint") or "none"
    blockers = current.get("blockers", [])
    blocker_text = "None." if not blockers else "\n".join(
        f"- [{b['severity']}] {b['id']}: {b['summary']}" for b in blockers
    )
    next_op = current.get("next_operation", {})
    return f"""# Runtime Summary
<!-- cpt-state-revision: {current['state_revision']} -->

Generated from `.cpt/current.yaml` and `.cpt/task-index.yaml`. Do not edit manually.

## State

- Runtime status: `{current['runtime_status']}`
- Current task: {task_label}
- Current micro change: `{micro_label}`
- Current lease: `{lease_label}`
- Latest checkpoint: `{checkpoint_label}`

## Blockers

{blocker_text}

## Next operation

{next_op.get('summary', 'Not specified.')}
"""


def write_summary(root: Path, current: dict | None = None, index: dict | None = None) -> None:
    atomic_write_text(paths(root)["summary"], render_summary(root, current, index))


def validate_runtime(root: Path) -> tuple[list[str], list[str]]:
    p = paths(root)
    errors: list[str] = []
    warnings: list[str] = []
    required = [p["runtime"], p["current"], p["task_index"], p["summary"]]
    for path in required:
        if not path.exists():
            errors.append(f"missing: {path.relative_to(root)}")
    if errors:
        return errors, warnings

    runtime, current, index = load_state(root)
    errors += validate_schema(runtime, "runtime.schema.json", ".cpt/runtime.yaml")
    errors += validate_schema(current, "current.schema.json", ".cpt/current.yaml")
    errors += validate_schema(index, "task-index.schema.json", ".cpt/task-index.yaml")

    entries = index.get("tasks", [])
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        errors.append("task-index: duplicate task IDs")

    for entry in entries:
        path = root / entry["file"]
        if not path.exists():
            errors.append(f"task-index: missing task file {entry['file']}")
            continue
        data = load_yaml(path)
        errors += validate_schema(data, "task.schema.json", entry["file"])
        if data.get("id") != entry.get("id"):
            errors.append(f"task-index: ID mismatch for {entry['file']}")
        if data.get("status") != entry.get("status"):
            errors.append(f"task-index: status mismatch for {entry['id']}")

    current_task = current.get("current_task")
    current_micro = current.get("current_micro_change")
    if current.get("runtime_status") == "active" and not (current_task or current_micro):
        errors.append("current: runtime_status active requires a current task or micro change")
    if current.get("runtime_status") == "ready" and (current_task or current_micro):
        errors.append("current: runtime_status ready cannot have a current task or micro change")
    if current_task:
        if current_task not in ids:
            errors.append(f"current: task {current_task} not in task index")
        else:
            entry = next(e for e in entries if e["id"] == current_task)
            if entry["status"] not in {"active", "blocked", "review"}:
                errors.append(f"current: task {current_task} has non-current status {entry['status']}")
    if current_micro:
        path = micro_file(root, current_micro)
        if not path.exists():
            errors.append(f"current: missing micro change {current_micro}")
        else:
            data = load_yaml(path)
            errors += validate_schema(data, "micro-change.schema.json", str(path.relative_to(root)))
            if data.get("status") not in {"active", "verifying"}:
                errors.append(f"current: micro change {current_micro} has non-current status {data.get('status')}")
            if not all(data.get("eligibility", {}).values()):
                errors.append(f"current: active micro change {current_micro} is not fully eligible")

    # Validate all runtime records, including inactive/orphan records.
    indexed_task_files = {str((root / e["file"]).resolve()) for e in entries}
    for path in sorted(p["tasks"].glob("TKT-*.yaml")):
        data = load_yaml(path)
        errors += validate_schema(data, "task.schema.json", str(path.relative_to(root)))
        if str(path.resolve()) not in indexed_task_files:
            warnings.append(f"orphan task file not present in task-index: {path.relative_to(root)}")
    for path in sorted(p["micro_changes"].glob("MC-*.yaml")):
        data = load_yaml(path)
        errors += validate_schema(data, "micro-change.schema.json", str(path.relative_to(root)))
        if data.get("status") in {"active", "verifying"} and data.get("id") != current_micro:
            errors.append(f"micro change {data.get('id')} is active but not current")
    for path in sorted(p["leases"].glob("LEASE-*.yaml")):
        data = load_yaml(path)
        errors += validate_schema(data, "authorization-lease.schema.json", str(path.relative_to(root)))
        if data.get("status") == "active" and data.get("id") != current.get("current_lease"):
            errors.append(f"lease {data.get('id')} is active but not current")
        expires_at = data.get("expires", {}).get("at")
        if data.get("status") == "active" and expires_at:
            try:
                expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                if expiry <= datetime.now(timezone.utc):
                    errors.append(f"lease {data.get('id')} is active but expired at {expires_at}")
            except ValueError:
                pass
    for path in sorted(p["checkpoints"].glob("CP-*.yaml")):
        cp_data = load_yaml(path)
        errors += validate_schema(cp_data, "checkpoint.schema.json", str(path.relative_to(root)))
        errors += verify_checkpoint_integrity(cp_data)

    lease_id = current.get("current_lease")
    if lease_id:
        path = lease_file(root, lease_id)
        if not path.exists():
            errors.append(f"current: missing lease {lease_id}")
        else:
            lease = load_yaml(path)
            errors += validate_schema(lease, "authorization-lease.schema.json", str(path.relative_to(root)))
            if lease.get("status") != "active":
                errors.append(f"current: lease {lease_id} is not active")
            if current_task and lease.get("task_id") != current_task:
                errors.append(f"current: lease {lease_id} does not belong to {current_task}")
            if current_micro and lease.get("micro_change_id") != current_micro:
                errors.append(f"current: lease {lease_id} does not belong to {current_micro}")
            if not current_task and not current_micro:
                errors.append(f"current: lease {lease_id} exists without current unit")
            if current_task:
                tf = task_file(root, current_task)
                if tf.exists():
                    task_data = load_yaml(tf)
                    expected_path = f".cpt/leases/{lease_id}.yaml"
                    if task_data.get("authorization_lease", {}).get("path") != expected_path:
                        errors.append(f"current: task {current_task} does not reference active lease {lease_id}")

    checkpoint_id = current.get("latest_checkpoint")
    if checkpoint_id:
        path = checkpoint_file(root, checkpoint_id)
        if not path.exists():
            errors.append(f"current: missing checkpoint {checkpoint_id}")
        else:
            cp = load_yaml(path)
            errors += validate_schema(cp, "checkpoint.schema.json", str(path.relative_to(root)))
            errors += verify_checkpoint_integrity(cp)

    summary = p["summary"].read_text(encoding="utf-8")
    match = re.search(r"cpt-state-revision:\s*(\d+)", summary)
    if not match:
        errors.append("runtime-summary: missing state revision marker")
    elif int(match.group(1)) != current.get("state_revision"):
        errors.append("runtime-summary: revision does not match current.yaml")

    expected_summary = render_summary(root, current, index)
    if summary != expected_summary:
        warnings.append("runtime-summary: content differs from generated projection; run render-summary")

    agents = root / "AGENTS.md"
    if agents.exists():
        size = agents.stat().st_size
        if size > 8192:
            warnings.append(f"AGENTS.md is {size} bytes; kernel target is approximately 4–6 KB")

    return errors, warnings


def verify_checkpoint_integrity(cp: dict) -> list[str]:
    errors = []
    snap = cp["snapshot"]
    integrity = cp["integrity"]
    mapping = {
        "current_sha256": snap.get("current"),
        "task_index_sha256": snap.get("task_index"),
        "active_task_sha256": snap.get("active_task"),
        "active_micro_change_sha256": snap.get("active_micro_change"),
        "active_lease_sha256": snap.get("active_lease"),
    }
    for key, data in mapping.items():
        actual = digest(data)
        if actual != integrity.get(key):
            errors.append(f"checkpoint {cp['id']}: integrity mismatch for {key}")
    return errors


def next_task_id(index: dict) -> str:
    return next_numeric_id((e["id"] for e in index.get("tasks", [])), "TKT")


def next_micro_id(root: Path) -> str:
    ids = [p.stem for p in paths(root)["micro_changes"].glob("MC-*.yaml")]
    return next_numeric_id(ids, "MC")


def command_status(root: Path, _args) -> int:
    runtime, current, index = load_state(root)
    payload = {
        "runtime_id": runtime["runtime_id"],
        "storage_mode": runtime["storage_mode"],
        "runtime_status": current["runtime_status"],
        "current_task": current["current_task"],
        "current_micro_change": current["current_micro_change"],
        "current_lease": current["current_lease"],
        "latest_checkpoint": current["latest_checkpoint"],
        "state_revision": current["state_revision"],
        "tasks": len(index.get("tasks", [])),
        "blockers": current.get("blockers", []),
        "next_operation": current.get("next_operation"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def command_validate(root: Path, _args) -> int:
    errors, warnings = validate_runtime(root)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("RUNTIME VALIDATION PASSED")
    return 0


def command_render_summary(root: Path, _args) -> int:
    with runtime_lock(root):
        write_summary(root)
    print("runtime-summary.md regenerated")
    return 0


def command_create_task(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        if args.activate and (current.get("current_task") or current.get("current_micro_change")):
            raise RuntimeError("A current unit already exists. Complete or deactivate it first.")
        task_id = next_task_id(index)
        ts = utc_now()
        status = "active" if args.activate else "proposed"
        task = {
            "schema_version": SCHEMA_VERSION,
            "id": task_id,
            "title": args.title,
            "status": status,
            "task_type": args.task_type,
            "complexity": args.complexity,
            "user_intent": args.intent or args.objective,
            "objective": args.objective,
            "scope": {"in": [], "out": []},
            "acceptance_criteria": [],
            "product_knowledge": [],
            "expertise": {"roles": [], "skills": [], "gates": []},
            "impact_map": {"status": "not_started", "path": None},
            "authorization_lease": {"status": "none", "path": None},
            "verification": {"plan": [], "results": []},
            "blockers": [],
            "next_operation": {"type": "bounded_discovery", "summary": "Perform bounded discovery and prepare the Impact Map."},
            "created_at": ts,
            "updated_at": ts,
        }
        errors = validate_schema(task, "task.schema.json", task_id)
        if errors:
            raise RuntimeError("; ".join(errors))
        entry = {"id": task_id, "title": args.title, "status": status, "file": f".cpt/tasks/{task_id}.yaml", "updated_at": ts}
        index["tasks"].append(entry)
        index["updated_at"] = ts
        if args.activate:
            current["current_task"] = task_id
            current["runtime_status"] = "active"
            current["next_operation"] = copy.deepcopy(task["next_operation"])
        bump(current)
        atomic_write_yaml(task_file(root, task_id), task)
        atomic_write_yaml(p["task_index"], index)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(task_id)
    return 0


def command_activate_task(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        if current.get("current_task") or current.get("current_micro_change"):
            raise RuntimeError("A current unit already exists.")
        matches = [e for e in index["tasks"] if e["id"] == args.task]
        if not matches:
            raise RuntimeError(f"Unknown task: {args.task}")
        entry = matches[0]
        task = load_yaml(root / entry["file"])
        if task["status"] in {"done", "cancelled"}:
            raise RuntimeError(f"Cannot activate {task['status']} task")
        ts = utc_now()
        task["status"] = "active"
        task["updated_at"] = ts
        entry["status"] = "active"
        entry["updated_at"] = ts
        index["updated_at"] = ts
        current["current_task"] = args.task
        current["runtime_status"] = "active"
        current["next_operation"] = copy.deepcopy(task["next_operation"])
        bump(current)
        atomic_write_yaml(root / entry["file"], task)
        atomic_write_yaml(p["task_index"], index)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(f"Activated {args.task}")
    return 0


def command_complete_task(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        task_id = args.task or current.get("current_task")
        if not task_id:
            raise RuntimeError("No task specified or active")
        matches = [e for e in index["tasks"] if e["id"] == task_id]
        if not matches:
            raise RuntimeError(f"Unknown task: {task_id}")
        entry = matches[0]
        task = load_yaml(root / entry["file"])
        ts = utc_now()
        task["status"] = "done"
        task["next_operation"] = {"type": "complete", "summary": "Task complete."}
        task["updated_at"] = ts
        entry["status"] = "done"
        entry["updated_at"] = ts
        index["updated_at"] = ts
        if current.get("current_task") == task_id:
            if current.get("current_lease"):
                lf = lease_file(root, current["current_lease"])
                if lf.exists():
                    lease = load_yaml(lf)
                    lease["status"] = "consumed"
                    lease["updated_at"] = ts
                    atomic_write_yaml(lf, lease)
                task["authorization_lease"] = {"status": "consumed", "path": f".cpt/leases/{current['current_lease']}.yaml"}
            current["current_task"] = None
            current["current_lease"] = None
            current["runtime_status"] = "ready"
            current["next_operation"] = {"type": "await_user_task", "summary": "Await a user task and select Micro Change or Standard Task workflow."}
            bump(current)
        atomic_write_yaml(root / entry["file"], task)
        atomic_write_yaml(p["task_index"], index)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(f"Completed {task_id}")
    return 0


def command_micro_start(root: Path, args) -> int:
    if not args.confirm_eligible:
        raise RuntimeError("Micro change requires --confirm-eligible after checking every eligibility condition.")
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        if current.get("current_task") or current.get("current_micro_change"):
            raise RuntimeError("A current unit already exists.")
        micro_id = next_micro_id(root)
        ts = utc_now()
        eligibility = {k: True for k in ["local_scope","reversible","low_risk","no_public_api_change","no_dependency_change","no_data_migration","no_security_privacy_auth_risk","no_broad_external_read","verification_obvious"]}
        micro = {
            "schema_version": SCHEMA_VERSION,
            "id": micro_id,
            "title": args.title,
            "status": "active",
            "user_intent": args.intent,
            "authorization_basis": "direct_user_request",
            "eligibility": eligibility,
            "target_paths": args.target,
            "read_scope": args.target,
            "write_scope": args.target,
            "verification": args.verify,
            "escalation_reason": None,
            "created_at": ts,
            "updated_at": ts,
        }
        errors = validate_schema(micro, "micro-change.schema.json", micro_id)
        if errors:
            raise RuntimeError("; ".join(errors))
        current["current_micro_change"] = micro_id
        current["runtime_status"] = "active"
        current["next_operation"] = {"type": "implementation", "summary": "Perform only the declared micro change, then run the smallest verification."}
        bump(current)
        atomic_write_yaml(micro_file(root, micro_id), micro)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(micro_id)
    return 0


def command_micro_complete(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        micro_id = args.micro or current.get("current_micro_change")
        if not micro_id:
            raise RuntimeError("No micro change specified or active")
        mf = micro_file(root, micro_id)
        if not mf.exists():
            raise RuntimeError(f"Unknown micro change: {micro_id}")
        micro = load_yaml(mf)
        micro["status"] = "done"
        micro["updated_at"] = utc_now()
        if current.get("current_micro_change") == micro_id:
            if current.get("current_lease"):
                lf = lease_file(root, current["current_lease"])
                if lf.exists():
                    lease = load_yaml(lf)
                    lease["status"] = "consumed"
                    lease["updated_at"] = utc_now()
                    atomic_write_yaml(lf, lease)
            current["current_micro_change"] = None
            current["current_lease"] = None
            current["runtime_status"] = "ready"
            current["next_operation"] = {"type": "await_user_task", "summary": "Await a user task and select Micro Change or Standard Task workflow."}
            bump(current)
        atomic_write_yaml(mf, micro)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(f"Completed {micro_id}")
    return 0


def command_micro_escalate(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        micro_id = args.micro or current.get("current_micro_change")
        if not micro_id:
            raise RuntimeError("No micro change specified or active")
        mf = micro_file(root, micro_id)
        if not mf.exists():
            raise RuntimeError(f"Unknown micro change: {micro_id}")
        micro = load_yaml(mf)
        micro["status"] = "escalated"
        micro["escalation_reason"] = args.reason
        micro["updated_at"] = utc_now()
        if current.get("current_micro_change") == micro_id:
            current["current_micro_change"] = None
            current["current_lease"] = None
            current["runtime_status"] = "ready"
            current["next_operation"] = {"type": "intake", "summary": "Create a Standard Task for the escalated change before project writes."}
            bump(current)
        atomic_write_yaml(mf, micro)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(f"Escalated {micro_id}")
    return 0


def command_lease_create(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        _, current, index = load_state(root)
        unit = args.task or args.micro
        if args.task and current.get("current_task") != args.task:
            raise RuntimeError("Lease task must be the current task")
        if args.micro and current.get("current_micro_change") != args.micro:
            raise RuntimeError("Lease micro change must be current")
        if not unit:
            raise RuntimeError("Specify --task or --micro")
        serial = 1
        while True:
            lease_id = f"LEASE-{unit}-{serial:03d}"
            if not lease_file(root, lease_id).exists():
                break
            serial += 1
        ts = utc_now()
        verify = [{"command": cmd, "cwd": args.cwd, "purpose": "Verify approved task outcome"} for cmd in args.verify]
        lease = {
            "schema_version": SCHEMA_VERSION,
            "id": lease_id,
            "status": "active",
            "task_id": args.task,
            "micro_change_id": args.micro,
            "read_scope": args.read,
            "write_scope": args.write,
            "verification_scope": verify,
            "delegation": {"allowed": bool(args.worker), "max_workers": len(args.worker), "read_only": args.workers_read_only, "allowed_worker_archetypes": args.worker},
            "forbidden_operations": args.forbid,
            "expires": {"task_completion": True, "scope_change": True, "manual_revoke": True, "at": args.expires_at},
            "granted_by": "user",
            "rationale": args.rationale,
            "granted_at": ts,
            "updated_at": ts,
        }
        errors = validate_schema(lease, "authorization-lease.schema.json", lease_id)
        if errors:
            raise RuntimeError("; ".join(errors))
        if current.get("current_lease"):
            old = lease_file(root, current["current_lease"])
            if old.exists():
                old_data = load_yaml(old)
                old_data["status"] = "revoked"
                old_data["updated_at"] = ts
                atomic_write_yaml(old, old_data)
        current["current_lease"] = lease_id
        bump(current)
        atomic_write_yaml(lease_file(root, lease_id), lease)
        atomic_write_yaml(p["current"], current)
        if args.task:
            tf = task_file(root, args.task)
            task = load_yaml(tf)
            task["authorization_lease"] = {"status": "active", "path": f".cpt/leases/{lease_id}.yaml"}
            task["updated_at"] = ts
            atomic_write_yaml(tf, task)
            for entry in index["tasks"]:
                if entry["id"] == args.task:
                    entry["updated_at"] = ts
            index["updated_at"] = ts
            atomic_write_yaml(p["task_index"], index)
        write_summary(root, current, index)
    print(lease_id)
    return 0


def make_checkpoint(root: Path, source: str, reason: str) -> dict:
    _, current, index = load_state(root)
    active_task = load_yaml(task_file(root, current["current_task"])) if current.get("current_task") else None
    active_micro = load_yaml(micro_file(root, current["current_micro_change"])) if current.get("current_micro_change") else None
    active_lease = load_yaml(lease_file(root, current["current_lease"])) if current.get("current_lease") else None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = hashlib.sha256(f"{stamp}-{time.time_ns()}".encode()).hexdigest()[:6]
    cp_id = f"CP-{stamp}-{suffix}"
    cp = {
        "schema_version": SCHEMA_VERSION,
        "id": cp_id,
        "source": source,
        "reason": reason,
        "created_at": utc_now(),
        "runtime_revision": current["state_revision"],
        "snapshot": {"current": copy.deepcopy(current), "task_index": copy.deepcopy(index), "active_task": active_task, "active_micro_change": active_micro, "active_lease": active_lease},
        "unresolved_work": {"blockers": copy.deepcopy(current.get("blockers", [])), "unfinished_verification": [], "next_operation": copy.deepcopy(current.get("next_operation")), "worker_registry": []},
        "integrity": {},
    }
    cp["integrity"] = {
        "current_sha256": digest(cp["snapshot"]["current"]),
        "task_index_sha256": digest(cp["snapshot"]["task_index"]),
        "active_task_sha256": digest(active_task),
        "active_micro_change_sha256": digest(active_micro),
        "active_lease_sha256": digest(active_lease),
    }
    return cp


def command_checkpoint(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        errors, _ = validate_runtime(root)
        if errors:
            raise RuntimeError("Cannot checkpoint invalid runtime: " + "; ".join(errors))
        cp = make_checkpoint(root, args.source, args.reason)
        current = load_yaml(p["current"])
        index = load_yaml(p["task_index"])
        current["latest_checkpoint"] = cp["id"]
        bump(current)
        # Snapshot should represent pre-checkpoint state; current pointer update is intentionally outside snapshot.
        atomic_write_yaml(checkpoint_file(root, cp["id"]), cp)
        atomic_write_yaml(p["current"], current)
        write_summary(root, current, index)
    print(cp["id"])
    return 0


def resolve_checkpoint(root: Path, value: str) -> Path:
    if value != "latest":
        path = checkpoint_file(root, value)
        if not path.exists():
            raise RuntimeError(f"Checkpoint not found: {value}")
        return path
    current = load_yaml(paths(root)["current"])
    cp_id = current.get("latest_checkpoint")
    if not cp_id:
        raise RuntimeError("No latest checkpoint")
    path = checkpoint_file(root, cp_id)
    if not path.exists():
        raise RuntimeError(f"Latest checkpoint file missing: {cp_id}")
    return path


def snapshot_diff(root: Path, cp: dict) -> list[str]:
    _, current, index = load_state(root)
    snap = cp["snapshot"]
    diffs = []
    # Ignore latest_checkpoint/update timestamp/revision because checkpoint creation updates them.
    cur_cmp = copy.deepcopy(current)
    snap_cur = copy.deepcopy(snap["current"])
    for obj in (cur_cmp, snap_cur):
        obj.pop("latest_checkpoint", None)
        obj.pop("updated_at", None)
        obj.pop("state_revision", None)
    if cur_cmp != snap_cur:
        diffs.append("current state differs")
    if index != snap["task_index"]:
        diffs.append("task index differs")
    if snap["active_task"] is not None:
        path = task_file(root, snap["active_task"]["id"])
        live = load_yaml(path) if path.exists() else None
        if live != snap["active_task"]:
            diffs.append("active task differs")
    if snap["active_micro_change"] is not None:
        path = micro_file(root, snap["active_micro_change"]["id"])
        live = load_yaml(path) if path.exists() else None
        if live != snap["active_micro_change"]:
            diffs.append("active micro change differs")
    if snap["active_lease"] is not None:
        path = lease_file(root, snap["active_lease"]["id"])
        live = load_yaml(path) if path.exists() else None
        if live != snap["active_lease"]:
            diffs.append("active lease differs")
    return diffs


def restore_checkpoint(root: Path, cp: dict) -> None:
    p = paths(root)
    snap = cp["snapshot"]
    current = copy.deepcopy(snap["current"])
    current["latest_checkpoint"] = cp["id"]
    current["state_revision"] = max(int(current.get("state_revision", 0)), int(cp["runtime_revision"])) + 1
    current["updated_at"] = utc_now()
    index = copy.deepcopy(snap["task_index"])
    atomic_write_yaml(p["current"], current)
    atomic_write_yaml(p["task_index"], index)
    if snap["active_task"] is not None:
        atomic_write_yaml(task_file(root, snap["active_task"]["id"]), snap["active_task"])
    if snap["active_micro_change"] is not None:
        atomic_write_yaml(micro_file(root, snap["active_micro_change"]["id"]), snap["active_micro_change"])
    if snap["active_lease"] is not None:
        atomic_write_yaml(lease_file(root, snap["active_lease"]["id"]), snap["active_lease"])
    write_summary(root, current, index)


def command_recover(root: Path, args) -> int:
    with runtime_lock(root):
        path = resolve_checkpoint(root, args.checkpoint)
        cp = load_yaml(path)
        errors = validate_schema(cp, "checkpoint.schema.json", str(path.relative_to(root))) + verify_checkpoint_integrity(cp)
        if errors:
            raise RuntimeError("; ".join(errors))
        diffs = snapshot_diff(root, cp)
        if args.verify_only:
            if diffs:
                print("CHECKPOINT MISMATCH")
                for item in diffs:
                    print(f"- {item}")
                return 2
            print("CHECKPOINT MATCH")
            return 0
        if not diffs:
            print("Current state already matches checkpoint snapshot")
            return 0
        backup = make_checkpoint(root, "pre_recovery", f"Automatic backup before restoring {cp['id']}")
        atomic_write_yaml(checkpoint_file(root, backup["id"]), backup)
        restore_checkpoint(root, cp)
    print(f"Recovered from {cp['id']} (backup: {backup['id']})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CPT OS 4.0 Alpha 1 runtime CLI")
    parser.add_argument("--root", type=Path, help="Runtime root; defaults to nearest parent containing .cpt/runtime.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status")
    sub.add_parser("validate")
    sub.add_parser("render-summary")

    p = sub.add_parser("create-task")
    p.add_argument("--title", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--intent")
    p.add_argument("--task-type", default="implementation")
    p.add_argument("--complexity", choices=["tiny","fast","standard","complex","high_risk"], default="standard")
    p.add_argument("--activate", action="store_true")

    p = sub.add_parser("activate-task")
    p.add_argument("task")

    p = sub.add_parser("complete-task")
    p.add_argument("--task")

    p = sub.add_parser("micro-start")
    p.add_argument("--title", required=True)
    p.add_argument("--intent", required=True)
    p.add_argument("--target", action="append", required=True)
    p.add_argument("--verify", action="append", required=True)
    p.add_argument("--confirm-eligible", action="store_true")

    p = sub.add_parser("micro-complete")
    p.add_argument("--micro")

    p = sub.add_parser("micro-escalate")
    p.add_argument("--micro")
    p.add_argument("--reason", required=True)

    p = sub.add_parser("lease-create")
    owner = p.add_mutually_exclusive_group(required=True)
    owner.add_argument("--task")
    owner.add_argument("--micro")
    p.add_argument("--read", action="append", default=[])
    p.add_argument("--write", action="append", default=[])
    p.add_argument("--verify", action="append", default=[])
    p.add_argument("--cwd", default=".")
    p.add_argument("--worker", action="append", default=[])
    p.set_defaults(workers_read_only=True)
    p.add_argument("--workers-may-write", action="store_false", dest="workers_read_only", help="Allow approved workers to write; read-only is the safe default")
    p.add_argument("--forbid", action="append", default=["dependency_change","migration","public_api_change","network_access","destructive_git"])
    p.add_argument("--expires-at")
    p.add_argument("--rationale")

    p = sub.add_parser("checkpoint")
    p.add_argument("--source", choices=["manual","pre_compact","phase_handoff","synthetic"], default="manual")
    p.add_argument("--reason", required=True)

    p = sub.add_parser("recover")
    p.add_argument("--checkpoint", default="latest")
    p.add_argument("--verify-only", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        root = find_root(args.root) if args.root else find_root()
        commands = {
            "status": command_status,
            "validate": command_validate,
            "render-summary": command_render_summary,
            "create-task": command_create_task,
            "activate-task": command_activate_task,
            "complete-task": command_complete_task,
            "micro-start": command_micro_start,
            "micro-complete": command_micro_complete,
            "micro-escalate": command_micro_escalate,
            "lease-create": command_lease_create,
            "checkpoint": command_checkpoint,
            "recover": command_recover,
        }
        return commands[args.command](root, args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
