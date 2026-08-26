from __future__ import annotations

import copy
from dataclasses import dataclass
import re
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence


@dataclass(frozen=True)
class TargetAdapterEvidence:
    """Evidence returned by an in-process bounded target provider.

    JSON loaded from a user-selected file is deliberately not this type and is
    therefore non-authoritative. Future apply code must also restrict which
    adapter implementations it composes.
    """

    adapter_id: str
    descriptor: Mapping[str, Any]
    adapter_version: str = "1"
    capability_fingerprint: str = "resolve-materialize-v1"

    def copy_descriptor(self) -> dict[str, Any]:
        return copy.deepcopy(dict(self.descriptor))


@dataclass(frozen=True)
class SelectorAdapterEvidence:
    """Selector inventory returned by an in-process bounded host adapter."""

    adapter_id: str
    selectors: Sequence[Mapping[str, Any]]
    state_token: str | None = None
    adapter_version: str = "1"
    capability_fingerprint: str = "inspect-prepare-activate-restore-retire-v1"

    def copy_selectors(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(dict(item)) for item in self.selectors]


@dataclass(frozen=True)
class LifecycleAdapterEvidence:
    """Optional host-lifecycle evidence kept outside core transaction gates."""

    adapter_id: str
    status: str
    detail: str
    evidence: Mapping[str, Any]
    adapter_version: str = "1"
    capability_fingerprint: str = "inspect-session-lifecycle-v1"

    def as_report(self) -> dict[str, Any]:
        result = {
            "status": self.status,
            "adapter": self.adapter_id,
            "detail": self.detail,
        }
        result.update(copy.deepcopy(dict(self.evidence)))
        return result


class TargetProvider(Protocol):
    adapter_id: str
    adapter_version: str
    capability_fingerprint: str

    def resolve(self, request: Mapping[str, Any]) -> TargetAdapterEvidence:
        ...

    def materialize(
        self,
        evidence: TargetAdapterEvidence,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> TargetAdapterEvidence:
        ...

    def cleanup_created(
        self,
        destination: Path,
        *,
        transaction_id: str,
        operation_id: str,
    ) -> None:
        ...


class SelectorAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    capability_fingerprint: str

    def inspect(self) -> SelectorAdapterEvidence:
        ...

    def prepare(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        ...

    def activate(
        self,
        target_plugins: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        ...

    def restore(
        self,
        selectors: Sequence[Mapping[str, Any]],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        ...

    def retire(
        self,
        selectors: Sequence[str],
        *,
        transaction_id: str,
        operation_id: str,
        expected_state_token: str | None,
    ) -> SelectorAdapterEvidence:
        ...


class LifecycleAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    capability_fingerprint: str

    def inspect(self, journal: Mapping[str, Any]) -> LifecycleAdapterEvidence:
        ...


class AdapterRegistry:
    """Explicit in-process authority boundary for mutating adapters."""

    def __init__(
        self,
        *,
        target_providers: Sequence[TargetProvider] = (),
        selector_adapters: Sequence[SelectorAdapter] = (),
        lifecycle_adapters: Sequence[LifecycleAdapter] = (),
    ) -> None:
        self._target_providers: dict[str, TargetProvider] = {}
        self._selector_adapters: dict[str, SelectorAdapter] = {}
        self._lifecycle_adapters: dict[str, LifecycleAdapter] = {}
        for provider in target_providers:
            self.register_target(provider)
        for adapter in selector_adapters:
            self.register_selector(adapter)
        for adapter in lifecycle_adapters:
            self.register_lifecycle(adapter)

    @staticmethod
    def _identity(value: Any) -> str:
        if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", value):
            raise RuntimeError("Adapter id must be a kebab-case identity")
        return value

    def register_target(self, provider: TargetProvider) -> None:
        adapter_id = self._identity(getattr(provider, "adapter_id", None))
        self.binding(provider)
        for capability in ("resolve", "materialize", "cleanup_created"):
            if not callable(getattr(provider, capability, None)):
                raise RuntimeError(f"Target provider {adapter_id} is missing capability: {capability}")
        if adapter_id in self._target_providers:
            raise RuntimeError(f"Target provider is already registered: {adapter_id}")
        self._target_providers[adapter_id] = provider

    def register_selector(self, adapter: SelectorAdapter) -> None:
        adapter_id = self._identity(getattr(adapter, "adapter_id", None))
        self.binding(adapter)
        for capability in ("inspect", "prepare", "activate", "restore", "retire"):
            if not callable(getattr(adapter, capability, None)):
                raise RuntimeError(f"Selector adapter {adapter_id} is missing capability: {capability}")
        if adapter_id in self._selector_adapters:
            raise RuntimeError(f"Selector adapter is already registered: {adapter_id}")
        self._selector_adapters[adapter_id] = adapter

    def register_lifecycle(self, adapter: LifecycleAdapter) -> None:
        adapter_id = self._identity(getattr(adapter, "adapter_id", None))
        self.binding(adapter)
        if not callable(getattr(adapter, "inspect", None)):
            raise RuntimeError(
                f"Lifecycle adapter {adapter_id} is missing capability: inspect"
            )
        if adapter_id in self._lifecycle_adapters:
            raise RuntimeError(f"Lifecycle adapter is already registered: {adapter_id}")
        self._lifecycle_adapters[adapter_id] = adapter

    def target(self, adapter_id: str | None) -> TargetProvider:
        if adapter_id not in self._target_providers:
            raise RuntimeError(f"Target provider is not registered: {adapter_id}")
        return self._target_providers[adapter_id]

    def selector(self, adapter_id: str | None) -> SelectorAdapter:
        if adapter_id not in self._selector_adapters:
            raise RuntimeError(f"Selector adapter is not registered: {adapter_id}")
        return self._selector_adapters[adapter_id]

    def lifecycle(self, adapter_id: str | None) -> LifecycleAdapter:
        if adapter_id not in self._lifecycle_adapters:
            raise RuntimeError(f"Lifecycle adapter is not registered: {adapter_id}")
        return self._lifecycle_adapters[adapter_id]

    @staticmethod
    def binding(adapter: Any) -> dict[str, str]:
        adapter_id = AdapterRegistry._identity(getattr(adapter, "adapter_id", None))
        version = getattr(adapter, "adapter_version", None)
        fingerprint = getattr(adapter, "capability_fingerprint", None)
        if not isinstance(version, str) or not version:
            raise RuntimeError(f"Adapter version is missing: {adapter_id}")
        if not isinstance(fingerprint, str) or not fingerprint:
            raise RuntimeError(f"Adapter capability fingerprint is missing: {adapter_id}")
        return {
            "adapter_id": adapter_id,
            "adapter_version": version,
            "capability_fingerprint": fingerprint,
        }
