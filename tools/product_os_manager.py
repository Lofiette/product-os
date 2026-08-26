#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from manager.product_os_manager.adapters.base import AdapterRegistry
from manager.product_os_manager.adapters.codex import (
    CodexCliSelectorAdapter,
    SubprocessCodexPluginClient,
    discover_legacy_selector_revisions,
)
from manager.product_os_manager.adapters.codex_lifecycle import (
    CodexSessionLifecycleAdapter,
)
from manager.product_os_manager.adapters.repository import LocalGitTargetProvider
from manager.product_os_manager.context import InstallationContext
from manager.product_os_manager.doctor import run_migration_doctor
from manager.product_os_manager.inventory import detect_installation
from manager.product_os_manager.planning import (
    build_adoption_plan,
    validate_adoption_plan,
    write_adoption_plan,
)
from manager.product_os_manager.transaction import (
    load_transaction,
    list_adoption_transactions,
    prepare_adoption,
    recover_adoption,
    rollback_adoption,
    switch_adoption,
    validate_mutation_context,
)


def load_object(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(Path(path).resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object: {path}")
    return value


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _same_path(left: Path, right: Path) -> bool:
    left_value = str(left.resolve())
    right_value = str(right.resolve())
    if os.name == "nt":
        left_value = left_value.casefold()
        right_value = right_value.casefold()
    return left_value == right_value


def _explicit_context(args: argparse.Namespace) -> InstallationContext:
    required = ("project", "user_home", "codex_home", "product_os_home")
    missing = [name for name in required if not getattr(args, name, None)]
    if missing:
        raise RuntimeError(
            "Trusted Manager commands require explicit roots: " + ", ".join(missing)
        )
    project = Path(args.project).expanduser().resolve()
    user_home = Path(args.user_home).expanduser().resolve()
    codex_home = Path(args.codex_home).expanduser().resolve()
    product_os_home = Path(args.product_os_home).expanduser().resolve()
    for label, path in (
        ("project", project),
        ("user home", user_home),
        ("CODEX_HOME", codex_home),
        ("PRODUCT_OS_HOME", product_os_home),
    ):
        if not path.is_dir():
            raise RuntimeError(f"Explicit {label} does not exist: {path}")
    ambient_user = Path(
        os.environ.get("HOME") or os.environ.get("USERPROFILE") or Path.home()
    ).expanduser().resolve()
    ambient_codex = Path(
        os.environ.get("CODEX_HOME", ambient_user / ".codex")
    ).expanduser().resolve()
    if _same_path(codex_home, ambient_codex):
        confirmation = getattr(args, "confirmed_active_codex_home", None)
        if confirmation is None or not _same_path(Path(confirmation), codex_home):
            raise RuntimeError(
                "Trusted Manager commands refuse the process-active CODEX_HOME without "
                "an exact --confirmed-active-codex-home path"
            )
    marketplace_registry = Path(
        args.marketplace_registry
        if getattr(args, "marketplace_registry", None)
        else user_home / ".agents" / "plugins" / "marketplace.json"
    ).expanduser().resolve()
    context = InstallationContext(
        project=project,
        user_home=user_home,
        codex_home=codex_home,
        product_os_home=product_os_home,
        marketplace_registry=marketplace_registry,
    )
    validate_mutation_context(context)
    return context


def _provider(args: argparse.Namespace, context: InstallationContext) -> LocalGitTargetProvider:
    return LocalGitTargetProvider(
        Path(args.repository_root),
        context,
        git_executable=args.git_executable,
    )


def _codex_adapter(
    args: argparse.Namespace,
    context: InstallationContext,
    target: dict[str, Any],
    *,
    legacy_revisions: dict[str, str | None] | None = None,
) -> CodexCliSelectorAdapter:
    if target.get("evidence_adapter") != "local-git":
        raise RuntimeError("Trusted CLI requires a local-git target provider")
    plugins = target.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise RuntimeError("Trusted CLI target has no plugin inventory")
    client = SubprocessCodexPluginClient(
        context,
        executable=args.codex_executable,
    )
    names = [item.get("name") for item in plugins if isinstance(item, dict)]
    if legacy_revisions is None:
        legacy_revisions = discover_legacy_selector_revisions(
            client,
            names,
            target_marketplace_identity=target["marketplace_identity"],
        )
    return CodexCliSelectorAdapter(
        context,
        target_root=Path(target["materialized_root"]),
        marketplace_identity=target["marketplace_identity"],
        target_revision=target["resolved_commit"],
        target_product_version=target["product_version"],
        target_manifest_sha256=target["package_manifest_sha256"],
        target_plugins=plugins,
        legacy_selector_revisions=legacy_revisions,
        client=client,
    )


def _legacy_revisions_from_journal(journal: dict[str, Any]) -> dict[str, str | None]:
    target = journal["plan"]["target"]
    names = {item["name"] for item in target["plugins"]}
    target_selectors = {item["selector"] for item in target["plugins"]}
    result: dict[str, str | None] = {}
    for item in journal["initial"]["selector"]["selectors"]:
        selector = item.get("selector")
        if (
            item.get("name") in names
            and isinstance(selector, str)
            and selector not in target_selectors
        ):
            result[selector] = item.get("source_revision")
    return {selector: result[selector] for selector in sorted(result)}


def _journal_adapters(
    args: argparse.Namespace,
    context: InstallationContext,
    journal: dict[str, Any],
    *,
    lifecycle: bool = False,
    include_target_provider: bool = True,
) -> AdapterRegistry:
    target = journal["plan"]["target"]
    selector = _codex_adapter(
        args,
        context,
        target,
        legacy_revisions=_legacy_revisions_from_journal(journal),
    )
    lifecycle_adapters = [CodexSessionLifecycleAdapter(context)] if lifecycle else []
    return AdapterRegistry(
        target_providers=[_provider(args, context)] if include_target_provider else [],
        selector_adapters=[selector],
        lifecycle_adapters=lifecycle_adapters,
    )


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


def command_plan_local_git(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    provider = _provider(args, context)
    request = {
        "repository": provider.repository,
        "requested_ref": args.requested_ref,
        "marketplace_identity": args.marketplace_identity,
        "plugins": args.plugin,
    }
    target_evidence = provider.resolve(request)
    target = target_evidence.copy_descriptor()
    target.update(
        {
            "evidence_adapter": target_evidence.adapter_id,
            "evidence_adapter_version": target_evidence.adapter_version,
            "evidence_capability_fingerprint": target_evidence.capability_fingerprint,
        }
    )
    selector = _codex_adapter(args, context, target)
    report = detect_installation(
        context.project,
        context=context,
        selector_observation=selector.inspect(),
    )
    plan = build_adoption_plan(report, target_evidence, context=context)
    if args.output:
        write_adoption_plan(Path(args.output), plan)
    emit(plan)
    return 0 if plan["status"] == "ready" else 1


def command_prepare(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    plan = load_object(args.plan)
    if plan is None:
        raise RuntimeError("Adoption plan is required")
    validate_adoption_plan(plan)
    provider = _provider(args, context)
    selector = _codex_adapter(args, context, plan["target"])
    result = prepare_adoption(
        plan,
        confirmed_plan_hash=args.confirmed_plan_hash,
        context=context,
        adapters=AdapterRegistry(
            target_providers=[provider],
            selector_adapters=[selector],
        ),
    )
    emit(result)
    return 0 if result.get("status") in {"prepared", "committed"} else 1


def command_switch(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    journal = load_transaction(context, args.transaction_id)
    result = switch_adoption(
        args.transaction_id,
        confirmed_prepared_state_hash=args.confirmed_prepared_state_hash,
        context=context,
        adapters=_journal_adapters(args, context, journal),
    )
    emit(result)
    return 0 if result.get("status") == "committed" else 1


def command_rollback(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    journal = load_transaction(context, args.transaction_id)
    result = rollback_adoption(
        args.transaction_id,
        context=context,
        adapters=_journal_adapters(
            args,
            context,
            journal,
            include_target_provider=False,
        ),
        force=args.force,
        confirmed_current_state_hash=args.confirmed_current_state_hash,
    )
    emit(result)
    return 0 if result.get("status") == "rolled_back" else 1


def command_transactions(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    emit(list_adoption_transactions(context))
    return 0


def command_recover(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    journal = load_transaction(context, args.transaction_id)
    result = recover_adoption(
        args.transaction_id,
        context=context,
        adapters=_journal_adapters(args, context, journal),
    )
    emit(result)
    return 0 if result.get("status") in {
        "prepared",
        "committed",
        "rolled_back",
        "failed_no_mutation",
    } else 1


def command_doctor(args: argparse.Namespace) -> int:
    context = _explicit_context(args)
    journal = load_transaction(context, args.transaction_id)
    adapters = _journal_adapters(
        args,
        context,
        journal,
        lifecycle=args.require_codex_lifecycle,
        include_target_provider=False,
    )
    if args.require_codex_lifecycle:
        configured_home = os.environ.get("PRODUCT_OS_HOME")
        if configured_home is None or not _same_path(
            Path(configured_home).expanduser(), context.product_os_home
        ):
            raise RuntimeError(
                "Codex lifecycle verification requires PRODUCT_OS_HOME to match "
                "the explicit Manager root used by the new Codex process"
            )
    report = run_migration_doctor(
        context,
        adapters,
        transaction_id=args.transaction_id,
        lifecycle_adapter_id=(
            CodexSessionLifecycleAdapter.adapter_id
            if args.require_codex_lifecycle
            else None
        ),
    )
    emit(report)
    accepted = report["status"] == "PASS" and (
        not args.require_codex_lifecycle or report["lifecycle"]["status"] == "PASS"
    )
    return 0 if accepted else 1


def _trusted_context_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument("--project", required=True)
    command.add_argument("--user-home", required=True)
    command.add_argument("--codex-home", required=True)
    command.add_argument("--product-os-home", required=True)
    command.add_argument("--marketplace-registry")
    command.add_argument(
        "--confirmed-active-codex-home",
        help="Exact path confirmation required only for a separately authorized live migration",
    )


def _trusted_adapter_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument("--repository-root", required=True)
    command.add_argument("--git-executable", default="git")
    command.add_argument("--codex-executable", default="codex")


def _trusted_codex_argument(command: argparse.ArgumentParser) -> None:
    command.add_argument("--codex-executable", default="codex")


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

    trusted_plan = commands.add_parser(
        "plan-local-git",
        help="Build an authoritative dry-run plan from local Git and Codex JSON readback",
    )
    _trusted_context_arguments(trusted_plan)
    _trusted_adapter_arguments(trusted_plan)
    trusted_plan.add_argument("--requested-ref", required=True)
    trusted_plan.add_argument("--marketplace-identity", required=True)
    trusted_plan.add_argument("--plugin", action="append", required=True)
    trusted_plan.add_argument("--output")
    trusted_plan.set_defaults(handler=command_plan_local_git)

    prepare = commands.add_parser("prepare", help="Materialize and prepare an approved plan")
    _trusted_context_arguments(prepare)
    _trusted_adapter_arguments(prepare)
    prepare.add_argument("--plan", required=True)
    prepare.add_argument("--confirmed-plan-hash", required=True)
    prepare.set_defaults(handler=command_prepare)

    switch = commands.add_parser("switch", help="Commit a prepared two-phase adoption")
    _trusted_context_arguments(switch)
    _trusted_adapter_arguments(switch)
    switch.add_argument("--transaction-id", required=True)
    switch.add_argument("--confirmed-prepared-state-hash", required=True)
    switch.set_defaults(handler=command_switch)

    rollback = commands.add_parser("rollback", help="Rollback a prepared or committed adoption")
    _trusted_context_arguments(rollback)
    _trusted_codex_argument(rollback)
    rollback.add_argument("--transaction-id", required=True)
    rollback.add_argument("--force", action="store_true")
    rollback.add_argument("--confirmed-current-state-hash")
    rollback.set_defaults(handler=command_rollback)

    recover = commands.add_parser("recover", help="Reconcile an orphaned adoption journal")
    _trusted_context_arguments(recover)
    _trusted_adapter_arguments(recover)
    recover.add_argument("--transaction-id", required=True)
    recover.set_defaults(handler=command_recover)

    transactions = commands.add_parser(
        "transactions",
        help="List adoption journals for crash recovery without mutation",
    )
    _trusted_context_arguments(transactions)
    transactions.set_defaults(handler=command_transactions)

    doctor = commands.add_parser("doctor", help="Read-only committed migration verification")
    _trusted_context_arguments(doctor)
    _trusted_codex_argument(doctor)
    doctor.add_argument("--transaction-id", required=True)
    doctor.add_argument("--require-codex-lifecycle", action="store_true")
    doctor.set_defaults(handler=command_doctor)
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
