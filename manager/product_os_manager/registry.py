from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from .context import InstallationContext
from .state import (
    atomic_write_json,
    canonical_json_hash,
    exclusive_lock,
    file_sha256,
    read_json,
    utc_now,
)

REGISTRY_SCHEMA = "product-os-installation-registry-v1"
RECEIPT_SCHEMA_V2 = "cpt-install-receipt-v2"


class ConcurrentRegistryChange(RuntimeError):
    pass


def empty_registry() -> dict[str, Any]:
    return {
        "schema": REGISTRY_SCHEMA,
        "updated_at": utc_now(),
        "installations": {},
    }


def registry_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "installation-registry-v1.schema.json"


def validate_registry(data: dict[str, Any]) -> None:
    schema = read_json(registry_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(data),
        key=lambda item: list(item.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Invalid Product OS installation registry: {details}")


def receipt_entry(project: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    if receipt.get("schema") != RECEIPT_SCHEMA_V2 or not receipt.get("installation_id"):
        raise RuntimeError("Only installation receipt v2 can be registered")
    plugins = [
        item
        for item in receipt.get("installed_plugins", [])
        if isinstance(item, dict) and item.get("name")
    ]
    return {
        "installation_id": receipt["installation_id"],
        "project": str(project.resolve()),
        "receipt_path": str((project / ".cpt" / "install.json").resolve()),
        "receipt_sha256": canonical_json_hash(receipt),
        "product_version": receipt.get("version"),
        "runtime_schema": (receipt.get("product") or {}).get("runtime_schema"),
        "source_lineage": copy.deepcopy(receipt.get("source_lineage") or {}),
        "selectors": sorted({
            item["selector"]
            for item in plugins
            if isinstance(item.get("selector"), str) and item["selector"]
        }),
        "plugin_names": sorted({item["name"] for item in plugins}),
        "last_seen_at": utc_now(),
    }


class RegistryStore:
    def __init__(self, context: InstallationContext):
        self.context = context
        self.path = context.registry_path
        self.lock_path = context.product_os_home / "registry.lock"

    def snapshot(self) -> tuple[dict[str, Any], str | None]:
        if not self.path.exists():
            return empty_registry(), None
        data = read_json(self.path)
        if not isinstance(data, dict):
            raise RuntimeError("Product OS registry is not a JSON object")
        validate_registry(data)
        return data, file_sha256(self.path)

    def save(self, data: dict[str, Any], *, expected_digest: str | None) -> str:
        candidate = copy.deepcopy(data)
        candidate["schema"] = REGISTRY_SCHEMA
        candidate["updated_at"] = utc_now()
        validate_registry(candidate)
        with exclusive_lock(self.lock_path):
            current_digest = file_sha256(self.path)
            if current_digest != expected_digest:
                raise ConcurrentRegistryChange(
                    "Installation registry changed after it was inspected; rebuild the plan"
                )
            atomic_write_json(self.path, candidate)
        return file_sha256(self.path) or ""

    def upsert(self, project: Path, receipt: dict[str, Any]) -> str:
        data, digest = self.snapshot()
        entry = receipt_entry(project, receipt)
        data.setdefault("installations", {})[entry["installation_id"]] = entry
        return self.save(data, expected_digest=digest)

    def rebuild(
        self,
        project_receipts: Iterable[tuple[Path, dict[str, Any]]],
    ) -> tuple[dict[str, Any], list[str]]:
        data, digest = self.snapshot()
        rebuilt: dict[str, Any] = {}
        warnings: list[str] = []
        for project, receipt in project_receipts:
            if receipt.get("schema") != RECEIPT_SCHEMA_V2 or not receipt.get("installation_id"):
                warnings.append(
                    f"Skipped receipt without v2 installation identity: {project.resolve()}"
                )
                continue
            entry = receipt_entry(project, receipt)
            rebuilt[entry["installation_id"]] = entry
        data["installations"] = rebuilt
        self.save(data, expected_digest=digest)
        result, _ = self.snapshot()
        return result, warnings

    def selector_references(self, selector: str) -> list[str]:
        data, _ = self.snapshot()
        return sorted(
            installation_id
            for installation_id, entry in data.get("installations", {}).items()
            if selector in entry.get("selectors", [])
        )
