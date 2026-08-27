from __future__ import annotations

import copy
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from typing import Any, Mapping, Protocol, Sequence

from ..backup import assert_safe_ancestry
from ..context import InstallationContext
from ..planning import _is_link_like, _is_within
from ..state import (
    atomic_write_json,
    canonical_json_hash,
    canonical_text_file_sha256,
    exclusive_lock,
    read_json,
    utc_now,
)
from .base import SelectorAdapterEvidence
from .repository import _safe_marketplace_source_relative, verify_package_root

TRANSACTION_PATTERN = re.compile(
    r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
IDENTITY_PATTERN = re.compile(r"[a-z][a-z0-9-]*")
SELECTOR_PATTERN = re.compile(r"([a-z][a-z0-9-]*)@([a-z][a-z0-9-]*)")


class CodexPluginClient(Protocol):
    def list_plugins(self) -> Mapping[str, Any]: ...

    def list_marketplaces(self) -> Mapping[str, Any]: ...

    def add_marketplace(self, source: Path) -> Mapping[str, Any]: ...

    def remove_marketplace(self, marketplace: str) -> Mapping[str, Any]: ...

    def add_plugin(self, selector: str) -> Mapping[str, Any]: ...

    def remove_plugin(self, selector: str) -> Mapping[str, Any]: ...


class SubprocessCodexPluginClient:
    """Bounded JSON client for the local Codex plugin CLI."""

    def __init__(
        self,
        context: InstallationContext,
        *,
        executable: str = "codex",
    ) -> None:
        candidate = shutil.which(executable)
        if candidate is None:
            path = Path(executable)
            if not path.is_file():
                raise RuntimeError(f"Codex executable is unavailable: {executable}")
            candidate = str(path.resolve())
        self.executable = candidate
        self.context = context
        if not context.codex_home.is_absolute():
            raise RuntimeError("Codex adapter requires an absolute CODEX_HOME")
        if not context.codex_home.is_dir():
            raise RuntimeError(
                "Codex adapter requires an existing explicit CODEX_HOME; "
                "it will not create or infer one"
            )

    def _environment(self) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(self.context.user_home),
                "USERPROFILE": str(self.context.user_home),
                "CODEX_HOME": str(self.context.codex_home),
            }
        )
        return environment

    def _json(self, *arguments: str) -> dict[str, Any]:
        try:
            completed = subprocess.run(
                [self.executable, "plugin", *arguments, "--json"],
                capture_output=True,
                check=False,
                env=self._environment(),
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"Codex plugin command failed safely: {arguments[0]}: {exc}") from exc
        if completed.returncode:
            detail = completed.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"Codex plugin command failed: {arguments[0]}: {detail}")
        try:
            value = json.loads(completed.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Codex plugin command returned invalid JSON: {arguments[0]}") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"Codex plugin command did not return a JSON object: {arguments[0]}")
        return value

    def list_plugins(self) -> Mapping[str, Any]:
        return self._json("list", "--available")

    def list_marketplaces(self) -> Mapping[str, Any]:
        return self._json("marketplace", "list")

    def add_marketplace(self, source: Path) -> Mapping[str, Any]:
        return self._json("marketplace", "add", str(source))

    def remove_marketplace(self, marketplace: str) -> Mapping[str, Any]:
        return self._json("marketplace", "remove", marketplace)

    def add_plugin(self, selector: str) -> Mapping[str, Any]:
        return self._json("add", selector)

    def remove_plugin(self, selector: str) -> Mapping[str, Any]:
        return self._json("remove", selector)


def discover_legacy_selector_revisions(
    client: CodexPluginClient,
    managed_plugin_names: Sequence[str],
    *,
    target_marketplace_identity: str,
) -> dict[str, str]:
    """Capture installed legacy selector versions before binding an adapter."""

    managed = set(managed_plugin_names)
    if not managed or any(
        not isinstance(name, str) or not IDENTITY_PATTERN.fullmatch(name)
        for name in managed
    ):
        raise RuntimeError("Codex managed plugin names are invalid")
    value = client.list_plugins()
    installed = value.get("installed")
    if not isinstance(installed, list):
        raise RuntimeError("Codex plugin list JSON is missing the installed array")
    result: dict[str, str] = {}
    observed_names: set[str] = set()
    for item in installed:
        if not isinstance(item, dict):
            raise RuntimeError("Codex installed plugin entry is invalid")
        name = item.get("name")
        if name not in managed:
            continue
        selector = item.get("pluginId")
        marketplace = item.get("marketplaceName")
        version = item.get("version")
        if (
            not isinstance(selector, str)
            or not isinstance(marketplace, str)
            or selector != f"{name}@{marketplace}"
            or not SELECTOR_PATTERN.fullmatch(selector)
            or item.get("installed") is not True
            or item.get("enabled") is not True
            or not isinstance(version, str)
            or not version
            or name in observed_names
        ):
            raise RuntimeError("Codex installed managed plugin state is invalid or duplicated")
        observed_names.add(str(name))
        if marketplace != target_marketplace_identity:
            result[selector] = version
    return {selector: result[selector] for selector in sorted(result)}


class CodexCliSelectorAdapter:
    """Optional Codex selector adapter over documented JSON CLI commands.

    Prepare registers only the already-materialized local marketplace. Activate
    installs the selected plugins for future sessions. The current Codex
    session is intentionally not treated as refreshed; lifecycle evidence is a
    separate optional adapter concern.
    """

    adapter_id = "codex-cli-selector"
    adapter_version = "1"
    schema = "product-os-codex-selector-operations-v1"

    def __init__(
        self,
        context: InstallationContext,
        *,
        target_root: Path,
        marketplace_identity: str,
        target_revision: str,
        target_product_version: str,
        target_manifest_sha256: str,
        target_plugins: Sequence[Mapping[str, Any]],
        legacy_selector_revisions: Mapping[str, str | None] | None = None,
        client: CodexPluginClient | None = None,
    ) -> None:
        if not IDENTITY_PATTERN.fullmatch(marketplace_identity):
            raise RuntimeError("Codex target marketplace identity is invalid")
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", target_revision):
            raise RuntimeError("Codex target revision must be a commit id")
        if not isinstance(target_product_version, str) or not target_product_version:
            raise RuntimeError("Codex target product version is invalid")
        if not re.fullmatch(r"[0-9a-f]{64}", target_manifest_sha256):
            raise RuntimeError("Codex target package manifest digest is invalid")
        self.context = context
        self.target_root = target_root.resolve()
        sources_root = (context.product_os_home / "sources").resolve()
        if not _is_within(self.target_root, sources_root):
            raise RuntimeError("Codex target marketplace root escapes PRODUCT_OS_HOME sources")
        expected_root = (sources_root / marketplace_identity / target_revision).resolve()
        if self._path_key(self.target_root) != self._path_key(expected_root):
            raise RuntimeError("Codex target marketplace root is not commit-addressed")
        self.marketplace_identity = marketplace_identity
        self.target_revision = target_revision
        self.target_product_version = target_product_version
        self.target_manifest_sha256 = target_manifest_sha256
        bound_plugins: dict[str, dict[str, str]] = {}
        for item in target_plugins:
            if not isinstance(item, Mapping):
                raise RuntimeError("Codex target plugin descriptor is invalid")
            name = item.get("name")
            selector = item.get("selector")
            relative_path = item.get("relative_path")
            manifest_sha256 = item.get("manifest_sha256")
            pure = PurePosixPath(relative_path) if isinstance(relative_path, str) else None
            plugin_root = (
                (self.target_root / relative_path).resolve()
                if isinstance(relative_path, str)
                else None
            )
            if (
                not isinstance(name, str)
                or not IDENTITY_PATTERN.fullmatch(name)
                or selector != f"{name}@{marketplace_identity}"
                or pure is None
                or pure.is_absolute()
                or not pure.parts
                or any(part in {"", ".", ".."} for part in pure.parts)
                or pure.as_posix() != relative_path
                or "\\" in relative_path
                or re.match(r"^[A-Za-z]:", relative_path) is not None
                or plugin_root is None
                or not _is_within(plugin_root, self.target_root)
                or not isinstance(manifest_sha256, str)
                or not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256)
                or name in bound_plugins
            ):
                raise RuntimeError("Codex target plugin descriptor is invalid or duplicated")
            bound_plugins[name] = {
                "name": name,
                "selector": selector,
                "relative_path": relative_path,
                "manifest_sha256": manifest_sha256,
            }
        if not bound_plugins:
            raise RuntimeError("Codex target plugin selection must not be empty")
        self.bound_plugins = {
            name: bound_plugins[name] for name in sorted(bound_plugins)
        }
        self.managed_plugin_names = tuple(self.bound_plugins)
        self.target_selectors = {
            f"{name}@{marketplace_identity}" for name in self.managed_plugin_names
        }
        self.legacy_selector_revisions = dict(legacy_selector_revisions or {})
        for selector in self.legacy_selector_revisions:
            match = SELECTOR_PATTERN.fullmatch(selector)
            if match is None:
                raise RuntimeError(f"Legacy Codex selector is invalid: {selector}")
            if match.group(1) not in self.managed_plugin_names:
                raise RuntimeError(
                    f"Legacy Codex selector is outside managed plugin names: {selector}"
                )
        self.tracked_selectors = set(self.legacy_selector_revisions) | self.target_selectors
        self.client = client or SubprocessCodexPluginClient(context)
        binding_hash = canonical_json_hash(
            {
                "codex_home": self._path_key(context.codex_home),
                "target_root": str(self.target_root),
                "marketplace_identity": marketplace_identity,
                "target_revision": target_revision,
                "target_product_version": target_product_version,
                "target_manifest_sha256": target_manifest_sha256,
                "target_plugins": list(self.bound_plugins.values()),
                "legacy_selector_revisions": self.legacy_selector_revisions,
            }
        )
        self.capability_fingerprint = f"codex-json-cli-two-phase-v1:{binding_hash}"
        self.state_path = (
            context.product_os_home
            / "adapters"
            / "codex"
            / f"{binding_hash}.json"
        ).resolve()
        self.lock_path = (context.codex_home / ".product-os-manager.lock").resolve()
        assert_safe_ancestry(self.state_path, context.product_os_home)
        assert_safe_ancestry(self.lock_path, context.codex_home)

    def _plugin_root(self, name: str) -> Path:
        root = (self.target_root / self.bound_plugins[name]["relative_path"]).resolve()
        if not _is_within(root, self.target_root):
            raise RuntimeError(f"Codex target plugin path escapes the verified package: {name}")
        return root

    @staticmethod
    def _operation_key(transaction_id: str, operation_id: str) -> str:
        if not TRANSACTION_PATTERN.fullmatch(transaction_id):
            raise RuntimeError("Transaction id is invalid")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", operation_id):
            raise RuntimeError("Selector operation id is invalid")
        return f"{transaction_id}:{operation_id}"

    @staticmethod
    def _path_key(path: Path) -> str:
        value = str(path.resolve())
        if os.name == "nt" and value.startswith("\\\\?\\"):
            value = value[4:]
        return value.casefold() if os.name == "nt" else value

    def _marketplaces(self) -> list[dict[str, str]]:
        value = self.client.list_marketplaces()
        entries = value.get("marketplaces")
        if not isinstance(entries, list):
            raise RuntimeError("Codex marketplace list JSON is invalid")
        result: list[dict[str, str]] = []
        seen: set[str] = set()
        for item in entries:
            if not isinstance(item, dict):
                raise RuntimeError("Codex marketplace entry is invalid")
            name = item.get("name")
            root = item.get("root")
            if not isinstance(name, str) or not IDENTITY_PATTERN.fullmatch(name):
                raise RuntimeError("Codex marketplace name is invalid")
            if not isinstance(root, str) or not root:
                raise RuntimeError(f"Codex marketplace root is invalid: {name}")
            if name in seen:
                raise RuntimeError(f"Codex marketplace is duplicated: {name}")
            seen.add(name)
            result.append({"name": name, "root": root})
        return sorted(result, key=lambda item: item["name"])

    def _normalize_plugin(self, item: Any, *, available: bool) -> dict[str, Any]:
        if not isinstance(item, dict):
            raise RuntimeError("Codex plugin list entry is invalid")
        selector = item.get("pluginId")
        name = item.get("name")
        marketplace = item.get("marketplaceName")
        installed = item.get("installed")
        enabled = item.get("enabled")
        if (
            not isinstance(selector, str)
            or not isinstance(name, str)
            or not isinstance(marketplace, str)
            or selector != f"{name}@{marketplace}"
            or not SELECTOR_PATTERN.fullmatch(selector)
            or not isinstance(installed, bool)
            or not isinstance(enabled, bool)
        ):
            raise RuntimeError("Codex plugin selector entry has an invalid identity or state")
        if available and installed:
            raise RuntimeError(f"Codex available plugin is unexpectedly installed: {selector}")
        if enabled and not installed:
            raise RuntimeError(f"Codex plugin cannot be enabled without installation: {selector}")
        version = item.get("version")
        if not isinstance(version, str) or not version:
            raise RuntimeError(f"Codex plugin version is invalid: {selector}")
        if selector in self.target_selectors:
            if version != self.target_product_version:
                raise RuntimeError(f"Codex target plugin version changed: {selector}")
            source = item.get("source")
            marketplace_source = item.get("marketplaceSource")
            expected_path = self._plugin_root(name)
            if (
                not isinstance(source, dict)
                or source.get("source") != "local"
                or not isinstance(source.get("path"), str)
                or self._path_key(Path(source["path"])) != self._path_key(expected_path)
                or not isinstance(marketplace_source, dict)
                or marketplace_source.get("sourceType") != "local"
                or not isinstance(marketplace_source.get("source"), str)
                or self._path_key(Path(marketplace_source["source"]))
                != self._path_key(self.target_root)
            ):
                raise RuntimeError(f"Codex target plugin source is not the bound local marketplace: {selector}")
            revision: str | None = self.target_revision
        elif selector in self.legacy_selector_revisions:
            expected_revision = self.legacy_selector_revisions[selector]
            if expected_revision is not None and version != expected_revision:
                raise RuntimeError(f"Codex legacy plugin version changed: {selector}")
            revision = version
        else:
            revision = version
        return {
            "name": name,
            "selector": selector,
            "marketplace_identity": marketplace,
            "enabled": enabled,
            "source_revision": revision,
        }

    def _selectors(self) -> list[dict[str, Any]]:
        value = self.client.list_plugins()
        installed = value.get("installed")
        available = value.get("available")
        if not isinstance(installed, list) or not isinstance(available, list):
            raise RuntimeError("Codex plugin list JSON is missing installed/available arrays")
        by_selector: dict[str, dict[str, Any]] = {}
        for item in installed:
            normalized = self._normalize_plugin(item, available=False)
            selector = normalized["selector"]
            if selector in by_selector:
                raise RuntimeError(f"Codex installed plugin is duplicated: {selector}")
            by_selector[selector] = normalized
        for item in available:
            selector = item.get("pluginId") if isinstance(item, dict) else None
            if selector not in self.tracked_selectors or selector in by_selector:
                continue
            by_selector[str(selector)] = self._normalize_plugin(item, available=True)
        result = sorted(by_selector.values(), key=lambda item: (item["name"], item["selector"]))
        enabled_names = [item["name"] for item in result if item["enabled"]]
        duplicates = sorted({name for name in enabled_names if enabled_names.count(name) > 1})
        if duplicates:
            raise RuntimeError(f"Codex has multiple enabled selectors for: {', '.join(duplicates)}")
        return result

    def inspect(self) -> SelectorAdapterEvidence:
        marketplaces = self._marketplaces()
        target_marketplace = next(
            (item for item in marketplaces if item["name"] == self.marketplace_identity),
            None,
        )
        target_source = None
        if target_marketplace is not None:
            if self._path_key(Path(target_marketplace["root"])) != self._path_key(self.target_root):
                raise RuntimeError("Codex target marketplace name is bound to another root")
            target_source = self._verify_target_marketplace()
        selectors = self._selectors()
        token = canonical_json_hash(
            {
                "selectors": selectors,
                "marketplaces": marketplaces,
                "target_source": target_source,
            }
        )
        return SelectorAdapterEvidence(
            self.adapter_id,
            selectors,
            token,
            self.adapter_version,
            self.capability_fingerprint,
        )

    def _load_store(self) -> dict[str, Any]:
        value = read_json(
            self.state_path,
            {"schema": self.schema, "operations": {}},
        )
        if (
            not isinstance(value, dict)
            or value.get("schema") != self.schema
            or not isinstance(value.get("operations"), dict)
        ):
            raise RuntimeError("Codex selector operation store is invalid")
        return copy.deepcopy(value)

    def _save_store(self, value: Mapping[str, Any]) -> None:
        atomic_write_json(self.state_path, copy.deepcopy(dict(value)))

    def _assert_target_plugins(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in target_plugins:
            name = item.get("name")
            selector = item.get("selector")
            if (
                name not in self.managed_plugin_names
                or selector != f"{name}@{self.marketplace_identity}"
                or item.get("marketplace_identity") != self.marketplace_identity
                or item.get("source_revision") != self.target_revision
            ):
                raise RuntimeError("Codex target plugin payload does not match adapter binding")
            if selector in seen:
                raise RuntimeError(f"Codex target selector is duplicated: {selector}")
            seen.add(str(selector))
            result.append(copy.deepcopy(dict(item)))
        if seen != self.target_selectors:
            raise RuntimeError("Codex target plugin payload does not cover the bound plugin set")
        return sorted(result, key=lambda item: item["selector"])

    def _verify_target_marketplace(self) -> dict[str, Any]:
        if not self.target_root.is_dir() or _is_link_like(self.target_root):
            raise RuntimeError("Codex target marketplace root is missing or link-like")
        package = verify_package_root(
            self.target_root,
            expected_manifest_sha256=self.target_manifest_sha256,
        )
        if package.get("version") != self.target_product_version:
            raise RuntimeError("Codex target package version changed")
        marketplace = read_json(self.target_root / ".agents" / "plugins" / "marketplace.json")
        if not isinstance(marketplace, dict) or marketplace.get("name") != self.marketplace_identity:
            raise RuntimeError("Codex target marketplace manifest identity is invalid")
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            raise RuntimeError("Codex target marketplace plugin inventory is invalid")
        by_name = {
            item.get("name"): item
            for item in entries
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }
        if len(by_name) != len(entries):
            raise RuntimeError("Codex target marketplace plugins are invalid or duplicated")
        observed_plugins: list[dict[str, str]] = []
        for name, expected in self.bound_plugins.items():
            item = by_name.get(name)
            source = item.get("source") if isinstance(item, dict) else None
            canonical_source: str | None = None
            if isinstance(source, dict) and source.get("source") == "local":
                try:
                    canonical_source = _safe_marketplace_source_relative(
                        source.get("path")
                    ).as_posix()
                except RuntimeError:
                    canonical_source = None
            if canonical_source != expected["relative_path"]:
                raise RuntimeError(f"Codex target marketplace source changed: {name}")
            manifest_path = self._plugin_root(name) / ".codex-plugin" / "plugin.json"
            if canonical_text_file_sha256(manifest_path) != expected["manifest_sha256"]:
                raise RuntimeError(f"Codex target plugin manifest changed: {name}")
            observed_plugins.append(copy.deepcopy(expected))
        return {
            "package_manifest_sha256": self.target_manifest_sha256,
            "inventory_sha256": canonical_json_hash(package.get("files")),
            "plugins_sha256": canonical_json_hash(observed_plugins),
        }

    def prepare(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        key = self._operation_key(transaction_id, operation_id)
        targets = self._assert_target_plugins(target_plugins)
        self._verify_target_marketplace()
        with exclusive_lock(self.lock_path):
            store = self._load_store()
            existing = store["operations"].get(key)
            if isinstance(existing, dict) and existing.get("status") == "prepared":
                if (
                    existing.get("input_state_token") != expected_state_token
                    or existing.get("targets_sha256") != canonical_json_hash(targets)
                ):
                    raise RuntimeError("Codex selector operation id was reused with different inputs")
                current = self.inspect()
                if current.state_token != existing.get("result_state_token"):
                    raise RuntimeError("Codex prepared selector result is no longer current")
                return current
            current = self.inspect()
            if current.state_token != expected_state_token:
                raise RuntimeError("Codex selector state changed after inspection")
            marketplaces = self._marketplaces()
            target_marketplace = next(
                (item for item in marketplaces if item["name"] == self.marketplace_identity),
                None,
            )
            if target_marketplace is not None and self._path_key(Path(target_marketplace["root"])) != self._path_key(self.target_root):
                raise RuntimeError("Codex target marketplace name is already bound to another root")
            operation = {
                "transaction_id": transaction_id,
                "operation_id": operation_id,
                "method": "prepare",
                "status": "preparing",
                "input_state_token": expected_state_token,
                "targets_sha256": canonical_json_hash(targets),
                "marketplace_existed_before": target_marketplace is not None,
                "marketplace_add_intent": target_marketplace is None,
                "marketplace_added": False,
                "updated_at": utc_now(),
            }
            store["operations"][key] = operation
            self._save_store(store)
            if target_marketplace is None:
                self._verify_target_marketplace()
                result = self.client.add_marketplace(self.target_root)
                if (
                    result.get("marketplaceName") != self.marketplace_identity
                    or result.get("alreadyAdded") is not False
                ):
                    raise RuntimeError(
                        "Codex marketplace add did not prove transaction ownership"
                    )
                operation["marketplace_added"] = True
                operation["updated_at"] = utc_now()
                store["operations"][key] = operation
                self._save_store(store)
            prepared = self.inspect()
            operation["status"] = "prepared"
            operation["result_state_token"] = prepared.state_token
            operation["updated_at"] = utc_now()
            store["operations"][key] = operation
            self._save_store(store)
            return prepared

    def activate(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        key = self._operation_key(transaction_id, operation_id)
        targets = self._assert_target_plugins(target_plugins)
        with exclusive_lock(self.lock_path):
            store = self._load_store()
            existing = store["operations"].get(key)
            if isinstance(existing, dict) and existing.get("status") == "activated":
                if (
                    existing.get("input_state_token") != expected_state_token
                    or existing.get("targets_sha256") != canonical_json_hash(targets)
                ):
                    raise RuntimeError("Codex selector operation id was reused with different inputs")
                current = self.inspect()
                if current.state_token != existing.get("result_state_token"):
                    raise RuntimeError("Codex activated selector result is no longer current")
                return current
            current = self.inspect()
            if current.state_token != expected_state_token:
                raise RuntimeError("Codex selector state changed after inspection")
            operation = {
                "transaction_id": transaction_id,
                "operation_id": operation_id,
                "method": "activate",
                "status": "activating",
                "input_state_token": expected_state_token,
                "targets_sha256": canonical_json_hash(targets),
                "updated_at": utc_now(),
            }
            store["operations"][key] = operation
            self._save_store(store)
            current_enabled = {
                str(item["name"]): str(item["selector"])
                for item in current.selectors
                if item.get("enabled") and item.get("name") in self.managed_plugin_names
            }
            for target in targets:
                self._verify_target_marketplace()
                target_selector = str(target["selector"])
                active_selector = current_enabled.get(str(target["name"]))
                if active_selector is not None and active_selector != target_selector:
                    self.client.remove_plugin(active_selector)
                result = self.client.add_plugin(target_selector)
                plugin_id = result.get("pluginId")
                if plugin_id is not None and plugin_id != target_selector:
                    raise RuntimeError("Codex installed an unexpected plugin selector")
                self._verify_target_marketplace()
            activated = self.inspect()
            operation["status"] = "activated"
            operation["result_state_token"] = activated.state_token
            operation["updated_at"] = utc_now()
            store["operations"][key] = operation
            self._save_store(store)
            return activated

    def restore(
        self,
        selectors: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._operation_key(transaction_id, operation_id)
        desired = [copy.deepcopy(dict(item)) for item in selectors]
        desired_enabled: dict[str, str] = {}
        for item in desired:
            name = item.get("name")
            selector = item.get("selector")
            enabled = item.get("enabled")
            if not isinstance(name, str) or not isinstance(selector, str) or not isinstance(enabled, bool):
                raise RuntimeError("Codex restore selector payload is invalid")
            if name in self.managed_plugin_names and enabled:
                if name in desired_enabled:
                    raise RuntimeError(f"Codex restore has multiple enabled selectors for: {name}")
                desired_enabled[name] = selector
        with exclusive_lock(self.lock_path):
            current = self.inspect()
            if current.state_token != expected_state_token:
                raise RuntimeError("Codex selector state changed after rollback preflight")
            current_enabled = {
                str(item["name"]): str(item["selector"])
                for item in current.selectors
                if item.get("enabled") and item.get("name") in self.managed_plugin_names
            }
            for name in self.managed_plugin_names:
                wanted = desired_enabled.get(name)
                active = current_enabled.get(name)
                if wanted == active:
                    continue
                if active is not None:
                    self.client.remove_plugin(active)
                if wanted is not None:
                    if wanted not in self.tracked_selectors:
                        raise RuntimeError(f"Codex restore selector is outside adapter authority: {wanted}")
                    self.client.add_plugin(wanted)
            store = self._load_store()
            added_by_transaction = any(
                isinstance(record, dict)
                and record.get("transaction_id") == transaction_id
                and record.get("method") == "prepare"
                and record.get("marketplace_added") is True
                for record in store["operations"].values()
            )
            ambiguous_add_intent = any(
                isinstance(record, dict)
                and record.get("transaction_id") == transaction_id
                and record.get("method") == "prepare"
                and record.get("marketplace_add_intent") is True
                and record.get("marketplace_added") is not True
                for record in store["operations"].values()
            )
            desired_uses_target = any(
                item.get("selector") in self.target_selectors for item in desired
            )
            marketplaces = self._marketplaces()
            target_marketplace_present = any(
                item["name"] == self.marketplace_identity for item in marketplaces
            )
            if ambiguous_add_intent and target_marketplace_present and not desired_uses_target:
                raise RuntimeError(
                    "Codex marketplace ownership is ambiguous after an interrupted add"
                )
            if added_by_transaction and not desired_uses_target and target_marketplace_present:
                self._verify_target_marketplace()
                result = self.client.remove_marketplace(self.marketplace_identity)
                if (
                    result.get("marketplaceName") != self.marketplace_identity
                    or not (
                        result.get("removed") is True
                        or (
                            "installedRoot" in result
                            and result.get("installedRoot") is None
                        )
                    )
                ):
                    raise RuntimeError("Codex marketplace removal result is invalid")
                if any(
                    item["name"] == self.marketplace_identity
                    for item in self._marketplaces()
                ):
                    raise RuntimeError("Codex transaction-owned marketplace was not removed")
            return self.inspect()

    def retire(
        self,
        selectors: Sequence[str],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        self._operation_key(transaction_id, operation_id)
        selected = sorted(set(selectors))
        if len(selected) != len(list(selectors)) or any(
            selector not in self.tracked_selectors for selector in selected
        ):
            raise RuntimeError("Codex retire selectors are duplicated or outside adapter authority")
        with exclusive_lock(self.lock_path):
            current = self.inspect()
            if current.state_token != expected_state_token:
                raise RuntimeError("Codex selector state changed after retirement preflight")
            installed = {
                str(item["selector"])
                for item in current.selectors
                if item.get("enabled")
            }
            for selector in selected:
                if selector in installed:
                    raise RuntimeError("Cannot retire an enabled Codex selector")
            raise RuntimeError(
                "Codex selector retirement is unsupported until registry-wide references are proven"
            )


__all__ = [
    "CodexCliSelectorAdapter",
    "CodexPluginClient",
    "SubprocessCodexPluginClient",
    "discover_legacy_selector_revisions",
]
