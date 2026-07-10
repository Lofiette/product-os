#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from cpt_dist import metadata_budget_for_plugins, validate_plugin

errors = []
plugin = ROOT / 'payload' / 'marketplace-root' / 'plugins' / 'cpt-core'
try:
    validate_plugin(plugin)
except RuntimeError as exc:
    errors.append(str(exc))

budget = metadata_budget_for_plugins([plugin])
if budget['estimated_discovery_chars'] > 2000:
    errors.append(f"cpt-core metadata unexpectedly large: {budget['estimated_discovery_chars']}")

market = json.loads((ROOT / 'payload' / 'marketplace-root' / '.agents' / 'plugins' / 'marketplace.json').read_text())
if market['plugins'][0]['source']['path'] != './plugins/cpt-core':
    errors.append('marketplace source.path must be ./plugins/cpt-core')

agents = (ROOT / 'payload' / 'repo-scaffold' / 'AGENTS.md').read_text()
if '<!-- CPT-OS KERNEL BEGIN -->' not in agents or '<!-- CPT-OS KERNEL END -->' not in agents:
    errors.append('managed AGENTS markers missing')
if len(agents.encode()) > 6000:
    errors.append('repo AGENTS loader exceeds 6000-byte guidance target')

for forbidden in ['ai' + '-web', 'SOVA' + '_DESIGN_SYSTEM_KIT', 'Плат' + 'форма ОКО']:
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.md', '.json', '.yaml', '.yml', '.toml', '.py', '.txt'}:
            try:
                if forbidden.lower() in path.read_text(encoding='utf-8').lower():
                    errors.append(f'project-specific term {forbidden!r} found in {path.relative_to(ROOT)}')
            except UnicodeDecodeError:
                pass

if errors:
    print('DISTRIBUTION VALIDATION FAILED')
    for error in errors:
        print(f'- {error}')
    raise SystemExit(1)
print(f"DISTRIBUTION STATIC VALIDATION PASSED; core metadata={budget['estimated_discovery_chars']} chars")
