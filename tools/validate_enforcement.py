#!/usr/bin/env python3
from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HOOKS_ROOT = ROOT / "payload/marketplace-root/plugins/cpt-core/hooks"
ENFORCEMENT = ROOT / "payload/repo-scaffold/.cpt/enforcement.yaml"
HOOKS_JSON = HOOKS_ROOT / "hooks.json"
HOOK_WRAPPER = HOOKS_ROOT / "cpt_hook.py"
LIFECYCLE_HELPER = HOOKS_ROOT / "product_os_lifecycle.py"
RULES = [
    ROOT / "policies/rules/cpt-conservative.rules",
    ROOT / "policies/rules/cpt-strict.rules",
]
REQUIRED = [
    ENFORCEMENT,
    HOOKS_JSON,
    HOOK_WRAPPER,
    LIFECYCLE_HELPER,
    *RULES,
    ROOT / "ENFORCEMENT.md",
]
errors: list[str] = []

for path in REQUIRED:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")

try:
    config = yaml.safe_load(ENFORCEMENT.read_text(encoding="utf-8"))
    if config.get("mode") not in {"off", "audit", "enforce"}:
        errors.append("invalid enforcement mode")
except Exception as exc:
    errors.append(f"enforcement yaml: {exc}")

try:
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    expected = {
        "SessionStart", "SessionEnd", "PreToolUse", "PermissionRequest",
        "PostToolUse", "PreCompact", "PostCompact", "SubagentStart",
        "SubagentStop", "Stop",
    }
    if set(hooks) != expected:
        errors.append(f"hook events mismatch: {set(hooks) ^ expected}")
    session_end = hooks.get("SessionEnd")
    if not isinstance(session_end, list) or len(session_end) != 1:
        errors.append("SessionEnd hook binding is invalid")
    else:
        commands = session_end[0].get("hooks") if isinstance(session_end[0], dict) else None
        if (
            not isinstance(commands, list)
            or len(commands) != 1
            or commands[0].get("type") != "command"
            or commands[0].get("timeout", 99) > 3
        ):
            errors.append("SessionEnd must be one command hook with timeout <= 3 seconds")
except Exception as exc:
    errors.append(f"hooks json: {exc}")

for label, path in (("hook wrapper", HOOK_WRAPPER), ("lifecycle helper", LIFECYCLE_HELPER)):
    try:
        ast.parse(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label} syntax: {exc}")

try:
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(HOOKS_ROOT))
    spec = importlib.util.spec_from_file_location("cpt_hook_validation", HOOK_WRAPPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("hook wrapper import spec is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
finally:
    sys.dont_write_bytecode = previous if "previous" in locals() else False
    if sys.path and sys.path[0] == str(HOOKS_ROOT):
        sys.path.pop(0)

for path in RULES:
    text = path.read_text(encoding="utf-8")
    if "prefix_rule(" not in text or "match = [" not in text:
        errors.append(f"incomplete rules file {path.name}")

if errors:
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1)
print("ENFORCEMENT ASSET VALIDATION PASSED")
