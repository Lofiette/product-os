#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from cpt_dist import metadata_budget_for_plugins, validate_plugin

errors=[]
plugins=[ROOT/'payload/marketplace-root/plugins/cpt-core']+sorted(p for p in (ROOT/'domain-packs').glob('cpt-*') if p.is_dir())

if (ROOT/'VERSION').read_text().strip()!='4.0.0-alpha.3': errors.append('VERSION is not 4.0.0-alpha.3')

# Core/plugin validation.
for plugin in plugins:
    try: validate_plugin(plugin)
    except RuntimeError as exc: errors.append(str(exc))

core=plugins[0]
budget=metadata_budget_for_plugins([core])
if budget['estimated_discovery_chars']>2000: errors.append(f"cpt-core metadata unexpectedly large: {budget['estimated_discovery_chars']}")

market=json.loads((ROOT/'payload/marketplace-root/.agents/plugins/marketplace.json').read_text())
entries={x['name']:x for x in market.get('plugins',[])}
if entries.get('cpt-core',{}).get('source',{}).get('path')!='./plugins/cpt-core': errors.append('marketplace source.path must be ./plugins/cpt-core')

agents=(ROOT/'payload/repo-scaffold/AGENTS.md').read_text()
if '<!-- CPT-OS KERNEL BEGIN -->' not in agents or '<!-- CPT-OS KERNEL END -->' not in agents: errors.append('managed AGENTS markers missing')
if len(agents.encode())>6000: errors.append('repo AGENTS loader exceeds 6000-byte guidance target')

# Universal core terminology.
for forbidden in ['ai'+'-web','SOVA'+'_DESIGN_SYSTEM_KIT','Плат'+'форма ОКО']:
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.md','.json','.yaml','.yml','.toml','.py','.txt','.csv'}:
            try:
                if forbidden.lower() in path.read_text(encoding='utf-8').lower(): errors.append(f'project-specific term {forbidden!r} found in {path.relative_to(ROOT)}')
            except UnicodeDecodeError: pass

catalog=json.loads((ROOT/'domain-packs/PACK_CATALOG.json').read_text())
if catalog.get('schema_version')!='cpt-pack-catalog-v3': errors.append('PACK_CATALOG must use cpt-pack-catalog-v3')
if catalog.get('version')!='4.0.0-alpha.3': errors.append('PACK_CATALOG version mismatch')
cat_ids={x['id'] for x in catalog.get('domains',[])}
actual_ids={p.name for p in plugins[1:]}
if cat_ids!=actual_ids: errors.append(f'catalog/domain directory mismatch: {cat_ids ^ actual_ids}')
for item in catalog.get('domains',[]):
    pack_path=ROOT/'domain-packs'/item['id']
    try:
        validated=validate_plugin(pack_path)
        if item.get('skill_count')!=len(validated['skills']): errors.append(f"catalog skill_count mismatch for {item['id']}")
    except RuntimeError as exc: errors.append(str(exc))
for profile in catalog.get('profiles',[]):
    for name in profile.get('packs',[]):
        if name!='cpt-core' and name not in actual_ids: errors.append(f"profile {profile.get('id')} references missing {name}")
    if profile.get('estimated_discovery_chars',0)>7000: errors.append(f"profile {profile.get('id')} exceeds 7000 chars")

# Pack schema inventories and provenance.
registry=json.loads((ROOT/'skills/SKILL_REGISTRY.json').read_text())['skills']
for plugin in plugins:
    pack=json.loads((plugin/'cpt-pack.json').read_text())
    expected=sorted(x['id'] for x in registry if x['plugin']==plugin.name)
    if pack.get('schema_version')!='cpt-pack-v2': errors.append(f'{plugin.name}: old pack schema')
    if pack.get('skill_count')!=len(expected) or sorted(pack.get('skill_ids',[]))!=expected: errors.append(f'{plugin.name}: pack inventory mismatch')
    legacy=pack.get('legacy_source',{})
    if legacy.get('package')!='codex-product-team-3.0-ultra-beta2': errors.append(f'{plugin.name}: missing legacy package provenance')

# Current docs should not claim Alpha 2 as current.
for current in [ROOT/'README.md',ROOT/'README_RU.md',ROOT/'DOMAIN_PACKS.md',ROOT/'AUDIT_REPORT.md',ROOT/'CHANGELOG.md']:
    if current.exists():
        text=current.read_text()
        if 'Codex Product Operating System 4.0 Alpha 2 — Distribution Split Audit' in text: errors.append(f'stale Alpha 2 audit wording in {current.relative_to(ROOT)}')

# Required Alpha 3 assets.
for rel in ['skills/SKILL_REGISTRY.json','migration/SKILL_MIGRATION.json','migration/SKILL_MIGRATION.csv','evaluation/skill-trigger-cases.json','docs/SKILL_AUTHORING_STANDARD.md','docs/SKILL_INVOCATION_POLICY.md']:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')

if errors:
    print('DISTRIBUTION VALIDATION FAILED')
    for error in errors: print('-',error)
    raise SystemExit(1)
print(f"DISTRIBUTION STATIC VALIDATION PASSED; plugins={len(plugins)}, core metadata={budget['estimated_discovery_chars']} chars")
