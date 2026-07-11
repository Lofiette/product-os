from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tools" / "cpt_dist.py"


def run_dist(*args: str, env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, str(DIST), *args], text=True, capture_output=True, env=env)
    if check and result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result


class OrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha7-orchestration-base-"))
        cls.base_home = cls.base_tmp / "home"
        cls.base_home.mkdir()
        cls.base_repo = cls.base_tmp / "repo"
        cls.base_repo.mkdir()
        subprocess.run(["git", "init", "-q", str(cls.base_repo)], check=True)
        subprocess.run(["git", "-C", str(cls.base_repo), "config", "user.email", "tests@example.com"], check=True)
        subprocess.run(["git", "-C", str(cls.base_repo), "config", "user.name", "CPT Tests"], check=True)
        (cls.base_repo / "README.md").write_text("# fixture\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(cls.base_repo), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(cls.base_repo), "commit", "-qm", "fixture"], check=True)
        cls.base_env = os.environ.copy()
        cls.base_env["HOME"] = str(cls.base_home)
        cls.base_env["CODEX_HOME"] = str(cls.base_home / ".codex")
        run_dist(
            "install", "--project", str(cls.base_repo), "--mode", "local",
            "--plugin-scope", "none", "--enforcement-mode", "audit",
            env=cls.base_env,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.base_tmp, ignore_errors=True)

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cpt-alpha7-orchestration-case-"))
        self.repo = self.tmp / "repo"
        shutil.copytree(self.base_repo, self.repo)
        self.env = self.base_env.copy()
        self.runtime_tool = self.repo / ".cpt/bin/cpt_runtime.py"

    def tearDown(self) -> None:
        # Prune any worktrees registered against the copied fixture before removal.
        subprocess.run(["git", "-C", str(self.repo), "worktree", "prune"], capture_output=True)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def tool(self, *args: str, input_json: dict | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.runtime_tool), *args],
            cwd=self.repo,
            text=True,
            input=None if input_json is None else json.dumps(input_json),
            capture_output=True,
        )
        if check and result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return result

    def hook(self, event: str, **extra) -> subprocess.CompletedProcess[str]:
        payload = {
            "session_id": "S1",
            "turn_id": "T1",
            "cwd": str(self.repo),
            "hook_event_name": event,
            "model": "test-model",
            **extra,
        }
        return self.tool("hook-handle", input_json=payload, check=False)

    def create_task_lease(
        self,
        *,
        workers: tuple[str, ...] = ("cpt_explorer",),
        write: tuple[str, ...] = (),
        workers_may_write: bool = False,
        max_workers_expected: int | None = None,
    ) -> tuple[str, str]:
        task = self.tool("create-task", "--title", "Task", "--objective", "Test orchestration", "--activate").stdout.strip()
        args = ["lease-create", "--task", task, "--read", "src/**", "--rationale", "test"]
        for value in write:
            args += ["--write", value]
        for worker in workers:
            args += ["--worker", worker]
        if workers_may_write:
            args += ["--workers-may-write"]
        lease = self.tool(*args).stdout.strip()
        if max_workers_expected is not None:
            data = yaml.safe_load((self.repo / f".cpt/leases/{lease}.yaml").read_text(encoding="utf-8"))
            self.assertEqual(data["delegation"]["max_workers"], max_workers_expected)
        return task, lease

    def create_run(self, task: str, lease: str, *, strategy: str = "read_only", mode: str = "all_required", n: int | None = None) -> str:
        args = [
            "orchestration-create", "--title", "Run", "--purpose", "Test",
            "--task", task, "--lease", lease, "--write-strategy", strategy,
            "--quorum-mode", mode,
        ]
        if n is not None:
            args += ["--quorum-n", str(n)]
        return self.tool(*args).stdout.strip()

    def add_contract(
        self,
        run: str,
        archetype: str,
        *,
        required: bool = True,
        permission: str = "read_only",
        isolation: str = "direct",
        role: str | None = None,
        skill: str | None = None,
        write: tuple[str, ...] = (),
        timeout: int = 900,
    ) -> str:
        role = role or {
            "cpt_explorer": "frontend_engineer",
            "cpt_researcher": "ux_researcher",
            "cpt_product_mapper": "product_strategist",
            "cpt_design_reviewer": "product_designer",
            "cpt_implementer": "frontend_engineer",
            "cpt_test_runner": "qa_engineer",
            "cpt_code_reviewer": "code_reviewer",
            "cpt_risk_reviewer": "security_reviewer",
            "cpt_knowledge_curator": "information_architect",
            "cpt_incident_investigator": "incident_investigator",
        }[archetype]
        skill = skill or {
            "cpt_explorer": "cpt-task-planning",
            "cpt_researcher": "cpt-ux-research",
            "cpt_product_mapper": "cpt-knowledge-lifecycle",
            "cpt_design_reviewer": "cpt-visual-acceptance-review",
            "cpt_implementer": "cpt-frontend-integration",
            "cpt_test_runner": "cpt-implementation-review",
            "cpt_code_reviewer": "cpt-implementation-review",
            "cpt_risk_reviewer": "cpt-threat-model",
            "cpt_knowledge_curator": "cpt-knowledge-lifecycle",
            "cpt_incident_investigator": "cpt-incident-review",
        }[archetype]
        args = [
            "worker-contract-add", "--run", run, "--archetype", archetype,
            "--purpose", "Bounded worker", "--required" if required else "--optional",
            "--role", role, "--skill", skill, "--read", "src/**",
            "--permission-mode", permission, "--isolation", isolation,
            "--timeout", str(timeout), "--stop-condition", "Return bounded evidence",
        ]
        for value in write:
            args += ["--write", value]
        return self.tool(*args).stdout.strip()

    def approve_activate(self, run: str) -> None:
        self.tool("orchestration-approve", "--run", run)
        self.tool("orchestration-activate", "--run", run)

    def result(self, contract: str, status: str = "success", *, touched: tuple[str, ...] = (), verification: tuple[str, ...] = ()) -> subprocess.CompletedProcess[str]:
        args = [
            "worker-result-submit", "--contract", contract, "--status", status,
            "--summary", f"{status} result", "--evidence", "fixture:1", "--confidence", "high",
        ]
        for value in touched:
            args += ["--touched", value]
        for value in verification:
            args += ["--verification", value]
        return self.tool(*args, check=False)

    def status(self, run: str) -> dict:
        return json.loads(self.tool("orchestration-status", "--run", run).stdout)

    def test_required_quorum_and_manual_fallback_result(self):
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        contract = self.add_contract(run, "cpt_explorer")
        self.approve_activate(run)
        result = self.result(contract)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = self.status(run)
        self.assertTrue(state["quorum"]["satisfied"])
        self.assertEqual(state["status"], "satisfied")

    def test_partial_required_result_does_not_satisfy_quorum(self):
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        contract = self.add_contract(run, "cpt_explorer")
        self.approve_activate(run)
        self.assertEqual(self.result(contract, "partial").returncode, 0)
        state = self.status(run)
        self.assertFalse(state["quorum"]["satisfied"])
        self.assertFalse(state["quorum"]["possible"])
        self.assertEqual(state["status"], "blocked")

    def test_optional_failure_does_not_break_all_required(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer", "cpt_code_reviewer"))
        run = self.create_run(task, lease)
        required = self.add_contract(run, "cpt_explorer")
        optional = self.add_contract(run, "cpt_code_reviewer", required=False)
        self.approve_activate(run)
        self.assertEqual(self.result(required).returncode, 0)
        self.assertEqual(self.result(optional, "failure").returncode, 0)
        state = self.status(run)
        self.assertTrue(state["quorum"]["satisfied"])
        self.assertEqual(state["status"], "satisfied")

    def test_all_quorum_is_blocked_by_optional_failure(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer", "cpt_code_reviewer"))
        run = self.create_run(task, lease, mode="all")
        required = self.add_contract(run, "cpt_explorer")
        optional = self.add_contract(run, "cpt_code_reviewer", required=False)
        self.approve_activate(run)
        self.result(required)
        self.result(optional, "failure")
        state = self.status(run)
        self.assertFalse(state["quorum"]["satisfied"])
        self.assertFalse(state["quorum"]["possible"])

    def test_n_of_m_quorum(self):
        workers = ("cpt_explorer", "cpt_code_reviewer", "cpt_risk_reviewer")
        task, lease = self.create_task_lease(workers=workers)
        run = self.create_run(task, lease, mode="n_of_m", n=2)
        c1 = self.add_contract(run, workers[0], required=True)
        c2 = self.add_contract(run, workers[1], required=False)
        self.add_contract(run, workers[2], required=False)
        self.approve_activate(run)
        self.result(c1)
        self.result(c2)
        self.assertTrue(self.status(run)["quorum"]["satisfied"])

    def test_duplicate_archetype_rejected(self):
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        self.add_contract(run, "cpt_explorer")
        second = self.tool(
            "worker-contract-add", "--run", run, "--archetype", "cpt_explorer",
            "--purpose", "duplicate", "--optional", "--role", "frontend_engineer",
            "--skill", "cpt-task-planning", "--read", "src/**", check=False,
        )
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("Duplicate worker archetype", second.stderr)

    def test_disallowed_role_lens_rejected(self):
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        bad = self.tool(
            "worker-contract-add", "--run", run, "--archetype", "cpt_explorer",
            "--purpose", "bad lens", "--required", "--role", "security_reviewer",
            "--skill", "cpt-task-planning", "--read", "src/**", check=False,
        )
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("role lenses not allowed", bad.stderr)

    def test_lease_worker_budget_is_enforced(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer",), max_workers_expected=1)
        run = self.create_run(task, lease)
        self.add_contract(run, "cpt_explorer")
        second = self.tool(
            "worker-contract-add", "--run", run, "--archetype", "cpt_code_reviewer",
            "--purpose", "over budget", "--optional", "--role", "code_reviewer",
            "--skill", "cpt-implementation-review", "--read", "src/**", check=False,
        )
        self.assertNotEqual(second.returncode, 0)

    def test_read_only_lease_rejects_writable_worker(self):
        task, lease = self.create_task_lease(workers=("cpt_implementer",), write=("src/**",))
        run = self.create_run(task, lease, strategy="sequential_direct")
        bad = self.tool(
            "worker-contract-add", "--run", run, "--archetype", "cpt_implementer",
            "--purpose", "write", "--required", "--role", "frontend_engineer",
            "--skill", "cpt-frontend-integration", "--read", "src/**", "--write", "src/**",
            "--permission-mode", "workspace_write", "--isolation", "direct", check=False,
        )
        self.assertIn("read-only workers only", bad.stderr)

    def test_optional_worker_can_start_after_required_quorum(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer", "cpt_code_reviewer"))
        run = self.create_run(task, lease)
        required = self.add_contract(run, "cpt_explorer")
        optional = self.add_contract(run, "cpt_code_reviewer", required=False)
        self.approve_activate(run)
        self.result(required)
        self.assertEqual(self.status(run)["status"], "satisfied")
        started = self.hook("SubagentStart", agent_id="optional-1", agent_type="cpt_code_reviewer")
        self.assertEqual(started.returncode, 0)
        contract = yaml.safe_load((self.repo / f".cpt/orchestrations/contracts/{optional}.yaml").read_text(encoding="utf-8"))
        self.assertEqual(contract["status"], "active")

    def test_reconcile_times_out_worker(self):
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        contract = self.add_contract(run, "cpt_explorer", timeout=30)
        self.approve_activate(run)
        self.hook("SubagentStart", agent_id="slow", agent_type="cpt_explorer")
        path = self.repo / f".cpt/orchestrations/contracts/{contract}.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        old = datetime.now(timezone.utc) - timedelta(minutes=10)
        data["started_at"] = old.replace(microsecond=0).isoformat().replace("+00:00", "Z")
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        self.tool("orchestration-reconcile", "--run", run)
        updated = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(updated["status"], "timed_out")

    def test_contract_cancel_does_not_cancel_whole_run(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer", "cpt_code_reviewer"))
        run = self.create_run(task, lease)
        required = self.add_contract(run, "cpt_explorer")
        optional = self.add_contract(run, "cpt_code_reviewer", required=False)
        self.approve_activate(run)
        self.tool("worker-cancel", "--contract", optional, "--reason", "not needed")
        state = self.status(run)
        self.assertFalse(state["status"] == "cancelling")
        self.result(required)
        self.assertTrue(self.status(run)["quorum"]["satisfied"])

    def test_run_cancel_marks_all_unresolved_contracts(self):
        task, lease = self.create_task_lease(workers=("cpt_explorer", "cpt_code_reviewer"))
        run = self.create_run(task, lease)
        c1 = self.add_contract(run, "cpt_explorer")
        c2 = self.add_contract(run, "cpt_code_reviewer", required=False)
        self.approve_activate(run)
        self.tool("orchestration-cancel", "--run", run, "--reason", "stop")
        self.assertEqual(self.status(run)["status"], "cancelling")
        for cid in (c1, c2):
            data = yaml.safe_load((self.repo / f".cpt/orchestrations/contracts/{cid}.yaml").read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "cancel_requested")

    def test_multiple_direct_writers_rejected(self):
        workers = ("cpt_implementer", "cpt_test_runner")
        task, lease = self.create_task_lease(workers=workers, write=("src/**",), workers_may_write=True)
        run = self.create_run(task, lease, strategy="sequential_direct")
        self.add_contract(run, workers[0], permission="workspace_write", isolation="direct", write=("src/a/**",))
        self.add_contract(run, workers[1], required=False, permission="workspace_write", isolation="direct", write=("src/b/**",))
        approved = self.tool("orchestration-approve", "--run", run, check=False)
        self.assertNotEqual(approved.returncode, 0)
        self.assertIn("Multiple writable workers require parallel_worktree", approved.stderr)

    def test_parallel_write_requires_worktree_isolation(self):
        task, lease = self.create_task_lease(workers=("cpt_implementer",), write=("src/**",), workers_may_write=True)
        run = self.create_run(task, lease, strategy="parallel_worktree")
        bad = self.tool(
            "worker-contract-add", "--run", run, "--archetype", "cpt_implementer",
            "--purpose", "write", "--required", "--role", "frontend_engineer",
            "--skill", "cpt-frontend-integration", "--read", "src/**", "--write", "src/**",
            "--permission-mode", "workspace_write", "--isolation", "direct", check=False,
        )
        self.assertIn("requires worktree isolation", bad.stderr)

    def create_write_run(self, *, write_scope: str = "src/**") -> tuple[str, str, str, str]:
        task, lease = self.create_task_lease(workers=("cpt_implementer",), write=(write_scope,), workers_may_write=True)
        run = self.create_run(task, lease, strategy="parallel_worktree")
        contract = self.add_contract(run, "cpt_implementer", permission="workspace_write", isolation="worktree", write=(write_scope,))
        self.tool("orchestration-approve", "--run", run)
        return task, lease, run, contract

    def test_dirty_base_rejects_worktree(self):
        _, _, _, contract = self.create_write_run()
        (self.repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        result = self.tool("worktree-create", "--contract", contract, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Main repository is dirty", result.stderr)

    def test_worktree_scope_and_reported_paths_are_verified(self):
        _, _, run, contract = self.create_write_run(write_scope="src/allowed/**")
        record = json.loads(self.tool("worktree-create", "--contract", contract).stdout)
        wt = Path(record["path"])
        (wt / "src/allowed").mkdir(parents=True)
        (wt / "src/allowed/a.py").write_text("x=1\n", encoding="utf-8")
        self.assertEqual(self.result(contract, touched=("src/allowed/other.py",), verification=("checked",)).returncode, 0)
        plan = self.tool("worktree-plan", "--contract", contract, check=False)
        self.assertIn("do not match Git changes", plan.stderr)

    def test_worktree_out_of_scope_change_is_blocked(self):
        _, _, _, contract = self.create_write_run(write_scope="src/allowed/**")
        record = json.loads(self.tool("worktree-create", "--contract", contract).stdout)
        wt = Path(record["path"])
        (wt / "docs").mkdir()
        (wt / "docs/out.md").write_text("bad\n", encoding="utf-8")
        result = self.tool("worktree-plan", "--contract", contract, check=False)
        self.assertIn("outside contract write_scope", result.stderr)

    def test_tampered_worktree_record_is_blocked(self):
        _, _, _, contract = self.create_write_run()
        self.tool("worktree-create", "--contract", contract)
        path = self.repo / f".cpt/worktrees/{contract}.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["branch"] = "cpt/orc-999/orc-999-w99"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        result = self.tool("worktree-remove", "--contract", contract, "--discard", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("branch does not match", result.stderr)

    def test_managed_readonly_worker_allows_precompact_checkpoint(self):
        self.tool("enforcement-set", "--mode", "enforce", "--trust-state", "trusted")
        task, lease = self.create_task_lease()
        run = self.create_run(task, lease)
        self.add_contract(run, "cpt_explorer")
        self.approve_activate(run)
        self.hook("SubagentStart", agent_id="reader", agent_type="cpt_explorer", permission_mode="read_only")
        result = self.hook("PreCompact", trigger="auto")
        self.assertEqual(result.returncode, 0)
        current = yaml.safe_load((self.repo / ".cpt/current.yaml").read_text(encoding="utf-8"))
        self.assertTrue(current.get("latest_checkpoint"))
        self.assertNotIn('"continue": false', result.stdout.lower())

    def test_managed_write_worker_blocks_precompact(self):
        self.tool("enforcement-set", "--mode", "enforce", "--trust-state", "trusted")
        _, _, run, contract = self.create_write_run()
        self.tool("worktree-create", "--contract", contract)
        self.tool("orchestration-activate", "--run", run)
        self.hook("SubagentStart", agent_id="writer", agent_type="cpt_implementer", permission_mode="workspace_write")
        result = self.hook("PreCompact", trigger="auto")
        self.assertIn('"continue": false', result.stdout.lower())

    def test_worker_pack_install_status_remove(self):
        result = run_dist("workers-install", "--scope", "repo", "--project", str(self.repo), env=self.env)
        self.assertIn("Installed 10", result.stdout)
        status = run_dist("workers-status", "--scope", "repo", "--project", str(self.repo), env=self.env)
        payload = json.loads(status.stdout)
        self.assertTrue(payload["installed"])
        self.assertEqual(len(payload["files"]), 10)
        run_dist("workers-remove", "--scope", "repo", "--project", str(self.repo), env=self.env)
        self.assertFalse((self.repo / ".cpt/worker-pack.json").exists())

    def test_tampered_worker_receipt_cannot_remove_unrelated_file(self):
        run_dist("workers-install", "--scope", "repo", "--project", str(self.repo), env=self.env)
        unrelated = self.repo / ".codex/agents/unrelated.toml"
        unrelated.write_text("name='unrelated'\n", encoding="utf-8")
        receipt_path = self.repo / ".cpt/worker-pack.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["files"]["unrelated.toml"] = "0" * 64
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result = run_dist("workers-remove", "--scope", "repo", "--project", str(self.repo), env=self.env, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(unrelated.exists())

    def test_uninstall_refuses_active_orchestration(self):
        task, lease = self.create_task_lease()
        self.create_run(task, lease)
        result = run_dist("uninstall", "--project", str(self.repo), "--discard-state", env=self.env, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("current_orchestration", result.stderr)


if __name__ == "__main__":
    unittest.main()
