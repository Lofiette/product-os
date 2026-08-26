
#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from product_os_lifecycle import record_lifecycle_event


def find_runtime(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / '.cpt' / 'runtime.yaml').exists():
            return candidate
    return None


def main() -> int:
    raw = sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode('utf-8')) if raw else {}
    except Exception:
        payload = {}
    cwd = Path(payload.get('cwd') or Path.cwd())
    root = find_runtime(cwd)
    if root is None:
        return 0
    plugin_root = Path(__file__).resolve().parents[1]
    if payload.get('hook_event_name') == 'SessionEnd':
        try:
            record_lifecycle_event(root, plugin_root, payload)
        except Exception:
            pass
        return 0
    runtime = root / '.cpt' / 'bin' / 'cpt_runtime.py'
    if not runtime.exists():
        return 0
    completed = subprocess.run(
        [sys.executable, str(runtime), '--root', str(root), 'hook-handle'],
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    sys.stdout.buffer.write(completed.stdout)
    sys.stderr.buffer.write(completed.stderr)
    if completed.returncode == 0 and payload.get('hook_event_name') == 'SessionStart':
        try:
            record_lifecycle_event(root, plugin_root, payload)
        except Exception:
            pass
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
