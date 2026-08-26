"""Provider-neutral Product OS installation and adoption services."""

from .context import InstallationContext
from .inventory import detect_installation
from .planning import build_adoption_plan, inspect_target_descriptor
from .registry import ConcurrentRegistryChange, RegistryStore

__all__ = [
    "ConcurrentRegistryChange",
    "InstallationContext",
    "RegistryStore",
    "build_adoption_plan",
    "detect_installation",
    "inspect_target_descriptor",
]
