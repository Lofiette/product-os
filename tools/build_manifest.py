#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
EXCLUDED_NAMES = {"MANIFEST.json"}
EXCLUDED_PARTS = {"__pycache__", ".git"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def included_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if path.name in EXCLUDED_NAMES:
            continue
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def main() -> int:
    files = included_files()
    data = {
        "schema": "cpt-package-manifest-v7",
        "name": "codex-product-os",
        "version": "4.0.0-alpha.7",
        "phase": "managed-worker-orchestration",
        "manifest_excludes": ["MANIFEST.json", "**/__pycache__/**", "**/*.pyc", "**/*.pyo"],
        "file_count": len(files),
        "inventories": {
            "plugins": 6,
            "canonical_skills": 45,
            "legacy_skill_mappings": 95,
            "logical_roles": 50,
            "quality_gates": 25,
            "routing_profiles": 14,
            "knowledge_artifact_types": 6,
            "knowledge_templates": 6,
            "knowledge_examples": 3,
            "knowledge_lifecycle_cases": 11,
            "enforcement_policy_cases": 5,
            "enforcement_integration_checks": 13,
            "worker_archetypes": 10,
            "orchestration_policy_cases": 34,
            "orchestration_integration_checks": 16,
            "behavior_tests": 85,
            "hooks": 9,
            "rules_profiles": 2,
        },
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "size": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        ],
    }
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"MANIFEST BUILT: {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
