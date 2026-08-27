from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


def configured_user_home(env: Mapping[str, str]) -> Path:
    configured = env.get("HOME") or env.get("USERPROFILE")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path.home().resolve()


@dataclass(frozen=True)
class InstallationContext:
    project: Path
    user_home: Path
    codex_home: Path
    product_os_home: Path
    marketplace_registry: Path

    @classmethod
    def from_environment(
        cls,
        project: str | Path,
        env: Mapping[str, str] | None = None,
    ) -> "InstallationContext":
        values = os.environ if env is None else env
        user_home = configured_user_home(values)
        codex_home = Path(values.get("CODEX_HOME", user_home / ".codex")).expanduser().resolve()
        product_os_home = Path(
            values.get("PRODUCT_OS_HOME", user_home / ".product-os")
        ).expanduser().resolve()
        marketplace_registry = Path(
            values.get(
                "PRODUCT_OS_MARKETPLACE_REGISTRY",
                user_home / ".agents" / "plugins" / "marketplace.json",
            )
        ).expanduser().resolve()
        return cls(
            project=Path(project).expanduser().resolve(),
            user_home=user_home,
            codex_home=codex_home,
            product_os_home=product_os_home,
            marketplace_registry=marketplace_registry,
        )

    @property
    def registry_path(self) -> Path:
        return self.product_os_home / "registry.json"

    def as_dict(self) -> dict[str, str]:
        return {
            "project": str(self.project),
            "user_home": str(self.user_home),
            "codex_home": str(self.codex_home),
            "product_os_home": str(self.product_os_home),
            "marketplace_registry": str(self.marketplace_registry),
            "registry_path": str(self.registry_path),
        }
