from __future__ import annotations

import copy
from dataclasses import dataclass
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

    def copy_descriptor(self) -> dict[str, Any]:
        return copy.deepcopy(dict(self.descriptor))


@dataclass(frozen=True)
class SelectorAdapterEvidence:
    """Selector inventory returned by an in-process bounded host adapter."""

    adapter_id: str
    selectors: Sequence[Mapping[str, Any]]

    def copy_selectors(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(dict(item)) for item in self.selectors]


class TargetProvider(Protocol):
    adapter_id: str

    def resolve(self, request: Mapping[str, Any]) -> TargetAdapterEvidence:
        ...


class SelectorAdapter(Protocol):
    adapter_id: str

    def inspect(self) -> SelectorAdapterEvidence:
        ...
