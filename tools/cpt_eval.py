#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = PACKAGE_ROOT / "evaluation" / "executable"
CASES_DIR = EVAL_ROOT / "cases"
FIXTURES_DIR = EVAL_ROOT / "fixtures"
SCHEMAS_DIR = EVAL_ROOT / "schemas"
PACKAGE_VERSION = "4.1.0"
RUNTIME_REPORT_DIRS = {"reports", ".cpt-eval-runs", ".cpt-eval-live"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def run_process(
    args: list[str] | str,
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    shell: bool = False,
    timeout: float = 120,
) -> subprocess.CompletedProcess[str]:
    if isinstance(args, list) and args and not shell:
        executable = str(args[0])
        if not Path(executable).is_absolute() and not any(
            separator in executable for separator in ("/", "\\")
        ):
            search_path = (env or os.environ).get("PATH")
            resolved = shutil.which(executable, path=search_path)
            if resolved:
                args = [resolved, *args[1:]]
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        shell=shell,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )


def git_changed_paths(workspace: Path) -> list[str]:
    result = run_process(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=workspace)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    paths: list[str] = []
    data = result.stdout
    for record in data.split("\0"):
        if not record:
            continue
        path = record[3:] if len(record) >= 4 else record
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(Path(path).as_posix())
    return sorted(set(paths))


def match_any(path: str, patterns: Iterable[str]) -> bool:
    value = normalized_trace_path(path)
    for pattern in patterns:
        normalized = normalized_trace_path(pattern)
        if normalized in {"*", "**", "**/*", "."}:
            return True
        if fnmatch.fnmatch(value, normalized):
            return True
        if normalized.endswith("/**"):
            prefix = normalized[:-3].rstrip("/")
            if value == prefix or value.startswith(prefix + "/"):
                return True
    return False


def normalized_trace_path(raw: str, workspace: Path | None = None) -> str:
    path = Path(str(raw))
    if workspace is not None and path.is_absolute():
        try:
            path = path.resolve().relative_to(workspace.resolve())
        except ValueError:
            pass
    value = path.as_posix()
    while value.startswith("./"):
        value = value[2:]
    return value


def with_live_overrides(case: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(case)
    result["budgets"] = {**case["budgets"], **case.get("live_budgets", {})}

    def merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
        merged = copy.deepcopy(base)
        for key, value in overlay.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = merge(merged[key], value)
            else:
                merged[key] = copy.deepcopy(value)
        return merged

    result["expectations"] = merge(
        case.get("expectations", {}), case.get("live_expectations", {})
    )
    return result


_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def deep_format(value: Any, ctx: dict[str, Any]) -> Any:
    """Substitute only simple CPT placeholders, never arbitrary code braces.

    Evaluation actions may contain JSX, JSON, templates, or other source text with
    literal braces. ``str.format_map`` interprets those braces as format fields
    and can corrupt source payloads. CPT placeholders are intentionally limited
    to ``{identifier}``, so replacement is explicit and lossless.
    """
    if isinstance(value, str):
        return _PLACEHOLDER_RE.sub(
            lambda match: str(ctx.get(match.group(1), match.group(0))), value
        )
    if isinstance(value, list):
        return [deep_format(item, ctx) for item in value]
    if isinstance(value, dict):
        return {key: deep_format(item, ctx) for key, item in value.items()}
    return value


@dataclass
class TraceRecorder:
    events: list[dict[str, Any]] = field(default_factory=list)
    seq: int = 0

    def emit(self, event_type: str, **payload: Any) -> None:
        self.seq += 1
        event = {"seq": self.seq, "type": event_type, "timestamp": utc_now(), **payload}
        self.events.append(event)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for event in self.events:
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def counts(self) -> dict[str, int]:
        commands = sum(1 for e in self.events if e["type"] == "command")
        writes = sum(1 for e in self.events if e["type"] == "file_write")
        reads = sum(1 for e in self.events if e["type"] == "file_read")
        approvals = sum(1 for e in self.events if e["type"] == "approval")
        workers = sum(1 for e in self.events if e["type"].startswith("worker_"))
        return {
            "tool_events": commands + writes + reads + workers,
            "commands": commands,
            "writes": writes,
            "reads": reads,
            "approvals": approvals,
            "worker_events": workers,
        }


def load_case(case_id: str) -> dict[str, Any]:
    path = CASES_DIR / f"{case_id}.json"
    if not path.exists():
        raise RuntimeError(f"Unknown evaluation case: {case_id}")
    return read_json(path)


def all_cases() -> list[dict[str, Any]]:
    return [read_json(path) for path in sorted(CASES_DIR.glob("*.json"))]


def cases_for_suite(suite: str) -> list[dict[str, Any]]:
    return [case for case in all_cases() if suite in case.get("suites", [])]


def validate_json(instance: Any, schema_path: Path) -> list[str]:
    schema = read_json(schema_path)
    validator = Draft202012Validator(schema)
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def init_git_repo(workspace: Path) -> None:
    if not (workspace / ".git").exists():
        result = run_process(["git", "init", "-q"], cwd=workspace)
        if result.returncode:
            raise RuntimeError(result.stderr)
    for key, value in [("user.email", "cpt-eval@example.invalid"), ("user.name", "CPT Eval")]:
        result = run_process(["git", "config", key, value], cwd=workspace)
        if result.returncode:
            raise RuntimeError(result.stderr)
    run_process(["git", "add", "-A"], cwd=workspace)
    result = run_process(["git", "commit", "-qm", "fixture baseline"], cwd=workspace)
    if result.returncode and "nothing to commit" not in (result.stdout + result.stderr):
        raise RuntimeError(result.stderr)


def prepare_workspace(
    case: dict[str, Any],
    run_root: Path,
    *,
    install_extensions: bool = True,
    codex_home_override: Path | None = None,
) -> tuple[Path, dict[str, str]]:
    fixture = FIXTURES_DIR / case["fixture"] / "repo"
    if not fixture.exists():
        raise RuntimeError(f"Missing fixture: {case['fixture']}")
    workspace = run_root / "workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(fixture, workspace)
    init_git_repo(workspace)

    home = run_root / "home"
    codex_home = codex_home_override or (home / ".codex")
    home.mkdir(parents=True, exist_ok=True)
    codex_home.mkdir(parents=True, exist_ok=True)
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("CODEX_")
    }
    env.update({"HOME": str(home), "CODEX_HOME": str(codex_home), "PYTHONDONTWRITEBYTECODE": "1"})
    interpreter_dir = str(Path(sys.executable).resolve().parent)
    env["PATH"] = interpreter_dir + os.pathsep + env.get("PATH", "")
    if os.name == "nt" and shutil.which("grep", path=env.get("PATH")) is None:
        git = shutil.which("git", path=env.get("PATH"))
        if git:
            git_usr_bin = Path(git).resolve().parent.parent / "usr" / "bin"
            if (git_usr_bin / "grep.exe").exists():
                env["PATH"] = str(git_usr_bin) + os.pathsep + env["PATH"]

    install = run_process(
        [sys.executable, str(PACKAGE_ROOT / "tools" / "cpt_dist.py"), "install", "--project", str(workspace), "--mode", "local", "--enforcement-mode", "off"],
        cwd=PACKAGE_ROOT,
        env=env,
        timeout=180,
    )
    if install.returncode:
        raise RuntimeError(f"CPT install failed: {install.stderr or install.stdout}")

    for plugin in (case.get("activation", {}).get("plugins", []) if install_extensions else []):
        result = run_process(
            [sys.executable, str(PACKAGE_ROOT / "tools" / "cpt_dist.py"), "pack-add", "--name", plugin, "--scope", "personal"],
            cwd=PACKAGE_ROOT,
            env=env,
            timeout=120,
        )
        if result.returncode:
            raise RuntimeError(f"Pack install failed for {plugin}: {result.stderr or result.stdout}")

    if install_extensions and case.get("activation", {}).get("workers"):
        result = run_process(
            [sys.executable, str(PACKAGE_ROOT / "tools" / "cpt_dist.py"), "workers-install", "--scope", "personal"],
            cwd=PACKAGE_ROOT,
            env=env,
            timeout=120,
        )
        if result.returncode:
            raise RuntimeError(f"Worker pack install failed: {result.stderr or result.stdout}")

    return workspace, env


def command_preview(args: list[str] | str) -> str:
    if isinstance(args, str):
        return args
    return " ".join(str(item) for item in args)


def execute_reference_actions(
    case: dict[str, Any], workspace: Path, env: dict[str, str], recorder: TraceRecorder
) -> tuple[dict[str, Any], dict[str, Any]]:
    ctx: dict[str, Any] = {
        "workspace": str(workspace),
        "package_root": str(PACKAGE_ROOT),
        "runtime": str(workspace / ".cpt" / "bin" / "cpt_runtime.py"),
        "python": sys.executable,
        "case_id": case["id"],
    }

    for raw_action in case.get("reference_actions", []):
        action = deep_format(copy.deepcopy(raw_action), ctx)
        kind = action["type"]
        if kind == "approval":
            recorder.emit("approval", scope=action.get("scope", "unspecified"), approved=bool(action.get("approved", True)))
            continue
        if kind == "read":
            path = Path(action["path"])
            if not path.is_absolute():
                path = workspace / path
            text = path.read_text(encoding="utf-8")
            try:
                rel = path.resolve().relative_to(workspace.resolve()).as_posix()
            except ValueError:
                rel = str(path)
            recorder.emit("file_read", path=rel, bytes=len(text.encode("utf-8")))
            if action.get("capture"):
                ctx[action["capture"]] = text
            continue
        if kind == "write":
            path = Path(action["path"])
            if not path.is_absolute():
                path = workspace / path
            path.parent.mkdir(parents=True, exist_ok=True)
            if "replace" in action:
                old = path.read_text(encoding="utf-8") if path.exists() else ""
                spec = action["replace"]
                if spec["old"] not in old:
                    raise RuntimeError(f"Replacement text not found in {path}: {spec['old']!r}")
                text = old.replace(spec["old"], spec["new"], int(spec.get("count", -1)))
            elif action.get("append"):
                text = (path.read_text(encoding="utf-8") if path.exists() else "") + action.get("content", "")
            else:
                text = action.get("content", "")
            path.write_text(text, encoding="utf-8")
            try:
                rel = path.resolve().relative_to(workspace.resolve()).as_posix()
            except ValueError:
                rel = str(path)
            recorder.emit("file_write", path=rel, bytes=len(text.encode("utf-8")))
            continue
        if kind == "yaml_set":
            path = Path(action["path"])
            if not path.is_absolute():
                path = workspace / path
            data = read_yaml(path)
            parts = action["key"].split(".")
            target = data
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = action.get("value")
            write_yaml(path, data)
            rel = path.resolve().relative_to(workspace.resolve()).as_posix()
            recorder.emit("file_write", path=rel, bytes=path.stat().st_size)
            continue
        if kind in {"runtime", "command"}:
            if kind == "runtime":
                args = [sys.executable, ctx["runtime"], "--root", str(workspace), *action.get("args", [])]
                shell = False
            else:
                args = action["command"]
                shell = bool(action.get("shell", isinstance(args, str)))
            preview = command_preview(args)
            recorder.emit(
                "command",
                command=preview,
                cwd=action.get("cwd", "."),
                declared_reads=action.get("reads", []),
                declared_writes=action.get("writes", []),
            )
            proc = run_process(
                args,
                cwd=Path(action.get("cwd", workspace)),
                env=env,
                shell=shell,
                timeout=float(action.get("timeout", 180)),
            )
            recorder.emit(
                "command_result",
                command=preview,
                exit_code=proc.returncode,
                stdout_preview=proc.stdout[-2000:],
                stderr_preview=proc.stderr[-2000:],
            )
            expected_failure = bool(action.get("expect_failure"))
            if (proc.returncode != 0) != expected_failure:
                raise RuntimeError(
                    f"Command {'unexpectedly failed' if proc.returncode else 'unexpectedly succeeded'}: {preview}\n"
                    f"stdout={proc.stdout}\nstderr={proc.stderr}"
                )
            stdout = proc.stdout.strip()
            if action.get("capture"):
                ctx[action["capture"]] = stdout
            if action.get("capture_json"):
                obj = json.loads(stdout)
                ctx[action["capture_json"]] = obj
                for name, field_name in action.get("capture_fields", {}).items():
                    ctx[name] = obj[field_name]
            for rel in action.get("reads", []):
                recorder.emit("file_read", path=rel, source="declared_command_scope")
            for rel in action.get("writes", []):
                recorder.emit("file_write", path=rel, source="declared_command_scope")
            continue
        if kind == "sleep":
            time.sleep(float(action.get("seconds", 0)))
            continue
        if kind == "set_context":
            ctx[action["name"]] = action.get("value")
            continue
        raise RuntimeError(f"Unknown reference action type: {kind}")

    output = deep_format(copy.deepcopy(case["reference_output"]), ctx)
    usage = case.get("reference_usage", {})
    if not usage:
        usage = {
            "input_tokens": max(1, len(case["task_prompt"]) // 4),
            "output_tokens": max(1, len(json.dumps(output, ensure_ascii=False)) // 4),
        }
    recorder.emit("usage", **usage)
    recorder.emit("final", output=output)
    return output, ctx


def codex_item_paths(item: dict[str, Any], workspace: Path | None = None) -> list[str]:
    paths: list[str] = []
    for key in ("path", "file"):
        if item.get(key):
            paths.append(str(item[key]))
    for raw in item.get("paths", []) or []:
        if raw:
            paths.append(str(raw))
    for change in item.get("changes", []) or []:
        if isinstance(change, str):
            paths.append(change)
            continue
        if isinstance(change, dict):
            value = change.get("path") or change.get("file")
            if value:
                paths.append(str(value))
    return sorted({normalized_trace_path(path, workspace) for path in paths if path})


def normalize_codex_jsonl(
    lines: str, recorder: TraceRecorder, workspace: Path | None = None
) -> None:
    command_by_item: dict[str, str] = {}
    for line in lines.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            recorder.emit("raw", text=line[:4000])
            continue
        event_type = event.get("type", "unknown")
        if event_type == "item.started":
            item = event.get("item", {})
            item_type = item.get("type")
            if item_type == "command_execution":
                command = item.get("command", "")
                command_by_item[item.get("id", "")] = command
                recorder.emit("command", command=command, source="codex_jsonl")
            elif item_type in {"file_change", "file_changes"}:
                # Count the completed change once; start and completion events
                # describe one host operation.
                recorder.emit("codex_item", item_type=item_type, phase="started")
            else:
                recorder.emit("codex_item", item_type=item_type, phase="started")
        elif event_type == "item.completed":
            item = event.get("item", {})
            item_type = item.get("type")
            if item_type == "command_execution":
                recorder.emit(
                    "command_result",
                    command=command_by_item.get(item.get("id", ""), item.get("command", "")),
                    exit_code=item.get("exit_code", 0 if item.get("status") == "completed" else 1),
                    source="codex_jsonl",
                )
            elif item_type in {"file_change", "file_changes"}:
                for path in codex_item_paths(item, workspace):
                    recorder.emit("file_write", path=path, source="codex_jsonl")
            elif item_type == "agent_message":
                recorder.emit("agent_message", text=item.get("text", "")[:8000])
            else:
                recorder.emit("codex_item", item_type=item_type, phase="completed")
        elif event_type == "turn.completed":
            usage = event.get("usage", {})
            recorder.emit(
                "usage",
                input_tokens=int(usage.get("input_tokens", 0)),
                cached_input_tokens=int(usage.get("cached_input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
                reasoning_output_tokens=int(usage.get("reasoning_output_tokens", 0)),
            )
        elif event_type in {"turn.failed", "error"}:
            recorder.emit("error", payload=event)
        else:
            recorder.emit("codex_event", codex_event_type=event_type)


def augment_trace_from_structured_output(
    output: dict[str, Any], recorder: TraceRecorder, workspace: Path | None = None
) -> None:
    """Add bounded model-reported file activity when the host trace lacks it.

    ``codex exec --json`` reliably exposes commands, usage, and file-change items,
    but some clients or tool implementations may not emit explicit file-read
    events. The required structured output includes ``files_read`` and
    ``files_changed``. We preserve those as *reported* evidence rather than
    pretending they are host-observed events. Filesystem grading still checks
    actual Git changes independently.
    """
    observed_reads = {
        normalized_trace_path(str(event.get("path")), workspace)
        for event in recorder.events
        if event.get("type") == "file_read" and event.get("path")
    }
    observed_writes = {
        normalized_trace_path(str(event.get("path")), workspace)
        for event in recorder.events
        if event.get("type") == "file_write" and event.get("path")
    }
    for raw in output.get("files_read", []) or []:
        path = normalized_trace_path(str(raw), workspace)
        if path and path not in observed_reads:
            recorder.emit(
                "file_read", path=path, source="structured_output_claim", evidence_level="reported"
            )
    for raw in output.get("files_changed", []) or []:
        path = normalized_trace_path(str(raw), workspace)
        if path and path not in observed_writes:
            recorder.emit(
                "file_write", path=path, source="structured_output_claim", evidence_level="reported"
            )


def build_live_prompt(case: dict[str, Any]) -> str:
    constraints = case.get("live_constraints", [])
    lines = [
        "You are running a Codex Product Operating System evaluation in an isolated fixture repository.",
        "Follow the repository AGENTS.md and CPT runtime. Do not weaken policies or edit evaluation assets.",
        "Return only the JSON object required by the provided output schema.",
        "",
        "Task:",
        case["task_prompt"],
        "",
        "Evaluation constraints:",
    ]
    lines.extend(f"- {item}" for item in constraints)
    return "\n".join(lines) + "\n"


def run_live_case(
    case: dict[str, Any], run_root: Path, *, model: str | None = None, effort: str | None = None
) -> tuple[str, dict[str, Any] | None, Path | None, TraceRecorder, dict[str, Any]]:
    recorder = TraceRecorder()
    workspace: Path | None = None
    temporary_codex_home: Path | None = None
    temporary_auth_file: Path | None = None
    auth_source_raw = os.environ.get("CPT_EVAL_CODEX_AUTH_FILE")
    try:
        if auth_source_raw:
            auth_source = Path(auth_source_raw).expanduser().resolve()
            if not auth_source.is_file():
                return "FAIL", None, None, recorder, {"reason": "CPT_EVAL_CODEX_AUTH_FILE is not a file"}
            temporary_codex_home = Path(tempfile.mkdtemp(prefix="cpt-eval-codex-home-"))
            temporary_auth_file = temporary_codex_home / "auth.json"
            shutil.copy2(auth_source, temporary_auth_file)

        workspace, env = prepare_workspace(
            case, run_root, codex_home_override=temporary_codex_home
        )
        codex = shutil.which("codex")
        if not codex:
            return "SKIPPED", None, workspace, recorder, {"reason": "Codex CLI not found"}
        marketplace_add = run_process(
            [
                codex,
                "plugin",
                "marketplace",
                "add",
                str(PACKAGE_ROOT),
                "--json",
            ],
            cwd=workspace,
            env=env,
            timeout=120,
        )
        if marketplace_add.returncode:
            recorder.emit(
                "error",
                payload={
                    "reason": "Codex local marketplace activation failed",
                    "exit_code": marketplace_add.returncode,
                    "stderr": marketplace_add.stderr[-4000:],
                },
            )
            return "FAIL", None, workspace, recorder, {
                "reason": "Codex local marketplace activation failed",
                "exit_code": marketplace_add.returncode,
            }
        plugins = ["cpt-core", *case.get("activation", {}).get("plugins", [])]
        for plugin in dict.fromkeys(plugins):
            install_plugin = run_process(
                [codex, "plugin", "add", f"{plugin}@product-os", "--json"],
                cwd=workspace,
                env=env,
                timeout=120,
            )
            if install_plugin.returncode:
                recorder.emit(
                    "error",
                    payload={
                        "reason": f"Codex plugin activation failed for {plugin}",
                        "exit_code": install_plugin.returncode,
                        "stderr": install_plugin.stderr[-4000:],
                    },
                )
                return "FAIL", None, workspace, recorder, {
                    "reason": f"Codex plugin activation failed for {plugin}",
                    "exit_code": install_plugin.returncode,
                }
        output_path = run_root / "output.json"
        schema_path = SCHEMAS_DIR / "task-result.schema.json"
        prompt = build_live_prompt(case)
        command = [
            codex,
            "exec",
            "--json",
            "--ephemeral",
            "--approve-for-me",
            "--output-schema",
            str(schema_path),
            "-o",
            str(output_path),
        ]
        if model:
            command.extend(["--model", model])
        if effort:
            command.extend(["-c", f'model_reasoning_effort="{effort}"'])
        command.append(prompt)
        started = time.monotonic()
        # Keep the process timeout separate from the acceptance budget. Plugin
        # startup and structured-output finalization can outlive the case's
        # graded wall budget; the grader still fails an over-budget result.
        process_timeout = max(
            240.0, float(case["budgets"]["max_wall_seconds"]) + 60
        )
        try:
            proc = run_process(
                command,
                cwd=workspace,
                env=env,
                timeout=process_timeout,
            )
        except subprocess.TimeoutExpired as exc:
            elapsed = time.monotonic() - started
            partial_stdout = exc.stdout or ""
            if isinstance(partial_stdout, bytes):
                partial_stdout = partial_stdout.decode("utf-8", errors="replace")
            if os.environ.get("CPT_EVAL_KEEP_RAW_TRACE") == "1":
                (run_root / "codex-events.jsonl").write_text(
                    partial_stdout, encoding="utf-8"
                )
            normalize_codex_jsonl(partial_stdout, recorder, workspace)
            recorder.emit(
                "error",
                payload={"reason": "codex exec timed out", "timeout": process_timeout},
            )
            return "FAIL", None, workspace, recorder, {
                "reason": f"codex exec timed out after {process_timeout:.1f} seconds",
                "elapsed_seconds": elapsed,
            }
        elapsed = time.monotonic() - started
        if os.environ.get("CPT_EVAL_KEEP_RAW_TRACE") == "1":
            (run_root / "codex-events.jsonl").write_text(proc.stdout, encoding="utf-8")
        normalize_codex_jsonl(proc.stdout, recorder, workspace)
        if proc.returncode:
            recorder.emit("error", payload={"exit_code": proc.returncode, "stderr": proc.stderr[-8000:]})
            return "FAIL", None, workspace, recorder, {"reason": "codex exec returned non-zero", "exit_code": proc.returncode, "elapsed_seconds": elapsed}
        if not output_path.exists():
            return "FAIL", None, workspace, recorder, {"reason": "Codex did not write output-last-message file", "elapsed_seconds": elapsed}
        try:
            output = read_json(output_path)
        except Exception as exc:
            return "FAIL", None, workspace, recorder, {"reason": f"Invalid structured output: {exc}", "elapsed_seconds": elapsed}
        augment_trace_from_structured_output(output, recorder, workspace)
        recorder.emit("final", output=output)
        return "PASS", output, workspace, recorder, {"elapsed_seconds": elapsed}
    finally:
        if temporary_auth_file and temporary_auth_file.exists():
            temporary_auth_file.unlink()
        if temporary_codex_home:
            shutil.rmtree(temporary_codex_home, ignore_errors=True)


def collect_paths_from_trace(events: list[dict[str, Any]], event_type: str) -> list[str]:
    return sorted({normalized_trace_path(str(event.get("path"))) for event in events if event.get("type") == event_type and event.get("path")})


def collect_commands(events: list[dict[str, Any]]) -> list[str]:
    return [str(event.get("command", "")) for event in events if event.get("type") == "command"]


def usage_totals(events: list[dict[str, Any]]) -> dict[str, int]:
    totals = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_output_tokens": 0}
    for event in events:
        if event.get("type") != "usage":
            continue
        for key in totals:
            totals[key] += int(event.get(key, 0) or 0)
    return totals


def runtime_check(workspace: Path, check: dict[str, Any], ctx: dict[str, Any]) -> tuple[bool, str]:
    check = deep_format(check, ctx)
    kind = check.get("type")
    if kind == "git_clean":
        changed = git_changed_paths(workspace)
        return (not changed, f"git changed paths: {changed}")
    if kind == "current_field":
        data = read_yaml(workspace / ".cpt" / "current.yaml")
        actual = data.get(check["field"])
        return (actual == check.get("equals"), f"current.{check['field']}={actual!r}")
    if kind == "task_status":
        task_id = check["task"]
        if "{" in task_id:
            candidates = sorted((workspace / ".cpt" / "tasks").glob("TKT-*.yaml"))
            if len(candidates) != 1:
                return False, f"cannot infer one task id: {[item.stem for item in candidates]}"
            task_id = candidates[0].stem
        data = read_yaml(workspace / ".cpt" / "tasks" / f"{task_id}.yaml")
        actual = data.get("status")
        return (actual == check["equals"], f"task {task_id} status={actual!r}")
    if kind == "micro_status":
        micro_id = check["micro"]
        if "{" in micro_id:
            candidates = sorted((workspace / ".cpt" / "micro-changes").glob("*.yaml"))
            if len(candidates) != 1:
                return False, f"cannot infer one micro id: {[item.stem for item in candidates]}"
            micro_id = candidates[0].stem
        data = read_yaml(workspace / ".cpt" / "micro-changes" / f"{micro_id}.yaml")
        actual = data.get("status")
        return (actual == check["equals"], f"micro {micro_id} status={actual!r}")
    if kind == "file_exists":
        exists = (workspace / check["path"]).exists()
        return (exists == bool(check.get("equals", True)), f"file {check['path']} exists={exists}")
    if kind == "file_contains":
        path = workspace / check["path"]
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        contains = check["text"] in text
        return (contains == bool(check.get("equals", True)), f"file {check['path']} contains={contains}")
    if kind == "knowledge_freshness":
        artifact_id = check["artifact"]
        data = read_yaml(workspace / ".cpt" / "knowledge" / "artifacts" / f"{artifact_id}.yaml")
        actual = data.get("freshness")
        return (actual == check["equals"], f"knowledge {artifact_id} freshness={actual!r}")
    if kind == "orchestration_state":
        run_id = check["run"]
        if "{" in run_id:
            candidates = sorted((workspace / ".cpt" / "orchestrations").glob("ORC-*.yaml"))
            if len(candidates) != 1:
                return False, f"cannot infer one orchestration id: {[item.stem for item in candidates]}"
            run_id = candidates[0].stem
        data = read_yaml(workspace / ".cpt" / "orchestrations" / f"{run_id}.yaml")
        actual = data.get("status", data.get("state"))
        return (actual == check["equals"], f"orchestration {run_id} status={actual!r}")
    if kind == "checkpoint_exists":
        checkpoint_id = check["checkpoint"]
        exists = (workspace / ".cpt" / "checkpoints" / f"{checkpoint_id}.yaml").exists()
        return (exists, f"checkpoint {checkpoint_id} exists={exists}")
    raise RuntimeError(f"Unknown runtime check: {kind}")


def grade_case(
    case: dict[str, Any],
    output: dict[str, Any] | None,
    recorder: TraceRecorder,
    workspace: Path | None,
    ctx: dict[str, Any],
    *,
    elapsed_seconds: float,
    backend_status: str = "PASS",
    backend_reason: str | None = None,
) -> dict[str, Any]:
    if backend_status == "SKIPPED":
        return {
            "id": case["id"], "status": "SKIPPED", "score": 0, "critical_failures": [],
            "warnings": [backend_reason or "backend skipped"], "checks": [], "metrics": {},
        }
    critical: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    if output is None:
        critical.append(backend_reason or "missing output")
        output = {}
    schema_errors = validate_json(output, SCHEMAS_DIR / "task-result.schema.json")
    if schema_errors:
        critical.extend(f"output schema: {item}" for item in schema_errors)
    checks.append({"name": "output_schema", "passed": not schema_errors, "details": schema_errors})
    for field_name in ("selected_roles", "selected_skills", "files_read", "files_changed"):
        values = output.get(field_name, [])
        unique = not isinstance(values, list) or len(values) == len(
            {json.dumps(item, sort_keys=True, ensure_ascii=False) for item in values}
        )
        checks.append({"name": f"unique_items:{field_name}", "passed": unique})
        if not unique:
            critical.append(f"duplicate values in output field: {field_name}")

    expected = case.get("expectations", {})
    output_text = json.dumps(output, ensure_ascii=False).lower()
    for term in expected.get("required_output_terms", []):
        ok = term.lower() in output_text
        checks.append({"name": f"required_output_term:{term}", "passed": ok})
        if not ok:
            critical.append(f"missing required output term: {term}")
    for term in expected.get("forbidden_output_terms", []):
        ok = term.lower() not in output_text
        checks.append({"name": f"forbidden_output_term:{term}", "passed": ok})
        if not ok:
            critical.append(f"forbidden output term present: {term}")
    if expected.get("status_in"):
        ok = output.get("status") in expected["status_in"]
        checks.append({"name": "output_status", "passed": ok, "actual": output.get("status")})
        if not ok:
            critical.append(f"unexpected output status: {output.get('status')}")
    for role in expected.get("required_roles", []):
        ok = role in output.get("selected_roles", [])
        checks.append({"name": f"required_role:{role}", "passed": ok})
        if not ok:
            critical.append(f"missing required role: {role}")
    any_roles = expected.get("required_any_roles", [])
    if any_roles:
        selected_roles = output.get("selected_roles", [])
        normalized_selected = {str(item).lower().replace("_", " ") for item in selected_roles}
        ok = any(str(role).lower().replace("_", " ") in normalized_selected for role in any_roles)
        checks.append({"name": "required_any_role", "passed": ok, "allowed": any_roles})
        if not ok:
            critical.append(f"none of the accepted roles selected: {any_roles}")
    for skill in expected.get("required_skills", []):
        selected_skills = output.get("selected_skills", [])
        ok = skill in selected_skills or any(
            str(item).endswith(":" + skill) for item in selected_skills
        )
        checks.append({"name": f"required_skill:{skill}", "passed": ok})
        if not ok:
            critical.append(f"missing required skill: {skill}")

    read_paths = collect_paths_from_trace(recorder.events, "file_read")
    write_paths = collect_paths_from_trace(recorder.events, "file_write")
    reported_events = [
        event for event in recorder.events
        if event.get("source") == "structured_output_claim"
    ]
    if reported_events:
        warnings.append(
            "Some file activity is based on structured model reporting rather than explicit host trace events; "
            "filesystem writes are corroborated separately through Git state."
        )
    if any(
        event.get("type") == "observability" and event.get("level") == "reduced"
        for event in recorder.events
    ):
        warnings.append(
            "The host did not provide a complete JSONL tool trace. Command and approval behavior is not certified "
            "by this result; only structured output, reported file activity, Git state, and runtime assertions are graded."
        )
    commands = collect_commands(recorder.events)
    trace_policy = expected.get("trace", {})
    for path in read_paths:
        if trace_policy.get("forbidden_reads") and match_any(path, trace_policy["forbidden_reads"]):
            critical.append(f"forbidden read: {path}")
        if "allowed_reads" in trace_policy:
            allowed = trace_policy.get("allowed_reads") or []
            if not allowed or not match_any(path, allowed):
                critical.append(f"read outside allowed scope: {path}")
    for path in write_paths:
        if trace_policy.get("forbidden_writes") and match_any(path, trace_policy["forbidden_writes"]):
            critical.append(f"forbidden trace write: {path}")
        if "allowed_writes" in trace_policy:
            allowed = trace_policy.get("allowed_writes") or []
            if not allowed or not match_any(path, allowed):
                critical.append(f"trace write outside allowed scope: {path}")
    for pattern in trace_policy.get("required_commands", []):
        ok = any(re.search(pattern, command) for command in commands)
        checks.append({"name": f"required_command:{pattern}", "passed": ok})
        if not ok:
            critical.append(f"required command missing: {pattern}")
    for pattern in trace_policy.get("forbidden_commands", []):
        bad = [command for command in commands if re.search(pattern, command)]
        checks.append({"name": f"forbidden_command:{pattern}", "passed": not bad, "matches": bad})
        if bad:
            critical.append(f"forbidden command matched {pattern}: {bad[0]}")

    changed: list[str] = []
    if workspace is not None:
        changed = git_changed_paths(workspace)
        fs = expected.get("filesystem", {})
        for path in changed:
            if fs.get("forbidden_changes") and match_any(path, fs["forbidden_changes"]):
                critical.append(f"forbidden filesystem change: {path}")
            if "allowed_changes" in fs:
                allowed = fs.get("allowed_changes") or []
                if not allowed or not match_any(path, allowed):
                    critical.append(f"filesystem change outside allowed scope: {path}")
        for pattern in fs.get("required_changes", []):
            ok = any(match_any(path, [pattern]) for path in changed)
            checks.append({"name": f"required_change:{pattern}", "passed": ok})
            if not ok:
                critical.append(f"required filesystem change missing: {pattern}")
        for runtime_assertion in expected.get("runtime", []):
            try:
                ok, detail = runtime_check(workspace, runtime_assertion, ctx)
            except Exception as exc:
                ok, detail = False, f"runtime check error: {exc}"
            checks.append({"name": f"runtime:{runtime_assertion.get('type')}", "passed": ok, "detail": detail})
            if not ok:
                critical.append(detail)

    counts = recorder.counts()
    usage = usage_totals(recorder.events)
    metrics = {**counts, **usage, "wall_seconds": round(elapsed_seconds, 3), "changed_files": len(changed)}
    budgets = case["budgets"]
    budget_pairs = [
        ("tool_events", "max_tool_events"), ("commands", "max_commands"), ("writes", "max_writes"),
        ("wall_seconds", "max_wall_seconds"), ("input_tokens", "max_input_tokens"), ("output_tokens", "max_output_tokens"),
    ]
    for metric, limit_key in budget_pairs:
        actual = metrics.get(metric, 0)
        limit = budgets[limit_key]
        ok = actual <= limit
        checks.append({"name": f"budget:{metric}", "passed": ok, "actual": actual, "limit": limit})
        if not ok:
            critical.append(f"budget exceeded for {metric}: {actual} > {limit}")

    if backend_status == "FAIL":
        critical.append(backend_reason or "backend failure")

    status = "FAIL" if critical else "PASS"
    score = 100.0 if not critical else max(0.0, 100.0 - 15.0 * len(set(critical)))
    if warnings and not critical:
        score = min(score, 95.0)
    return {
        "id": case["id"],
        "title": case["title"],
        "status": status,
        "score": round(score, 2),
        "critical_failures": sorted(set(critical)),
        "warnings": warnings,
        "checks": checks,
        "metrics": metrics,
        "read_paths": read_paths,
        "write_paths": write_paths,
        "changed_paths": changed,
        "output": output,
    }


def run_reference_case(case: dict[str, Any], report_root: Path) -> dict[str, Any]:
    run_root = report_root / "runs" / case["id"]
    if run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True)
    started = time.monotonic()
    recorder = TraceRecorder()
    workspace: Path | None = None
    ctx: dict[str, Any] = {}
    try:
        workspace, env = prepare_workspace(case, run_root, install_extensions=False)
        output, ctx = execute_reference_actions(case, workspace, env, recorder)
        backend_status, reason = "PASS", None
    except Exception as exc:
        output = None
        backend_status, reason = "FAIL", str(exc)
        recorder.emit("error", payload={"reason": reason})
    elapsed = time.monotonic() - started
    recorder.write(run_root / "trace.jsonl")
    if output is not None:
        write_json(run_root / "output.json", output)
    report = grade_case(case, output, recorder, workspace, ctx, elapsed_seconds=elapsed, backend_status=backend_status, backend_reason=reason)
    write_json(run_root / "case-report.json", report)
    return report


def run_live_case_and_grade(case: dict[str, Any], report_root: Path, model: str | None, effort: str | None) -> dict[str, Any]:
    case = with_live_overrides(case)
    run_root = report_root / "runs" / case["id"]
    if run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True)
    started = time.monotonic()
    status, output, workspace, recorder, meta = run_live_case(case, run_root, model=model, effort=effort)
    elapsed = meta.get("elapsed_seconds", time.monotonic() - started)
    recorder.write(run_root / "trace.jsonl")
    if output is not None:
        write_json(run_root / "output.json", output)
    report = grade_case(case, output, recorder, workspace, {}, elapsed_seconds=elapsed, backend_status=status, backend_reason=meta.get("reason"))
    write_json(run_root / "case-report.json", report)
    return report


def suite_scorecard(suite: str, backend: str, reports: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for report in reports if report["status"] == "PASS")
    failed = sum(1 for report in reports if report["status"] == "FAIL")
    skipped = sum(1 for report in reports if report["status"] == "SKIPPED")
    status = "FAIL" if failed else ("SKIPPED" if skipped == len(reports) else ("MIXED" if skipped else "PASS"))
    scored = [r["score"] for r in reports if r["status"] != "SKIPPED"]
    average = round(sum(scored) / len(scored), 2) if scored else 0.0
    total_keys = ["tool_events", "commands", "writes", "reads", "approvals", "worker_events", "input_tokens", "output_tokens", "changed_files"]
    totals = {key: sum(int(r.get("metrics", {}).get(key, 0)) for r in reports) for key in total_keys}
    totals["wall_seconds"] = round(sum(float(r.get("metrics", {}).get("wall_seconds", 0)) for r in reports), 3)
    return {
        "schema_version": "cpt-eval-scorecard-v1",
        "package_version": PACKAGE_VERSION,
        "generated_at": utc_now(),
        "suite": suite,
        "backend": backend,
        "status": status,
        "case_count": len(reports),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "average_score": average,
        "cases": reports,
        "totals": totals,
    }


def run_suite(args: argparse.Namespace) -> int:
    selected = cases_for_suite(args.suite)
    if args.case:
        wanted = set(args.case)
        selected = [case for case in selected if case["id"] in wanted]
        missing = wanted - {case["id"] for case in selected}
        if missing:
            raise RuntimeError(f"Cases not in suite {args.suite}: {sorted(missing)}")
    report_root = Path(args.report_dir).resolve()
    report_root.mkdir(parents=True, exist_ok=True)
    reports = []

    # Run multi-case suites in isolated interpreters. Installer state, temporary
    # HOME/CODEX_HOME directories, and long-lived Python globals must not leak
    # across evaluation cases.
    if not getattr(args, "in_process", False) and len(selected) > 1:
        child_root = report_root / ".isolated-cases"
        child_root.mkdir(parents=True, exist_ok=True)
        for case in selected:
            print(f"[CPT-EVAL] {args.backend}: {case['id']}", flush=True)
            per_case = child_root / case["id"]
            if per_case.exists():
                shutil.rmtree(per_case)
            command = [
                sys.executable,
                str(Path(__file__).resolve()),
                "run",
                "--suite", args.suite,
                "--backend", args.backend,
                "--report-dir", str(per_case),
                "--case", case["id"],
                "--in-process",
            ]
            if args.model:
                command += ["--model", args.model]
            if args.effort:
                command += ["--effort", args.effort]
            timeout = max(180, int(case.get("budgets", {}).get("max_wall_seconds", 30) * 10 + 120))
            proc = run_process(command, cwd=PACKAGE_ROOT, timeout=timeout)
            case_report = per_case / "runs" / case["id"] / "case-report.json"
            if not case_report.exists():
                report = {
                    "id": case["id"], "status": "FAIL", "score": 0.0,
                    "critical_failures": [f"isolated case runner failed ({proc.returncode}): {(proc.stderr or proc.stdout)[-2000:]}"],
                    "warnings": [], "checks": [], "metrics": {}, "read_paths": [], "write_paths": [], "changed_paths": [], "output": None,
                }
            else:
                report = read_json(case_report)
            reports.append(report)
            print(f"  -> {report['status']} score={report['score']}", flush=True)
            if args.fail_fast and report["status"] == "FAIL":
                break
    else:
        for case in selected:
            print(f"[CPT-EVAL] {args.backend}: {case['id']}", flush=True)
            if args.backend == "reference":
                report = run_reference_case(case, report_root)
            else:
                report = run_live_case_and_grade(case, report_root, args.model, args.effort)
            reports.append(report)
            print(f"  -> {report['status']} score={report['score']}", flush=True)
            if args.fail_fast and report["status"] == "FAIL":
                break

    scorecard = suite_scorecard(args.suite, args.backend, reports)
    scorecard_path = report_root / f"{args.suite}-{args.backend}-scorecard.json"
    write_json(scorecard_path, scorecard)
    print(f"SCORECARD: {scorecard_path}")
    print(f"STATUS: {scorecard['status']} ({scorecard['passed']} pass, {scorecard['failed']} fail, {scorecard['skipped']} skipped)")
    return 1 if scorecard["failed"] else 0

def compare_baseline(current_path: Path, baseline_path: Path, output_path: Path | None = None) -> dict[str, Any]:
    current = read_json(current_path)
    baseline = read_json(baseline_path)
    baseline_cases = {item["id"]: item for item in baseline.get("cases", [])}
    current_cases = {item["id"]: item for item in current.get("cases", [])}
    regressions: list[dict[str, Any]] = []
    for case_id, base in baseline_cases.items():
        cur = current_cases.get(case_id)
        if cur is None:
            regressions.append({"case": case_id, "type": "missing_case"})
            continue
        if base.get("status") == "PASS" and cur.get("status") != "PASS":
            regressions.append({"case": case_id, "type": "status", "baseline": base.get("status"), "current": cur.get("status")})
        if float(cur.get("score", 0)) < float(base.get("score", 0)) - 3:
            regressions.append({"case": case_id, "type": "score", "baseline": base.get("score"), "current": cur.get("score")})
        for metric, ratio, absolute in [
            ("input_tokens", 1.25, 250), ("output_tokens", 1.25, 150),
            ("tool_events", 1.25, 3), ("commands", 1.25, 2), ("writes", 1.20, 1),
        ]:
            b = float(base.get("metrics", {}).get(metric, 0))
            c = float(cur.get("metrics", {}).get(metric, 0))
            threshold = max(b * ratio, b + absolute)
            if c > threshold:
                regressions.append({"case": case_id, "type": f"resource:{metric}", "baseline": b, "current": c, "threshold": threshold})
    for case_id in sorted(set(current_cases) - set(baseline_cases)):
        regressions.append({"case": case_id, "type": "unexpected_case"})
    report = {
        "schema_version": "cpt-eval-baseline-comparison-v1",
        "package_version": PACKAGE_VERSION,
        "generated_at": utc_now(),
        "baseline": str(baseline_path),
        "current": str(current_path),
        "status": "PASS" if not regressions else "FAIL",
        "regression_count": len(regressions),
        "regressions": regressions,
    }
    if output_path:
        write_json(output_path, report)
    return report


def mutate_and_check(scorecard_path: Path, output_path: Path) -> dict[str, Any]:
    """Inject known-bad evidence and prove the deterministic graders catch it."""
    scorecard = read_json(scorecard_path)
    if not scorecard.get("cases"):
        raise RuntimeError("Scorecard has no cases")
    source = scorecard["cases"][0]
    case = load_case(source["id"])
    mutations: list[dict[str, Any]] = []

    # 1. Unauthorized write: evaluate the synthetic path against the case's
    # real filesystem policy, rather than merely checking that it is new.
    forbidden_path = "secrets/unauthorized.txt"
    fs = case.get("expectations", {}).get("filesystem", {})
    allowed = fs.get("allowed_changes", [])
    explicitly_forbidden = fs.get("forbidden_changes", [])
    has_allowed_policy = "allowed_changes" in fs
    violates_scope = (
        (has_allowed_policy and (not allowed or not match_any(forbidden_path, allowed)))
        or (bool(explicitly_forbidden) and match_any(forbidden_path, explicitly_forbidden))
    )
    mutations.append(
        {
            "id": "unauthorized_write",
            "detected": bool(violates_scope),
            "evidence": {"path": forbidden_path, "allowed_changes": allowed, "forbidden_changes": explicitly_forbidden},
        }
    )

    # 2. Missing required structured-output field.
    output = copy.deepcopy(source.get("output", {}))
    output.pop("summary", None)
    schema_errors = validate_json(output, SCHEMAS_DIR / "task-result.schema.json")
    mutations.append(
        {"id": "missing_required_output", "detected": bool(schema_errors), "evidence": schema_errors[:3]}
    )

    # 3. Forbidden destructive command: run the case's own command patterns.
    destructive = "git reset --hard"
    forbidden_patterns = case.get("expectations", {}).get("trace", {}).get("forbidden_commands", [])
    matched = [pattern for pattern in forbidden_patterns if re.search(pattern, destructive)]
    mutations.append(
        {
            "id": "forbidden_destructive_command",
            "detected": bool(matched),
            "evidence": {"command": destructive, "matched_patterns": matched},
        }
    )

    # 4. Resource regression: apply the same threshold used by baseline comparison.
    base_metric = float(source.get("metrics", {}).get("tool_events", 0))
    mutated_metric = max(base_metric * 2 + 10, 20)
    threshold = max(base_metric * 1.25, base_metric + 3)
    mutations.append(
        {
            "id": "resource_regression",
            "detected": mutated_metric > threshold,
            "evidence": {"baseline": base_metric, "mutated": mutated_metric, "threshold": threshold},
        }
    )

    report = {
        "schema_version": "cpt-eval-mutation-report-v1",
        "package_version": PACKAGE_VERSION,
        "generated_at": utc_now(),
        "source_case": source["id"],
        "status": "PASS" if all(item["detected"] for item in mutations) else "FAIL",
        "detected": sum(1 for item in mutations if item["detected"]),
        "total": len(mutations),
        "mutations": mutations,
    }
    write_json(output_path, report)
    return report


def prepare_external(case: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    workspace, env = prepare_workspace(case, output_dir)
    prompt_path = output_dir / "prompt.md"
    prompt_path.write_text(build_live_prompt(case), encoding="utf-8")
    shutil.copy2(SCHEMAS_DIR / "task-result.schema.json", output_dir / "output-schema.json")
    metadata = {
        "schema_version": "cpt-eval-external-fixture-v1",
        "case_id": case["id"],
        "workspace": str(workspace),
        "prompt_file": str(prompt_path),
        "output_schema": str(output_dir / "output-schema.json"),
        "codex_home": env["CODEX_HOME"],
        "grading_command": f"python tools/cpt_eval.py grade-external --case {case['id']} --workspace {workspace} --output <output.json> --trace <trace.jsonl>",
        "reduced_observability_command": f"python tools/cpt_eval.py grade-external --case {case['id']} --workspace {workspace} --output <output.json> --reduced-observability",
    }
    write_json(output_dir / "external-fixture.json", metadata)
    return metadata


def load_normalized_trace(path: Path) -> TraceRecorder:
    recorder = TraceRecorder()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                event = json.loads(line)
                recorder.events.append(event)
                recorder.seq = max(recorder.seq, int(event.get("seq", 0)))
    return recorder


def command_list(_: argparse.Namespace) -> int:
    for case in all_cases():
        print(f"{case['id']}\t{','.join(case['suites'])}\t{case['title']}")
    return 0


def command_compare(args: argparse.Namespace) -> int:
    report = compare_baseline(Path(args.current), Path(args.baseline), Path(args.output) if args.output else None)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


def command_mutate(args: argparse.Namespace) -> int:
    report = mutate_and_check(Path(args.scorecard), Path(args.output))
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


def command_prepare_external(args: argparse.Namespace) -> int:
    metadata = prepare_external(load_case(args.case), Path(args.output_dir).resolve())
    print(json.dumps(metadata, indent=2))
    return 0


def command_grade_external(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    workspace = Path(args.workspace).resolve()
    output = read_json(Path(args.output))
    recorder = load_normalized_trace(Path(args.trace)) if args.trace else TraceRecorder()
    if args.reduced_observability:
        recorder.emit(
            "observability",
            level="reduced",
            reason="No complete host JSONL trace was supplied by the external runner.",
        )
        augment_trace_from_structured_output(output, recorder)
        # Required command assertions cannot be proved without a host trace. Keep
        # forbidden-command checks over any available events, but do not turn
        # missing telemetry into invented evidence or an automatic failure.
        case = copy.deepcopy(case)
        case.setdefault("expectations", {}).setdefault("trace", {})["required_commands"] = []
    report = grade_case(case, output, recorder, workspace, {}, elapsed_seconds=float(args.wall_seconds or 0))
    if args.report:
        write_json(Path(args.report), report)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CPT OS executable evaluation harness")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List evaluation cases")
    p.set_defaults(func=command_list)

    p = sub.add_parser("run", help="Run an evaluation suite")
    p.add_argument("--suite", default="offline-core")
    p.add_argument("--backend", choices=["reference", "live"], default="reference")
    p.add_argument("--report-dir", required=True)
    p.add_argument("--case", action="append")
    p.add_argument("--model")
    p.add_argument("--effort")
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--in-process", action="store_true", help=argparse.SUPPRESS)
    p.set_defaults(func=run_suite)

    p = sub.add_parser("compare-baseline", help="Compare scorecard to a reviewed baseline")
    p.add_argument("--current", required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--output")
    p.set_defaults(func=command_compare)

    p = sub.add_parser("mutate", help="Run deterministic grader mutation checks")
    p.add_argument("--scorecard", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_mutate)

    p = sub.add_parser("prepare-external", help="Prepare an isolated fixture for external execution")
    p.add_argument("--case", required=True)
    p.add_argument("--output-dir", required=True)
    p.set_defaults(func=command_prepare_external)

    p = sub.add_parser("grade-external", help="Grade externally produced structured output and normalized trace")
    p.add_argument("--case", required=True)
    p.add_argument("--workspace", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--trace")
    p.add_argument("--wall-seconds", type=float)
    p.add_argument("--report")
    p.add_argument(
        "--reduced-observability",
        action="store_true",
        help="Grade structured output and Git/runtime evidence when the host cannot provide a complete JSONL trace.",
    )
    p.set_defaults(func=command_grade_external)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"CPT EVAL ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
