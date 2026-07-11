#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tools/cpt_dist.py"
REPORT = ROOT / "evaluation/orchestration-integration-report.json"


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None, stdin: dict | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, input=None if stdin is None else json.dumps(stdin), capture_output=True, timeout=60)
    if check and result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def hook(tool: Path, repo: Path, event: str, **extra) -> subprocess.CompletedProcess[str]:
    payload = {"session_id":"integration-session","turn_id":"integration-turn","cwd":str(repo),"hook_event_name":event,"model":"integration-model",**extra}
    return run([sys.executable, str(tool), "hook-handle"], cwd=repo, stdin=payload, check=False)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha7-orchestration-integration-"))
    checks: list[dict[str, object]] = []
    try:
        home = tmp / "home"; home.mkdir()
        repo = tmp / "repo"; repo.mkdir()
        run(["git", "init", "-q", str(repo)])
        run(["git", "-C", str(repo), "config", "user.email", "integration@example.com"])
        run(["git", "-C", str(repo), "config", "user.name", "CPT Integration"])
        (repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        run(["git", "-C", str(repo), "add", "README.md"])
        run(["git", "-C", str(repo), "commit", "-qm", "fixture"])
        env = os.environ.copy(); env["HOME"] = str(home); env["CODEX_HOME"] = str(home / ".codex")

        install = run([sys.executable, str(DIST), "install", "--project", str(repo), "--mode", "local", "--plugin-scope", "none", "--enforcement-mode", "audit"], env=env)
        checks.append({"name":"install", "passed": install.returncode == 0})
        git_clean = run(["git", "-C", str(repo), "status", "--short", "--untracked-files=all"])
        checks.append({"name":"local_git_clean", "passed": not git_clean.stdout.strip()})
        workers = run([sys.executable, str(DIST), "workers-install", "--scope", "repo", "--project", str(repo)], env=env)
        checks.append({"name":"worker_pack", "passed":"Installed 10" in workers.stdout})

        tool = repo / ".cpt/bin/cpt_runtime.py"
        task = run([sys.executable, str(tool), "create-task", "--title", "Integration", "--objective", "Verify orchestration", "--activate"], cwd=repo).stdout.strip()
        lease = run([
            sys.executable, str(tool), "lease-create", "--task", task,
            "--read", "src/**", "--worker", "cpt_explorer", "--worker", "cpt_code_reviewer",
            "--rationale", "integration",
        ], cwd=repo).stdout.strip()
        checks.append({"name":"task_and_lease", "passed": bool(task and lease)})
        orchestration = run([
            sys.executable, str(tool), "orchestration-create", "--title", "Read review", "--purpose", "Map and review", "--task", task, "--lease", lease,
        ], cwd=repo).stdout.strip()
        c1 = run([
            sys.executable, str(tool), "worker-contract-add", "--run", orchestration, "--archetype", "cpt_explorer", "--purpose", "Explore", "--required",
            "--role", "frontend_engineer", "--skill", "cpt-task-planning", "--read", "src/**",
        ], cwd=repo).stdout.strip()
        c2 = run([
            sys.executable, str(tool), "worker-contract-add", "--run", orchestration, "--archetype", "cpt_code_reviewer", "--purpose", "Review", "--required",
            "--role", "code_reviewer", "--skill", "cpt-implementation-review", "--read", "src/**",
        ], cwd=repo).stdout.strip()
        run([sys.executable, str(tool), "orchestration-approve", "--run", orchestration], cwd=repo)
        run([sys.executable, str(tool), "orchestration-activate", "--run", orchestration], cwd=repo)
        checks.append({"name":"approved_contracts", "passed": bool(c1 and c2)})

        start1 = hook(tool, repo, "SubagentStart", agent_id="worker-explorer", agent_type="cpt_explorer", permission_mode="read_only")
        checks.append({"name":"native_binding_1", "passed":"managed worker contract" in start1.stdout})
        pre = hook(tool, repo, "PreCompact", trigger="auto")
        checks.append({"name":"precompact_checkpoint", "passed":"checkpoint" in pre.stdout.lower()})
        post = hook(tool, repo, "PostCompact", trigger="auto")
        checks.append({"name":"postcompact_recovery", "passed":"verified" in post.stdout.lower()})
        hook(tool, repo, "SubagentStop", agent_id="worker-explorer", agent_type="cpt_explorer", last_assistant_message="done")
        run([sys.executable, str(tool), "worker-result-submit", "--contract", c1, "--status", "success", "--summary", "Mapped", "--evidence", "fixture:explore", "--confidence", "high"], cwd=repo)

        start2 = hook(tool, repo, "SubagentStart", agent_id="worker-review", agent_type="cpt_code_reviewer", permission_mode="read_only")
        checks.append({"name":"native_binding_2", "passed":"managed worker contract" in start2.stdout})
        hook(tool, repo, "SubagentStop", agent_id="worker-review", agent_type="cpt_code_reviewer", last_assistant_message="done")
        run([sys.executable, str(tool), "worker-result-submit", "--contract", c2, "--status", "success", "--summary", "Reviewed", "--evidence", "fixture:review", "--confidence", "high"], cwd=repo)
        state = json.loads(run([sys.executable, str(tool), "orchestration-status", "--run", orchestration], cwd=repo).stdout)
        checks.append({"name":"required_quorum", "passed": state["quorum"]["satisfied"]})
        run([sys.executable, str(tool), "orchestration-integrate", "--run", orchestration, "--summary", "Integrated", "--apply"], cwd=repo)
        completed = json.loads(run([sys.executable, str(tool), "orchestration-complete", "--run", orchestration], cwd=repo).stdout)
        checks.append({"name":"orchestration_complete", "passed": completed["status"] == "completed"})
        run([sys.executable, str(tool), "knowledge-task-assess", "--task", task, "--status", "not_required", "--summary", "No durable knowledge change"], cwd=repo)
        run([sys.executable, str(tool), "complete-task", "--task", task], cwd=repo)
        checks.append({"name":"task_complete", "passed": True})
        validation = run([sys.executable, str(tool), "validate"], cwd=repo)
        orchestration_validation = run([sys.executable, str(tool), "orchestration-validate"], cwd=repo)
        checks.append({"name":"runtime_validation", "passed":"RUNTIME VALIDATION PASSED" in validation.stdout})
        checks.append({"name":"orchestration_validation", "passed":"ORCHESTRATION VALIDATION PASSED" in orchestration_validation.stdout})
        doctor = run([sys.executable, str(DIST), "doctor", "--project", str(repo)], env=env)
        checks.append({"name":"doctor", "passed":"runtime: PASS" in doctor.stdout})
        final_checkpoint = run([sys.executable, str(tool), "checkpoint", "--reason", "Final integration checkpoint"], cwd=repo)
        verify = run([sys.executable, str(tool), "recover", "--checkpoint", "latest", "--verify-only"], cwd=repo)
        checks.append({"name":"final_checkpoint", "passed": bool(final_checkpoint.stdout.strip()) and "checkpoint match" in verify.stdout.lower()})

        report = {
            "schema_version":"4.0-alpha7",
            "total":len(checks),
            "passed":sum(1 for item in checks if item["passed"]),
            "checks":checks,
            "limitations":[
                "This simulates hook payloads and structured results; it does not launch live Codex subagent threads.",
                "Host cancellation delivery and real reconnect ordering require live-client evaluation.",
            ],
        }
        REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ORCHESTRATION INTEGRATION: {report['passed']}/{report['total']}")
        return 0 if report["passed"] == report["total"] else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
