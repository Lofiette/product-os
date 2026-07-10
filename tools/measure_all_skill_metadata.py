#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
plugins = [ROOT / 'payload/marketplace-root/plugins/cpt-core'] + sorted((ROOT / 'domain-packs').glob('cpt-*'))


def plugin_metadata(path: Path) -> dict:
    total = 0
    count = 0
    for file in sorted((path / 'skills').glob('*/SKILL.md')):
        text = file.read_text(encoding='utf-8')
        end = text.find('\n---\n', 4)
        fm = yaml.safe_load(text[4:end])
        entry = f"{fm['name']}\n{fm['description']}\n{path.name}/skills/{fm['name']}/SKILL.md"
        total += len(entry)
        count += 1
    return {'plugin': path.name, 'skills': count, 'estimated_discovery_chars': total}

reports = [plugin_metadata(path) for path in plugins]
by_name = {item['plugin']: item for item in reports}
profiles = {
    'core_only': ['cpt-core'],
    'product_discovery': ['cpt-core', 'cpt-product-research'],
    'ui_implementation': ['cpt-core', 'cpt-design-ui', 'cpt-engineering'],
    'engineering_change': ['cpt-core', 'cpt-engineering'],
    'risk_sensitive_change': ['cpt-core', 'cpt-engineering', 'cpt-risk-operations'],
    'ai_product': ['cpt-core', 'cpt-product-research', 'cpt-ai-agentic', 'cpt-risk-operations'],
}
profile_reports = []
errors = []
for name, enabled in profiles.items():
    value = sum(by_name[item]['estimated_discovery_chars'] for item in enabled)
    profile_reports.append({'profile': name, 'plugins': enabled, 'estimated_discovery_chars': value})
    if value > 8000:
        errors.append(f'{name} exceeds 8000 chars: {value}')
for item in reports:
    if item['estimated_discovery_chars'] > 3500:
        errors.append(f"{item['plugin']} exceeds 3500 chars: {item['estimated_discovery_chars']}")
all_chars = sum(item['estimated_discovery_chars'] for item in reports)
result = {
    'plugins': reports,
    'profiles': profile_reports,
    'all_plugins_chars': all_chars,
    'all_plugins_warning': all_chars > 8000,
    'all_plugins_note': 'All optional packs are not intended to be enabled simultaneously; select packs by task domain.',
    'errors': errors,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 2)
