from pathlib import Path
import sys, json, re
try:
    import tomllib
except Exception:
    tomllib = None

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

required = [
    'AGENTS.md','FIRST_PROMPT.md','TASK.md','CHRONICLE.md','TEAM.md','README.md',
    'docs/QUESTION_TREE.md','docs/WORK_MODES.md','docs/ROLE_ROUTING_MATRIX.md',
    'docs/OWNERSHIP_MATRIX.md','docs/QUALITY_GATES.md','docs/RISK_POLICY.md',
    'docs/EVIDENCE_POLICY.md','docs/LANGUAGE_POLICY.md','docs/FAST_LANE.md',
    'docs/COMPLEXITY_MODEL.md','docs/ROLE_OUTPUT_SCHEMAS.md','docs/EXTERNAL_EVIDENCE_PROTOCOL.md',
    'docs/FINAL_FANTASY_CODENAME_POLICY.md','docs/SCENARIO_TESTS.json'
]
for r in required:
    if not (ROOT/r).exists():
        errors.append(f'Missing required file: {r}')

playbooks = sorted((ROOT/'.agents/playbooks').glob('*.md'))
agents = sorted((ROOT/'.codex/agents').glob('*.toml'))
skills = sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))

role_ids = set()
for pb in playbooks:
    text = pb.read_text(encoding='utf-8')
    m = re.search(r'Role ID: `([^`]+)`', text)
    if not m:
        errors.append(f'{pb.name} missing Role ID')
    else:
        role_ids.add(m.group(1))

if len(playbooks) != len(agents):
    errors.append(f'Playbook/agent count mismatch: {len(playbooks)} playbooks vs {len(agents)} agents')
if len(skills) < 10:
    errors.append(f'Expected at least 10 skills, found {len(skills)}')

required_sections = [
    '## Mission','## Activation criteria','## Do not do','## Ideal expertise','## Methodological operating model',
    '## Required output artifact','## Handoff rules','## Escalation triggers','## Common failure modes','## Strict output schema v1.3'
]
for pb in playbooks:
    text = pb.read_text(encoding='utf-8')
    for sec in required_sections:
        if sec not in text:
            errors.append(f'{pb.name} missing section {sec}')
    if 'knows core methods, when to use them, common traps, evidence requirements, and handoff implications' in text:
        errors.append(f'{pb.name} still contains old generic expertise phrasing')
    if 'Squall / Consistency Auditor when instructions or role outputs conflict' in text and 'consistency_auditor' in pb.name:
        errors.append('Consistency Auditor escalates to self')
    if 'Role-specific triggers:' not in text:
        warnings.append(f'{pb.name} has no explicit Role-specific triggers marker')

if tomllib:
    for agent in agents:
        try:
            data = tomllib.loads(agent.read_text(encoding='utf-8'))
            for k in ['name','description','developer_instructions']:
                if k not in data:
                    errors.append(f'{agent.name} missing TOML key {k}')
        except Exception as e:
            errors.append(f'{agent.name} TOML parse error: {e}')
else:
    warnings.append('tomllib unavailable, TOML parsing skipped')

for f in ['AGENTS.md','FIRST_PROMPT.md','TASK.md']:
    text=(ROOT/f).read_text(encoding='utf-8')
    if 'LANGUAGE_POLICY.md' not in text and 'Language policy' not in text:
        errors.append(f'{f} does not reference language policy')

# Scenario validation
try:
    scenarios = json.loads((ROOT/'docs/SCENARIO_TESTS.json').read_text(encoding='utf-8'))
    for s in scenarios.get('scenarios', []):
        if 'max_roles' not in s or 'max_questions' not in s:
            errors.append(f"Scenario {s.get('id')} missing max_roles/max_questions")
        for field in ['required_roles','optional_roles','forbidden_roles']:
            for rid in s.get(field, []):
                if rid not in role_ids:
                    errors.append(f"Scenario {s.get('id')} references unknown role {rid} in {field}")
        if len(s.get('required_roles', [])) > s.get('max_roles', 999):
            errors.append(f"Scenario {s.get('id')} has required_roles > max_roles")
except Exception as e:
    errors.append(f'SCENARIO_TESTS.json parse/validation error: {e}')

# Core docs references
ag = (ROOT/'AGENTS.md').read_text(encoding='utf-8')
for doc in ['COMPLEXITY_MODEL.md','ROLE_OUTPUT_SCHEMAS.md','EXTERNAL_EVIDENCE_PROTOCOL.md','FINAL_FANTASY_CODENAME_POLICY.md']:
    if doc not in ag:
        errors.append(f'AGENTS.md does not reference {doc}')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('ERROR:', e)
    for w in warnings:
        print('WARN:', w)
    sys.exit(1)

print(f'VALIDATION PASSED: {len(playbooks)} roles, {len(skills)} skills, {len(scenarios.get("scenarios", []))} scenarios.')
for w in warnings:
    print('WARN:', w)
