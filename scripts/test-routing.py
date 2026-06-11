#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
roles = {r['id'] for r in json.loads((ROOT/'docs/ROLE_INDEX.json').read_text())['roles']}
skills = {s['id'] for s in json.loads((ROOT/'docs/SKILL_INDEX.json').read_text())['skills']}
scenarios = json.loads((ROOT/'docs/SCENARIO_TESTS.json').read_text())['scenarios']
errors=[]

known_behavior_fields = {
    'max_questions','expected_complexity','expected_mode','expected_ds_mode','expected_orchestration',
    'expected_first_step','max_roles','max_active_roles','max_spawned_agents_default',
    'requires_approval_before_spawn','requires_approval_if','must_not_spawn_without_approval',
    'must_not_implement','must_not_implement_without_approval','must_not_implement_before_reference_spec',
    'must_use_phased_orchestration','must_not_duplicate_running_role','must_block_self_validating_manifest',
    'must_not_pass_without_classification','must_not_load','forbidden_files_to_update_as_working_memory',
    'forbidden_terms','forbidden_spawn','forbidden_implementation','required_artifacts','notes'
}
base_fields = {'id','description','request','prompt','required_roles','optional_roles','required_skills','forbidden_skills'}

def req(s): return set(s.get('required_skills') or [])
def opt_roles(s): return set(s.get('optional_roles') or [])
def roles_req(s): return set(s.get('required_roles') or [])

for s in scenarios:
    sid=s.get('id','<missing-id>')
    if not s.get('id'): errors.append('Scenario missing id')
    for rid in s.get('required_roles') or []:
        if rid not in roles: errors.append(f'{sid}: unknown required role {rid}')
    for rid in s.get('optional_roles') or []:
        if rid not in roles: errors.append(f'{sid}: unknown optional role {rid}')
    for sk in s.get('required_skills') or []:
        if sk not in skills: errors.append(f'{sid}: unknown required skill {sk}')
    for sk in s.get('forbidden_skills') or []:
        if sk not in skills: errors.append(f'{sid}: unknown forbidden skill {sk}')
    for k in s.keys():
        if k not in base_fields and k not in known_behavior_fields:
            errors.append(f'{sid}: unknown scenario behavior field {k}')

    if s.get('must_not_spawn_without_approval') is True and not s.get('requires_approval_before_spawn'):
        errors.append(f'{sid}: must_not_spawn_without_approval requires requires_approval_before_spawn=true')
    if s.get('requires_approval_before_spawn') is True and s.get('forbidden_spawn') is True:
        errors.append(f'{sid}: cannot both forbid spawn and require approval before spawn')
    if s.get('must_not_implement_before_reference_spec') is True and 'reference-fidelity' not in req(s):
        errors.append(f'{sid}: reference implementation block requires reference-fidelity')
    if s.get('must_block_self_validating_manifest') is True:
        for sk in ['design-source-authority','manifest-freeze-check']:
            if sk not in req(s): errors.append(f'{sid}: self-validation block requires {sk}')
    if s.get('must_use_phased_orchestration') is True and 'production-service-planning' not in req(s):
        errors.append(f'{sid}: phased orchestration requires production-service-planning')
    if 'TASK.md' in (s.get('forbidden_files_to_update_as_working_memory') or []):
        if not req(s).intersection({'ticket-router','task-ledger','memory-integrity-check'}):
            errors.append(f'{sid}: TASK.md working-memory ban requires a ticketed-memory skill')
    if s.get('max_active_roles') is not None and len(roles_req(s)) > int(s['max_active_roles']):
        errors.append(f'{sid}: required roles exceed max_active_roles')
    if s.get('max_roles') is not None and len(roles_req(s)) > int(s['max_roles']):
        errors.append(f'{sid}: required roles exceed max_roles')
    if s.get('max_spawned_agents_default') is not None:
        if not s.get('requires_approval_before_spawn'):
            errors.append(f'{sid}: bounded spawned agents default should require approval before spawn')
        if int(s['max_spawned_agents_default']) > 2 and 'High-risk' not in str(s.get('expected_complexity','')):
            errors.append(f'{sid}: max_spawned_agents_default too high for non-high-risk workflow')
    if s.get('must_not_load'):
        if not isinstance(s['must_not_load'], list):
            errors.append(f'{sid}: must_not_load must be a list')
    if sid == 'tiny_copy_change':
        if s.get('required_skills') not in ([], None): errors.append(f'{sid}: tiny copy should not require skills by default')
        if s.get('forbidden_spawn') is not True: errors.append(f'{sid}: tiny copy must forbid spawn')
        for item in ['docs/ROLE_TINY_INDEX.json','docs/SKILL_TINY_INDEX.json']:
            if item not in (s.get('must_not_load') or []): errors.append(f'{sid}: must_not_load missing {item}')
    if sid == 'production_web_service_code_ds':
        for sk in ['repo-recon','design-recon','production-service-planning','production-readiness-review','design-system-compliance','ds-code-contract-enforcement','visual-qa-loop','component-contract-scan']:
            if sk not in req(s): errors.append(f'{sid}: missing required production skill {sk}')
    if sid == 'ui_prototype_no_ds':
        if s.get('expected_ds_mode') != 'none': errors.append(f'{sid}: expected_ds_mode should be none')
        if 'prototype-ui-kit' not in req(s): errors.append(f'{sid}: no-DS prototype requires prototype-ui-kit')

if errors:
    print('ROUTING TEST FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f'ROUTING TEST PASSED: {len(scenarios)} scenarios, {len(roles)} roles, {len(skills)} skills.')
