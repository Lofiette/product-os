from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from pathlib import Path
import re
from typing import Any, Callable

from ..state import (
    atomic_write_json,
    canonical_json_hash,
    exclusive_lock,
    file_sha256,
    read_json,
)
from .base import SelectorAdapterEvidence, TargetAdapterEvidence
from .repository import DirectoryTargetProvider


class DeterministicFixtureAdapter:
    """No-I/O adapter used only by deterministic tests and synthetic harnesses."""

    adapter_id = "deterministic-fixture"
    adapter_version = "1"
    capability_fingerprint = "read-only-fixture-v1"

    def target(self, descriptor: Mapping[str, Any]) -> TargetAdapterEvidence:
        return TargetAdapterEvidence(
            self.adapter_id,
            descriptor,
            self.adapter_version,
            self.capability_fingerprint,
        )

    def selectors(self, selectors: Sequence[Mapping[str, Any]]) -> SelectorAdapterEvidence:
        return SelectorAdapterEvidence(
            self.adapter_id,
            selectors,
            None,
            self.adapter_version,
            self.capability_fingerprint,
        )


class DeterministicSelectorAdapter:
    """File-backed selector adapter for isolated transaction tests only."""

    adapter_id = "deterministic-selector"
    adapter_version = "1"
    capability_fingerprint = "file-cas-batch-selector-v1"
    schema = "deterministic-selector-state-v1"

    def __init__(
        self,
        state_path: Path,
        selectors: Sequence[Mapping[str, Any]] = (),
        *,
        faults: set[str] | None = None,
    ) -> None:
        self.state_path = state_path.resolve()
        self.lock_path = self.state_path.with_suffix(self.state_path.suffix + ".lock")
        self.faults = set(faults or set())
        if not self.state_path.exists():
            self._write_document(selectors, {})

    @staticmethod
    def _normalize(selectors: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for item in selectors:
            name = item.get("name")
            selector = item.get("selector")
            enabled = item.get("enabled", True)
            if not isinstance(name, str) or not name or not isinstance(selector, str) or not selector:
                raise RuntimeError("Selector entries require non-empty name and selector")
            if not isinstance(enabled, bool):
                raise RuntimeError("Selector enabled state must be boolean")
            key = (name, selector)
            if key in seen:
                raise RuntimeError(f"Duplicate selector entry: {name}={selector}")
            seen.add(key)
            normalized.append({
                "name": name,
                "selector": selector,
                "marketplace_identity": item.get("marketplace_identity"),
                "enabled": enabled,
                "source_revision": item.get("source_revision"),
            })
        normalized.sort(key=lambda item: (item["name"], item["selector"]))
        enabled_names = [item["name"] for item in normalized if item["enabled"]]
        duplicates = sorted({name for name in enabled_names if enabled_names.count(name) > 1})
        if duplicates:
            raise RuntimeError(f"Multiple enabled selectors for: {', '.join(duplicates)}")
        return normalized

    def _write_document(
        self,
        selectors: Sequence[Mapping[str, Any]],
        operations: Mapping[str, Mapping[str, Any]],
    ) -> None:
        atomic_write_json(
            self.state_path,
            {
                "schema": self.schema,
                "selectors": self._normalize(selectors),
                "operations": copy.deepcopy(dict(operations)),
            },
        )

    def _read_document(self) -> dict[str, Any]:
        value = read_json(self.state_path)
        if not isinstance(value, dict) or value.get("schema") != self.schema:
            raise RuntimeError("Deterministic selector state is invalid")
        selectors = value.get("selectors")
        operations = value.get("operations", {})
        if not isinstance(selectors, list) or not isinstance(operations, dict):
            raise RuntimeError("Deterministic selector state is missing selectors or operations")
        return {
            "schema": self.schema,
            "selectors": self._normalize(selectors),
            "operations": copy.deepcopy(operations),
        }

    def _read(self) -> list[dict[str, Any]]:
        return self._read_document()["selectors"]

    def inspect(self) -> SelectorAdapterEvidence:
        return SelectorAdapterEvidence(
            self.adapter_id,
            self._read(),
            file_sha256(self.state_path),
            self.adapter_version,
            self.capability_fingerprint,
        )

    def _fail(self, name: str) -> None:
        if name in self.faults:
            raise RuntimeError(f"Injected deterministic selector failure: {name}")

    @staticmethod
    def _operation_key(transaction_id: str, operation_id: str) -> str:
        if not re.fullmatch(r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", transaction_id):
            raise RuntimeError("Transaction id is invalid")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", operation_id):
            raise RuntimeError("Selector operation id is invalid")
        return f"{transaction_id}:{operation_id}"

    def _apply_operation(
        self,
        method: str,
        payload: Any,
        mutate: Callable[[list[dict[str, Any]]], list[dict[str, Any]]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
        after_write_fault: str,
    ) -> SelectorAdapterEvidence:
        key = self._operation_key(transaction_id, operation_id)
        payload_sha = canonical_json_hash(payload)
        with exclusive_lock(self.lock_path):
            document = self._read_document()
            current_token = file_sha256(self.state_path)
            existing = document["operations"].get(key)
            if existing is not None:
                expected_record = {
                    "method": method,
                    "input_state_token": expected_state_token,
                    "payload_sha256": payload_sha,
                }
                if any(existing.get(name) != value for name, value in expected_record.items()):
                    raise RuntimeError("Selector operation id was reused with different inputs")
                if existing.get("result_selectors_sha256") != canonical_json_hash(document["selectors"]):
                    raise RuntimeError("Selector operation result is no longer current")
            else:
                if current_token != expected_state_token:
                    raise RuntimeError("Selector state changed after inspection")
                result = self._normalize(mutate(copy.deepcopy(document["selectors"])))
                document["operations"][key] = {
                    "method": method,
                    "input_state_token": expected_state_token,
                    "payload_sha256": payload_sha,
                    "result_selectors_sha256": canonical_json_hash(result),
                }
                self._write_document(result, document["operations"])
        self._fail(after_write_fault)
        return self.inspect()

    @staticmethod
    def _target_entries(target_plugins: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        names: set[str] = set()
        selectors: set[str] = set()
        for plugin in target_plugins:
            selector = plugin.get("selector")
            name = plugin.get("name")
            if not isinstance(selector, str) or not isinstance(name, str):
                raise RuntimeError("Target plugin is missing selector identity")
            if name in names or selector in selectors:
                raise RuntimeError("Target plugin names and selectors must be unique")
            names.add(name)
            selectors.add(selector)
            entries.append({
                "name": name,
                "selector": selector,
                "marketplace_identity": plugin.get("marketplace_identity")
                or selector.split("@", 1)[-1],
                "enabled": False,
                "source_revision": plugin.get("source_revision"),
            })
        return sorted(entries, key=lambda item: (item["name"], item["selector"]))

    def prepare(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._fail("prepare")
        targets = self._target_entries(target_plugins)

        def mutate(current: list[dict[str, Any]]) -> list[dict[str, Any]]:
            enabled_before = {
                (item["name"], item["selector"])
                for item in current
                if item["enabled"]
            }
            by_key = {(item["name"], item["selector"]): copy.deepcopy(item) for item in current}
            for target in targets:
                key = (target["name"], target["selector"])
                if key in by_key and by_key[key]["enabled"]:
                    if by_key[key].get("source_revision") == target.get("source_revision"):
                        raise RuntimeError("Target selector is already active before prepare")
                    continue
                by_key[key] = target
            result = list(by_key.values())
            enabled_after = {
                (item["name"], item["selector"])
                for item in result
                if item["enabled"]
            }
            if enabled_after != enabled_before:
                raise RuntimeError("Selector prepare changed active selector state")
            return result

        return self._apply_operation(
            "prepare",
            targets,
            mutate,
            transaction_id=transaction_id,
            operation_id=operation_id,
            expected_state_token=expected_state_token,
            after_write_fault="prepare_after_write",
        )

    def activate(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._fail("activate_before_write")
        target_entries = self._target_entries(target_plugins)
        target_by_name = {item["name"]: item for item in target_entries}
        if "activate_after_first" in self.faults and target_entries:
            key = self._operation_key(transaction_id, operation_id)
            del key
            with exclusive_lock(self.lock_path):
                if file_sha256(self.state_path) != expected_state_token:
                    raise RuntimeError("Selector state changed after inspection")
                document = self._read_document()
                first = target_entries[0]
                changed = copy.deepcopy(document["selectors"])
                if not any(
                    item["name"] == first["name"] and item["selector"] == first["selector"]
                    for item in changed
                ):
                    raise RuntimeError("Prepared target selector is missing")
                for item in changed:
                    if item["name"] == first["name"]:
                        item["enabled"] = item["selector"] == first["selector"]
                self._write_document(changed, document["operations"])
            raise RuntimeError("Injected deterministic selector failure: activate_after_first")

        def mutate(current: list[dict[str, Any]]) -> list[dict[str, Any]]:
            keys = {(item["name"], item["selector"]) for item in current}
            missing = [
                target["selector"]
                for target in target_entries
                if (target["name"], target["selector"]) not in keys
            ]
            if missing:
                raise RuntimeError(f"Prepared target selectors are missing: {', '.join(missing)}")
            changed = []
            for item in current:
                candidate = copy.deepcopy(item)
                target = target_by_name.get(item["name"])
                if target:
                    candidate["enabled"] = item["selector"] == target["selector"]
                    if candidate["enabled"]:
                        candidate["source_revision"] = target.get("source_revision")
                changed.append(candidate)
            for target in target_entries:
                active = [
                    item for item in changed
                    if item["name"] == target["name"] and item["enabled"]
                ]
                if len(active) != 1 or active[0]["selector"] != target["selector"]:
                    raise RuntimeError("Selector activation did not produce the complete target mapping")
            return changed

        return self._apply_operation(
            "activate",
            target_entries,
            mutate,
            transaction_id=transaction_id,
            operation_id=operation_id,
            expected_state_token=expected_state_token,
            after_write_fault="activate_after_write",
        )

    def restore(
        self,
        selectors: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._fail("restore")
        normalized = self._normalize(selectors)
        return self._apply_operation(
            "restore",
            normalized,
            lambda _current: normalized,
            transaction_id=transaction_id,
            operation_id=operation_id,
            expected_state_token=expected_state_token,
            after_write_fault="restore_after_write",
        )

    def recover_incomplete_activation(
        self, *, transaction_id: str
    ) -> SelectorAdapterEvidence:
        del transaction_id
        return self.inspect()

    def retire(
        self,
        selectors: Sequence[str],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._fail("retire")
        selected = set(selectors)

        def mutate(current: list[dict[str, Any]]) -> list[dict[str, Any]]:
            for item in current:
                if item["selector"] in selected and item["enabled"]:
                    raise RuntimeError("Cannot retire an enabled selector")
            return [item for item in current if item["selector"] not in selected]

        return self._apply_operation(
            "retire",
            sorted(selected),
            mutate,
            transaction_id=transaction_id,
            operation_id=operation_id,
            expected_state_token=expected_state_token,
            after_write_fault="retire_after_write",
        )


__all__ = [
    "DeterministicFixtureAdapter",
    "DeterministicSelectorAdapter",
    "DirectoryTargetProvider",
]
