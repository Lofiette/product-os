#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tools" / "cpt_dist.py"
REPORT = ROOT / "evaluation" / "enforcement-integration-report.json"


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None,
        stdin: dict | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        input=None if stdin is None else json.dumps(stdin),
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def hook(tool: Path, repo: Path, event: str, **extra) -> dict:
    payload = {
        "session_id": "integration-session",
        "turn_id": "integration-turn",
        "cwd": str(repo),
        "hook_event_name": event,
        "model": "integration-model",
        **extra,
    }
    result = run([sys.executable, str(tool), "hook-handle"], cwd=repo, stdin=payload, check=False)
    if not result.stdout.strip():
        return {"returncode": result.returncode, "output": None, "stderr": result.stderr}
    return {"returncode": result.returncode, "output": json.loads(result.stdout), "stderr": result.stderr}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha8-integration-"))
    checks: list[dict] = []
    try:
        home = tmp / "home"
        home.mkdir()
        repo = tmp / "repo"
        repo.mkdir()
        run(["git", "init", "-q", str(repo)])
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["CODEX_HOME"] = str(home / ".codex")

        install = run([
            sys.executable, str(DIST), "install",
            "--project", str(repo), "--mode", "local",
            "--enforcement-mode", "audit",
            "--rules-profile", "conservative",
        ], env=env)
        checks.append({"name": "install", "passed": install.returncode == 0})

        git_status = run(["git", "-C", str(repo), "status", "--short", "--untracked-files=all"])
        checks.append({"name": "local_git_clean", "passed": not git_status.stdout.strip()})

        doctor = run([sys.executable, str(DIST), "doctor", "--project", str(repo)], env=env)
        checks.append({"name": "doctor", "passed": "runtime: PASS" in doctor.stdout})

        tool = repo / ".cpt" / "bin" / "cpt_runtime.py"
        run([sys.executable, str(tool), "enforcement-set", "--mode", "enforce", "--trust-state", "trusted"], cwd=repo)
        task_id = run([sys.executable, str(tool), "create-task", "--title", "Integration task", "--objective", "Verify enforcement", "--activate"], cwd=repo).stdout.strip()
        lease_id = run([
            sys.executable, str(tool), "lease-create", "--task", task_id,
            "--read", "src/**", "--write", "src/**",
            "--verify", "python -m pytest -q",
        ], cwd=repo).stdout.strip()
        checks.append({"name": "task_and_lease", "passed": bool(task_id and lease_id)})

        allowed = hook(tool, repo, "PreToolUse", tool_name="apply_patch", tool_input={"command": "*** Update File: src/feature.py\n@@\n-x\n+y"})
        denied_scope = hook(tool, repo, "PreToolUse", tool_name="apply_patch", tool_input={"command": "*** Update File: docs/outside.md\n@@\n-x\n+y"})
        denied_git = hook(tool, repo, "PreToolUse", tool_name="Bash", tool_input={"command": "git reset --hard HEAD~1"})
        checks.extend([
            {"name": "allowed_write_in_lease", "passed": allowed["output"] is None},
            {"name": "denied_write_outside_lease", "passed": "deny" in json.dumps(denied_scope["output"])},
            {"name": "denied_destructive_git", "passed": "destructive_git" in json.dumps(denied_git["output"])},
        ])

        run([sys.executable, str(tool), "knowledge-init", "--title", "Knowledge", "--mode", "existing", "--owner-role", "product_strategist"], cwd=repo)
        run([sys.executable, str(tool), "knowledge-create", "--id", "area-integration", "--type", "area_map", "--title", "Integration Area", "--owner-role", "product_designer", "--review-path", "src/**"], cwd=repo)
        (repo / "src").mkdir()
        (repo / "src" / "feature.py").write_text("value = 1\n", encoding="utf-8")
        post = hook(tool, repo, "PostToolUse", tool_name="apply_patch", tool_input={"command": "*** Update File: src/feature.py"}, tool_response={"ok": True})
        artifact = yaml.safe_load((repo / ".cpt/knowledge/artifacts/area-integration.yaml").read_text(encoding="utf-8"))
        checks.append({"name": "knowledge_freshness", "passed": artifact["freshness"] == "needs_review"})

        pre = hook(tool, repo, "PreCompact", trigger="auto")
        post_compact = hook(tool, repo, "PostCompact", trigger="auto")
        current = yaml.safe_load((repo / ".cpt/current.yaml").read_text(encoding="utf-8"))
        checks.extend([
            {"name": "precompact_checkpoint", "passed": bool(current.get("latest_checkpoint")) and "checkpoint" in json.dumps(pre["output"]).lower()},
            {"name": "postcompact_verify", "passed": "verified" in json.dumps(post_compact["output"]).lower()},
        ])

        hook(tool, repo, "SubagentStart", agent_id="worker-1", agent_type="explorer", permission_mode="default")
        hook(tool, repo, "SubagentStop", agent_id="worker-1", agent_type="explorer", agent_transcript_path=None, stop_hook_active=False, last_assistant_message="done", permission_mode="default")
        worker = yaml.safe_load((repo / ".cpt/workers/worker-1.yaml").read_text(encoding="utf-8"))
        checks.append({"name": "worker_record", "passed": worker["status"] == "completed"})

        audit = run([sys.executable, str(tool), "audit-validate"], cwd=repo)
        runtime = run([sys.executable, str(tool), "validate"], cwd=repo)
        checks.extend([
            {"name": "audit_valid", "passed": audit.returncode == 0},
            {"name": "runtime_valid", "passed": runtime.returncode == 0},
        ])

        report = {
            "schema_version": "4.0-alpha8",
            "total": len(checks),
            "passed": sum(1 for item in checks if item["passed"]),
            "checks": checks,
            "notes": [
                "This is a deterministic runtime integration test, not a live Codex behavioral certification.",
                "Plugin hook trust and Codex rule parsing require a live Codex installation.",
            ],
        }
        REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ENFORCEMENT INTEGRATION: {report['passed']}/{report['total']}")
        return 0 if report["passed"] == report["total"] else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
