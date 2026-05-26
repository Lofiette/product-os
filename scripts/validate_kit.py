#!/usr/bin/env python3
from pathlib import Path
import json, tomllib, sys, re
ROOT = Path(__file__).resolve().parents[1]
errors=[]
required = [
 'AGENTS.md','FIRST_PROMPT.md','TASK.md','CHRONICLE.md','TEAM.md','README.md',
 'docs/ROLE_SKILL_ARCHITECTURE.md','docs/SUBAGENT_ORCHESTRATION.md','docs/SUBAGENT_PROMPT_RECIPES.md',
 'docs/ORCHESTRATION_APPROVAL_POLICY.md','docs/DESIGN_SYSTEM_MODES.md','docs/DESIGN_RECON.md','docs/UI_QUALITY_GATES.md',
 'docs/UI_OBVIOUS_ERRORS_CHECKLIST.md','docs/ROLE_INDEX.json','docs/SKILL_INDEX.json','docs/SCENARIO_TESTS.json'
]
for p in required:
    if not (ROOT/p).exists(): errors.append(f'Missing required file: {p}')
for p in ROOT.rglob('*'):
    if p.suffix in ['.bak','.tmp']: errors.append(f'Forbidden temp file: {p.relative_to(ROOT)}')
role_index=json.loads((ROOT/'docs/ROLE_INDEX.json').read_text())
roles=role_index.get('roles',[])
ids=[r['id'] for r in roles]
if len(ids)!=len(set(ids)): errors.append('Duplicate role IDs')
for forbidden in ['\"codename\"',' / Task Intake Orchestrator',' / Product Strategist',' / Chronicle Keeper',' / Consistency Auditor']:
    text='\n'.join([p.read_text(errors='ignore') for p in [ROOT/'TEAM.md', ROOT/'docs/ROLE_INDEX.json'] if p.exists()])
    if forbidden in text: errors.append(f'Forbidden codename marker found in core role docs: {forbidden}')
skill_index=json.loads((ROOT/'docs/SKILL_INDEX.json').read_text())
skills={s['id'] for s in skill_index.get('skills',[])}
for s in skills:
    if not (ROOT/'.agents/skills'/s/'SKILL.md').exists(): errors.append(f'Missing skill SKILL.md: {s}')
for r in roles:
    rid=r['id']
    if not list((ROOT/'.agents/playbooks').glob(f'*-{rid}.md')): errors.append(f'Missing playbook for {rid}')
    if not (ROOT/'.agents/role_cards'/f'{rid}.md').exists(): errors.append(f'Missing role card for {rid}')
    toml_path=ROOT/'.codex/agents'/f'{rid}.toml'
    if not toml_path.exists(): errors.append(f'Missing toml agent for {rid}')
    else:
        try:
            data=tomllib.loads(toml_path.read_text())
            if data.get('name')!=rid: errors.append(f'TOML name mismatch for {rid}: {data.get("name")}')
        except Exception as e: errors.append(f'Invalid TOML for {rid}: {e}')
    for s in r.get('default',[])+r.get('optional',[]):
        if s not in skills: errors.append(f'Role {rid} references unknown skill: {s}')
# scenario references
sc=json.loads((ROOT/'docs/SCENARIO_TESTS.json').read_text())
for s in sc.get('scenarios',[]):
    for rid in s.get('required_roles',[]):
        if rid not in ids: errors.append(f'Scenario {s["id"]} unknown role: {rid}')
    for sk in s.get('required_skills',[]):
        if sk not in skills: errors.append(f'Scenario {s["id"]} unknown skill: {sk}')
# critical v2 roles
for rid in ['product_designer','design_engineer','service_designer','information_architect','data_visualization_designer','conversation_designer']:
    if rid not in ids: errors.append(f'Missing critical v2 role: {rid}')
# make sure first prompt includes no spawn yet / approval
fp=(ROOT/'FIRST_PROMPT.md').read_text()
for phrase in ['Do not spawn real subagents yet','Ask for approval before spawning real subagents']:
    if phrase not in fp: errors.append(f'FIRST_PROMPT missing phrase: {phrase}')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f'VALIDATION PASSED: {len(ids)} roles, {len(skills)} skills, {len(sc.get("scenarios",[]))} scenarios.')
