#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from tools.build_manifest import canonical_bytes, included_files
except ModuleNotFoundError:
    from build_manifest import canonical_bytes, included_files

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

MANAGER_BEHAVIOR_INVENTORIES = {
    "installation_receipts": "installation_receipt_tests",
    "manager_registry": "manager_registry_tests",
    "manager_planning": "manager_planning_tests",
    "manager_backup": "manager_backup_tests",
    "manager_transaction": "manager_transaction_tests",
    "manager_git_provider": "manager_git_provider_tests",
    "manager_codex_adapter": "manager_codex_adapter_tests",
    "manager_lifecycle": "manager_lifecycle_tests",
    "manager_cli": "manager_cli_tests",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_json(instance: Any, schema_path: Path) -> list[str]:
    validator = Draft202012Validator(read_json(schema_path))
    return [e.message for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def package_facts() -> dict[str, Any]:
    manifest = read_json(ROOT / "MANIFEST.json") if (ROOT / "MANIFEST.json").exists() else {}
    behavior = read_json(ROOT / "evaluation" / "behavior-test-report.json") if (ROOT / "evaluation" / "behavior-test-report.json").exists() else {}
    suites = read_json(ROOT / "evaluation" / "executable" / "SUITES.json")
    cases = list((ROOT / "evaluation" / "executable" / "cases").glob("*.json"))
    tracks = read_json(RELEASE / "TRIALS.json").get("tracks", [])
    gates = read_json(RELEASE / "GATES.json").get("gates", [])
    return {
        "manifest": manifest,
        "behavior": behavior,
        "suites": suites,
        "offline_cases": sum(1 for p in cases if "offline-core" in read_json(p).get("suites", [])),
        "release_tracks": len(tracks),
        "release_gates": len(gates),
    }


def manifest_matches_checkout(manifest: dict[str, Any]) -> bool:
    files = included_files()
    listed = {
        item.get("path"): item
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    actual_paths = {path.relative_to(ROOT).as_posix() for path in files}
    if manifest.get("file_count") != len(files) or set(listed) != actual_paths:
        return False
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        data = canonical_bytes(path)
        item = listed[relative]
        if item.get("size") != len(data):
            return False
        if item.get("sha256") != hashlib.sha256(data).hexdigest():
            return False
    return True


def behavior_report_matches_manifest(
    behavior: dict[str, Any], manifest: dict[str, Any]
) -> tuple[bool, int, dict[str, dict[str, Any]]]:
    expected = int(manifest.get("inventories", {}).get("behavior_tests", 0))
    total = int(behavior.get("total") or behavior.get("behavior_tests") or 0)
    if not total and isinstance(behavior.get("suites"), list):
        total = sum(int(item.get("count", 0)) for item in behavior["suites"])
    modules = {
        str(item.get("module")): item
        for item in behavior.get("modules", [])
        if isinstance(item, dict) and isinstance(item.get("module"), str)
    }
    manager_ok = all(
        isinstance(modules.get(module), dict)
        and modules[module].get("total")
        == manifest.get("inventories", {}).get(inventory)
        and modules[module].get("passed") == modules[module].get("total")
        for module, inventory in MANAGER_BEHAVIOR_INVENTORIES.items()
    )
    passed = int(behavior.get("passed", -1))
    failed = int(behavior.get("failed", -1))
    return (
        expected > 0
        and total == expected
        and passed == total
        and failed == 0
        and manager_ok,
        total,
        modules,
    )


def candidate_manifest_digest() -> str:
    """Bind reviewed evidence to the exact packaged candidate, without self-reference."""
    entries = []
    for path in included_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative == "release/EVIDENCE.json":
            continue
        data = canonical_bytes(path)
        entries.append(
            {
                "path": relative,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    payload = json.dumps(
        entries,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def reviewed_release_evidence() -> tuple[dict[str, dict[str, Any]], list[str]]:
    evidence_path = RELEASE / "EVIDENCE.json"
    schema_path = RELEASE / "schemas" / "release-evidence.schema.json"
    if not evidence_path.exists():
        return {}, ["missing release/EVIDENCE.json"]
    if not schema_path.exists():
        return {}, ["missing release evidence schema"]
    try:
        document = read_json(evidence_path)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"release evidence cannot be read: {exc}"]
    errors = validate_json(document, schema_path)
    if document.get("version") != VERSION:
        errors.append("release evidence version mismatch")
    recorded_digest = document.get("candidate_manifest_digest")
    current_digest = candidate_manifest_digest()
    if recorded_digest != current_digest:
        errors.append(
            "release evidence candidate digest mismatch: "
            f"expected {current_digest}, recorded {recorded_digest}"
        )
    if errors:
        return {}, errors
    return dict(document.get("gates", {})), []


def offline_evidence() -> dict[str, tuple[bool, list[str]]]:
    facts = package_facts()
    manifest = facts["manifest"]
    behavior = facts["behavior"]
    expected_behavior = manifest.get("inventories", {}).get("behavior_tests", 0)
    behavior_ok, behavior_total, modules = behavior_report_matches_manifest(
        behavior, manifest
    )
    manager_ok = all(
        module in modules for module in MANAGER_BEHAVIOR_INVENTORIES
    ) and all(
        (ROOT / path).exists()
        for path in [
            "manager/product_os_manager/transaction.py",
            "manager/product_os_manager/doctor.py",
            "manager/product_os_manager/adapters/codex.py",
            "tests/test_manager_transaction.py",
            "tests/test_manager_codex_adapter.py",
            "tests/test_manager_cli.py",
        ]
    )
    _, release_evidence_errors = reviewed_release_evidence()

    checks = {
        "package_integrity": (
            manifest.get("version") == VERSION
            and manifest_matches_checkout(manifest)
            and not release_evidence_errors,
            ["MANIFEST.json exact checkout inventory and hashes", "valid reviewed release evidence registry", "distribution validator", "ZIP verification required at packaging"],
        ),
        "offline_regression": (
            facts["offline_cases"] >= 21 and behavior_ok,
            [f"{facts['offline_cases']} offline executable cases", f"behavior report {behavior_total}/{expected_behavior} with zero failures", "Manager suite inventories match MANIFEST", "baseline and mutation reports"],
        ),
        "manager_adoption": (
            manager_ok and behavior_ok,
            ["provider-neutral Manager suites", "Local Git and bounded Codex adapter suites", "transaction discovery, backup, rollback, recovery, and doctor"],
        ),
        "migration_safety": (
            (ROOT / "tests" / "test_migration.py").exists() and (ROOT / "tools" / "cpt_migrate.py").exists(),
            ["migration assistant", "migration tests", "backup and rollback contracts"],
        ),
        "install_update_rollback": (
            (ROOT / "tools" / "cpt_dist.py").exists() and (ROOT / "tests" / "test_distribution.py").exists(),
            ["distribution tests", "installer and doctor", "safe uninstall"],
        ),
        "universality": (
            (ROOT / "KNOWN_LIMITATIONS.md").exists() and (ROOT / "docs" / "RC_TRIALS_AND_RELEASE_GATES.md").exists(),
            ["universal core terminology", "optional integrations policy", "self-contained file-only fallback"],
        ),
        "documentation": (
            all((ROOT / p).exists() for p in ["README.md", "README_RU.md", "INSTALL.md", "docs/MIGRATION_3X_TO_4X.md", "docs/TROUBLESHOOTING.md", "KNOWN_LIMITATIONS.md"]),
            ["installation", "migration", "troubleshooting", "limitations"],
        ),
    }
    return checks


def assess(scope: str) -> dict[str, Any]:
    gate_defs = read_json(RELEASE / "GATES.json")["gates"]
    evidence = offline_evidence()
    reviewed, reviewed_errors = reviewed_release_evidence()
    rows = []
    for gate in gate_defs:
        required = bool(gate["beta_required"] if scope == "offline" else gate["rc_required"])
        if gate["id"] in evidence:
            ok, items = evidence[gate["id"]]
            status = "PASS" if ok else "BLOCKED"
            notes: list[str] = []
        elif gate["id"] in reviewed:
            record = reviewed[gate["id"]]
            items = list(record["evidence"])
            status = str(record["status"])
            notes = list(record.get("notes", []))
            review = record["review"]
            notes.append(
                f"Reviewed by {review['authority']} at {review['recorded_at']}."
            )
        else:
            items = list(gate.get("evidence", []))
            status = "PENDING"
            notes = ["Requires native-platform or live Codex evidence."]
            if reviewed_errors:
                notes.append("Reviewed evidence registry is invalid: " + "; ".join(reviewed_errors))
        rows.append({"id": gate["id"], "status": status, "required": required, "evidence": items, "notes": notes})

    blocked = sum(1 for x in rows if x["required"] and x["status"] == "BLOCKED")
    pending_required = sum(1 for x in rows if x["required"] and x["status"] == "PENDING")
    if blocked or pending_required:
        status = "BLOCKED"
    elif scope == "offline":
        status = "BETA_READY"
    else:
        status = "RC_READY"
    return {
        "schema_version": "cpt-release-scorecard-v1",
        "version": VERSION,
        "scope": scope,
        "status": status,
        "generated_at": utc_now(),
        "gates": rows,
        "summary": {
            "passed": sum(1 for x in rows if x["status"] == "PASS"),
            "pending": sum(1 for x in rows if x["status"] == "PENDING"),
            "blocked": sum(1 for x in rows if x["status"] == "BLOCKED"),
        },
    }


def readiness(scope: str) -> dict[str, Any]:
    scorecard = assess(scope)
    facts = package_facts()
    manifest = facts["manifest"]
    return {
        "schema_version": "cpt-release-readiness-v1",
        "version": VERSION,
        "certification_scope": "offline" if scope == "offline" else "live",
        "status": scorecard["status"],
        "behavioral_tests": int(manifest.get("inventories", {}).get("behavior_tests", 0)),
        "offline_cases": facts["offline_cases"],
        "release_tracks": facts["release_tracks"],
        "release_gates": facts["release_gates"],
        "generated_at": utc_now(),
        "scorecard_summary": scorecard["summary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CPT release readiness plane")
    sub = parser.add_subparsers(dest="command", required=True)
    p_assess = sub.add_parser("assess")
    p_assess.add_argument("--scope", choices=["offline", "rc"], default="offline")
    p_assess.add_argument("--output", type=Path)
    p_ready = sub.add_parser("readiness")
    p_ready.add_argument("--scope", choices=["offline", "rc"], default="offline")
    p_ready.add_argument("--output", type=Path)
    p_validate = sub.add_parser("validate-scorecard")
    p_validate.add_argument("path", type=Path)
    args = parser.parse_args()

    if args.command == "assess":
        result = assess(args.scope)
        errors = validate_json(result, RELEASE / "schemas" / "release-scorecard.schema.json")
        if errors:
            raise SystemExit("\n".join(errors))
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] != "BLOCKED" else 1
    if args.command == "readiness":
        result = readiness(args.scope)
        errors = validate_json(result, RELEASE / "schemas" / "release-readiness.schema.json")
        if errors:
            raise SystemExit("\n".join(errors))
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] != "BLOCKED" else 1
    if args.command == "validate-scorecard":
        data = read_json(args.path)
        errors = validate_json(data, RELEASE / "schemas" / "release-scorecard.schema.json")
        if errors:
            print("RELEASE SCORECARD INVALID")
            for error in errors:
                print("-", error)
            return 1
        print("RELEASE SCORECARD VALID")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
