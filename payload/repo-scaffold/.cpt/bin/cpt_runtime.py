#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import fnmatch
import subprocess
import json
import os
import re
import shutil
import shlex
import uuid
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
    import fastjsonschema
except ImportError as exc:
    raise SystemExit(
        "Missing runtime dependencies. Install PyYAML and fastjsonschema using the CPT package requirements."
    ) from exc

SCHEMA_VERSION = "4.0-alpha6"
KNOWLEDGE_SCHEMA_VERSION = "4.0-alpha6"


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
        "knowledge": cpt / "knowledge",
        "knowledge_index": cpt / "knowledge" / "index.yaml",
        "knowledge_artifacts": cpt / "knowledge" / "artifacts",
        "knowledge_views": cpt / "knowledge" / "views",
        "enforcement": cpt / "enforcement.yaml",
        "audit": cpt / "audit" / "events.jsonl",
        "workers": cpt / "workers",
    }


_SCHEMA_BUNDLE: dict[str, Any] | None = None


def schema_bundle() -> dict[str, Any]:
    global _SCHEMA_BUNDLE
    if _SCHEMA_BUNDLE is None:
        _SCHEMA_BUNDLE = json.loads((package_root() / "schema-bundle.json").read_text(encoding="utf-8"))
    return _SCHEMA_BUNDLE


_COMPILED_VALIDATORS: dict[str, Any] = {}


def validate_schema(data: Any, name: str, label: str) -> list[str]:
    try:
        validator = _COMPILED_VALIDATORS.get(name)
        if validator is None:
            validator = fastjsonschema.compile(schema_bundle()[name], use_default=False)
            _COMPILED_VALIDATORS[name] = validator
        validator(data)
        return []
    except fastjsonschema.JsonSchemaException as error:
        loc = error.path or "<root>"
        return [f"{label}:{loc}: {error.message}"]


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
    knowledge = load_knowledge_index(root, required=False)
    if knowledge:
        stale = sum(1 for a in knowledge.get("artifacts", []) if a.get("freshness") != "current")
        knowledge_text = f"`{knowledge['id']}` ({len(knowledge.get('artifacts', []))} artifacts, {stale} requiring review)"
    else:
        knowledge_text = "not initialized"
    return f"""# Runtime Summary
<!-- cpt-state-revision: {current['state_revision']} -->

Generated from `.cpt/current.yaml` and `.cpt/task-index.yaml`. Do not edit manually.

## State

- Runtime status: `{current['runtime_status']}`
- Current task: {task_label}
- Current micro change: `{micro_label}`
- Current lease: `{lease_label}`
- Latest checkpoint: `{checkpoint_label}`
- Product Knowledge: {knowledge_text}

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

    enforcement_path = p["enforcement"]
    if enforcement_path.exists():
        enforcement = load_yaml(enforcement_path)
        errors += validate_schema(enforcement, "enforcement.schema.json", ".cpt/enforcement.yaml")
    for worker in sorted(p["workers"].glob("*.yaml")):
        errors += validate_schema(load_yaml(worker), "worker-record.schema.json", str(worker.relative_to(root)))

    knowledge_errors, knowledge_warnings = validate_knowledge(root, check_views=True)
    errors += knowledge_errors
    warnings += knowledge_warnings

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
    knowledge = load_knowledge_index(root, required=False)
    payload["knowledge"] = None if knowledge is None else {"id": knowledge["id"], "mode": knowledge["mode"], "status": knowledge["status"], "artifacts": len(knowledge.get("artifacts", [])), "requires_review": sum(1 for a in knowledge.get("artifacts", []) if a.get("freshness") != "current")}
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
            "knowledge_update": {"status": "not_assessed", "affected_artifacts": [], "summary": None, "updated_at": None},
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
        knowledge_update = task.get("knowledge_update")
        if knowledge_update and knowledge_update.get("status") not in {"not_required", "applied", "deferred"}:
            raise RuntimeError("Task knowledge update is not accounted for. Use knowledge-task-assess before completion.")
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
        default_forbidden = {"dependency_change", "migration", "public_api_change", "network_access", "destructive_git"}
        allowed_operations = set(args.allow_operation or [])
        forbidden_operations = sorted((default_forbidden | set(args.forbid or [])) - allowed_operations)
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
            "forbidden_operations": forbidden_operations,
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
        "unresolved_work": {"blockers": copy.deepcopy(current.get("blockers", [])), "unfinished_verification": [], "next_operation": copy.deepcopy(current.get("next_operation")), "worker_registry": copy.deepcopy(worker_records(root))},
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
    checkpoint_workers = cp.get("unresolved_work", {}).get("worker_registry", [])
    if worker_records(root) != checkpoint_workers:
        diffs.append("worker lifecycle state differs")
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



# ---- Product Knowledge ----------------------------------------------------

CLAIM_TRANSITIONS = {
    "planned": {"confirmed", "deprecated"},
    "hypothesized": {"inferred", "confirmed", "needs_review", "deprecated"},
    "inferred": {"confirmed", "needs_review", "stale", "deprecated"},
    "confirmed": {"validated", "needs_review", "stale", "deprecated"},
    "validated": {"needs_review", "stale", "deprecated"},
    "needs_review": {"confirmed", "validated", "stale", "deprecated"},
    "stale": {"needs_review", "confirmed", "validated", "deprecated"},
    "deprecated": set(),
}

KNOWLEDGE_TARGET_LINES = {
    "product_map": (80, 150),
    "area_map": (70, 140),
    "flow_map": (60, 120),
    "decision_record": (40, 90),
    "api_data_contract": (60, 120),
    "context_packet": (80, 160),
}


def knowledge_artifact_file(root: Path, artifact_id: str) -> Path:
    return paths(root)["knowledge_artifacts"] / f"{artifact_id}.yaml"


def knowledge_view_file(root: Path, artifact_id: str) -> Path:
    return paths(root)["knowledge_views"] / f"{artifact_id}.md"


def knowledge_index_view_file(root: Path) -> Path:
    return paths(root)["knowledge_views"] / "KNOWLEDGE_INDEX.md"


def source_revision(kind: str, value: str | None, recorded_at: str | None = None) -> dict:
    return {"kind": kind, "value": value, "recorded_at": recorded_at or utc_now()}


def load_knowledge_index(root: Path, required: bool = True) -> dict | None:
    path = paths(root)["knowledge_index"]
    if not path.exists():
        if required:
            raise RuntimeError("Product Knowledge is not initialized. Run knowledge-init.")
        return None
    return load_yaml(path)


def artifact_content_skeleton(artifact_type: str, task_id: str | None = None) -> dict:
    entry = lambda: []
    skeletons = {
        "product_map": {"summary": "", "actors": [], "areas": entry(), "surfaces": entry(), "top_flows": entry(), "routing_guidance": [], "shared_boundaries": []},
        "area_map": {"summary": "", "actors": [], "surfaces": entry(), "responsibilities": entry(), "states": entry(), "candidate_flows": entry(), "boundaries": {"inside": [], "outside": []}, "where_to_look_next": []},
        "flow_map": {"summary": "", "actors": [], "trigger": "", "preconditions": [], "steps": [], "states": [], "data_touchpoints": [], "failure_states": [], "permissions": [], "files_involved": []},
        "decision_record": {"decision": "", "decision_status": "proposed", "context": "", "alternatives": [], "consequences": []},
        "api_data_contract": {"summary": "", "boundaries": [], "entities": entry(), "operations": entry(), "error_model": [], "auth_model": [], "ui_implications": [], "task_driven_unknowns": []},
        "context_packet": {"task_id": task_id or "", "objective": "", "selected_artifacts": [], "current_evidence": [], "impact_map": {}, "risks": [], "verification_plan": []},
    }
    return copy.deepcopy(skeletons[artifact_type])


def next_claim_id(artifact: dict) -> str:
    return next_numeric_id((c["id"] for c in artifact.get("claims", [])), "CLM")


def next_unknown_id(artifact: dict) -> str:
    return next_numeric_id((u["id"] for u in artifact.get("unknowns", [])), "UNK")


def claim_counts(artifact: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for claim in artifact.get("claims", []):
        counts[claim["lifecycle"]] = counts.get(claim["lifecycle"], 0) + 1
    return counts


KNOWLEDGE_CLASSIFICATIONS = ("public", "internal", "confidential", "restricted")
KNOWLEDGE_EXTERNAL_SHARING = ("allowed", "after_sanitization", "prohibited")
KNOWLEDGE_SANITIZATION_STATUSES = ("not_reviewed", "not_required", "sanitized", "blocked")
KNOWLEDGE_SENSITIVE_PATTERNS = (
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("openai_style_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{20,}=*")),
    ("credential_assignment", re.compile(r"(?i)\b(?:password|passwd|client_secret|api_secret)\s*[:=]\s*[\"']?[A-Za-z0-9!@#$%^&*()_+./=-]{8,}")),
)


def default_sharing(classification: str = "internal", external_sharing: str = "prohibited") -> dict:
    status = "not_required" if external_sharing == "prohibited" or (classification == "public" and external_sharing == "allowed") else "not_reviewed"
    return {"external_sharing": external_sharing, "sanitization_status": status, "redactions": [], "notes": []}


def sensitive_findings(value: Any, location: str = "$") -> list[dict]:
    findings: list[dict] = []
    if isinstance(value, dict):
        for key, child in value.items():
            findings.extend(sensitive_findings(child, f"{location}.{key}"))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            findings.extend(sensitive_findings(child, f"{location}[{i}]"))
    elif isinstance(value, str):
        for pattern_id, pattern in KNOWLEDGE_SENSITIVE_PATTERNS:
            if pattern.search(value):
                findings.append({"pattern": pattern_id, "location": location})
    return findings


def sharing_policy_errors(artifact: dict, *, external_check: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    classification = artifact.get("data_classification", "internal")
    sharing = artifact.get("sharing") or {}
    external = sharing.get("external_sharing", "prohibited")
    status = sharing.get("sanitization_status", "not_reviewed")
    if classification == "restricted" and external != "prohibited":
        errors.append(f"{artifact.get('id')}: restricted knowledge must prohibit external sharing")
    if classification == "confidential" and external == "allowed":
        errors.append(f"{artifact.get('id')}: confidential knowledge cannot allow external sharing without sanitization")
    if status == "blocked" and external != "prohibited":
        errors.append(f"{artifact.get('id')}: blocked sanitization status requires prohibited external sharing")
    if external == "allowed" and status not in {"not_required", "sanitized"}:
        errors.append(f"{artifact.get('id')}: external sharing is allowed but sanitization is not complete")
    if external == "after_sanitization" and status == "not_reviewed":
        warnings.append(f"{artifact.get('id')}: external sharing requires a sanitization review")
    if external_check and external == "prohibited":
        errors.append(f"{artifact.get('id')}: external sharing is prohibited")
    if external_check and external == "after_sanitization" and status != "sanitized":
        errors.append(f"{artifact.get('id')}: external sharing requires sanitization_status=sanitized")
    return errors, warnings


def artifact_index_entry(artifact: dict) -> dict:
    return {
        "id": artifact["id"], "artifact_type": artifact["artifact_type"], "title": artifact["title"],
        "path": f".cpt/knowledge/artifacts/{artifact['id']}.yaml", "view_path": f".cpt/knowledge/views/{artifact['id']}.md",
        "status": artifact["status"], "freshness": artifact["freshness"], "confidence": artifact["confidence"],
        "perspective": artifact["perspective"], "owner_role": artifact["owner_role"],
        "data_classification": artifact["data_classification"], "sanitization_status": artifact["sharing"]["sanitization_status"],
        "source_revision": copy.deepcopy(artifact["source_revision"]),
        "dependencies": copy.deepcopy(artifact.get("dependencies", [])), "review_triggers": copy.deepcopy(artifact.get("review_triggers", [])),
        "claim_counts": claim_counts(artifact), "updated_at": artifact["updated_at"],
    }


def sync_artifact_in_index(index: dict, artifact: dict) -> None:
    entry = artifact_index_entry(artifact)
    matches = [i for i, existing in enumerate(index.get("artifacts", [])) if existing["id"] == artifact["id"]]
    if matches:
        index["artifacts"][matches[0]] = entry
    else:
        index.setdefault("artifacts", []).append(entry)
    index["updated_at"] = utc_now()


def knowledge_dependency_cycles(artifacts: dict[str, dict]) -> list[list[str]]:
    graph = {aid: [dep["artifact_id"] for dep in artifact.get("dependencies", []) if dep["artifact_id"] in artifacts] for aid, artifact in artifacts.items()}
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            if cycle not in cycles:
                cycles.append(cycle)
            return
        if node in visited:
            return
        visiting.add(node); stack.append(node)
        for dep in graph.get(node, []):
            visit(dep)
        stack.pop(); visiting.remove(node); visited.add(node)

    for node in graph:
        visit(node)
    return cycles


def semantic_knowledge_errors(artifact: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    claim_ids = [c.get("id") for c in artifact.get("claims", [])]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append(f"{artifact['id']}: duplicate claim IDs")
    unknown_ids = [u.get("id") for u in artifact.get("unknowns", [])]
    if len(unknown_ids) != len(set(unknown_ids)):
        errors.append(f"{artifact['id']}: duplicate unknown IDs")
    for claim in artifact.get("claims", []):
        lifecycle = claim["lifecycle"]
        evidence = claim.get("evidence", [])
        types = {item["type"] for item in evidence}
        if evidence and claim.get("evidence_depth") == "none":
            errors.append(f"{artifact['id']}:{claim['id']}: evidence_depth cannot be none when evidence exists")
        if not evidence and claim.get("evidence_depth") != "none":
            errors.append(f"{artifact['id']}:{claim['id']}: evidence_depth requires evidence")
        if lifecycle == "confirmed" and not evidence:
            errors.append(f"{artifact['id']}:{claim['id']}: confirmed claim requires evidence")
        if lifecycle == "validated" and not ({"test", "runtime_observation"} & types):
            errors.append(f"{artifact['id']}:{claim['id']}: validated claim requires test or runtime_observation evidence")
        if lifecycle == "hypothesized" and claim["confidence"] == "high":
            errors.append(f"{artifact['id']}:{claim['id']}: hypothesis cannot have high confidence")
        if lifecycle == "inferred" and claim["confidence"] == "high":
            warnings.append(f"{artifact['id']}:{claim['id']}: high-confidence inference should be reviewed")
        if lifecycle == "validated" and claim["source_revision"]["kind"] == "none":
            errors.append(f"{artifact['id']}:{claim['id']}: validated claim requires source revision")
    dep_ids = [d["artifact_id"] for d in artifact.get("dependencies", [])]
    if artifact["id"] in dep_ids:
        errors.append(f"{artifact['id']}: artifact cannot depend on itself")
    policy_errors, policy_warnings = sharing_policy_errors(artifact)
    errors.extend(policy_errors); warnings.extend(policy_warnings)
    for finding in sensitive_findings(artifact):
        errors.append(f"{artifact['id']}: possible sensitive value ({finding['pattern']}) at {finding['location']}; redact before storing canonical knowledge")
    return errors, warnings


def validate_knowledge(root: Path, check_views: bool = True) -> tuple[list[str], list[str]]:
    p = paths(root)
    errors: list[str] = []
    warnings: list[str] = []
    index = load_knowledge_index(root, required=False)
    if index is None:
        return errors, warnings
    errors += validate_schema(index, "knowledge-index.schema.json", ".cpt/knowledge/index.yaml")
    ids = [e.get("id") for e in index.get("artifacts", [])]
    if len(ids) != len(set(ids)):
        errors.append("knowledge-index: duplicate artifact IDs")
    by_id: dict[str, dict] = {}
    for entry in index.get("artifacts", []):
        path = root / entry["path"]
        if not path.exists():
            errors.append(f"knowledge-index: missing artifact {entry['path']}")
            continue
        artifact = load_yaml(path)
        by_id[artifact["id"]] = artifact
        errors += validate_schema(artifact, "knowledge-artifact.schema.json", entry["path"])
        sem_err, sem_warn = semantic_knowledge_errors(artifact)
        errors += sem_err; warnings += sem_warn
        expected = artifact_index_entry(artifact)
        if expected != entry:
            errors.append(f"knowledge-index: entry drift for {artifact['id']}; render/sync knowledge")
        for dep in artifact.get("dependencies", []):
            if dep["artifact_id"] not in ids:
                errors.append(f"{artifact['id']}: missing dependency artifact {dep['artifact_id']}")
        if check_views:
            view = root / entry["view_path"]
            expected_view = render_knowledge_artifact(artifact)
            if not view.exists():
                warnings.append(f"knowledge view missing: {entry['view_path']}")
            elif view.read_text(encoding="utf-8") != expected_view:
                warnings.append(f"knowledge view drift: {entry['view_path']}")
            lines = expected_view.count("\n") + 1
            target = KNOWLEDGE_TARGET_LINES[artifact["artifact_type"]]
            if lines > target[1]:
                warnings.append(f"{artifact['id']}: generated view has {lines} lines; target guidance is {target[0]}–{target[1]}. Preserve quality and consider splitting lower-level detail.")
    for cycle in knowledge_dependency_cycles(by_id):
        errors.append("knowledge dependency cycle: " + " -> ".join(cycle))
    artifact_files = {path.stem for path in p["knowledge_artifacts"].glob("*.yaml")} if p["knowledge_artifacts"].exists() else set()
    orphans = artifact_files - set(ids)
    for orphan in sorted(orphans):
        warnings.append(f"orphan knowledge artifact not indexed: {orphan}")
    return errors, warnings


def md_scalar(value: Any) -> str:
    if value is None: return "none"
    if isinstance(value, bool): return "true" if value else "false"
    return str(value)


def render_section_value(value: Any, level: int = 3) -> str:
    if isinstance(value, str):
        return value or "_Not yet populated._"
    if isinstance(value, list):
        if not value: return "_None recorded._"
        if all(isinstance(item, dict) and all(not isinstance(v, (dict, list)) for v in item.values()) for item in value):
            keys = []
            for item in value:
                for key in item:
                    if key not in keys: keys.append(key)
            lines = ["| " + " | ".join(k.replace("_", " ").title() for k in keys) + " |", "|" + "|".join(["---"] * len(keys)) + "|"]
            for item in value:
                lines.append("| " + " | ".join(md_scalar(item.get(k, "")).replace("\n", " ") for k in keys) + " |")
            return "\n".join(lines)
        lines = []
        for item in value:
            if isinstance(item, dict):
                label = item.get("label") or item.get("id") or "item"
                lines.append(f"- **{label}**: {item.get('summary', '')}")
            else: lines.append(f"- {md_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, dict):
        if not value: return "_None recorded._"
        lines = []
        for k,v in value.items():
            lines.append(f"{'#' * level} {k.replace('_',' ').title()}\n\n{render_section_value(v, level+1)}")
        return "\n\n".join(lines)
    return md_scalar(value)


def render_knowledge_artifact(artifact: dict) -> str:
    lines = [f"# {artifact['title']}", "", "> Generated from canonical YAML. Do not edit this view manually.", "", "## Metadata", ""]
    metadata = [
        ("Artifact ID", artifact["id"]), ("Type", artifact["artifact_type"]), ("Mode", artifact["mode"]),
        ("Perspective", artifact["perspective"]), ("Status", artifact["status"]), ("Freshness", artifact["freshness"]),
        ("Confidence", artifact["confidence"]), ("Owner role", artifact["owner_role"]),
        ("Data classification", artifact["data_classification"]),
        ("External sharing", artifact["sharing"]["external_sharing"]),
        ("Sanitization", artifact["sharing"]["sanitization_status"]),
        ("Source revision", f"{artifact['source_revision']['kind']}:{artifact['source_revision']['value'] or 'none'}"),
        ("Updated", artifact["updated_at"]),
    ]
    lines += ["| Field | Value |", "|---|---|"] + [f"| {k} | {v} |" for k,v in metadata]
    lines += ["", "## Scope", "", artifact["scope"]["summary"] or "_Not yet populated._"]
    if artifact["scope"]["in_scope"]:
        lines += ["", "### In Scope", ""] + [f"- {x}" for x in artifact["scope"]["in_scope"]]
    if artifact["scope"]["out_of_scope"]:
        lines += ["", "### Out of Scope", ""] + [f"- {x}" for x in artifact["scope"]["out_of_scope"]]
    lines += ["", "## Content", ""]
    for key,value in artifact["content"].items():
        lines += [f"### {key.replace('_',' ').title()}", "", render_section_value(value), ""]
    lines += ["## Claims", ""]
    if artifact["claims"]:
        lines += ["| ID | Lifecycle | Confidence | Statement | Evidence Depth |", "|---|---|---|---|---|"]
        for c in artifact["claims"]:
            lines.append(f"| {c['id']} | {c['lifecycle']} | {c['confidence']} | {c['statement'].replace('|','/')} | {c['evidence_depth']} |")
        for c in artifact["claims"]:
            lines += ["", f"### {c['id']} Evidence", ""]
            if c["evidence"]:
                for e in c["evidence"]:
                    lines.append(f"- `{e['type']}` — `{e['source']}`{(' @ ' + e['locator']) if e['locator'] else ''}: {e['summary']}")
            else: lines.append("_No evidence recorded._")
            if c["unknowns"]:
                lines += ["", "Unknowns:"] + [f"- {u}" for u in c["unknowns"]]
    else: lines.append("_No claims recorded._")
    lines += ["", "## Unknowns", ""]
    if artifact["unknowns"]:
        lines += ["| ID | Status | Question | Impact | Owner |", "|---|---|---|---|---|"]
        for u in artifact["unknowns"]:
            lines.append(f"| {u['id']} | {u['status']} | {u['question'].replace('|','/')} | {u['impact'].replace('|','/')} | {u['owner_role']} |")
    else: lines.append("_None recorded._")
    lines += ["", "## Dependencies", ""]
    lines += [f"- `{d['relation']}` → `{d['artifact_id']}`" for d in artifact["dependencies"]] or ["_None recorded._"]
    lines += ["", "## Review Triggers", ""]
    if artifact["review_triggers"]:
        for t in artifact["review_triggers"]:
            lines.append(f"- **{t['id']}**: {t['description']} | paths={t['path_globs']} | events={t['events']}")
    else: lines.append("_None recorded._")
    return "\n".join(lines).rstrip() + "\n"


def render_knowledge_index(index: dict) -> str:
    lines = [f"# {index['title']}", "", "> Generated from `.cpt/knowledge/index.yaml`. Do not edit manually.", "", "## State", ""]
    lines += [f"- Mode: `{index['mode']}`", f"- Status: `{index['status']}`", f"- Owner: `{index['owner_role']}`", f"- Updated: `{index['updated_at']}`", "", "## Artifacts", ""]
    if index["artifacts"]:
        lines += ["| ID | Type | Status | Freshness | Confidence | Classification | Sanitization | Owner |", "|---|---|---|---|---|---|---|---|"]
        for a in index["artifacts"]:
            lines.append(f"| `{a['id']}` | {a['artifact_type']} | {a['status']} | {a['freshness']} | {a['confidence']} | {a['data_classification']} | {a['sanitization_status']} | {a['owner_role']} |")
    else: lines.append("_No artifacts yet._")
    return "\n".join(lines).rstrip()+"\n"


def write_knowledge_views(root: Path, index: dict, artifact_ids: list[str] | None = None) -> None:
    p = paths(root)
    p["knowledge_views"].mkdir(parents=True, exist_ok=True)
    selected = set(artifact_ids or [a["id"] for a in index.get("artifacts", [])])
    for entry in index.get("artifacts", []):
        if entry["id"] in selected:
            artifact = load_yaml(root / entry["path"])
            atomic_write_text(root / entry["view_path"], render_knowledge_artifact(artifact))
    atomic_write_text(knowledge_index_view_file(root), render_knowledge_index(index))


def save_artifact_and_index(root: Path, artifact: dict, index: dict, render: bool = True) -> None:
    errors = validate_schema(artifact, "knowledge-artifact.schema.json", artifact["id"])
    sem_err, sem_warn = semantic_knowledge_errors(artifact)
    if errors or sem_err:
        raise RuntimeError("; ".join(errors + sem_err))
    atomic_write_yaml(knowledge_artifact_file(root, artifact["id"]), artifact)
    sync_artifact_in_index(index, artifact)
    atomic_write_yaml(paths(root)["knowledge_index"], index)
    if render: write_knowledge_views(root, index, [artifact["id"]])
    for warning in sem_warn: print(f"WARNING: {warning}")


def command_knowledge_init(root: Path, args) -> int:
    p = paths(root)
    with runtime_lock(root):
        if p["knowledge_index"].exists() and not args.force:
            raise RuntimeError("Product Knowledge is already initialized. Use --force only to replace an empty index.")
        if p["knowledge_index"].exists() and args.force:
            existing = load_yaml(p["knowledge_index"])
            if existing.get("artifacts"):
                raise RuntimeError("Refusing to replace non-empty Product Knowledge index")
        p["knowledge_artifacts"].mkdir(parents=True, exist_ok=True)
        p["knowledge_views"].mkdir(parents=True, exist_ok=True)
        ts = utc_now()
        rev = source_revision(args.source_kind, args.source_value, ts)
        index = {
            "schema_version": KNOWLEDGE_SCHEMA_VERSION, "id": args.id, "title": args.title, "mode": args.mode,
            "status": "active", "owner_role": args.owner_role, "source_revision": rev, "current_source_revision": copy.deepcopy(rev),
            "artifact_sequence": 0, "artifacts": [],
            "size_policy": {"mode": "soft_targets", "quality_over_line_count": True, "default_profile": args.size_profile},
            "created_at": ts, "updated_at": ts,
        }
        errors = validate_schema(index, "knowledge-index.schema.json", ".cpt/knowledge/index.yaml")
        if errors: raise RuntimeError("; ".join(errors))
        atomic_write_yaml(p["knowledge_index"], index)
        write_knowledge_views(root, index)
        write_summary(root)
    print(args.id)
    return 0


def command_knowledge_status(root: Path, args) -> int:
    index = load_knowledge_index(root, required=False)
    if index is None:
        payload = {"initialized": False, "artifacts": 0}
    else:
        counts: dict[str,int] = {}
        freshness: dict[str,int] = {}
        for a in index.get("artifacts", []):
            counts[a["artifact_type"]] = counts.get(a["artifact_type"],0)+1
            freshness[a["freshness"]] = freshness.get(a["freshness"],0)+1
        payload = {"initialized": True, "id": index["id"], "mode": index["mode"], "status": index["status"], "artifacts": len(index["artifacts"]), "types": counts, "freshness": freshness, "current_source_revision": index.get("current_source_revision")}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def command_knowledge_create(root: Path, args) -> int:
    with runtime_lock(root):
        index = load_knowledge_index(root)
        if knowledge_artifact_file(root, args.id).exists(): raise RuntimeError(f"Artifact already exists: {args.id}")
        ts = utc_now()
        rev = copy.deepcopy(index.get("current_source_revision") or index["source_revision"])
        perspective = args.perspective or {"existing":"current","greenfield":"planned","redesign":"delta"}[index["mode"]]
        artifact = {
            "schema_version": KNOWLEDGE_SCHEMA_VERSION, "id": args.id, "artifact_type": args.type, "title": args.title,
            "mode": index["mode"], "perspective": perspective, "status": "draft", "freshness": "current", "confidence": args.confidence,
            "scope": {"summary": args.scope_summary or "", "in_scope": args.in_scope, "out_of_scope": args.out_of_scope},
            "owner_role": args.owner_role, "data_classification": args.classification,
            "sharing": default_sharing(args.classification, args.external_sharing), "source_revision": rev,
            "review_triggers": [{"id": f"TRG-{i+1:03d}", "path_globs": [path], "events": [], "description": f"Review when {path} changes."} for i,path in enumerate(args.review_path)],
            "dependencies": [{"artifact_id": dep, "relation": "depends_on"} for dep in args.depends_on],
            "claims": [], "unknowns": [],
            "size_guidance": {"profile": args.size_profile, "quality_over_line_count": True, "split_strategy": "Move lower-level detail into an existing child artifact and retain links and a compact summary."},
            "content": artifact_content_skeleton(args.type, args.task_id), "created_at": ts, "updated_at": ts,
        }
        save_artifact_and_index(root, artifact, index)
        write_summary(root)
    print(args.id)
    return 0


def make_evidence(args, revision: dict) -> list[dict]:
    if not getattr(args, "evidence_type", None): return []
    if not getattr(args, "evidence_source", None): raise RuntimeError("--evidence-source is required with --evidence-type")
    return [{"type": args.evidence_type, "source": args.evidence_source, "locator": getattr(args,"evidence_locator",None), "summary": getattr(args,"evidence_summary",None) or "", "source_revision": copy.deepcopy(revision), "observed_at": utc_now()}]


def command_knowledge_claim_add(root: Path, args) -> int:
    with runtime_lock(root):
        index = load_knowledge_index(root); artifact = load_yaml(knowledge_artifact_file(root,args.artifact))
        ts=utc_now(); evidence=make_evidence(args, artifact["source_revision"])
        claim={"id":next_claim_id(artifact),"statement":args.statement,"lifecycle":args.lifecycle,"confidence":args.confidence,"owner_role":args.owner_role,"evidence_depth":args.evidence_type or "none","evidence":evidence,"source_revision":copy.deepcopy(artifact["source_revision"]),"last_verified":ts if args.lifecycle in {"confirmed","validated"} else None,"review_triggers":[{"id":f"CLM-TRG-{i+1:03d}","path_globs":[p],"events":[],"description":f"Review claim when {p} changes."} for i,p in enumerate(args.review_path)],"unknowns":args.unknown}
        artifact["claims"].append(claim); artifact["updated_at"]=ts
        if artifact["status"]=="draft": artifact["status"]="active"
        save_artifact_and_index(root,artifact,index)
    print(claim["id"]); return 0


def command_knowledge_claim_transition(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root); artifact=load_yaml(knowledge_artifact_file(root,args.artifact))
        matches=[c for c in artifact["claims"] if c["id"]==args.claim]
        if not matches: raise RuntimeError(f"Unknown claim: {args.claim}")
        claim=matches[0]; old=claim["lifecycle"]
        if args.to not in CLAIM_TRANSITIONS[old]: raise RuntimeError(f"Invalid claim transition: {old} -> {args.to}")
        evidence=make_evidence(args, artifact["source_revision"])
        if evidence:
            claim["evidence"].extend(evidence); claim["evidence_depth"]=args.evidence_type
        claim["lifecycle"]=args.to
        if args.confidence: claim["confidence"]=args.confidence
        if args.to in {"confirmed","validated"}: claim["last_verified"]=utc_now(); claim["source_revision"]=copy.deepcopy(artifact["source_revision"])
        artifact["updated_at"]=utc_now()
        save_artifact_and_index(root,artifact,index)
    print(f"{args.claim}: {old} -> {args.to}"); return 0


def command_knowledge_unknown_add(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root); artifact=load_yaml(knowledge_artifact_file(root,args.artifact))
        unknown={"id":next_unknown_id(artifact),"question":args.question,"impact":args.impact or "","owner_role":args.owner_role,"status":"open"}
        artifact["unknowns"].append(unknown); artifact["updated_at"]=utc_now(); save_artifact_and_index(root,artifact,index)
    print(unknown["id"]); return 0


def command_knowledge_link(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root)
        ids={a["id"] for a in index["artifacts"]}
        if args.artifact not in ids or args.depends_on not in ids: raise RuntimeError("Both artifacts must exist")
        artifact=load_yaml(knowledge_artifact_file(root,args.artifact)); dep={"artifact_id":args.depends_on,"relation":args.relation}
        if dep not in artifact["dependencies"]: artifact["dependencies"].append(dep)
        artifact["updated_at"]=utc_now(); save_artifact_and_index(root,artifact,index)
    print(f"Linked {args.artifact} {args.relation} {args.depends_on}"); return 0


def command_knowledge_trigger_add(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root); artifact=load_yaml(knowledge_artifact_file(root,args.artifact))
        seq=len(artifact["review_triggers"])+1
        artifact["review_triggers"].append({"id":f"TRG-{seq:03d}","path_globs":args.path,"events":args.event,"description":args.description or "Review when declared path/event changes."})
        artifact["updated_at"]=utc_now(); save_artifact_and_index(root,artifact,index)
    print(f"Trigger added to {args.artifact}"); return 0


def command_knowledge_render(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root)
        ids=None if args.all else [args.artifact]
        if not args.all and args.artifact not in {a["id"] for a in index["artifacts"]}: raise RuntimeError(f"Unknown artifact: {args.artifact}")
        write_knowledge_views(root,index,ids)
    print("Knowledge views regenerated"); return 0


def command_knowledge_validate(root: Path, _args) -> int:
    errors,warnings=validate_knowledge(root,check_views=True)
    for warning in warnings: print(f"WARNING: {warning}")
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    print("KNOWLEDGE VALIDATION PASSED"); return 0


def trigger_matches(trigger: dict, changed: list[str], events: list[str]) -> bool:
    return any(any(fnmatch.fnmatch(path,glob) for glob in trigger.get("path_globs",[])) for path in changed) or bool(set(events)&set(trigger.get("events",[])))


def command_knowledge_stale_scan(root: Path, args) -> int:
    changed=list(args.changed); events=list(args.event)
    if args.git_base:
        result=subprocess.run(["git","-C",str(root),"diff","--name-only",f"{args.git_base}...HEAD"],text=True,capture_output=True)
        if result.returncode!=0: raise RuntimeError(result.stderr.strip() or "git diff failed")
        changed.extend(line.strip() for line in result.stdout.splitlines() if line.strip())
    changed=sorted(set(changed)); events=sorted(set(events))
    with runtime_lock(root):
        index=load_knowledge_index(root); artifacts={e["id"]:load_yaml(root/e["path"]) for e in index["artifacts"]}
        marked:set[str]=set()
        for aid,artifact in artifacts.items():
            direct=any(trigger_matches(t,changed,events) for t in artifact.get("review_triggers",[]))
            for claim in artifact.get("claims",[]):
                claim_match=any(trigger_matches(t,changed,events) for t in claim.get("review_triggers",[]))
                evidence_match=any(any(fnmatch.fnmatch(path,e["source"]) or path==e["source"] for path in changed) for e in claim.get("evidence",[]))
                if claim_match or evidence_match:
                    if claim["lifecycle"] not in {"deprecated","stale"}: claim["lifecycle"]="needs_review"
                    claim["confidence"]="low" if claim["confidence"]=="low" else "medium"
                    direct=True
            if direct: marked.add(aid)
        # Propagate to dependents.
        changed_flag=True
        while changed_flag:
            changed_flag=False
            for aid,artifact in artifacts.items():
                if aid in marked: continue
                if any(dep["artifact_id"] in marked for dep in artifact.get("dependencies",[])):
                    marked.add(aid); changed_flag=True
        ts=utc_now()
        if args.source_kind:
            index["current_source_revision"]=source_revision(args.source_kind,args.source_value,ts)
        for aid in marked:
            artifact=artifacts[aid]; artifact["freshness"]="needs_review"
            if artifact["status"]=="active": artifact["status"]="needs_review"
            artifact["updated_at"]=ts; save_artifact_and_index(root,artifact,index,render=False)
        index["status"]="needs_review" if marked else index["status"]
        index["updated_at"]=ts; atomic_write_yaml(paths(root)["knowledge_index"],index); write_knowledge_views(root,index,list(marked))
    print(json.dumps({"changed_paths":changed,"events":events,"marked_artifacts":sorted(marked)},ensure_ascii=False,indent=2)); return 0


def command_knowledge_refresh(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root); artifact=load_yaml(knowledge_artifact_file(root,args.artifact))
        unresolved=[c["id"] for c in artifact["claims"] if c["lifecycle"] in {"needs_review","stale"}]
        if unresolved and not args.allow_unresolved: raise RuntimeError(f"Claims still require review: {unresolved}")
        rev=source_revision(args.source_kind,args.source_value,utc_now()) if args.source_kind else copy.deepcopy(index.get("current_source_revision") or artifact["source_revision"])
        artifact["source_revision"]=rev; artifact["freshness"]="current"; artifact["status"]="active"; artifact["updated_at"]=utc_now(); save_artifact_and_index(root,artifact,index)
    print(f"Refreshed {args.artifact}"); return 0


def command_knowledge_task_assess(root: Path, args) -> int:
    with runtime_lock(root):
        tf=task_file(root,args.task)
        if not tf.exists(): raise RuntimeError(f"Unknown task: {args.task}")
        task=load_yaml(tf); index=load_knowledge_index(root,required=False)
        known={a["id"] for a in index.get("artifacts",[])} if index else set()
        missing=[a for a in args.artifact if a not in known]
        if missing: raise RuntimeError(f"Unknown knowledge artifacts: {missing}")
        if args.status in {"applied","deferred"} and not args.summary: raise RuntimeError("--summary is required for applied or deferred knowledge update")
        task["knowledge_update"]={"status":args.status,"affected_artifacts":args.artifact,"summary":args.summary,"updated_at":utc_now()}
        task["product_knowledge"]=sorted(set(task.get("product_knowledge",[])+args.artifact)); task["updated_at"]=utc_now(); atomic_write_yaml(tf,task)
    print(f"{args.task}: knowledge update = {args.status}"); return 0


def command_knowledge_packet_create(root: Path, args) -> int:
    with runtime_lock(root):
        index=load_knowledge_index(root); tf=task_file(root,args.task)
        if not tf.exists(): raise RuntimeError(f"Unknown task: {args.task}")
        task=load_yaml(tf); by_id={a["id"]:a for a in index["artifacts"]}
        missing=[a for a in args.artifact if a not in by_id]
        if missing: raise RuntimeError(f"Unknown knowledge artifacts: {missing}")
        if knowledge_artifact_file(root,args.id).exists(): raise RuntimeError(f"Artifact already exists: {args.id}")
        ts=utc_now(); rev=copy.deepcopy(index.get("current_source_revision") or index["source_revision"])
        evidence=[]
        for aid in args.artifact:
            art=load_yaml(root/by_id[aid]["path"])
            for claim in art.get("claims",[]):
                if claim["lifecycle"] in {"confirmed","validated"}: evidence.append(f"{aid}/{claim['id']}: {claim['statement']}")
        artifact={"schema_version":KNOWLEDGE_SCHEMA_VERSION,"id":args.id,"artifact_type":"context_packet","title":args.title,"mode":index["mode"],"perspective":"mixed","status":"active","freshness":"current","confidence":"medium","scope":{"summary":f"Task-specific context packet for {args.task}","in_scope":args.artifact,"out_of_scope":[]},"owner_role":args.owner_role,"data_classification":"internal","sharing":default_sharing("internal","prohibited"),"source_revision":rev,"review_triggers":[],"dependencies":[{"artifact_id":a,"relation":"references"} for a in args.artifact],"claims":[],"unknowns":[],"size_guidance":{"profile":"compact","quality_over_line_count":True,"split_strategy":"Remove unrelated evidence; never copy whole parent artifacts."},"content":{"task_id":args.task,"objective":task["objective"],"selected_artifacts":args.artifact,"current_evidence":evidence[:args.max_evidence],"impact_map":{"status":task["impact_map"]["status"],"path":task["impact_map"]["path"]},"risks":task.get("blockers",[]),"verification_plan":task["verification"]["plan"]},"created_at":ts,"updated_at":ts}
        save_artifact_and_index(root,artifact,index)
        task["product_knowledge"]=sorted(set(task.get("product_knowledge",[])+args.artifact+[args.id])); task["updated_at"]=ts; atomic_write_yaml(tf,task)
    print(args.id); return 0

def command_knowledge_sharing_set(root: Path, args) -> int:
    with runtime_lock(root):
        index = load_knowledge_index(root)
        path = knowledge_artifact_file(root, args.artifact)
        if not path.exists():
            raise RuntimeError(f"Unknown artifact: {args.artifact}")
        artifact = load_yaml(path)
        if args.classification:
            artifact["data_classification"] = args.classification
        sharing = artifact.setdefault("sharing", default_sharing())
        if args.external_sharing:
            sharing["external_sharing"] = args.external_sharing
        if args.sanitization_status:
            sharing["sanitization_status"] = args.sanitization_status
        if args.redaction:
            sharing["redactions"] = sorted(set(sharing.get("redactions", []) + args.redaction))
        if args.note:
            sharing["notes"] = sharing.get("notes", []) + args.note
        artifact["updated_at"] = utc_now()
        save_artifact_and_index(root, artifact, index)
    print(f"Updated sharing policy for {args.artifact}")
    return 0


def command_knowledge_sanitize_check(root: Path, args) -> int:
    index = load_knowledge_index(root, required=False)
    if index is None:
        print(json.dumps({"initialized": False, "artifacts": [], "findings": [], "policy_errors": []}, indent=2))
        return 0
    selected = set(args.artifact or [entry["id"] for entry in index.get("artifacts", [])])
    known = {entry["id"] for entry in index.get("artifacts", [])}
    missing = sorted(selected - known)
    if missing:
        raise RuntimeError(f"Unknown artifacts: {missing}")
    findings: list[dict] = []
    policy_errors: list[str] = []
    policy_warnings: list[str] = []
    for aid in sorted(selected):
        artifact = load_yaml(knowledge_artifact_file(root, aid))
        for finding in sensitive_findings(artifact):
            findings.append({"artifact": aid, **finding})
        errors, warnings = sharing_policy_errors(artifact, external_check=args.external)
        policy_errors.extend(errors); policy_warnings.extend(warnings)
    payload = {"initialized": True, "artifacts": sorted(selected), "external_check": bool(args.external), "findings": findings, "policy_errors": policy_errors, "policy_warnings": policy_warnings}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if findings or policy_errors else 0



# ---------------------------------------------------------------------------
# Alpha 6 deterministic runtime enforcement
# ---------------------------------------------------------------------------

SENSITIVE_REDACTIONS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(authorization:\s*bearer\s+)[^\s]+"),
    re.compile(r"(?i)(password|token|secret|api[_-]?key)\s*[=:]\s*[^\s]+"),
]


def enforcement_file(root: Path) -> Path:
    return paths(root)["enforcement"]


def default_enforcement_config() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "off",
        "hooks": {
            "bundled_with_core_plugin": True,
            "trust_state": "unknown",
            "project_trust_required": True,
        },
        "lease_policy": {
            "require_for_project_writes": True,
            "require_for_expensive_verification": True,
            "read_scope_mode": "audit",
            "unknown_write_target": "deny",
            "runtime_path_exemptions": [".cpt/**"],
        },
        "command_policy": {
            "deny_globally": ["destructive_git", "filesystem_root_delete"],
            "dependency_changes_require_lease": True,
            "network_requires_lease": True,
            "migrations_require_lease": True,
            "public_contract_changes_require_lease": True,
            "dependency_manifest_paths": [
                "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock*",
                "requirements*.txt", "pyproject.toml", "poetry.lock", "uv.lock", "Pipfile", "Pipfile.lock",
                "Cargo.toml", "Cargo.lock", "go.mod", "go.sum", "composer.json", "composer.lock"
            ],
            "migration_paths": ["migrations/**", "db/migrate/**", "alembic/**", "prisma/migrations/**", "drizzle/**"],
            "public_contract_paths": [],
        },
        "compaction": {
            "checkpoint_before_compaction": True,
            "block_when_checkpoint_fails": True,
            "verify_after_compaction": True,
            "block_on_mismatch": True,
            "block_with_active_workers": True,
            "retain_automatic_checkpoints": 5,
        },
        "knowledge": {
            "stale_scan_after_project_write": True,
            "exclude_paths": [".cpt/**", ".codex/**", ".git/**"],
        },
        "audit": {
            "log_path": ".cpt/audit/events.jsonl",
            "command_preview_chars": 240,
            "tool_output_soft_chars": 12000,
            "tool_output_hard_chars": 50000,
            "rotate_bytes": 5242880,
            "retain_files": 5,
            "redact_sensitive_values": True,
        },
        "subagents": {"record_lifecycle": True, "default_max_active": 3},
        "stop": {"validate_runtime": True, "continue_once_when_invalid": True},
        "approval": {"auto_allow_within_lease": False},
        "updated_at": utc_now(),
    }


def load_enforcement(root: Path) -> dict:
    path = enforcement_file(root)
    if not path.exists():
        return default_enforcement_config()
    return load_yaml(path)


def sanitize_preview(text: str, limit: int) -> str:
    value = text or ""
    for pattern in SENSITIVE_REDACTIONS:
        value = pattern.sub(lambda m: (m.group(1) if m.lastindex else "") + "[REDACTED]", value)
    value = value.replace("\x00", "")
    return value[:limit]


def sanitize_audit_value(value: Any, string_limit: int = 2000) -> Any:
    if isinstance(value, str):
        return sanitize_preview(value, string_limit)
    if isinstance(value, list):
        return [sanitize_audit_value(item, string_limit) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_audit_value(item, string_limit) for key, item in value.items()}
    return value


def audit_log_path(root: Path, config: dict) -> Path:
    configured = config.get("audit", {}).get("log_path", ".cpt/audit/events.jsonl")
    return root / configured


@contextmanager
def audit_lock(root: Path, timeout: float = 5.0):
    lock = root / ".cpt" / ".audit.lock"
    deadline = time.time() + timeout
    fd = None
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if time.time() >= deadline:
                raise RuntimeError(f"Audit lock timeout: {lock}")
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def rotate_audit(root: Path, config: dict) -> None:
    path = audit_log_path(root, config)
    if not path.exists():
        return
    audit = config.get("audit", {})
    threshold = int(audit.get("rotate_bytes", 5 * 1024 * 1024))
    if path.stat().st_size < threshold:
        return
    retain = int(audit.get("retain_files", 5))
    for index in range(retain - 1, 0, -1):
        src = path.with_name(f"{path.name}.{index}")
        dst = path.with_name(f"{path.name}.{index + 1}")
        if src.exists():
            if index + 1 > retain:
                src.unlink()
            else:
                os.replace(src, dst)
    os.replace(path, path.with_name(f"{path.name}.1"))


def append_audit(root: Path, config: dict, *, event: str, decision: str, summary: str,
                 payload: dict | None = None, tool_name: str | None = None,
                 command: str | None = None, paths_seen: list[str] | None = None,
                 violations: list[str] | None = None, metadata: dict | None = None) -> dict:
    audit = config.get("audit", {})
    preview_limit = int(audit.get("command_preview_chars", 240))
    command_hash = hashlib.sha256(command.encode("utf-8")).hexdigest() if command else None
    record = {
        "schema_version": SCHEMA_VERSION,
        "id": f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}",
        "timestamp": utc_now(),
        "event": event,
        "mode": config.get("mode", "off"),
        "decision": decision,
        "summary": summary,
        "session_id": (payload or {}).get("session_id"),
        "turn_id": (payload or {}).get("turn_id"),
        "tool_name": tool_name,
        "command_sha256": command_hash,
        "command_preview": sanitize_preview(command or "", preview_limit) if command else None,
        "paths": sanitize_audit_value(sorted(set(paths_seen or []))),
        "violations": sanitize_audit_value(list(violations or [])),
        "metadata": sanitize_audit_value(metadata or {}),
    }
    errors = validate_schema(record, "audit-event.schema.json", "audit event")
    if errors:
        raise RuntimeError("; ".join(errors))
    path = audit_log_path(root, config)
    path.parent.mkdir(parents=True, exist_ok=True)
    with audit_lock(root):
        rotate_audit(root, config)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record


def normalize_command(command: str) -> str:
    return re.sub(r"\s+", " ", command.strip())


def normalize_rel_path(root: Path, value: str) -> str:
    value = value.strip().strip('"').strip("'")
    if not value or value in {"/dev/null", "NUL"}:
        return value
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return path.resolve().as_posix()
    return Path(os.path.normpath(value)).as_posix().lstrip("./") or "."


def matches_scope(path: str, scopes: list[str]) -> bool:
    if not path:
        return False
    for scope in scopes:
        normalized = scope.strip().lstrip("./")
        if normalized in {".", "**", "*"}:
            return True
        if fnmatch.fnmatch(path, normalized) or fnmatch.fnmatch(path + "/", normalized):
            return True
        if normalized.endswith("/**") and (path == normalized[:-3].rstrip("/") or path.startswith(normalized[:-3])):
            return True
    return False


def extract_patch_paths(command: str, root: Path) -> list[str]:
    found: list[str] = []
    for line in command.splitlines():
        match = re.match(r"^\*\*\* (?:Update|Add|Delete) File:\s+(.+)$", line)
        if match:
            found.append(normalize_rel_path(root, match.group(1)))
            continue
        match = re.match(r"^(?:\+\+\+|---) [ab]/(.+)$", line)
        if match:
            found.append(normalize_rel_path(root, match.group(1)))
    return sorted(set(p for p in found if p))


def extract_bash_paths(command: str, root: Path) -> list[str]:
    paths_found: list[str] = []
    for match in re.finditer(r"(?:>|>>)\s*([^|;&\s]+)", command):
        paths_found.append(normalize_rel_path(root, match.group(1)))
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        tokens = []
    if tokens:
        base = Path(tokens[0]).name
        if base in {"cp", "mv", "install"} and len(tokens) >= 3:
            paths_found.extend(normalize_rel_path(root, item) for item in tokens[-2:])
        elif base in {"rm", "touch", "mkdir", "rmdir"}:
            paths_found.extend(normalize_rel_path(root, item) for item in tokens[1:] if not item.startswith("-"))
        elif base == "sed" and any(item.startswith("-i") for item in tokens[1:]):
            paths_found.extend(normalize_rel_path(root, item) for item in tokens[1:] if not item.startswith("-") and not item.startswith("s"))
        elif base == "git" and len(tokens) >= 3 and tokens[1] in {"restore", "checkout", "rm", "mv"}:
            paths_found.extend(normalize_rel_path(root, item) for item in tokens[2:] if not item.startswith("-"))
        elif base == "rg" and "--files" in tokens:
            candidates = [item for item in tokens[tokens.index("--files") + 1:] if not item.startswith("-")]
            paths_found.extend(normalize_rel_path(root, item) for item in candidates or ["."])
        elif base in {"find", "tree", "ls"}:
            candidates = [item for item in tokens[1:] if not item.startswith("-")]
            paths_found.extend(normalize_rel_path(root, item) for item in candidates or ["."])
        elif base in {"cat", "head", "tail"}:
            candidates = [item for item in tokens[1:] if not item.startswith("-") and not item.isdigit()]
            paths_found.extend(normalize_rel_path(root, item) for item in candidates)
        elif base == "sed" and "-n" in tokens:
            candidates = [item for item in tokens[1:] if not item.startswith("-")]
            if len(candidates) > 1:
                candidates = candidates[1:]
            paths_found.extend(normalize_rel_path(root, item) for item in candidates)
        elif base in {"grep", "rg"} and len(tokens) >= 3:
            candidates = [item for item in tokens[2:] if not item.startswith("-")]
            paths_found.extend(normalize_rel_path(root, item) for item in candidates)
    return sorted(set(p for p in paths_found if p and p != "-"))


def operation_tags_for_paths(paths_seen: list[str], config: dict) -> list[str]:
    policy = config.get("command_policy", {})
    tagged: list[str] = []
    mappings = {
        "dependency_change": policy.get("dependency_manifest_paths", []),
        "migration": policy.get("migration_paths", []),
        "public_api_change": policy.get("public_contract_paths", []),
    }
    for tag, patterns in mappings.items():
        if patterns and any(matches_scope(path, patterns) for path in paths_seen):
            tagged.append(tag)
    return tagged


def classify_command(command: str, tool_name: str, root: Path) -> dict:
    normalized = normalize_command(command)
    lower = normalized.lower()
    tags: list[str] = []
    write = tool_name == "apply_patch"
    read = False
    broad_read = False
    verification = bool(re.search(r"(?:^|\s)(?:pytest|unittest|jest|vitest|playwright|eslint|ruff|mypy|tsc|cargo test|go test|npm (?:run )?(?:test|lint|build)|pnpm (?:test|lint|build)|yarn (?:test|lint|build))(?:\s|$)", lower))
    if re.search(r"\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[^\s]*(?:f[^\s]*d|d[^\s]*f)|\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|\s-f(?:\s|$))", lower):
        tags.append("destructive_git")
        write = True
    if re.search(r"\brm\s+-[^\s]*r[^\s]*f[^\s]*\s+/(?:\s|$)", lower):
        tags.append("filesystem_root_delete")
        write = True
    if re.search(r"(?:^|[;&|]\s*)(?:npm|pnpm|yarn|pip3?|uv|poetry)\s+(?:install|i|add|remove|uninstall)\b", lower):
        tags.append("dependency_change")
        write = True
    if re.search(r"(?:^|[;&|]\s*)(?:curl|wget|ssh|scp|rsync\s+[^ ]+@|gh\s+api)\b", lower):
        tags.append("network_access")
    if re.search(r"\b(?:alembic|prisma\s+migrate|manage\.py\s+migrate|rails\s+db:migrate|typeorm\s+migration|flyway|liquibase)\b", lower):
        tags.append("migration")
        write = True
    if tool_name == "Bash":
        if re.search(r"(?:>|>>)|\b(?:tee|sed\s+-i|perl\s+-pi|cp|mv|rm|touch|mkdir|rmdir|git\s+(?:checkout|restore|add|commit|merge|rebase|cherry-pick))\b", lower):
            write = True
        if re.match(r"^(?:cat|head|tail|sed\s+-n|rg|grep|find|ls|tree|git\s+(?:status|diff|show|log)|python\s+-m\s+json\.tool)\b", lower):
            read = True
        if re.match(r"^(?:find|tree)\s+(?:\.|/)|^rg\s+--files(?:\s+\.|\s*$)|^git\s+grep\b", lower):
            broad_read = True
    paths_seen = extract_patch_paths(command, root) if tool_name == "apply_patch" else extract_bash_paths(command, root)
    return {"write": write, "read": read, "broad_read": broad_read, "verification": verification, "tags": sorted(set(tags)), "paths": paths_seen, "normalized": normalized}


def active_lease(root: Path) -> dict | None:
    current = load_yaml(paths(root)["current"])
    lease_id = current.get("current_lease")
    if not lease_id:
        return None
    path = lease_file(root, lease_id)
    if not path.exists():
        return None
    lease = load_yaml(path)
    if lease.get("status") != "active":
        return None
    expires_at = lease.get("expires", {}).get("at")
    if expires_at:
        try:
            if datetime.fromisoformat(expires_at.replace("Z", "+00:00")) <= datetime.now(timezone.utc):
                return None
        except ValueError:
            return None
    return lease


def is_runtime_exempt(path: str, config: dict) -> bool:
    return matches_scope(path, config.get("lease_policy", {}).get("runtime_path_exemptions", [".cpt/**"]))


def command_policy(root: Path, config: dict, tool_name: str, command: str) -> dict:
    info = classify_command(command, tool_name, root)
    info["tags"] = sorted(set(info.get("tags", []) + operation_tags_for_paths(info.get("paths", []), config)))
    lease = active_lease(root)
    violations: list[str] = []
    warnings: list[str] = []
    denied_tags = set(config.get("command_policy", {}).get("deny_globally", []))
    for tag in info["tags"]:
        if tag in denied_tags:
            violations.append(f"globally forbidden operation: {tag}")
    if lease:
        forbidden = set(lease.get("forbidden_operations", []))
        for tag in info["tags"]:
            if tag in forbidden:
                violations.append(f"lease forbids operation: {tag}")
    elif any(tag in {"dependency_change", "network_access", "migration", "public_api_change"} for tag in info["tags"]):
        violations.append("operation requires an active scoped lease")
    if info["write"]:
        non_runtime = [path for path in info["paths"] if not is_runtime_exempt(path, config)]
        if non_runtime:
            if not lease and config.get("lease_policy", {}).get("require_for_project_writes", True):
                violations.append("project write requires an active scoped lease")
            elif lease:
                outside = [path for path in non_runtime if not matches_scope(path, lease.get("write_scope", []))]
                if outside:
                    violations.append("write target outside lease scope: " + ", ".join(outside))
        elif not info["paths"] and tool_name == "apply_patch":
            violations.append("apply_patch target could not be determined")
        elif not info["paths"] and config.get("lease_policy", {}).get("unknown_write_target") == "deny":
            runtime_command = info["normalized"].startswith("python .cpt/bin/cpt_runtime.py") or info["normalized"].startswith("python3 .cpt/bin/cpt_runtime.py")
            broad_lease = bool(lease and any(scope.strip() in {".", "*", "**", "./**"} for scope in lease.get("write_scope", [])))
            if not runtime_command and not broad_lease:
                violations.append("write command target could not be determined; use an explicit broad write scope only when the operation is intentionally project-wide")
    if info["verification"] and config.get("lease_policy", {}).get("require_for_expensive_verification", True):
        approved = [] if not lease else [normalize_command(item["command"]) for item in lease.get("verification_scope", [])]
        if info["normalized"] not in approved:
            violations.append("verification command is not listed in the active lease")
    if info["broad_read"]:
        read_mode = config.get("lease_policy", {}).get("read_scope_mode", "audit")
        in_scope = bool(lease and any(matches_scope(path, lease.get("read_scope", [])) for path in info["paths"]))
        message = "broad read should be bounded by an approved read scope"
        if read_mode == "enforce" and not in_scope:
            violations.append(message)
        elif read_mode == "audit" and not in_scope:
            warnings.append(message)
    decision = "deny" if violations else ("warn" if warnings else "allow")
    return {"decision": decision, "violations": violations, "warnings": warnings, "classification": info, "lease_id": None if lease is None else lease["id"]}


def tool_command(payload: dict) -> tuple[str | None, str]:
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, dict):
        command = tool_input.get("command")
        if isinstance(command, str):
            return tool_name, command
    return tool_name, json.dumps(tool_input, ensure_ascii=False, sort_keys=True)


def hook_json(**kwargs) -> int:
    if "continue_" in kwargs:
        kwargs["continue"] = kwargs.pop("continue_")
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    print(json.dumps(kwargs, ensure_ascii=False))
    return 0


def mode_blocks(config: dict) -> bool:
    return config.get("mode") == "enforce"


def git_changed_paths(root: Path) -> list[str]:
    try:
        result = subprocess.run(["git", "-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"], text=False, capture_output=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    items = result.stdout.split(b"\x00")
    found: list[str] = []
    for item in items:
        if not item:
            continue
        text = item.decode("utf-8", errors="replace")
        if len(text) < 4:
            continue
        path = text[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        found.append(Path(path).as_posix())
    return sorted(set(found))


def knowledge_changed_paths(root: Path, config: dict, changed: list[str]) -> list[str]:
    excluded = config.get("knowledge", {}).get("exclude_paths", [])
    return [path for path in changed if not matches_scope(path, excluded)]


def tool_response_size(value: Any) -> int:
    try:
        return len(json.dumps(value, ensure_ascii=False))
    except Exception:
        return len(str(value))


def worker_path(root: Path, agent_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", agent_id)
    return paths(root)["workers"] / f"{safe}.yaml"


def worker_records(root: Path) -> list[dict]:
    result = []
    for path in sorted(paths(root)["workers"].glob("*.yaml")):
        try:
            result.append(load_yaml(path))
        except Exception:
            continue
    return result


def active_worker_limit(root: Path, config: dict) -> int:
    lease = active_lease(root)
    if lease and lease.get("delegation", {}).get("allowed"):
        return int(lease["delegation"].get("max_workers", 0))
    return int(config.get("subagents", {}).get("default_max_active", 3))


def record_worker_start(root: Path, config: dict, payload: dict) -> tuple[dict, list[str]]:
    current = load_yaml(paths(root)["current"])
    record = {
        "schema_version": SCHEMA_VERSION,
        "agent_id": payload.get("agent_id") or "unknown",
        "agent_type": payload.get("agent_type") or "unknown",
        "status": "running",
        "session_id": payload.get("session_id"),
        "turn_id": payload.get("turn_id"),
        "task_id": current.get("current_task"),
        "lease_id": current.get("current_lease"),
        "permission_mode": payload.get("permission_mode"),
        "started_at": utc_now(),
        "stopped_at": None,
        "transcript_path": None,
        "last_message_sha256": None,
        "updated_at": utc_now(),
    }
    errors = validate_schema(record, "worker-record.schema.json", "worker record")
    if errors:
        raise RuntimeError("; ".join(errors))
    path = worker_path(root, record["agent_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_yaml(path, record)
    running = [item for item in worker_records(root) if item.get("status") == "running"]
    warnings = []
    limit = active_worker_limit(root, config)
    if len(running) > limit:
        warnings.append(f"active workers {len(running)} exceed approved limit {limit}")
    lease = active_lease(root)
    if lease and not lease.get("delegation", {}).get("allowed"):
        warnings.append("active lease does not allow delegation")
    return record, warnings


def record_worker_stop(root: Path, payload: dict) -> dict:
    agent_id = payload.get("agent_id") or "unknown"
    path = worker_path(root, agent_id)
    record = load_yaml(path) if path.exists() else {
        "schema_version": SCHEMA_VERSION,
        "agent_id": agent_id,
        "agent_type": payload.get("agent_type") or "unknown",
        "status": "unknown",
        "session_id": payload.get("session_id"),
        "turn_id": payload.get("turn_id"),
        "task_id": None,
        "lease_id": None,
        "permission_mode": payload.get("permission_mode"),
        "started_at": None,
        "stopped_at": None,
        "transcript_path": None,
        "last_message_sha256": None,
        "updated_at": utc_now(),
    }
    message = payload.get("last_assistant_message")
    record["status"] = "completed" if message else "interrupted"
    record["stopped_at"] = utc_now()
    record["transcript_path"] = payload.get("agent_transcript_path")
    record["last_message_sha256"] = hashlib.sha256(message.encode("utf-8")).hexdigest() if message else None
    record["updated_at"] = utc_now()
    errors = validate_schema(record, "worker-record.schema.json", "worker record")
    if errors:
        raise RuntimeError("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_yaml(path, record)
    return record


def prune_automatic_checkpoints(root: Path, retain: int) -> None:
    candidates = []
    for path in paths(root)["checkpoints"].glob("CP-*.yaml"):
        try:
            data = load_yaml(path)
        except Exception:
            continue
        if data.get("source") == "pre_compact":
            candidates.append((data.get("created_at", ""), path))
    candidates.sort(reverse=True)
    for _, path in candidates[retain:]:
        path.unlink(missing_ok=True)


def handle_session_start(root: Path, config: dict, payload: dict) -> int:
    errors, warnings = validate_runtime(root)
    current = load_yaml(paths(root)["current"])
    summary = f"CPT mode={config.get('mode')}; runtime={current.get('runtime_status')}; task={current.get('current_task') or 'none'}; lease={current.get('current_lease') or 'none'}."
    if errors:
        append_audit(root, config, event="SessionStart", decision="stop" if mode_blocks(config) else "warn", summary="Runtime validation failed at session start", payload=payload, violations=errors, metadata={"warnings": warnings})
        message = "CPT runtime is invalid: " + "; ".join(errors[:5])
        if mode_blocks(config):
            return hook_json(continue_=False, stopReason=message, systemMessage=message)
        return hook_json(systemMessage=message, hookSpecificOutput={"hookEventName":"SessionStart","additionalContext":summary + " Validate runtime before making project changes."})
    append_audit(root, config, event="SessionStart", decision="record", summary=summary, payload=payload, metadata={"warnings": warnings})
    return hook_json(hookSpecificOutput={"hookEventName":"SessionStart","additionalContext":summary + " Load .cpt/runtime-summary.md and referenced active records only."})


def handle_pre_tool(root: Path, config: dict, payload: dict, permission_request: bool = False) -> int:
    tool_name, command = tool_command(payload)
    policy = command_policy(root, config, tool_name or "unknown", command)
    violations = policy["violations"]
    warnings = policy["warnings"]
    decision = "deny" if violations and mode_blocks(config) else ("warn" if violations or warnings else "allow")
    append_audit(root, config, event="PermissionRequest" if permission_request else "PreToolUse", decision=decision, summary="; ".join(violations or warnings) or "Tool request within CPT policy", payload=payload, tool_name=tool_name, command=command, paths_seen=policy["classification"]["paths"], violations=violations, metadata={"warnings":warnings,"lease_id":policy["lease_id"],"classification":policy["classification"]})
    if violations and mode_blocks(config):
        reason = "CPT enforcement blocked the request: " + "; ".join(violations)
        if permission_request:
            return hook_json(hookSpecificOutput={"hookEventName":"PermissionRequest","decision":{"behavior":"deny","message":reason}})
        return hook_json(hookSpecificOutput={"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":reason})
    if permission_request and not violations and config.get("approval", {}).get("auto_allow_within_lease") and policy.get("lease_id"):
        return hook_json(hookSpecificOutput={"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}})
    context = "; ".join(violations or warnings)
    if context:
        if permission_request:
            return hook_json(systemMessage="CPT audit warning: " + context)
        return hook_json(hookSpecificOutput={"hookEventName":"PreToolUse","additionalContext":"CPT audit warning: " + context})
    return 0


def handle_post_tool(root: Path, config: dict, payload: dict) -> int:
    tool_name, command = tool_command(payload)
    policy = command_policy(root, config, tool_name or "unknown", command)
    response_size = tool_response_size(payload.get("tool_response"))
    warnings = list(policy.get("warnings", []))
    soft = int(config.get("audit", {}).get("tool_output_soft_chars", 12000))
    hard = int(config.get("audit", {}).get("tool_output_hard_chars", 50000))
    if response_size > soft:
        warnings.append(f"tool output was {response_size} chars; prefer a narrower command or summarized evidence")
    changed: list[str] = []
    if policy.get("classification", {}).get("write"):
        detected = list(policy.get("classification", {}).get("paths", []))
        changed = detected or git_changed_paths(root)
    relevant = knowledge_changed_paths(root, config, changed)
    marked: list[str] = []
    if relevant and config.get("knowledge", {}).get("stale_scan_after_project_write") and paths(root)["knowledge_index"].exists():
        args = argparse.Namespace(changed=relevant, event=[], git_base=None, source_kind=None, source_value=None)
        capture = []
        original_stdout = sys.stdout
        try:
            from io import StringIO
            buffer = StringIO(); sys.stdout = buffer
            command_knowledge_stale_scan(root, args)
            capture_text = buffer.getvalue()
            capture.append(capture_text)
            try:
                marked = json.loads(capture_text).get("marked_artifacts", [])
            except Exception:
                pass
        finally:
            sys.stdout = original_stdout
    errors, runtime_warnings = validate_runtime(root)
    decision = "stop" if errors and mode_blocks(config) else ("warn" if errors or warnings or runtime_warnings else "record")
    append_audit(root, config, event="PostToolUse", decision=decision, summary="Post-tool audit", payload=payload, tool_name=tool_name, command=command, paths_seen=changed, violations=errors, metadata={"tool_output_chars":response_size,"warnings":warnings+runtime_warnings,"knowledge_marked":marked})
    messages = warnings + runtime_warnings
    if response_size > hard:
        messages.append(f"tool output exceeded hard guidance ({hard} chars)")
    if errors and mode_blocks(config):
        reason = "CPT runtime invalid after tool use: " + "; ".join(errors[:5])
        return hook_json(continue_=False, stopReason=reason, systemMessage=reason)
    if messages:
        return hook_json(systemMessage="CPT post-tool warning: " + "; ".join(messages[:5]), hookSpecificOutput={"hookEventName":"PostToolUse","additionalContext":"Review the CPT warnings before the next operation."})
    return 0


def handle_pre_compact(root: Path, config: dict, payload: dict) -> int:
    if not config.get("compaction", {}).get("checkpoint_before_compaction", True):
        return 0
    active_workers = [item for item in worker_records(root) if item.get("status") == "running"]
    worker_warning = None
    if active_workers:
        worker_warning = f"{len(active_workers)} subagent worker(s) are still active"
        if mode_blocks(config) and config.get("compaction", {}).get("block_with_active_workers", True):
            append_audit(root, config, event="PreCompact", decision="stop", summary=worker_warning, payload=payload, violations=[worker_warning])
            return hook_json(continue_=False, stopReason=worker_warning, systemMessage=worker_warning)
    try:
        with runtime_lock(root):
            errors, _ = validate_runtime(root)
            if errors:
                raise RuntimeError("; ".join(errors))
            cp = make_checkpoint(root, "pre_compact", f"Automatic checkpoint before {payload.get('trigger','unknown')} compaction")
            current = load_yaml(paths(root)["current"]); index = load_yaml(paths(root)["task_index"])
            current["latest_checkpoint"] = cp["id"]; bump(current)
            atomic_write_yaml(checkpoint_file(root, cp["id"]), cp); atomic_write_yaml(paths(root)["current"], current); write_summary(root,current,index)
            prune_automatic_checkpoints(root, int(config.get("compaction", {}).get("retain_automatic_checkpoints", 5)))
        append_audit(root, config, event="PreCompact", decision="warn" if worker_warning else "record", summary=f"Created checkpoint {cp['id']}", payload=payload, violations=[worker_warning] if worker_warning else [], metadata={"checkpoint_id":cp["id"]})
        message = f"CPT checkpoint {cp['id']} created before compaction."
        if worker_warning:
            message += " Warning: " + worker_warning
        return hook_json(systemMessage=message)
    except Exception as exc:
        message = f"CPT could not checkpoint before compaction: {exc}"
        append_audit(root, config, event="PreCompact", decision="stop" if mode_blocks(config) else "warn", summary=message, payload=payload, violations=[str(exc)])
        if mode_blocks(config) and config.get("compaction", {}).get("block_when_checkpoint_fails", True):
            return hook_json(continue_=False, stopReason=message, systemMessage=message)
        return hook_json(systemMessage=message)


def handle_post_compact(root: Path, config: dict, payload: dict) -> int:
    if not config.get("compaction", {}).get("verify_after_compaction", True):
        return 0
    try:
        cp_path = resolve_checkpoint(root, "latest")
        cp = load_yaml(cp_path)
        diffs = verify_checkpoint_integrity(cp) + snapshot_diff(root, cp)
        errors, warnings = validate_runtime(root)
        diffs += errors
        if diffs:
            raise RuntimeError("; ".join(diffs))
        append_audit(root, config, event="PostCompact", decision="record", summary=f"Verified checkpoint {cp['id']} after compaction", payload=payload, metadata={"checkpoint_id":cp["id"],"warnings":warnings})
        return hook_json(systemMessage=f"CPT checkpoint {cp['id']} verified. Reload .cpt/runtime-summary.md and the referenced active records before continuing.")
    except Exception as exc:
        message = f"CPT state mismatch after compaction: {exc}"
        append_audit(root, config, event="PostCompact", decision="stop" if mode_blocks(config) else "warn", summary=message, payload=payload, violations=[str(exc)])
        if mode_blocks(config) and config.get("compaction", {}).get("block_on_mismatch", True):
            return hook_json(continue_=False, stopReason=message, systemMessage=message)
        return hook_json(systemMessage=message)


def handle_subagent_start(root: Path, config: dict, payload: dict) -> int:
    if not config.get("subagents", {}).get("record_lifecycle", True):
        return 0
    record, warnings = record_worker_start(root, config, payload)
    append_audit(root, config, event="SubagentStart", decision="warn" if warnings else "record", summary=f"Worker {record['agent_id']} started", payload=payload, violations=warnings, metadata={"agent_type":record["agent_type"],"task_id":record["task_id"],"lease_id":record["lease_id"]})
    context = f"CPT worker record: task={record['task_id'] or 'none'}, lease={record['lease_id'] or 'none'}. Stay inside the delegated bounded contract and return a compact evidence-backed artifact."
    if warnings:
        context += " Warnings: " + "; ".join(warnings)
    return hook_json(hookSpecificOutput={"hookEventName":"SubagentStart","additionalContext":context}, systemMessage="; ".join(warnings) if warnings else None)


def handle_subagent_stop(root: Path, config: dict, payload: dict) -> int:
    if not config.get("subagents", {}).get("record_lifecycle", True):
        return 0
    record = record_worker_stop(root, payload)
    append_audit(root, config, event="SubagentStop", decision="record", summary=f"Worker {record['agent_id']} stopped with status {record['status']}", payload=payload, metadata={"agent_type":record["agent_type"],"status":record["status"]})
    return hook_json(systemMessage=f"CPT recorded worker {record['agent_id']} as {record['status']}.")


def handle_stop(root: Path, config: dict, payload: dict) -> int:
    if not config.get("stop", {}).get("validate_runtime", True):
        return 0
    errors, warnings = validate_runtime(root)
    if not errors:
        append_audit(root, config, event="Stop", decision="record", summary="Runtime valid at stop", payload=payload, metadata={"warnings":warnings})
        return 0
    message = "CPT runtime invalid at stop: " + "; ".join(errors[:5])
    append_audit(root, config, event="Stop", decision="stop" if mode_blocks(config) else "warn", summary=message, payload=payload, violations=errors, metadata={"warnings":warnings})
    if mode_blocks(config) and config.get("stop", {}).get("continue_once_when_invalid", True) and not payload.get("stop_hook_active"):
        return hook_json(decision="block", reason=message + " Repair or explicitly defer the runtime inconsistency before finishing.")
    return hook_json(continue_=False, stopReason=message, systemMessage=message) if mode_blocks(config) else hook_json(systemMessage=message)


def command_hook_handle(root: Path, _args) -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"Invalid hook input: {exc}", file=sys.stderr)
        return 1
    config = load_enforcement(root)
    if config.get("mode", "off") == "off":
        return 0
    event = payload.get("hook_event_name")
    try:
        if event == "SessionStart": return handle_session_start(root, config, payload)
        if event == "PreToolUse": return handle_pre_tool(root, config, payload, False)
        if event == "PermissionRequest": return handle_pre_tool(root, config, payload, True)
        if event == "PostToolUse": return handle_post_tool(root, config, payload)
        if event == "PreCompact": return handle_pre_compact(root, config, payload)
        if event == "PostCompact": return handle_post_compact(root, config, payload)
        if event == "SubagentStart": return handle_subagent_start(root, config, payload)
        if event == "SubagentStop": return handle_subagent_stop(root, config, payload)
        if event == "Stop": return handle_stop(root, config, payload)
        append_audit(root, config, event=event or "unknown", decision="record", summary="Unhandled hook event", payload=payload)
        return 0
    except Exception as exc:
        try:
            append_audit(root, config, event=event or "unknown", decision="error", summary=str(exc), payload=payload, violations=[str(exc)])
        except Exception:
            pass
        if mode_blocks(config):
            if event in {"PreToolUse"}:
                return hook_json(hookSpecificOutput={"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":f"CPT enforcement error: {exc}"})
            if event == "PermissionRequest":
                return hook_json(hookSpecificOutput={"hookEventName":"PermissionRequest","decision":{"behavior":"deny","message":f"CPT enforcement error: {exc}"}})
            return hook_json(continue_=False, stopReason=f"CPT enforcement error: {exc}", systemMessage=f"CPT enforcement error: {exc}")
        return hook_json(systemMessage=f"CPT enforcement audit error: {exc}")


def command_enforcement_status(root: Path, _args) -> int:
    config = load_enforcement(root)
    log = audit_log_path(root, config)
    workers = worker_records(root)
    data = {
        "mode": config.get("mode", "off"),
        "hook_trust": config.get("hooks", {}).get("trust_state", "unknown"),
        "plugin_hooks_bundled": config.get("hooks", {}).get("bundled_with_core_plugin", False),
        "audit_log": str(log.relative_to(root)),
        "audit_bytes": log.stat().st_size if log.exists() else 0,
        "active_workers": sum(1 for item in workers if item.get("status") == "running"),
        "worker_records": len(workers),
        "latest_checkpoint": load_yaml(paths(root)["current"]).get("latest_checkpoint"),
        "native_boundary_note": "CPT enforcement is a guardrail. Native Codex sandbox, permissions, approvals, and rules remain authoritative.",
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def command_enforcement_set(root: Path, args) -> int:
    with runtime_lock(root):
        config = load_enforcement(root)
        effective_trust = args.trust_state or config.get("hooks", {}).get("trust_state", "unknown")
        if args.mode == "enforce" and effective_trust != "trusted":
            raise RuntimeError("enforce mode requires an explicit trusted hook review record; use --trust-state trusted after reviewing the bundled hooks")
        config["mode"] = args.mode
        if args.trust_state:
            config.setdefault("hooks", {})["trust_state"] = args.trust_state
        config["updated_at"] = utc_now()
        errors = validate_schema(config, "enforcement.schema.json", ".cpt/enforcement.yaml")
        if errors:
            raise RuntimeError("; ".join(errors))
        atomic_write_yaml(enforcement_file(root), config)
    print(f"Enforcement mode set to {args.mode}")
    return 0


def command_policy_check(root: Path, args) -> int:
    config = load_enforcement(root)
    result = command_policy(root, config, args.tool_name, args.command_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["decision"] == "deny" else 0


def audit_log_files(root: Path, config: dict) -> list[Path]:
    path = audit_log_path(root, config)
    retain = int(config.get("audit", {}).get("retain_files", 5))
    rotated = [path.with_name(f"{path.name}.{index}") for index in range(retain, 0, -1)]
    return [item for item in rotated + [path] if item.exists()]


def command_audit_tail(root: Path, args) -> int:
    config = load_enforcement(root)
    lines: list[str] = []
    for path in audit_log_files(root, config):
        lines.extend(path.read_text(encoding="utf-8").splitlines())
    records = [json.loads(line) for line in lines[-args.limit:] if line.strip()]
    print(json.dumps(records, ensure_ascii=False, indent=2))
    return 0


def command_audit_validate(root: Path, _args) -> int:
    config = load_enforcement(root)
    errors: list[str] = []
    count = 0
    files = audit_log_files(root, config)
    for path in files:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            count += 1
            label = str(path.relative_to(root))
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{label} line {number}: invalid JSON: {exc}")
                continue
            errors += validate_schema(record, "audit-event.schema.json", f"{label} line {number}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"AUDIT LOG VALIDATION PASSED: {count} events across {len(files)} file(s)")
    return 0


def command_worker_status(root: Path, _args) -> int:
    print(json.dumps(worker_records(root), ensure_ascii=False, indent=2))
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CPT OS 4.0 Alpha 6 runtime, Product Knowledge, and deterministic enforcement CLI")
    parser.add_argument("--root", type=Path, help="Runtime root; defaults to nearest parent containing .cpt/runtime.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status")
    sub.add_parser("validate")
    sub.add_parser("render-summary")

    sub.add_parser("hook-handle")
    sub.add_parser("enforcement-status")

    p = sub.add_parser("enforcement-set")
    p.add_argument("--mode", choices=["off","audit","enforce"], required=True)
    p.add_argument("--trust-state", choices=["unknown","trusted","untrusted","disabled"])

    p = sub.add_parser("policy-check")
    p.add_argument("--tool-name", choices=["Bash","apply_patch"], required=True)
    p.add_argument("--command", dest="command_text", required=True)

    p = sub.add_parser("audit-tail")
    p.add_argument("--limit", type=int, default=20)
    sub.add_parser("audit-validate")
    sub.add_parser("worker-status")

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
    p.add_argument("--forbid", action="append", default=[])
    p.add_argument("--allow-operation", action="append", default=[], choices=["dependency_change","migration","public_api_change","network_access"], help="Explicitly remove a normally forbidden operation class from this lease; global destructive operations remain blocked")
    p.add_argument("--expires-at")
    p.add_argument("--rationale")

    p = sub.add_parser("checkpoint")
    p.add_argument("--source", choices=["manual","pre_compact","phase_handoff","synthetic"], default="manual")
    p.add_argument("--reason", required=True)

    p = sub.add_parser("recover")
    p.add_argument("--checkpoint", default="latest")
    p.add_argument("--verify-only", action="store_true")

    p = sub.add_parser("knowledge-init")
    p.add_argument("--id", default="product-knowledge")
    p.add_argument("--title", required=True)
    p.add_argument("--mode", choices=["existing","greenfield","redesign"], required=True)
    p.add_argument("--owner-role", required=True)
    p.add_argument("--source-kind", choices=["git_commit","git_tree","user_approval","design_version","external_version","timestamp","none"], default="none")
    p.add_argument("--source-value")
    p.add_argument("--size-profile", choices=["compact","standard","extended"], default="compact")
    p.add_argument("--force", action="store_true")

    sub.add_parser("knowledge-status")

    p = sub.add_parser("knowledge-create")
    p.add_argument("--id", required=True)
    p.add_argument("--type", choices=["product_map","area_map","flow_map","decision_record","api_data_contract","context_packet"], required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--owner-role", required=True)
    p.add_argument("--perspective", choices=["current","target","delta","planned","mixed"])
    p.add_argument("--confidence", choices=["low","medium","high"], default="low")
    p.add_argument("--scope-summary")
    p.add_argument("--in-scope", action="append", default=[])
    p.add_argument("--out-of-scope", action="append", default=[])
    p.add_argument("--depends-on", action="append", default=[])
    p.add_argument("--review-path", action="append", default=[])
    p.add_argument("--size-profile", choices=["compact","standard","extended"], default="compact")
    p.add_argument("--task-id")
    p.add_argument("--classification", choices=list(KNOWLEDGE_CLASSIFICATIONS), default="internal")
    p.add_argument("--external-sharing", choices=list(KNOWLEDGE_EXTERNAL_SHARING), default="prohibited")

    def add_evidence_args(p):
        p.add_argument("--evidence-type", choices=["user_approved_decision","design_artifact","source_file","route","component","hook_store","api_type","test","runtime_observation","external_source","other"])
        p.add_argument("--evidence-source")
        p.add_argument("--evidence-locator")
        p.add_argument("--evidence-summary")

    p = sub.add_parser("knowledge-claim-add")
    p.add_argument("--artifact", required=True); p.add_argument("--statement", required=True)
    p.add_argument("--lifecycle", choices=list(CLAIM_TRANSITIONS), required=True)
    p.add_argument("--confidence", choices=["low","medium","high"], required=True)
    p.add_argument("--owner-role", required=True); p.add_argument("--review-path", action="append", default=[]); p.add_argument("--unknown", action="append", default=[])
    add_evidence_args(p)

    p = sub.add_parser("knowledge-claim-transition")
    p.add_argument("--artifact", required=True); p.add_argument("--claim", required=True); p.add_argument("--to", choices=list(CLAIM_TRANSITIONS), required=True)
    p.add_argument("--confidence", choices=["low","medium","high"]); add_evidence_args(p)

    p = sub.add_parser("knowledge-unknown-add")
    p.add_argument("--artifact", required=True); p.add_argument("--question", required=True); p.add_argument("--impact"); p.add_argument("--owner-role", required=True)

    p = sub.add_parser("knowledge-link")
    p.add_argument("--artifact", required=True); p.add_argument("--depends-on", required=True); p.add_argument("--relation", choices=["parent","child","depends_on","feeds","implements","supersedes","references"], default="depends_on")

    p = sub.add_parser("knowledge-trigger-add")
    p.add_argument("--artifact", required=True); p.add_argument("--path", action="append", default=[]); p.add_argument("--event", action="append", default=[]); p.add_argument("--description")

    p = sub.add_parser("knowledge-render")
    g = p.add_mutually_exclusive_group(required=True); g.add_argument("--artifact"); g.add_argument("--all", action="store_true")
    sub.add_parser("knowledge-validate")

    p = sub.add_parser("knowledge-stale-scan")
    p.add_argument("--changed", action="append", default=[]); p.add_argument("--event", action="append", default=[]); p.add_argument("--git-base")
    p.add_argument("--source-kind", choices=["git_commit","git_tree","user_approval","design_version","external_version","timestamp","none"]); p.add_argument("--source-value")

    p = sub.add_parser("knowledge-refresh")
    p.add_argument("--artifact", required=True); p.add_argument("--source-kind", choices=["git_commit","git_tree","user_approval","design_version","external_version","timestamp","none"]); p.add_argument("--source-value"); p.add_argument("--allow-unresolved", action="store_true")

    p = sub.add_parser("knowledge-task-assess")
    p.add_argument("--task", required=True); p.add_argument("--status", choices=["not_required","planned","applied","deferred"], required=True); p.add_argument("--artifact", action="append", default=[]); p.add_argument("--summary")

    p = sub.add_parser("knowledge-packet-create")
    p.add_argument("--id", required=True); p.add_argument("--title", required=True); p.add_argument("--task", required=True); p.add_argument("--artifact", action="append", required=True); p.add_argument("--owner-role", required=True); p.add_argument("--max-evidence", type=int, default=20)

    p = sub.add_parser("knowledge-sharing-set")
    p.add_argument("--artifact", required=True)
    p.add_argument("--classification", choices=list(KNOWLEDGE_CLASSIFICATIONS))
    p.add_argument("--external-sharing", choices=list(KNOWLEDGE_EXTERNAL_SHARING))
    p.add_argument("--sanitization-status", choices=list(KNOWLEDGE_SANITIZATION_STATUSES))
    p.add_argument("--redaction", action="append", default=[])
    p.add_argument("--note", action="append", default=[])

    p = sub.add_parser("knowledge-sanitize-check")
    p.add_argument("--artifact", action="append", default=[])
    p.add_argument("--external", action="store_true", help="Validate that selected artifacts are permitted and sanitized for external sharing")

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
            "hook-handle": command_hook_handle,
            "enforcement-status": command_enforcement_status,
            "enforcement-set": command_enforcement_set,
            "policy-check": command_policy_check,
            "audit-tail": command_audit_tail,
            "audit-validate": command_audit_validate,
            "worker-status": command_worker_status,
            "create-task": command_create_task,
            "activate-task": command_activate_task,
            "complete-task": command_complete_task,
            "micro-start": command_micro_start,
            "micro-complete": command_micro_complete,
            "micro-escalate": command_micro_escalate,
            "lease-create": command_lease_create,
            "checkpoint": command_checkpoint,
            "recover": command_recover,
            "knowledge-init": command_knowledge_init,
            "knowledge-status": command_knowledge_status,
            "knowledge-create": command_knowledge_create,
            "knowledge-claim-add": command_knowledge_claim_add,
            "knowledge-claim-transition": command_knowledge_claim_transition,
            "knowledge-unknown-add": command_knowledge_unknown_add,
            "knowledge-link": command_knowledge_link,
            "knowledge-trigger-add": command_knowledge_trigger_add,
            "knowledge-render": command_knowledge_render,
            "knowledge-validate": command_knowledge_validate,
            "knowledge-stale-scan": command_knowledge_stale_scan,
            "knowledge-refresh": command_knowledge_refresh,
            "knowledge-task-assess": command_knowledge_task_assess,
            "knowledge-packet-create": command_knowledge_packet_create,
            "knowledge-sharing-set": command_knowledge_sharing_set,
            "knowledge-sanitize-check": command_knowledge_sanitize_check,
        }
        return commands[args.command](root, args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
