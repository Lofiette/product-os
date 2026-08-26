from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Mapping

EVENT_SCHEMA = "product-os-codex-lifecycle-event-v1"
ADAPTER_ID = "codex-session-lifecycle"
TRANSACTION_PATTERN = re.compile(
    r"TX-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
UUID_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)
DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")
MAX_EVENT_FILES = 64


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _canonical_hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _file_hash(path: Path, *, canonical_text: bool = False) -> str:
    data = path.read_bytes()
    if canonical_text and b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _path_key(path: Path) -> str:
    value = str(path.resolve())
    return value.casefold() if os.name == "nt" else value


def _within(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    root = root.resolve()
    return resolved == root or root in resolved.parents


def _link_like(path: Path) -> bool:
    if path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)()):
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return bool(attributes & 0x400)


def _safe_ancestry(path: Path, root: Path) -> bool:
    try:
        relative = path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except (OSError, ValueError):
        return False
    current = root.resolve(strict=False)
    if _link_like(current):
        return False
    for part in relative.parts:
        current = current / part
        if _link_like(current):
            return False
    return _within(path, root)


def _try_lock(handle: Any) -> bool:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            return True
        except OSError:
            return False
    import fcntl

    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _unlock(handle: Any) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _atomic_write(path: Path, value: Mapping[str, Any]) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _load_object(path: Path) -> tuple[dict[str, Any], bytes] | None:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return (value, raw) if isinstance(value, dict) else None


def _product_os_home(env: Mapping[str, str]) -> Path | None:
    configured = env.get("PRODUCT_OS_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    user_home = env.get("HOME") or env.get("USERPROFILE")
    return (Path(user_home).expanduser() / ".product-os").resolve() if user_home else None


def record_lifecycle_event(
    project: Path,
    plugin_root: Path,
    payload: Mapping[str, Any],
    *,
    env: Mapping[str, str] | None = None,
    observed_at: str | None = None,
) -> bool:
    """Persist a bounded hash-only lifecycle receipt, or safely do nothing."""

    values = os.environ if env is None else env
    event_name = payload.get("hook_event_name")
    source = payload.get("source") if event_name == "SessionStart" else None
    session_id = payload.get("session_id")
    if event_name not in {"SessionStart", "SessionEnd"}:
        return False
    if event_name == "SessionStart" and source not in {
        "startup",
        "resume",
        "clear",
        "compact",
    }:
        return False
    if not isinstance(session_id, str) or not session_id:
        return False
    product_os_home = _product_os_home(values)
    if product_os_home is None or not product_os_home.is_dir() or _link_like(product_os_home):
        return False
    project = project.resolve()
    plugin_root = plugin_root.resolve()
    receipt_loaded = _load_object(project / ".cpt" / "install.json")
    if receipt_loaded is None:
        return False
    receipt, receipt_raw = receipt_loaded
    manager = receipt.get("manager")
    lineage = receipt.get("source_lineage")
    transaction_id = manager.get("last_transaction_id") if isinstance(manager, dict) else None
    installation_id = receipt.get("installation_id")
    if (
        receipt.get("schema") != "cpt-install-receipt-v2"
        or not isinstance(lineage, dict)
        or lineage.get("delivery_type") != "git_marketplace"
        or lineage.get("observed_from") != "product-os-manager"
        or not isinstance(transaction_id, str)
        or not TRANSACTION_PATTERN.fullmatch(transaction_id)
        or not isinstance(installation_id, str)
        or not UUID_PATTERN.fullmatch(installation_id)
    ):
        return False
    core = next(
        (
            item
            for item in receipt.get("installed_plugins", [])
            if isinstance(item, dict) and item.get("name") == "cpt-core"
        ),
        None,
    )
    expected_plugin_hash = core.get("manifest_sha256") if isinstance(core, dict) else None
    payload_path = core.get("payload_path") if isinstance(core, dict) else None
    running_manifest = plugin_root / ".codex-plugin" / "plugin.json"
    target_manifest = (
        Path(payload_path) / ".codex-plugin" / "plugin.json"
        if isinstance(payload_path, str)
        else None
    )
    try:
        if (
            not isinstance(expected_plugin_hash, str)
            or not DIGEST_PATTERN.fullmatch(expected_plugin_hash)
            or target_manifest is None
            or not _within(target_manifest, product_os_home / "sources")
            or _file_hash(running_manifest, canonical_text=True) != expected_plugin_hash
            or _file_hash(target_manifest, canonical_text=True) != expected_plugin_hash
        ):
            return False
    except OSError:
        return False

    project_hash = hashlib.sha256(_path_key(project).encode("utf-8")).hexdigest()
    journal_path = (
        product_os_home
        / "transactions"
        / project_hash
        / transaction_id
        / "journal.json"
    )
    journal_loaded = _load_object(journal_path)
    if journal_loaded is None:
        return False
    journal, _journal_raw = journal_loaded
    journal_hash = journal.get("journal_hash")
    hashable_journal = dict(journal)
    hashable_journal.pop("journal_hash", None)
    context = journal.get("context")
    if (
        journal.get("state") != "committed"
        or journal.get("transaction_id") != transaction_id
        or journal.get("installation_id") != installation_id
        or _path_key(Path(str(journal.get("project")))) != _path_key(project)
        or not isinstance(context, dict)
        or _path_key(Path(str(context.get("product_os_home"))))
        != _path_key(product_os_home)
        or not isinstance(journal_hash, str)
        or not DIGEST_PATTERN.fullmatch(journal_hash)
        or journal_hash != _canonical_hash(hashable_journal)
    ):
        return False

    timestamp = observed_at
    if timestamp is None:
        from datetime import datetime, timezone

        timestamp = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    if not isinstance(timestamp, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",
        timestamp,
    ):
        return False
    session_key = hashlib.sha256(
        (installation_id + "\0" + session_id).encode("utf-8")
    ).hexdigest()
    directory = (
        product_os_home
        / "lifecycle"
        / "codex"
        / hashlib.sha256(
            (_path_key(project) + "\0" + transaction_id).encode("utf-8")
        ).hexdigest()[:32]
    )
    event_path = directory / f"{session_key[:32]}.json"
    lock_path = directory / ".lock"
    if not _safe_ancestry(event_path, product_os_home) or not _safe_ancestry(
        lock_path, product_os_home
    ):
        return False
    directory.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock_path.open("a+b")
    except OSError:
        return False
    locked = False
    try:
        locked = _try_lock(handle)
        if not locked:
            return False
        existing_loaded = _load_object(event_path) if event_path.exists() else None
        existing = existing_loaded[0] if existing_loaded is not None else None
        identity = {
            "schema": EVENT_SCHEMA,
            "adapter": ADAPTER_ID,
            "installation_id": installation_id,
            "transaction_id": transaction_id,
            "project_path_sha256": project_hash,
            "session_key_sha256": session_key,
            "receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "journal_hash": journal_hash,
        }
        if existing is not None and any(
            existing.get(key) != value for key, value in identity.items()
        ):
            return False
        event_files = sorted(
            directory.glob("*.json"),
            key=lambda path: (path.stat().st_mtime_ns, path.name),
        )
        startup_files: list[tuple[str, int, str, Path]] = []
        for candidate in event_files:
            loaded = _load_object(candidate)
            startup = loaded[0].get("startup_observed_at") if loaded is not None else None
            if isinstance(startup, str):
                startup_files.append(
                    (startup, candidate.stat().st_mtime_ns, candidate.name, candidate)
                )
        protected_startup = max(startup_files)[3] if startup_files else None
        keep_before_write = MAX_EVENT_FILES if event_path.exists() else MAX_EVENT_FILES - 1
        remove_count = max(0, len(event_files) - keep_before_write)
        removable = [
            path
            for path in event_files
            if path != event_path and path != protected_startup
        ]
        for stale in removable[:remove_count]:
            stale.unlink()
        event = {
            **identity,
            "startup_observed_at": (
                timestamp
                if event_name == "SessionStart" and source == "startup"
                else existing.get("startup_observed_at") if existing else None
            ),
            "ended_at": (
                timestamp
                if event_name == "SessionEnd"
                else existing.get("ended_at") if existing else None
            ),
            "last_event": event_name,
            "last_source": source,
            "last_observed_at": timestamp,
        }
        event["event_hash"] = _canonical_hash(event)
        _atomic_write(event_path, event)
        return True
    except (OSError, ValueError, TypeError):
        return False
    finally:
        if locked:
            try:
                _unlock(handle)
            except OSError:
                pass
        handle.close()


__all__ = ["record_lifecycle_event"]
