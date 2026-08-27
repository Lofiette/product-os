#!/usr/bin/env python3
from __future__ import annotations

import json
import ast
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

required = [
    ROOT / "payload/repo-scaffold/.cpt/bin/cpt_orchestration.py",
    ROOT / "payload/repo-scaffold/.cpt/worker-archetypes.json",
    ROOT / "payload/worker-pack/worker-pack.json",
    ROOT / "payload/worker-pack/config/agents.example.toml",
    ROOT / "ORCHESTRATION.md",
    ROOT / "WORKER_PACK.md",
]
for path in required:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")

try:
    ast.parse(required[0].read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"orchestration module compile: {exc}")

try:
    registry_doc = json.loads(required[1].read_text(encoding="utf-8"))
    archetypes = registry_doc.get("archetypes", [])
    if registry_doc.get("version") != "4.1.0":
        errors.append("worker archetype registry version mismatch")
    if registry_doc.get("archetype_count") != 10 or len(archetypes) != 10:
        errors.append("worker archetype registry must contain exactly 10 archetypes")
    ids = [item.get("id") for item in archetypes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate worker archetype IDs")
    role_registry = json.loads((ROOT / "roles/ROLE_REGISTRY.json").read_text(encoding="utf-8"))
    role_ids = {item["id"] for item in role_registry.get("roles", [])}
    skill_registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
    skill_ids = {item["id"] for item in skill_registry.get("skills", [])}
    valid_fields = {"summary", "evidence", "blockers", "confidence", "touched_paths", "verification", "recommendations"}
    for item in archetypes:
        if item.get("default_permission_mode") not in {"read_only", "workspace_write"}:
            errors.append(f"{item.get('id')}: invalid default_permission_mode")
        if item.get("default_isolation") not in {"direct", "worktree"}:
            errors.append(f"{item.get('id')}: invalid default_isolation")
        if item.get("default_permission_mode") == "workspace_write" and item.get("default_isolation") != "worktree":
            errors.append(f"{item.get('id')}: writable archetype must default to worktree")
        unknown_roles = sorted(set(item.get("allowed_role_lenses", [])) - role_ids)
        if unknown_roles:
            errors.append(f"{item.get('id')}: unknown role lenses {unknown_roles}")
        unknown_skills = sorted(set(item.get("recommended_skills", [])) - skill_ids)
        if unknown_skills:
            errors.append(f"{item.get('id')}: unknown recommended skills {unknown_skills}")
        unknown_fields = sorted(set(item.get("required_output_fields", [])) - valid_fields)
        if unknown_fields:
            errors.append(f"{item.get('id')}: unknown output fields {unknown_fields}")
except Exception as exc:
    errors.append(f"worker archetype registry: {exc}")

try:
    pack = json.loads(required[2].read_text(encoding="utf-8"))
    if pack.get("version") != "4.1.0" or pack.get("agent_count") != 10:
        errors.append("worker pack metadata mismatch")
    agents = sorted((ROOT / "payload/worker-pack/agents").glob("*.toml"))
    if len(agents) != 10:
        errors.append(f"worker pack must contain 10 TOML files; found {len(agents)}")
    try:
        import tomllib
    except ImportError:
        tomllib = None
    if tomllib:
        names = []
        for path in agents:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            for key in ("name", "description", "developer_instructions"):
                if not data.get(key):
                    errors.append(f"{path.relative_to(ROOT)} missing {key}")
            if data.get("name") != path.stem:
                errors.append(f"{path.relative_to(ROOT)} name/file mismatch")
            instructions = data.get("developer_instructions", "").lower()
            if "do not spawn" not in instructions and "must not spawn" not in instructions:
                errors.append(f"{path.relative_to(ROOT)} must forbid nested subagents")
            names.append(data.get("name"))
        if len(names) != len(set(names)):
            errors.append("worker TOML names are not unique")
except Exception as exc:
    errors.append(f"worker pack: {exc}")

try:
    schema = json.loads((ROOT / "payload/repo-scaffold/.cpt/schema-bundle.json").read_text(encoding="utf-8"))
    for name in (
        "orchestration-run.schema.json",
        "worker-contract.schema.json",
        "worker-result.schema.json",
        "worktree-record.schema.json",
    ):
        if name not in schema:
            errors.append(f"missing schema {name}")
except Exception as exc:
    errors.append(f"schema bundle: {exc}")

runtime_text = (ROOT / "payload/repo-scaffold/.cpt/bin/cpt_runtime.py").read_text(encoding="utf-8")
for command in (
    "orchestration-create", "worker-contract-add", "orchestration-approve", "orchestration-activate",
    "worker-result-submit", "worker-cancel", "orchestration-reconcile", "orchestration-integrate",
    "orchestration-complete", "worktree-create", "worktree-plan", "worktree-remove",
):
    if command not in runtime_text:
        errors.append(f"runtime CLI missing {command}")

config = (ROOT / "payload/worker-pack/config/agents.example.toml").read_text(encoding="utf-8")
for expected in ("max_threads = 4", "max_depth = 1", "job_max_runtime_seconds = 900"):
    if expected not in config:
        errors.append(f"worker config example missing {expected}")

if errors:
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1)
print("ORCHESTRATION ASSET VALIDATION PASSED")
