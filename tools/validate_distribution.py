#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_manifest import canonical_bytes
from cpt_dist import metadata_budget_for_plugins, validate_plugin

errors=[]
plugins=[ROOT/'payload/marketplace-root/plugins/cpt-core']+sorted(p for p in (ROOT/'domain-packs').glob('cpt-*') if p.is_dir())

if (ROOT/'VERSION').read_text(encoding='utf-8').strip()!='4.1.0': errors.append('VERSION is not 4.1.0')

pyproject_text = (ROOT/'pyproject.toml').read_text(encoding='utf-8')
if 'version = "4.1.0"' not in pyproject_text: errors.append('pyproject project.version is not 4.1.0')
if 'package_version = "4.1.0"' not in pyproject_text: errors.append('pyproject CPT package_version mismatch')
if (ROOT/'ALPHA8_LIMITATIONS.md').exists(): errors.append('stale current-release filename ALPHA8_LIMITATIONS.md')
if (ROOT/'docs/ALPHA9_RELEASE_INTEGRATION.md').exists(): errors.append('stale current-release filename ALPHA9_RELEASE_INTEGRATION.md')

# Core/plugin validation.
for plugin in plugins:
    try: validate_plugin(plugin)
    except RuntimeError as exc: errors.append(str(exc))

core=plugins[0]
budget=metadata_budget_for_plugins([core])
if budget['estimated_discovery_chars']>2000: errors.append(f"cpt-core metadata unexpectedly large: {budget['estimated_discovery_chars']}")

market=json.loads((ROOT/'payload/marketplace-root/.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
entries={x['name']:x for x in market.get('plugins',[])}
if entries.get('cpt-core',{}).get('source',{}).get('path')!='./plugins/cpt-core': errors.append('marketplace source.path must be ./plugins/cpt-core')

# Repository marketplace validation for local and Git-backed Codex installation.
root_market_path = ROOT / '.agents' / 'plugins' / 'marketplace.json'
if not root_market_path.exists():
    errors.append('missing repository marketplace .agents/plugins/marketplace.json')
else:
    root_market = json.loads(root_market_path.read_text(encoding='utf-8'))
    if root_market.get('name') != 'product-os':
        errors.append('repository marketplace name must be product-os')
    root_entries = {item.get('name'): item for item in root_market.get('plugins', [])}
    expected_market_plugins = {p.name for p in plugins}
    if set(root_entries) != expected_market_plugins:
        errors.append(f'repository marketplace plugin mismatch: {set(root_entries) ^ expected_market_plugins}')
    for name, entry in root_entries.items():
        source = entry.get('source', {})
        source_path = source.get('path')
        if source.get('source') != 'local' or not isinstance(source_path, str) or not source_path.startswith('./'):
            errors.append(f'{name}: invalid repository marketplace source')
            continue
        target = (ROOT / source_path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f'{name}: repository marketplace path escapes repository')
            continue
        if not (target / '.codex-plugin' / 'plugin.json').exists():
            errors.append(f'{name}: repository marketplace path does not contain a plugin manifest')

agents=(ROOT/'payload/repo-scaffold/AGENTS.md').read_text(encoding='utf-8')
if '<!-- CPT-OS KERNEL BEGIN -->' not in agents or '<!-- CPT-OS KERNEL END -->' not in agents: errors.append('managed AGENTS markers missing')
if len(agents.encode())>6000: errors.append('repo AGENTS loader exceeds 6000-byte guidance target')

# Universal core terminology.
for forbidden in ['ai'+'-web','SOVA'+'_DESIGN_SYSTEM_KIT','Плат'+'форма ОКО']:
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.md','.json','.yaml','.yml','.toml','.py','.txt','.csv'}:
            try:
                if forbidden.lower() in path.read_text(encoding='utf-8').lower(): errors.append(f'project-specific term {forbidden!r} found in {path.relative_to(ROOT)}')
            except UnicodeDecodeError: pass

catalog=json.loads((ROOT/'domain-packs/PACK_CATALOG.json').read_text(encoding='utf-8'))
if catalog.get('schema_version')!='cpt-pack-catalog-v3': errors.append('PACK_CATALOG must use cpt-pack-catalog-v3')
if catalog.get('version')!='4.1.0': errors.append('PACK_CATALOG version mismatch')
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
registry=json.loads((ROOT/'skills/SKILL_REGISTRY.json').read_text(encoding='utf-8'))['skills']
for plugin in plugins:
    pack=json.loads((plugin/'cpt-pack.json').read_text(encoding='utf-8'))
    expected=sorted(x['id'] for x in registry if x['plugin']==plugin.name)
    if pack.get('schema_version')!='cpt-pack-v2': errors.append(f'{plugin.name}: old pack schema')
    if pack.get('skill_count')!=len(expected) or sorted(pack.get('skill_ids',[]))!=expected: errors.append(f'{plugin.name}: pack inventory mismatch')
    legacy=pack.get('legacy_source',{})
    if legacy.get('package')!='codex-product-team-3.0-ultra-beta2': errors.append(f'{plugin.name}: missing legacy package provenance')
    if pack.get('role_model')!='logical_lenses_in_cpt_core_references': errors.append(f'{plugin.name}: missing role_model')
    if pack.get('role_count')!=len(pack.get('role_ids',[])): errors.append(f'{plugin.name}: role_count mismatch')

# Optional worker pack validation.
worker_pack=json.loads((ROOT/'payload/worker-pack/worker-pack.json').read_text(encoding='utf-8'))
worker_agents=sorted((ROOT/'payload/worker-pack/agents').glob('*.toml'))
if worker_pack.get('version')!='4.1.0': errors.append('worker pack version mismatch')
if worker_pack.get('agent_count')!=10 or len(worker_agents)!=10: errors.append('worker pack must contain 10 agents')
registry_workers=json.loads((ROOT/'orchestration/WORKER_ARCHETYPES.json').read_text(encoding='utf-8'))
if registry_workers.get('archetype_count')!=10: errors.append('worker archetype registry count mismatch')
if {p.stem for p in worker_agents}!={x['id'] for x in registry_workers.get('archetypes',[])}: errors.append('worker pack/archetype registry mismatch')

# Current docs should not claim Alpha 2 as current.
for current in [ROOT/'README.md',ROOT/'README_RU.md',ROOT/'DOMAIN_PACKS.md',ROOT/'AUDIT_REPORT.md',ROOT/'CHANGELOG.md']:
    if current.exists():
        text=current.read_text(encoding='utf-8')
        if 'Codex Product Operating System 4.0 Alpha 2 — Distribution Split Audit' in text: errors.append(f'stale Alpha 2 audit wording in {current.relative_to(ROOT)}')

# Required current and historical release assets.
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
    'tests/test_release.py','docs/RC_TRIALS_AND_RELEASE_GATES.md','docs/BETA1_RELEASE_INTEGRATION.md','KNOWN_LIMITATIONS.md',
    'docs/MIGRATION_4.0_TO_4.1.md','docs/VERSIONING_AND_GIT.md','docs/PLUGIN_AND_MARKETPLACE.md',
    'scripts/product-os.ps1','scripts/register-codex-marketplace.ps1','.agents/plugins/marketplace.json',
    'manager/schemas/installation-receipt-v2.schema.json','tests/test_receipts.py',
    'manager/schemas/installation-registry-v1.schema.json','tests/test_manager_registry.py',
    'manager/schemas/detection-report-v1.schema.json','manager/schemas/adoption-plan-v1.schema.json',
    'manager/schemas/backup-manifest-v1.schema.json','manager/schemas/adoption-transaction-v1.schema.json',
    'manager/schemas/migration-doctor-report-v1.schema.json','manager/product_os_manager/doctor.py',
    'manager/schemas/codex-lifecycle-event-v1.schema.json',
    'manager/product_os_manager/adapters/base.py','manager/product_os_manager/adapters/repository.py',
    'manager/product_os_manager/adapters/codex.py','manager/product_os_manager/adapters/codex_lifecycle.py',
    'payload/marketplace-root/plugins/cpt-core/hooks/product_os_lifecycle.py',
    'manager/product_os_manager/backup.py','manager/product_os_manager/transaction.py',
    'tests/test_manager_planning.py','tests/test_manager_backup.py','tests/test_manager_transaction.py',
    'tests/test_manager_git_provider.py','tests/test_manager_codex_adapter.py',
    'tests/test_manager_lifecycle.py','tests/test_manager_cli.py',
    'tools/product_os_manager.py',
    'docs/INSTALLATION_RECEIPT_V2.md','docs/INSTALLATION_REGISTRY.md','docs/PRODUCT_OS_MANAGER.md'
]:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')

for rel in [
    'manager/schemas/installation-receipt-v2.schema.json',
    'manager/schemas/installation-registry-v1.schema.json',
    'manager/schemas/detection-report-v1.schema.json',
    'manager/schemas/adoption-plan-v1.schema.json',
    'manager/schemas/backup-manifest-v1.schema.json',
    'manager/schemas/adoption-transaction-v1.schema.json',
    'manager/schemas/migration-doctor-report-v1.schema.json',
    'manager/schemas/codex-lifecycle-event-v1.schema.json',
]:
    try:
        Draft202012Validator.check_schema(json.loads((ROOT/rel).read_text(encoding='utf-8')))
    except Exception as exc:
        errors.append(f'invalid JSON schema {rel}: {exc}')

# Package manifest integrity.
manifest_path = ROOT / 'MANIFEST.json'
if not manifest_path.exists():
    errors.append('missing MANIFEST.json')
else:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'cpt-package-manifest-v10': errors.append('MANIFEST schema mismatch')
    if manifest.get('version') != '4.1.0': errors.append('MANIFEST version mismatch')
    if manifest.get('phase') != 'offline-certified-live-pending': errors.append('MANIFEST phase mismatch')
    inventories = manifest.get('inventories', {})
    expected_inventories = {
        'behavior_tests': 198,
        'installation_receipt_tests': 5,
        'manager_registry_tests': 7,
        'manager_planning_tests': 11,
        'manager_backup_tests': 5,
        'manager_transaction_tests': 20,
        'manager_git_provider_tests': 8,
        'manager_codex_adapter_tests': 16,
        'manager_lifecycle_tests': 6,
        'manager_cli_tests': 4,
        'evaluation_unit_tests': 13,
        'migration_tests': 7,
        'release_unit_tests': 10,
        'release_tracks': 35,
        'release_gates': 11,
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
        if len(rel.parts) == 1 and rel.name == 'AGENTS.md':
            continue
        if rel.parts and rel.parts[0] in {'.cpt', '.runtime'}:
            continue
        if any(part in {'__pycache__', '.git', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cpt-eval-runs', '.cpt-eval-live'} for part in rel.parts):
            continue
        if rel.parts[:3] == ('evaluation', 'executable', 'reports') and path.name != '.gitkeep':
            continue
        if path.name.endswith('-comparison.json'):
            continue
        data = canonical_bytes(path)
        h = hashlib.sha256(data).hexdigest()
        actual[rel.as_posix()] = {'size': len(data), 'sha256': h}
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
