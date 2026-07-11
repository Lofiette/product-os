#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evaluation/orchestration-cases.json").read_text(encoding="utf-8"))["cases"]
registry = json.loads((ROOT / "orchestration/WORKER_ARCHETYPES.json").read_text(encoding="utf-8"))
roles = {item["id"] for item in json.loads((ROOT / "roles/ROLE_REGISTRY.json").read_text(encoding="utf-8"))["roles"]}
skills = {item["id"] for item in json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))["skills"]}
schema = json.loads((ROOT / "payload/repo-scaffold/.cpt/schema-bundle.json").read_text(encoding="utf-8"))
orch = (ROOT / "payload/repo-scaffold/.cpt/bin/cpt_orchestration.py").read_text(encoding="utf-8")
runtime = (ROOT / "payload/repo-scaffold/.cpt/bin/cpt_runtime.py").read_text(encoding="utf-8")
dist = (ROOT / "tools/cpt_dist.py").read_text(encoding="utf-8")
config = (ROOT / "payload/worker-pack/config/agents.example.toml").read_text(encoding="utf-8")
pack = json.loads((ROOT / "payload/worker-pack/worker-pack.json").read_text(encoding="utf-8"))
agents = sorted((ROOT / "payload/worker-pack/agents").glob("*.toml"))
items = registry["archetypes"]
ids = [item["id"] for item in items]
valid_fields = {"summary","evidence","blockers","confidence","touched_paths","verification","recommendations"}

try:
    import tomllib
except ImportError:
    tomllib = None
parsed_agents = [tomllib.loads(p.read_text(encoding="utf-8")) for p in agents] if tomllib else []

checks = {
    "registry-count": len(items) == 10 and registry.get("archetype_count") == 10,
    "registry-unique": len(ids) == len(set(ids)),
    "role-lens-integrity": all(set(item.get("allowed_role_lenses", [])) <= roles for item in items),
    "skill-integrity": all(set(item.get("recommended_skills", [])) <= skills for item in items),
    "output-field-integrity": all(set(item.get("required_output_fields", [])) <= valid_fields for item in items),
    "read-heavy-default": all(item["default_permission_mode"] == "read_only" for item in items if item["id"] not in {"cpt_implementer","cpt_test_runner"}),
    "writer-isolation": all(item["default_permission_mode"] == "workspace_write" and item["default_isolation"] == "worktree" for item in items if item["id"] in {"cpt_implementer","cpt_test_runner"}),
    "worker-pack-count": len(agents) == 10 and pack.get("agent_count") == 10,
    "worker-pack-unique": bool(parsed_agents) and len({item.get("name") for item in parsed_agents}) == 10,
    "nested-spawn-ban": bool(parsed_agents) and all(("do not spawn" in item.get("developer_instructions", "").lower() or "must not spawn" in item.get("developer_instructions", "").lower()) for item in parsed_agents),
    "thread-budget": "max_threads = 4" in config,
    "depth-budget": "max_depth = 1" in config,
    "runtime-budget": "job_max_runtime_seconds = 900" in config,
    "run-schema": "orchestration-run.schema.json" in schema,
    "contract-schema": "worker-contract.schema.json" in schema,
    "result-schema": "worker-result.schema.json" in schema,
    "worktree-schema": "worktree-record.schema.json" in schema,
    "quorum-modes": all(mode in orch for mode in ("all_required", "n_of_m", 'mode == "all"')),
    "partial-not-success": 'SUCCESS_RESULT_STATUS = "success"' in orch and '"partial": "partial"' in orch,
    "unique-archetype-binding": "Duplicate worker archetype in one orchestration run is not allowed" in orch,
    "structured-result": "worker-result-submit" in runtime and "submit_result" in orch,
    "manual-fallback": 'contract.get("status") not in {"approved"' in orch,
    "cooperative-cancel": "host_action_required" in runtime,
    "timeout-reconcile": 'contract["status"] = "timed_out"' in orch,
    "checkpoint-bundle": "active_orchestration" in runtime and "bundle_for_checkpoint" in runtime,
    "compaction-readonly": "allow_managed_readonly_compaction" in runtime,
    "compaction-writer-block": "managed_compaction_issues" in runtime,
    "dirty-base-guard": "Main repository is dirty; refusing worktree creation" in orch,
    "worktree-scope": "outside contract write_scope" in orch,
    "touched-path-proof": "Worker-reported touched paths do not match Git changes" in orch,
    "no-auto-merge": "review_only_no_automatic_merge" in orch,
    "receipt-safety": "validate_workers_receipt" in dist and "Unsafe worker receipt path" in dist,
    "uninstall-active-guard": "Refusing uninstall while CPT runtime is active" in dist,
    "optional-pack": '"status": "not_installed"' in dist and "workers-install" in dist,
}
results = []
for case in CASES:
    passed = bool(checks.get(case["id"], False))
    results.append({**case, "passed": passed})
report = {
    "schema_version": "4.0-alpha8",
    "total": len(results),
    "passed": sum(item["passed"] for item in results),
    "cases": results,
    "limitations": [
        "This is a deterministic asset and policy proxy, not a live Codex subagent certification.",
        "Native spawn, cancellation delivery, reconnect ordering, and model output quality require live-client evaluation.",
    ],
}
(ROOT / "evaluation/orchestration-eval-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"ORCHESTRATION POLICY EVAL: {report['passed']}/{report['total']}")
if report["passed"] != report["total"]:
    for item in results:
        if not item["passed"]:
            print("FAILED:", item["id"])
    raise SystemExit(1)
