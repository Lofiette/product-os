#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.inventory import detect_installation
from manager.product_os_manager.planning import build_adoption_plan, write_adoption_plan


def load_object(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(Path(path).resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object: {path}")
    return value


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def command_detect(args: argparse.Namespace) -> int:
    context = InstallationContext.from_environment(args.project)
    report = detect_installation(
        context.project,
        context=context,
        selector_observation=load_object(args.selector_state),
    )
    emit(report)
    return 0 if report["receipt"]["valid"] and report["runtime"]["valid"] else 1


def command_plan(args: argparse.Namespace) -> int:
    context = InstallationContext.from_environment(args.project)
    report = detect_installation(
        context.project,
        context=context,
        selector_observation=load_object(args.selector_state),
    )
    target = load_object(args.target)
    if target is None:
        raise RuntimeError("Target evidence is required")
    plan = build_adoption_plan(report, target, context=context)
    if args.output:
        write_adoption_plan(Path(args.output), plan)
    emit(plan)
    return 0 if plan["status"] == "ready" else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Provider-neutral Product OS installation and adoption manager"
    )
    commands = root.add_subparsers(dest="command", required=True)

    detect = commands.add_parser("detect", help="Read installation state without mutation")
    detect.add_argument("--project", default=".")
    detect.add_argument(
        "--selector-state",
        help="Optional untrusted selector claims JSON for preview diagnostics",
    )
    detect.set_defaults(handler=command_detect)

    plan = commands.add_parser("plan", help="Build a deterministic dry-run adoption plan")
    plan.add_argument("--project", default=".")
    plan.add_argument(
        "--target",
        required=True,
        help="Untrusted target claims JSON; executable plans require an in-process provider adapter",
    )
    plan.add_argument(
        "--selector-state",
        help="Untrusted selector claims JSON; executable plans require an in-process selector adapter",
    )
    plan.add_argument(
        "--output",
        help="Explicitly persist the plan; without this option plan only writes JSON to stdout",
    )
    plan.set_defaults(handler=command_plan)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
