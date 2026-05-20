from pathlib import Path
import sys
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
    'docs/EVIDENCE_POLICY.md','docs/LANGUAGE_POLICY.md','docs/FAST_LANE.md'
]
for r in required:
    if not (ROOT/r).exists():
        errors.append(f'Missing required file: {r}')

playbooks = sorted((ROOT/'.agents/playbooks').glob('*.md'))
agents = sorted((ROOT/'.codex/agents').glob('*.toml'))
skills = sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))

if len(playbooks) != len(agents):
    errors.append(f'Playbook/agent count mismatch: {len(playbooks)} playbooks vs {len(agents)} agents')
if len(skills) < 10:
    errors.append(f'Expected at least 10 skills, found {len(skills)}')

required_sections = ['## Mission','## Activation criteria','## Do not do','## Ideal expertise','## Methodological operating model','## Required output artifact','## Handoff rules','## Escalation triggers','## Common failure modes']
for pb in playbooks:
    text = pb.read_text(encoding='utf-8')
    for sec in required_sections:
        if sec not in text:
            errors.append(f'{pb.name} missing section {sec}')
    if 'know core methods, trade-offs, failure modes' in text:
        warnings.append(f'{pb.name} still contains old generic expertise phrasing')
    if 'Squall / Consistency Auditor when instructions or role outputs conflict' in text and 'consistency_auditor' in pb.name:
        errors.append('Consistency Auditor escalates to self')

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

# Ensure core docs reference language policy
for f in ['AGENTS.md','FIRST_PROMPT.md','TASK.md']:
    text=(ROOT/f).read_text(encoding='utf-8')
    if 'LANGUAGE_POLICY.md' not in text and 'Language policy' not in text:
        errors.append(f'{f} does not reference language policy')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('ERROR:', e)
    for w in warnings:
        print('WARN:', w)
    sys.exit(1)

print(f'VALIDATION PASSED: {len(playbooks)} roles, {len(skills)} skills.')
for w in warnings:
    print('WARN:', w)
