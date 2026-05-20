from pathlib import Path
import tomllib, re, sys
root = Path(__file__).resolve().parents[1]
required = ['AGENTS.md','FIRST_PROMPT.md','TASK.md','CHRONICLE.md','TEAM.md','README.md','docs/QUESTION_TREE.md','docs/ROLE_ROUTING_MATRIX.md','docs/OWNERSHIP_MATRIX.md','docs/EVIDENCE_POLICY.md','docs/FAST_LANE.md','docs/QUALITY_GATES.md','docs/RISK_POLICY.md']
errors=[]; warnings=[]
for f in required:
    if not (root/f).exists(): errors.append(f'Missing required file: {f}')
playbooks=list((root/'.agents/playbooks').glob('*.md'))
agents=list((root/'.codex/agents').glob('*.toml'))
if len(playbooks)<40: warnings.append(f'Expected deep maximum role set, found {len(playbooks)} playbooks')
if len(playbooks)!=len(agents): errors.append(f'Playbook/agent count mismatch: {len(playbooks)} vs {len(agents)}')
for a in agents:
    try:
        data=tomllib.loads(a.read_text())
    except Exception as e:
        errors.append(f'Invalid TOML {a}: {e}'); continue
    for k in ['name','description','developer_instructions']:
        if k not in data: errors.append(f'{a} missing {k}')
    m=re.search(r'playbooks/([^ ]+\.md)', data.get('developer_instructions',''))
    if m and not (root/'.agents/playbooks'/m.group(1)).exists():
        errors.append(f'{a} references missing playbook {m.group(1)}')
for pb in playbooks:
    t=pb.read_text()
    for section in ['## Mission','## Activation criteria','## Do not do','## Ideal expertise and professional depth','## Methodological operating model','## Required output artifact','## Handoff rules','## Escalation triggers','## Common failure modes to avoid']:
        if section not in t: errors.append(f'{pb.name} missing section {section}')
    if len(t.split())<450: warnings.append(f'{pb.name} may be too shallow: {len(t.split())} words')
for skill in (root/'.agents/skills').glob('*/SKILL.md'):
    t=skill.read_text()
    if '## Procedure' not in t: errors.append(f'{skill} missing Procedure')
    if 'description:' not in t.split('---',2)[1]: errors.append(f'{skill} missing description metadata')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('ERROR:',e)
    for w in warnings: print('WARN:',w)
    sys.exit(1)
print(f'VALIDATION PASSED: {len(playbooks)} roles, {len(list((root/".agents/skills").glob("*/SKILL.md")))} skills.')
for w in warnings: print('WARN:',w)
