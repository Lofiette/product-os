#!/usr/bin/env python3
from pathlib import Path
import json, tomllib, sys, subprocess
ROOT = Path(__file__).resolve().parents[1]
errors=[]
required = [
 'AGENTS.md','FIRST_PROMPT.md','TASK.md','CHRONICLE.md','TEAM.md','README.md',
 'docs/ROLE_SKILL_ARCHITECTURE.md','docs/SUBAGENT_ORCHESTRATION.md','docs/SUBAGENT_PROMPT_RECIPES.md',
 'docs/ORCHESTRATION_APPROVAL_POLICY.md','docs/DESIGN_SYSTEM_MODES.md','docs/DESIGN_RECON.md','docs/UI_QUALITY_GATES.md',
 'docs/UI_OBVIOUS_ERRORS_CHECKLIST.md','docs/ROLE_INDEX.json','docs/ROLE_MINI_INDEX.json','docs/SKILL_INDEX.json','docs/SCENARIO_TESTS.json',
 'docs/PHASED_ORCHESTRATION.md','docs/PRODUCTION_READINESS_GATES.md','docs/WEB_SERVICE_ROUTING.md','docs/MODULE_DESIGN.md',
 'docs/DESIGN_HANDOFF_QA.md','docs/PROTOTYPE_UI_KIT.md','docs/OPERATIONAL_UI_WORKFLOWS.md',
 'docs/TEAM_CULTURE.md','docs/TASTE_PROFILE.md','docs/TASTE_REVIEW.md','docs/CREATIVE_TENSION.md','docs/EXPECTATION_ANTICIPATION.md','docs/AGENT_NAMING_POLICY.md',
 'docs/TEAM_CULTURE.md','docs/TASTE_PROFILE.md','docs/TASTE_REVIEW.md','docs/CREATIVE_TENSION.md',
 'docs/ANTICIPATION_BRANCH.md','docs/PROACTIVE_PROPOSALS.md','docs/AGENT_NAMING_POLICY.md',
 'scripts/find-raw-ui-values.mjs','scripts/check-component-imports.mjs','scripts/test-routing.py'
]
for p in required:
    if not (ROOT/p).exists(): errors.append(f'Missing required file: {p}')
for p in ROOT.rglob('*'):
    if p.suffix in ['.bak','.tmp']: errors.append(f'Forbidden temp file: {p.relative_to(ROOT)}')
role_index=json.loads((ROOT/'docs/ROLE_INDEX.json').read_text())
roles=role_index.get('roles',[])
ids=[r['id'] for r in roles]
if len(ids)!=len(set(ids)): errors.append('Duplicate role IDs')
skill_index=json.loads((ROOT/'docs/SKILL_INDEX.json').read_text())
skills={s['id'] for s in skill_index.get('skills',[])}
required_skills = {
 'repo-recon','design-recon','prototype-ui-kit','screen-redesign','module-design','state-matrix',
 'design-system-manifest','design-system-compliance','design-handoff-qa','design-qa','visual-qa-loop',
 'ui-heuristic-audit','component-contract-scan','ds-code-contract-enforcement','production-service-planning','production-readiness-review',
 'taste-calibration','taste-review','creative-tension-review','expectation-anticipation','example-taste-board',
 'taste-calibration','taste-review','creative-tension-review','anticipation-radar','proactive-proposal-review'
}
for sk in required_skills:
    if sk not in skills: errors.append(f'Missing beta1 required skill in index: {sk}')
    if not (ROOT/'.agents/skills'/sk/'SKILL.md').exists(): errors.append(f'Missing beta1 skill file: {sk}')
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
    for rid in s.get('required_roles') or []:
        if rid not in ids: errors.append(f'Scenario {s["id"]} unknown role: {rid}')
    for rid in s.get('optional_roles') or []:
        if rid not in ids: errors.append(f'Scenario {s["id"]} unknown optional role: {rid}')
    for sk in s.get('required_skills') or []:
        if sk not in skills: errors.append(f'Scenario {s["id"]} unknown skill: {sk}')
    for sk in s.get('forbidden_skills') or []:
        if sk not in skills: errors.append(f'Scenario {s["id"]} unknown forbidden skill: {sk}')

# scenario markdown sync
scenario_ids = {s.get('id') for s in sc.get('scenarios', [])}
md_ids = {p.stem for p in (ROOT/'docs/scenario_tests').glob('*.md')}
if scenario_ids != md_ids:
    missing = sorted(scenario_ids - md_ids)
    extra = sorted(md_ids - scenario_ids)
    if missing: errors.append(f'Scenario markdown mismatch: missing {missing}')
    if extra: errors.append(f'Scenario markdown mismatch: extra {extra}')

# critical v2 roles
for rid in ['product_designer','design_engineer','service_designer','information_architect','data_visualization_designer','conversation_designer']:
    if rid not in ids: errors.append(f'Missing critical v2 role: {rid}')
# first prompt critical phrases
fp=(ROOT/'FIRST_PROMPT.md').read_text()
for phrase in ['Do not spawn real subagents yet','Ask for approval before spawning real subagents','ROLE_MINI_INDEX.json','No real subagents spawned','TEAM_CULTURE.md','AGENT_NAMING_POLICY.md','taste-calibration','anticipation-radar']:
    if phrase not in fp: errors.append(f'FIRST_PROMPT missing phrase: {phrase}')

# exact agent ID / no personal labels in core docs
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/SUBAGENT_ORCHESTRATION.md']:
    text=(ROOT/doc).read_text()
    for term in ['Final Fantasy','codename policy']:
        if term in text and 'ignore' not in text.lower():
            errors.append(f'Core doc {doc} contains suspicious personal/codename term: {term}')

# script syntax
for js in ['scripts/find-raw-ui-values.mjs','scripts/check-component-imports.mjs']:
    try:
        subprocess.run(['node','--check',str(ROOT/js)], check=True, capture_output=True, text=True)
    except Exception as e:
        errors.append(f'Node syntax check failed for {js}: {e}')
try:
    subprocess.run([sys.executable, str(ROOT/'scripts/test-routing.py')], check=True, capture_output=True, text=True)
except Exception as e:
    errors.append(f'Routing test failed: {e}')


# beta 2 no-alias rule in custom agent instructions
for toml_path in (ROOT/'.codex/agents').glob('*.toml'):
    try:
        data=tomllib.loads(toml_path.read_text())
        instr=data.get('developer_instructions','')
        if 'Do not use aliases' not in instr:
            errors.append(f'TOML missing no-alias instruction: {toml_path.name}')
    except Exception:
        pass

# beta 2 docs references
for phrase in ['Taste Review','Anticipation','Agent Naming Policy']:
    combined=(ROOT/'AGENTS.md').read_text() + (ROOT/'FIRST_PROMPT.md').read_text()
    if phrase not in combined:
        errors.append(f'Missing beta2 phrase in AGENTS/FIRST_PROMPT: {phrase}')

if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f'VALIDATION PASSED: {len(ids)} roles, {len(skills)} skills, {len(sc.get("scenarios",[]))} scenarios.')
