from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg):
    errors.append(msg)

team = (ROOT / 'TEAM.md').read_text(encoding='utf-8')
role_ids = re.findall(r'\| `([^`]+)` \| [^|]+ \| [^|]+ \|', team)
role_ids = [r for r in role_ids if r != 'Role ID']

if not role_ids:
    fail('No roles found in TEAM.md role catalog.')

if len(role_ids) != len(set(role_ids)):
    fail('Duplicate role IDs in TEAM.md.')

for rid in role_ids:
    playbooks = list((ROOT / '.agents/playbooks').glob(f'*-{rid}.md'))
    if not playbooks:
        fail(f'Missing playbook for role: {rid}')
    toml = ROOT / f'.codex/agents/{rid}.toml'
    if not toml.exists():
        fail(f'Missing custom agent TOML for role: {rid}')
    else:
        txt = toml.read_text(encoding='utf-8')
        for key in ['name', 'description', 'developer_instructions']:
            if key not in txt:
                fail(f'Missing {key} in {toml}')

config = (ROOT / '.codex/config.toml').read_text(encoding='utf-8')
for rid in role_ids:
    if f'[agents.{rid}]' not in config:
        fail(f'Missing [agents.{rid}] in .codex/config.toml')
    if f'config_file = "agents/{rid}.toml"' not in config:
        fail(f'Missing config_file for {rid} in .codex/config.toml')

for skill_dir in (ROOT / '.agents/skills').iterdir():
    if skill_dir.is_dir():
        skill = skill_dir / 'SKILL.md'
        if not skill.exists():
            fail(f'Missing SKILL.md in {skill_dir}')
        else:
            text = skill.read_text(encoding='utf-8')
            if not text.startswith('---') or 'name:' not in text or 'description:' not in text:
                fail(f'Invalid skill front matter: {skill}')

required_files = [
    'AGENTS.md','TASK.md','CHRONICLE.md','TEAM.md','FIRST_PROMPT.md','README.md',
    'docs/QUESTION_TREE.md','docs/ROLE_ROUTING_MATRIX.md','docs/WORK_MODES.md','docs/QUALITY_GATES.md','docs/RISK_POLICY.md','docs/PROMPT_RECIPES.md',
]
for rel in required_files:
    if not (ROOT / rel).exists():
        fail(f'Missing required file: {rel}')

agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
for rel in ['TASK.md','CHRONICLE.md','TEAM.md','docs/QUESTION_TREE.md','docs/ROLE_ROUTING_MATRIX.md','docs/QUALITY_GATES.md','docs/RISK_POLICY.md']:
    if rel not in agents:
        fail(f'AGENTS.md does not reference required file: {rel}')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)

print(f'VALIDATION PASSED: {len(role_ids)} roles checked, skills checked, required files present.')
