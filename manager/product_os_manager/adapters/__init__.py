"""Bounded provider and selector adapter contracts."""

from .base import (
    AdapterRegistry,
    LifecycleAdapterEvidence,
    SelectorAdapterEvidence,
    TargetAdapterEvidence,
)
from .codex import CodexCliSelectorAdapter, SubprocessCodexPluginClient
from .codex_lifecycle import CodexSessionLifecycleAdapter
from .repository import LocalGitTargetProvider

__all__ = [
    "AdapterRegistry",
    "CodexCliSelectorAdapter",
    "CodexSessionLifecycleAdapter",
    "LifecycleAdapterEvidence",
    "LocalGitTargetProvider",
    "SelectorAdapterEvidence",
    "SubprocessCodexPluginClient",
    "TargetAdapterEvidence",
]
