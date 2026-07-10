
#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
