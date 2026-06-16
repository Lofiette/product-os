#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, hashlib
ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(path):
    if not (ROOT/path).exists():
        errors.append(f"Missing {path}")

def read(path):
    return (ROOT/path).read_text(encoding='utf-8')

def load(path):
    return json.loads(read(path))

required = [
    'AGENTS.md','README.md','FIRST_PROMPT.md','docs/PRODUCT_KNOWLEDGE_SYSTEM.md','docs/PRODUCT_ONBOARDING.md','docs/BOUNDED_DISCOVERY.md','docs/FRAMEWORK_LOADING_POLICY.md','docs/API_DATA_SHAPE_PREWARM.md','docs/GREENFIELD_PRODUCT_MODE.md','docs/REDESIGN_MIGRATION_MODE.md','docs/IMPACT_MAP_PROTOCOL.md','docs/NEW_TASK_PROTOCOL.md','docs/CHRONICLE_COMPACTION.md','kernel/AGENTS.override.template.md','product-knowledge/templates/PRODUCT_MAP.template.md','framework/FRAMEWORK_INDEX.md','audits/AUDIT_CHECKLIST.md','docs/ROLE_ROUTING_MATRIX.md','docs/SKILL_ROUTING_MATRIX.md'
]
for pth in required:
    check(pth)
roles = load('docs/ROLE_INDEX.json')['roles']
skills = load('docs/SKILL_INDEX.json')['skills']
scenarios = load('docs/SCENARIO_TESTS.json')['scenarios']
role_ids = {r['id'] for r in roles}
skill_ids = {s['id'] for s in skills}
for rid in ['frontend_engineer','frontend_architect','product_designer','design_engineer','api_contract_guardian','chronicle_keeper']:
    if rid not in role_ids:
        errors.append(f'Missing required role {rid}')
for sid in ['new-task-protocol','bounded-discovery','impact-map','product-knowledge-onboarding','knowledge-update','api-data-shape-prewarm','framework-loading','greenfield-onboarding','knowledge-freshness-review','chronicle-compaction','frontend-integration-review']:
    if sid not in skill_ids:
        errors.append(f'Missing required skill {sid}')
    check(f'.agents/skills/{sid}/SKILL.md')
if len(role_ids) < 50:
    errors.append(f'Expected at least 50 roles including preserved 49 + frontend_engineer, got {len(role_ids)}')
# universal docs should not bake in project-specific DS names
for pth in ['AGENTS.md','docs/PRODUCT_KNOWLEDGE_SYSTEM.md','docs/BOUNDED_DISCOVERY.md','docs/FRAMEWORK_LOADING_POLICY.md']:
    if re.search(r'SOVA|Sova|sova_', read(pth)):
        errors.append(f'Project-specific design system name found in universal doc {pth}')
# soft artifact-size policy
text = read('AGENTS.md') + read('docs/KNOWLEDGE_MAP_POLICY.md') + read('docs/PRODUCT_KNOWLEDGE_SYSTEM.md')
if not re.search(r'not hard (caps|truncation)|guidance ranges', text, re.I):
    errors.append('Soft target size policy missing')
# stale labels outside archive
stale = re.compile(r'codex-product-team-2\.0|2\.0 beta|2\.1 beta|2\.1-beta|v2\.0|required v2\.0', re.I)
for file in ROOT.rglob('*'):
    if not file.is_file():
        continue
    rel = file.relative_to(ROOT).as_posix()
    if rel.startswith('archive/') or rel.endswith('.zip'):
        continue
    if file.suffix.lower() not in {'.md','.json','.toml','.py','.txt'}:
        continue
    txt = file.read_text(encoding='utf-8', errors='ignore')
    if stale.search(txt):
        errors.append(f'Stale 2.x label outside archive: {rel}')
# routing must mention critical 3.0 assets
role_routing = read('docs/ROLE_ROUTING_MATRIX.md')
skill_routing = read('docs/SKILL_ROUTING_MATRIX.md')
for term in ['frontend_engineer','Runtime Kernel','Product Knowledge','API-dependent UI']:
    if term not in role_routing:
        errors.append(f'ROLE_ROUTING_MATRIX missing {term}')
for term in ['new-task-protocol','bounded-discovery','impact-map','api-data-shape-prewarm','knowledge-update','framework-loading']:
    if term not in skill_routing:
        errors.append(f'SKILL_ROUTING_MATRIX missing {term}')
# role metadata
for r in roles:
    for key in ['default_execution','spawn_policy','load_cost','primary_task_types']:
        if key not in r:
            errors.append(f'Role {r.get("id")} missing staged-loading metadata {key}')
# scenario markdown sync
scenario_ids = {s['id'] for s in scenarios}
md_ids = {p.stem for p in (ROOT/'docs/scenario_tests').glob('*.md')}
if scenario_ids != md_ids:
    errors.append(f'Scenario markdown/JSON mismatch: missing={sorted(scenario_ids-md_ids)} extra={sorted(md_ids-scenario_ids)}')
# critical scenarios
for sid in ['existing_product_knowledge_onboarding','new_task_safe_autonomy','greenfield_product_start','api_data_shape_prewarm']:
    if sid not in scenario_ids:
        errors.append(f'Missing 3.0 scenario {sid}')
if errors:
    print('3.0 VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)
print(f'3.0 VALIDATION PASSED: {len(role_ids)} roles, {len(skill_ids)} skills, {len(scenarios)} scenarios.')
