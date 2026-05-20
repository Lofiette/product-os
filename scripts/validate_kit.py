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
    'docs/COMPLEXITY_MODEL.md','docs/ROLE_OUTPUT_SCHEMAS.md','docs/ROLE_METHOD_LIBRARY.md',
    'docs/EXTERNAL_EVIDENCE_PROTOCOL.md','docs/FINAL_FANTASY_CODENAME_POLICY.md',
    'docs/SCENARIO_TESTS.json','docs/VALIDATOR_RULES.md','docs/ULTIMATE_RELEASE_NOTES.md'
]
for r in required:
    if not (ROOT/r).exists():
        errors.append(f'Missing required file: {r}')

# No backup/editor residue
for p in ROOT.rglob('*'):
    if p.is_file() and (p.name.endswith('.bak') or p.name.endswith('.tmp') or p.name.endswith('~')):
        errors.append(f'Backup/temp file should not be shipped: {p.relative_to(ROOT)}')

playbooks = sorted((ROOT/'.agents/playbooks').glob('*.md'))
agents = sorted((ROOT/'.codex/agents').glob('*.toml'))
skills = sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))

role_ids = set()
role_file = {}
role_identity = {}
for pb in playbooks:
    text = pb.read_text(encoding='utf-8')
    m = re.search(r'Role ID: `([^`]+)`', text)
    h = re.search(r'^#\s+(.+)$', text, flags=re.M)
    if not m:
        errors.append(f'{pb.name} missing Role ID')
    else:
        rid = m.group(1)
        role_ids.add(rid)
        role_file[rid] = pb
        if h:
            title = h.group(1).strip()
            # Expected form: Codename / Role
            role_identity[rid] = title

if len(playbooks) != len(agents):
    errors.append(f'Playbook/agent count mismatch: {len(playbooks)} playbooks vs {len(agents)} agents')
if len(skills) < 10:
    errors.append(f'Expected at least 10 skills, found {len(skills)}')

required_sections = [
    '## Mission','## Activation criteria','## Do not do','## Ideal expertise','## Methodological operating model',
    '## Required output artifact','## Handoff rules','## Escalation triggers','## Common failure modes','## Strict output schema'
]
old_phrase = 'knows core methods, when to use them, common traps, evidence requirements, and handoff implications'
for rid, pb in role_file.items():
    text = pb.read_text(encoding='utf-8')
    for sec in required_sections:
        if sec not in text:
            errors.append(f'{pb.name} missing section {sec}')
    if old_phrase in text:
        errors.append(f'{pb.name} still contains old generic expertise phrasing')
    if 'Role-specific triggers:' not in text:
        warnings.append(f'{pb.name} has no explicit Role-specific triggers marker')
    # self escalation: header identity must not appear in Escalate-to bullets, except user-provided explanatory text outside section
    ident = role_identity.get(rid, '')
    codename = ident.split('/')[0].strip() if '/' in ident else None
    role_title = ident.split('/')[1].strip() if '/' in ident else None
    esc = re.search(r'## Escalation triggers\n\n(.*?)(\n## |\Z)', text, flags=re.S)
    if esc:
        esc_text = esc.group(1)
        if codename and re.search(rf'-\s*{re.escape(codename)}\s*/', esc_text):
            errors.append(f'{pb.name} escalates to its own codename: {codename}')
        if role_title and re.search(rf'/\s*{re.escape(role_title)}\b', esc_text):
            errors.append(f'{pb.name} escalates to its own role title: {role_title}')

if tomllib:
    agent_names=set()
    for agent in agents:
        try:
            data = tomllib.loads(agent.read_text(encoding='utf-8'))
            for k in ['name','description','developer_instructions']:
                if k not in data:
                    errors.append(f'{agent.name} missing TOML key {k}')
            agent_names.add(agent.stem)
        except Exception as e:
            errors.append(f'{agent.name} TOML parse error: {e}')
else:
    warnings.append('tomllib unavailable, TOML parsing skipped')

# core docs references
for f in ['AGENTS.md','FIRST_PROMPT.md','TASK.md']:
    text=(ROOT/f).read_text(encoding='utf-8')
    if 'LANGUAGE_POLICY.md' not in text and 'Language policy' not in text:
        errors.append(f'{f} does not reference language policy')

ag = (ROOT/'AGENTS.md').read_text(encoding='utf-8') if (ROOT/'AGENTS.md').exists() else ''
for doc in ['COMPLEXITY_MODEL.md','ROLE_OUTPUT_SCHEMAS.md','ROLE_METHOD_LIBRARY.md','EXTERNAL_EVIDENCE_PROTOCOL.md','FINAL_FANTASY_CODENAME_POLICY.md']:
    if doc not in ag:
        errors.append(f'AGENTS.md does not reference {doc}')

fp = (ROOT/'FIRST_PROMPT.md').read_text(encoding='utf-8') if (ROOT/'FIRST_PROMPT.md').exists() else ''
if re.search(r'`docs/[^`]+,\s*docs/', fp):
    errors.append('FIRST_PROMPT.md contains comma-packed document references inside one code span')
for doc in ['COMPLEXITY_MODEL.md','ROLE_OUTPUT_SCHEMAS.md','ROLE_METHOD_LIBRARY.md','SCENARIO_TESTS.json']:
    if doc not in fp:
        errors.append(f'FIRST_PROMPT.md does not reference {doc}')

# Scenario validation and markdown sync
try:
    scenarios = json.loads((ROOT/'docs/SCENARIO_TESTS.json').read_text(encoding='utf-8'))
    scenario_ids = []
    for s in scenarios.get('scenarios', []):
        sid=s.get('id')
        scenario_ids.append(sid)
        if 'max_roles' not in s or 'max_questions' not in s:
            errors.append(f"Scenario {sid} missing max_roles/max_questions")
        for field in ['required_roles','optional_roles','forbidden_roles']:
            for rid in s.get(field, []):
                if rid not in role_ids:
                    errors.append(f"Scenario {sid} references unknown role {rid} in {field}")
        if len(s.get('required_roles', [])) > s.get('max_roles', 999):
            errors.append(f"Scenario {sid} has required_roles > max_roles")
    md_dir = ROOT/'docs/scenario_tests'
    md_files = sorted(md_dir.glob('*.md')) if md_dir.exists() else []
    md_ids = []
    for f in md_files:
        m = re.match(r'\d{2}-(.+)\.md$', f.name)
        if m:
            md_ids.append(m.group(1))
    if set(md_ids) != set(scenario_ids):
        errors.append(f'Scenario markdown mismatch. JSON={sorted(scenario_ids)} MD={sorted(md_ids)}')
    if len(md_files) != len(scenario_ids):
        errors.append(f'Scenario markdown count mismatch: {len(md_files)} markdown vs {len(scenario_ids)} JSON')
except Exception as e:
    errors.append(f'SCENARIO_TESTS.json parse/validation error: {e}')

# Review mode guardrail
for f in ['AGENTS.md','docs/ROLE_OUTPUT_SCHEMAS.md']:
    text=(ROOT/f).read_text(encoding='utf-8') if (ROOT/f).exists() else ''
    if 'read-only' not in text.lower():
        warnings.append(f'{f} may not clearly state review mode is read-only')

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
