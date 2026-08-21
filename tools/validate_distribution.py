#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from cpt_dist import metadata_budget_for_plugins, validate_plugin

errors=[]
plugins=[ROOT/'payload/marketplace-root/plugins/cpt-core']+sorted(p for p in (ROOT/'domain-packs').glob('cpt-*') if p.is_dir())

if (ROOT/'VERSION').read_text().strip()!='4.0.0': errors.append('VERSION is not 4.0.0')

pyproject_text = (ROOT/'pyproject.toml').read_text(encoding='utf-8')
if 'version = "4.0.0b1"' not in pyproject_text: errors.append('pyproject project.version is not 4.0.0b1')
if 'package_version = "4.0.0"' not in pyproject_text: errors.append('pyproject CPT package_version mismatch')
if (ROOT/'ALPHA8_LIMITATIONS.md').exists(): errors.append('stale current-release filename ALPHA8_LIMITATIONS.md')
if (ROOT/'docs/ALPHA9_RELEASE_INTEGRATION.md').exists(): errors.append('stale current-release filename ALPHA9_RELEASE_INTEGRATION.md')

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
if catalog.get('version')!='4.0.0': errors.append('PACK_CATALOG version mismatch')
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
    if pack.get('role_model')!='logical_lenses_in_cpt_core_references': errors.append(f'{plugin.name}: missing role_model')
    if pack.get('role_count')!=len(pack.get('role_ids',[])): errors.append(f'{plugin.name}: role_count mismatch')

# Optional worker pack validation.
worker_pack=json.loads((ROOT/'payload/worker-pack/worker-pack.json').read_text())
worker_agents=sorted((ROOT/'payload/worker-pack/agents').glob('*.toml'))
if worker_pack.get('version')!='4.0.0': errors.append('worker pack version mismatch')
if worker_pack.get('agent_count')!=10 or len(worker_agents)!=10: errors.append('worker pack must contain 10 agents')
registry_workers=json.loads((ROOT/'orchestration/WORKER_ARCHETYPES.json').read_text())
if registry_workers.get('archetype_count')!=10: errors.append('worker archetype registry count mismatch')
if {p.stem for p in worker_agents}!={x['id'] for x in registry_workers.get('archetypes',[])}: errors.append('worker pack/archetype registry mismatch')

# Current docs should not claim Alpha 2 as current.
for current in [ROOT/'README.md',ROOT/'README_RU.md',ROOT/'DOMAIN_PACKS.md',ROOT/'AUDIT_REPORT.md',ROOT/'CHANGELOG.md']:
    if current.exists():
        text=current.read_text()
        if 'Codex Product Operating System 4.0 Alpha 2 — Distribution Split Audit' in text: errors.append(f'stale Alpha 2 audit wording in {current.relative_to(ROOT)}')

# Required Beta 1 assets.
for rel in [
    'skills/SKILL_REGISTRY.json','migration/SKILL_MIGRATION.json','migration/SKILL_MIGRATION.csv',
    'evaluation/skill-trigger-cases.json','docs/SKILL_AUTHORING_STANDARD.md','docs/SKILL_INVOCATION_POLICY.md',
    'roles/ROLE_REGISTRY.json','roles/ROLE_ROUTING_PROFILES.json','roles/GATE_REGISTRY.json',
    'migration/ROLE_MIGRATION.json','evaluation/role-trigger-cases.json','evaluation/role-routing-cases.json',
    'docs/ROLE_SOURCES.md','ROLES.md',
    'orchestration/WORKER_ARCHETYPES.json','payload/worker-pack/worker-pack.json',
    'payload/worker-pack/config/agents.example.toml','payload/repo-scaffold/.cpt/bin/cpt_orchestration.py',
    'ORCHESTRATION.md','WORKER_PACK.md','EVALUATION_LIMITATIONS.md','EVALUATION.md','AUDIT_REPORT.md',
    'evaluation/orchestration-cases.json','evaluation/orchestration-integration-report.json',
    'evaluation/behavior-test-report.json','tools/validate_orchestration.py','tools/eval_orchestration.py',
    'tools/run_orchestration_integration.py','tools/build_manifest.py','tests/test_orchestration.py',
    'tools/cpt_eval.py','tools/validate_evaluation.py','tests/test_evaluation.py',
    'evaluation/executable/SUITES.json','evaluation/executable/baselines/offline-core-alpha8.json',
    'evaluation/executable/mutations/offline-core-alpha8-mutations.json',
    '.github/workflows/offline-evals.yml','.github/workflows/live-smoke.yml',
    'docs/ALPHA7_TO_ALPHA8.md',
    'release/GATES.json','release/TRIALS.json','release/schemas/release-scorecard.schema.json',
    'release/schemas/release-readiness.schema.json','tools/cpt_release.py','tools/validate_release.py',
    'tests/test_release.py','docs/RC_TRIALS_AND_RELEASE_GATES.md','docs/BETA1_RELEASE_INTEGRATION.md','BETA1_LIMITATIONS.md'
]:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')

# Package manifest integrity.
manifest_path = ROOT / 'MANIFEST.json'
if not manifest_path.exists():
    errors.append('missing MANIFEST.json')
else:
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema') != 'cpt-package-manifest-v9': errors.append('MANIFEST schema mismatch')
    if manifest.get('version') != '4.0.0': errors.append('MANIFEST version mismatch')
    if manifest.get('phase') != 'rc-trials-offline-beta': errors.append('MANIFEST phase mismatch')
    inventories = manifest.get('inventories', {})
    expected_inventories = {
        'behavior_tests': 115,
        'evaluation_unit_tests': 13,
        'migration_tests': 7,
        'release_unit_tests': 10,
        'release_tracks': 33,
        'release_gates': 9,
        'executable_evaluation_cases': 21,
        'fixture_repositories': 6,
        'evaluation_suites': 4,
        'mutation_cases': 4,
    }
    for key, value in expected_inventories.items():
        if inventories.get(key) != value:
            errors.append(f'MANIFEST inventory mismatch for {key}: {inventories.get(key)!r} != {value}')
    listed = {item.get('path'): item for item in manifest.get('files', [])}
    actual = {}
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if path.name == 'MANIFEST.json' or path.suffix in {'.pyc', '.pyo'}:
            continue
        if any(part in {'__pycache__', '.git', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cpt-eval-runs', '.cpt-eval-live'} for part in rel.parts):
            continue
        if rel.parts[:3] == ('evaluation', 'executable', 'reports') and path.name != '.gitkeep':
            continue
        if path.name.endswith('-comparison.json'):
            continue
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        actual[rel.as_posix()] = {'size': path.stat().st_size, 'sha256': h}
    if manifest.get('file_count') != len(actual): errors.append('MANIFEST file_count mismatch')
    if set(listed) != set(actual): errors.append(f"MANIFEST path mismatch: {sorted(set(listed) ^ set(actual))[:10]}")
    for rel, item in actual.items():
        if rel in listed and (listed[rel].get('size') != item['size'] or listed[rel].get('sha256') != item['sha256']):
            errors.append(f'MANIFEST hash/size mismatch: {rel}')
            break

if errors:
    print('DISTRIBUTION VALIDATION FAILED')
    for error in errors: print('-',error)
    raise SystemExit(1)
print(f"DISTRIBUTION STATIC VALIDATION PASSED; plugins={len(plugins)}, core metadata={budget['estimated_discovery_chars']} chars")
