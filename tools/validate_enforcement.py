
#!/usr/bin/env python3
from __future__ import annotations
import ast, json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
    ROOT/'payload/repo-scaffold/.cpt/enforcement.yaml',
    ROOT/'payload/marketplace-root/plugins/cpt-core/hooks/hooks.json',
    ROOT/'payload/marketplace-root/plugins/cpt-core/hooks/cpt_hook.py',
    ROOT/'policies/rules/cpt-conservative.rules',
    ROOT/'policies/rules/cpt-strict.rules',
    ROOT/'ENFORCEMENT.md',
]
for path in required:
    if not path.exists(): errors.append(f'missing {path.relative_to(ROOT)}')
try:
    config=yaml.safe_load(required[0].read_text());
    if config.get('mode') not in {'off','audit','enforce'}: errors.append('invalid enforcement mode')
except Exception as exc: errors.append(f'enforcement yaml: {exc}')
try:
    hooks=json.loads(required[1].read_text())['hooks']
    expected={'SessionStart','PreToolUse','PermissionRequest','PostToolUse','PreCompact','PostCompact','SubagentStart','SubagentStop','Stop'}
    if set(hooks)!=expected: errors.append(f'hook events mismatch: {set(hooks)^expected}')
except Exception as exc: errors.append(f'hooks json: {exc}')
try: ast.parse(required[2].read_text(encoding='utf-8'))
except Exception as exc: errors.append(f'hook wrapper syntax: {exc}')
for path in [required[3],required[4]]:
    text=path.read_text();
    if 'prefix_rule(' not in text or 'match = [' not in text: errors.append(f'incomplete rules file {path.name}')
if errors:
    for error in errors: print('ERROR:',error)
    raise SystemExit(1)
print('ENFORCEMENT ASSET VALIDATION PASSED')
