from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from ..backup import assert_safe_ancestry
from ..context import InstallationContext
from ..state import canonical_json_hash, file_sha256, read_json
from .base import LifecycleAdapterEvidence

EVENT_SCHEMA = "product-os-codex-lifecycle-event-v1"
TRANSACTION_PATTERN = re.compile(
    r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
MAX_EVENT_FILES = 64
MAX_EVENT_BYTES = 64 * 1024


def lifecycle_event_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas" / "codex-lifecycle-event-v1.schema.json"


def _path_key(path: Path) -> str:
    value = str(path.resolve())
    return value.casefold() if os.name == "nt" else value


def project_bucket(project: Path) -> str:
    return hashlib.sha256(_path_key(project).encode("utf-8")).hexdigest()


def lifecycle_bucket(project: Path, transaction_id: str) -> str:
    value = _path_key(project) + "\0" + transaction_id
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:32]


def _hashable_event(event: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(event))
    value.pop("event_hash", None)
    return value


def validate_lifecycle_event(event: dict[str, Any]) -> None:
    schema = read_json(lifecycle_event_schema_path(), {})
    errors = sorted(
        Draft202012Validator(schema).iter_errors(event),
        key=lambda item: list(item.path),
    )
    if errors:
        detail = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Invalid Codex lifecycle evidence: {detail}")
    if event["event_hash"] != canonical_json_hash(_hashable_event(event)):
        raise RuntimeError("Invalid Codex lifecycle evidence: event_hash does not match content")


class CodexSessionLifecycleAdapter:
    """Read-only observer for privacy-minimized Codex session hook evidence."""

    adapter_id = "codex-session-lifecycle"
    adapter_version = "1"
    capability_fingerprint = "hashed-startup-session-evidence-v1"

    def __init__(self, context: InstallationContext) -> None:
        self.context = context

    def _directory(self, journal: Mapping[str, Any]) -> Path:
        transaction_id = journal.get("transaction_id")
        if not isinstance(transaction_id, str) or not TRANSACTION_PATTERN.fullmatch(transaction_id):
            raise RuntimeError("Lifecycle transaction id is invalid")
        path = (
            self.context.product_os_home
            / "lifecycle"
            / "codex"
            / lifecycle_bucket(self.context.project, transaction_id)
        ).resolve()
        assert_safe_ancestry(path, self.context.product_os_home)
        return path

    @staticmethod
    def _failed(detail: str) -> LifecycleAdapterEvidence:
        return LifecycleAdapterEvidence(
            CodexSessionLifecycleAdapter.adapter_id,
            "FAIL",
            detail,
            {},
            CodexSessionLifecycleAdapter.adapter_version,
            CodexSessionLifecycleAdapter.capability_fingerprint,
        )

    def inspect(self, journal: Mapping[str, Any]) -> LifecycleAdapterEvidence:
        if journal.get("state") != "committed":
            return LifecycleAdapterEvidence(
                self.adapter_id,
                "pending",
                "the adoption transaction is not committed",
                {},
                self.adapter_version,
                self.capability_fingerprint,
            )
        receipt_path = self.context.project / ".cpt" / "install.json"
        receipt_digest = file_sha256(receipt_path)
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return self._failed(f"installation receipt cannot bind lifecycle evidence: {exc}")
        manager = receipt.get("manager") if isinstance(receipt, dict) else None
        lineage = receipt.get("source_lineage") if isinstance(receipt, dict) else None
        if (
            not isinstance(receipt, dict)
            or receipt.get("schema") != "cpt-install-receipt-v2"
            or not isinstance(manager, dict)
            or manager.get("last_transaction_id") != journal.get("transaction_id")
            or not isinstance(lineage, dict)
            or lineage.get("delivery_type") != "git_marketplace"
            or lineage.get("observed_from") != "product-os-manager"
            or receipt.get("installation_id") != journal.get("installation_id")
            or receipt_digest is None
        ):
            return self._failed("installation receipt does not match committed Manager lineage")

        directory = self._directory(journal)
        if not directory.exists():
            return LifecycleAdapterEvidence(
                self.adapter_id,
                "pending",
                "no new Codex startup session has been observed",
                {},
                self.adapter_version,
                self.capability_fingerprint,
            )
        if not directory.is_dir() or directory.is_symlink() or bool(
            getattr(directory, "is_junction", lambda: False)()
        ):
            return self._failed("lifecycle evidence directory is unsafe")
        files = sorted(directory.glob("*.json"))
        if len(files) > MAX_EVENT_FILES:
            return self._failed("lifecycle evidence exceeds the bounded file limit")
        events: list[dict[str, Any]] = []
        for path in files:
            try:
                assert_safe_ancestry(path, self.context.product_os_home)
                if path.stat().st_size > MAX_EVENT_BYTES:
                    raise RuntimeError("event file exceeds the size limit")
                event = read_json(path)
                if not isinstance(event, dict):
                    raise RuntimeError("event file is not a JSON object")
                validate_lifecycle_event(event)
                expected = {
                    "installation_id": journal["installation_id"],
                    "transaction_id": journal["transaction_id"],
                    "project_path_sha256": project_bucket(self.context.project),
                    "receipt_sha256": receipt_digest,
                    "journal_hash": journal["journal_hash"],
                }
                if any(event.get(key) != value for key, value in expected.items()):
                    raise RuntimeError("event does not match the current committed installation")
                events.append(event)
            except Exception as exc:
                return self._failed(f"lifecycle evidence is invalid: {path.name}: {exc}")
        startups = [event for event in events if event.get("startup_observed_at") is not None]
        if not startups:
            return LifecycleAdapterEvidence(
                self.adapter_id,
                "pending",
                "only resume, compact, clear, or end evidence exists; a new startup is required",
                {},
                self.adapter_version,
                self.capability_fingerprint,
            )
        latest = max(
            startups,
            key=lambda event: (str(event["startup_observed_at"]), str(event["session_key_sha256"])),
        )
        return LifecycleAdapterEvidence(
            self.adapter_id,
            "PASS",
            "a privacy-minimized Codex SessionStart(source=startup) matches the committed migration",
            {
                "evidence_sha256": latest["event_hash"],
                "session_key_sha256": latest["session_key_sha256"],
                "startup_observed_at": latest["startup_observed_at"],
                "ended_at": latest.get("ended_at"),
            },
            self.adapter_version,
            self.capability_fingerprint,
        )


__all__ = [
    "CodexSessionLifecycleAdapter",
    "EVENT_SCHEMA",
    "lifecycle_event_schema_path",
    "lifecycle_bucket",
    "project_bucket",
    "validate_lifecycle_event",
]
