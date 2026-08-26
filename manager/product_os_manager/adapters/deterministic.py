from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .base import SelectorAdapterEvidence, TargetAdapterEvidence


class DeterministicFixtureAdapter:
    """No-I/O adapter used only by deterministic tests and synthetic harnesses."""

    adapter_id = "deterministic-fixture"

    def target(self, descriptor: Mapping[str, Any]) -> TargetAdapterEvidence:
        return TargetAdapterEvidence(self.adapter_id, descriptor)

    def selectors(self, selectors: Sequence[Mapping[str, Any]]) -> SelectorAdapterEvidence:
        return SelectorAdapterEvidence(self.adapter_id, selectors)
