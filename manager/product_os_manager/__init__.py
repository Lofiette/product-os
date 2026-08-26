"""Provider-neutral Product OS installation and adoption services."""

from .adapters import (
    CodexCliSelectorAdapter,
    CodexSessionLifecycleAdapter,
    LocalGitTargetProvider,
)
from .context import InstallationContext
from .doctor import run_migration_doctor, validate_migration_doctor_report
from .inventory import detect_installation
from .planning import build_adoption_plan, inspect_target_descriptor
from .registry import ConcurrentRegistryChange, RegistryStore
from .transaction import (
    AdoptionTransactionError,
    ConcurrentAdoptionChange,
    list_adoption_transactions,
    load_transaction,
    prepare_adoption,
    recover_adoption,
    rollback_adoption,
    switch_adoption,
)

__all__ = [
    "ConcurrentRegistryChange",
    "AdoptionTransactionError",
    "ConcurrentAdoptionChange",
    "CodexCliSelectorAdapter",
    "CodexSessionLifecycleAdapter",
    "InstallationContext",
    "LocalGitTargetProvider",
    "RegistryStore",
    "build_adoption_plan",
    "detect_installation",
    "inspect_target_descriptor",
    "list_adoption_transactions",
    "load_transaction",
    "prepare_adoption",
    "recover_adoption",
    "rollback_adoption",
    "run_migration_doctor",
    "switch_adoption",
    "validate_migration_doctor_report",
]
