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
    'docs/BOOTSTRAP_INDEX.md','docs/QUESTION_TREE.md','docs/WORK_MODES.md','docs/ROLE_ROUTING_MATRIX.md',
    'docs/OWNERSHIP_MATRIX.md','docs/QUALITY_GATES.md','docs/RISK_POLICY.md',
    'docs/EVIDENCE_POLICY.md','docs/LANGUAGE_POLICY.md','docs/FAST_LANE.md',
    'docs/COMPLEXITY_MODEL.md','docs/ROLE_OUTPUT_SCHEMAS.md','docs/ROLE_METHOD_LIBRARY.md',
    'docs/EXTERNAL_EVIDENCE_PROTOCOL.md','docs/FINAL_FANTASY_CODENAME_POLICY.md',
    'docs/CREATIVE_METHODS.md','docs/OPPORTUNITY_EVENTS.md',
    'docs/SCENARIO_TESTS.json','docs/VALIDATOR_RULES.md','docs/ULTIMATE_RELEASE_NOTES.md'
]
for r in required:
    if not (ROOT/r).exists():
        errors.append(f'Missing required file: {r}')

# No backup/editor residue
for p in ROOT.rglob('*'):
    if p.is_file() and (p.name.endswith('.bak') or p.name.endswith('.tmp') or p.name.endswith('~')):
        errors.append(f'Backup/temp file should not be shipped: {p.relative_to(ROOT)}')

# Parse TEAM.md source of truth
team_roles = {}
team_path = ROOT/'TEAM.md'
if team_path.exists():
    blocks = re.split(r'(?=^## )', team_path.read_text(encoding='utf-8'), flags=re.M)
    for b in blocks:
        if not b.startswith('## '):
            continue
        h = re.match(r'^##\s+(.+?)\s*$', b, flags=re.M)
        m = re.search(r'- ID: `([^`]+)`', b)
        if h and m:
            header = h.group(1).strip()
            if '/' not in header:
                errors.append(f'TEAM.md header has no codename/title separator: {header}')
                continue
            codename, title = [x.strip() for x in header.split('/', 1)]
            team_roles[m.group(1)] = {'header': header, 'codename': codename, 'title': title}
else:
    errors.append('TEAM.md missing, cannot validate role identity')

playbooks = sorted((ROOT/'.agents/playbooks').glob('*.md'))
agents = sorted((ROOT/'.codex/agents').glob('*.toml'))
skills = sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))
role_cards = sorted((ROOT/'.agents/role_cards').glob('*.md')) if (ROOT/'.agents/role_cards').exists() else []

role_ids = set()
role_file = {}
role_identity = {}
for pb in playbooks:
    text = pb.read_text(encoding='utf-8')
    m = re.search(r'Role ID: `([^`]+)`', text)
    h = re.search(r'^#\s+(.+)$', text, flags=re.M)
    if not m:
        errors.append(f'{pb.name} missing Role ID')
        continue
    rid = m.group(1)
    role_ids.add(rid)
    role_file[rid] = pb
    if not h:
        errors.append(f'{pb.name} missing title header')
        continue
    header = h.group(1).strip()
    role_identity[rid] = header
    if rid not in team_roles:
        errors.append(f'{pb.name} has Role ID not listed in TEAM.md: {rid}')
    else:
        expected = team_roles[rid]['header']
        if header != expected:
            errors.append(f'{pb.name} header mismatch: playbook="{header}" TEAM="{expected}"')
        codename_line = re.search(r'- Codename:\s*([^,\n]+),', text)
        if not codename_line:
            errors.append(f'{pb.name} missing Codename line')
        elif codename_line.group(1).strip() != team_roles[rid]['codename']:
            errors.append(f'{pb.name} codename mismatch: {codename_line.group(1).strip()} != {team_roles[rid]["codename"]}')

if len(playbooks) != len(agents):
    errors.append(f'Playbook/agent count mismatch: {len(playbooks)} playbooks vs {len(agents)} agents')
if len(skills) < 13:
    errors.append(f'Expected at least 13 skills after v1.4, found {len(skills)}')
if len(role_cards) != len(playbooks):
    errors.append(f'Role card count mismatch: {len(role_cards)} cards vs {len(playbooks)} playbooks')

for rc in role_cards:
    text = rc.read_text(encoding='utf-8')
    m = re.search(r'Role ID: `([^`]+)`', text)
    if not m:
        errors.append(f'{rc.name} missing Role ID')
    elif m.group(1) not in role_ids:
        errors.append(f'{rc.name} references unknown Role ID {m.group(1)}')
    for marker in ['## Activate when','## Load full playbook when','## Role-card-only is enough when']:
        if marker not in text:
            errors.append(f'{rc.name} missing marker {marker}')

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
            rid = data.get('name')
            agent_names.add(agent.stem)
            if rid not in team_roles:
                errors.append(f'{agent.name} TOML name not listed in TEAM.md: {rid}')
            else:
                desc = data.get('description','')
                expected = team_roles[rid]['header']
                if expected not in desc:
                    errors.append(f'{agent.name} description missing TEAM identity "{expected}"')
                instr = data.get('developer_instructions','')
                if f'.agents/playbooks/' not in instr:
                    errors.append(f'{agent.name} developer_instructions missing playbook reference')
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
for doc in ['BOOTSTRAP_INDEX.md','COMPLEXITY_MODEL.md','ROLE_OUTPUT_SCHEMAS.md','ROLE_METHOD_LIBRARY.md','EXTERNAL_EVIDENCE_PROTOCOL.md','FINAL_FANTASY_CODENAME_POLICY.md','CREATIVE_METHODS.md','OPPORTUNITY_EVENTS.md']:
    if doc not in ag:
        errors.append(f'AGENTS.md does not reference {doc}')

fp = (ROOT/'FIRST_PROMPT.md').read_text(encoding='utf-8') if (ROOT/'FIRST_PROMPT.md').exists() else ''
if re.search(r'`docs/[^`]+,\s*docs/', fp):
    errors.append('FIRST_PROMPT.md contains comma-packed document references inside one code span')
# Lean startup guardrails
for heavy in ['TEAM.md','ROLE_METHOD_LIBRARY.md','ROLE_OUTPUT_SCHEMAS.md','SCENARIO_TESTS.json']:
    stage0 = re.search(r'## Stage 0.*?## Hard stops', fp, flags=re.S)
    if stage0 and heavy in stage0.group(0):
        errors.append(f'FIRST_PROMPT Stage 0 loads heavy/non-runtime asset: {heavy}')
if 'BOOTSTRAP_INDEX.md' not in fp:
    errors.append('FIRST_PROMPT.md does not reference BOOTSTRAP_INDEX.md')
if 'SCENARIO_TESTS.json' in fp:
    errors.append('FIRST_PROMPT.md should not load/reference SCENARIO_TESTS.json during normal startup')

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

# Creative docs and skill integration
if not (ROOT/'.agents/skills/creative-improvement-loop/SKILL.md').exists():
    errors.append('Missing creative-improvement-loop skill')
for f in ['docs/CREATIVE_METHODS.md','docs/OPPORTUNITY_EVENTS.md','docs/QUESTION_TREE.md','docs/ROLE_ROUTING_MATRIX.md']:
    text=(ROOT/f).read_text(encoding='utf-8') if (ROOT/f).exists() else ''
    if 'creative' not in text.lower() and 'opportunity' not in text.lower():
        errors.append(f'{f} does not appear to integrate opportunity/creative workflow')

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
