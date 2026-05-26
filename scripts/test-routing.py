#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
roles = {r['id'] for r in json.loads((ROOT/'docs/ROLE_INDEX.json').read_text())['roles']}
skills = {s['id'] for s in json.loads((ROOT/'docs/SKILL_INDEX.json').read_text())['skills']}
scenarios = json.loads((ROOT/'docs/SCENARIO_TESTS.json').read_text())['scenarios']
errors=[]
for s in scenarios:
    for rid in s.get('required_roles') or []:
        if rid not in roles: errors.append(f'{s["id"]}: unknown required role {rid}')
    for rid in s.get('optional_roles') or []:
        if rid not in roles: errors.append(f'{s["id"]}: unknown optional role {rid}')
    for sk in s.get('required_skills') or []:
        if sk not in skills: errors.append(f'{s["id"]}: unknown required skill {sk}')
    for sk in s.get('forbidden_skills') or []:
        if sk not in skills: errors.append(f'{s["id"]}: unknown forbidden skill {sk}')
    if s.get('must_not_spawn_without_approval') is True and 'max_questions' not in s:
        pass
if errors:
    print('ROUTING TEST FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f'ROUTING TEST PASSED: {len(scenarios)} scenarios, {len(roles)} roles, {len(skills)} skills.')
