from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


_PROCESS_LOCK_GUARD = threading.Lock()
_PROCESS_LOCKS: set[str] = set()


def _lock_key(path: Path) -> str:
    value = str(path.absolute())
    return value.casefold() if os.name == "nt" else value


def _acquire_os_lock(handle: Any) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise RuntimeError("State lock is already held") from exc
        return
    import fcntl

    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        raise RuntimeError("State lock is already held") from exc


def _release_os_lock(handle: Any) -> None:
    handle.seek(0)
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return
    import fcntl

    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_json_hash(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text_file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    data = path.read_bytes()
    if b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def exclusive_lock(path: Path) -> Iterator[None]:
    """Hold a process-scoped lock that the OS releases after a hard crash.

    The small lock file is intentionally persistent. Its existence is not lock
    ownership; only the operating-system byte/range lock is authoritative.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    token = f"{os.getpid()}:{uuid.uuid4()}:{utc_now()}"
    key = _lock_key(path)
    with _PROCESS_LOCK_GUARD:
        if key in _PROCESS_LOCKS:
            raise RuntimeError(f"State lock is already held: {path}")
        _PROCESS_LOCKS.add(key)
    handle = None
    locked = False
    try:
        handle = path.open("a+b")
        try:
            _acquire_os_lock(handle)
            locked = True
        except RuntimeError as exc:
            raise RuntimeError(f"State lock is already held: {path}") from exc
        handle.seek(0)
        handle.write(("\0" + token + "\n").encode("utf-8"))
        handle.truncate()
        handle.flush()
        os.fsync(handle.fileno())
        yield
    finally:
        try:
            if locked and handle is not None:
                _release_os_lock(handle)
        finally:
            if handle is not None:
                handle.close()
            with _PROCESS_LOCK_GUARD:
                _PROCESS_LOCKS.discard(key)


def lock_is_held(path: Path) -> bool:
    """Return true only for a live OS lock, not for a stale lock file."""

    with _PROCESS_LOCK_GUARD:
        if _lock_key(path) in _PROCESS_LOCKS:
            return True
    try:
        handle = path.open("r+b")
    except FileNotFoundError:
        return False
    try:
        try:
            _acquire_os_lock(handle)
        except RuntimeError:
            return True
        _release_os_lock(handle)
        return False
    finally:
        handle.close()
