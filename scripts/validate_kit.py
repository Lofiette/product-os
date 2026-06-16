#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

REQUIRED_FILES = [
    'AGENTS.md','FIRST_PROMPT.md','CURRENT.md','TASK_INDEX.md','TASK.md','CHRONICLE.md','TEAM.md','README.md',
    'docs/BOOTSTRAP_INDEX.md','docs/LANGUAGE_POLICY.md','docs/TICKETED_MEMORY.md','docs/CONTEXT_BUDGET_POLICY.md',
    'docs/RUNTIME_LOAD_POLICY.md','docs/TICKET_LIFECYCLE.md','docs/ROLE_SKILL_ARCHITECTURE.md',
    'docs/SUBAGENT_ORCHESTRATION.md','docs/SUBAGENT_PROMPT_RECIPES.md','docs/ORCHESTRATION_APPROVAL_POLICY.md',
    'docs/DESIGN_SYSTEM_MODES.md','docs/DESIGN_RECON.md','docs/UI_QUALITY_GATES.md','docs/UI_OBVIOUS_ERRORS_CHECKLIST.md',
    'docs/ROLE_INDEX.json','docs/ROLE_MINI_INDEX.json','docs/ROLE_TINY_INDEX.json',
    'docs/SKILL_INDEX.json','docs/SKILL_TINY_INDEX.json','docs/SKILL_ROUTER_INDEX.json','docs/SCENARIO_TESTS.json',
    'docs/PHASED_ORCHESTRATION.md','docs/PRODUCTION_READINESS_GATES.md','docs/WEB_SERVICE_ROUTING.md','docs/MODULE_DESIGN.md',
    'docs/DESIGN_HANDOFF_QA.md','docs/PROTOTYPE_UI_KIT.md','docs/OPERATIONAL_UI_WORKFLOWS.md','docs/TEAM_CULTURE.md',
    'docs/TASTE_PROFILE.md','docs/TASTE_REVIEW.md','docs/CREATIVE_TENSION.md','docs/EXPECTATION_ANTICIPATION.md',
    'docs/SKILL_DISCOVERY_POLICY.md','docs/CODEX_DIAGNOSTIC_EXPORT_WSL.md',
    'docs/AGENT_NAMING_POLICY.md','docs/SUBAGENT_RUN_CONTRACT.md','docs/SUBAGENT_FAILURE_POLICY.md',
    'docs/UI_REVIEW_PACKET.md','docs/UI_REVIEW_RUNBOOK.md','docs/REFERENCE_FIDELITY.md','docs/DESIGN_SOURCE_AUTHORITY.md',
    'docs/MANIFEST_FREEZE_POLICY.md','docs/SCREENSHOT_VISUAL_GATE.md','docs/CONTENT_REALISM.md','docs/DEBUG_CONTROL_GATE.md',
    'docs/VISUAL_ACCEPTANCE_CRITERIA.md','scripts/check-design-source-authority.mjs','scripts/find-raw-ui-values.mjs',
    'scripts/check-component-imports.mjs','scripts/check-memory-integrity.mjs','scripts/test-routing.py','scripts/export-codex-diagnostics-wsl.sh'
]

REQUIRED_DIRS = ['tasks','context/packets','context/snapshots','chronicle','archive']
CANONICAL_TIER0 = ['AGENTS.md','CURRENT.md','TASK_INDEX.md','CHRONICLE.md','docs/BOOTSTRAP_INDEX.md','docs/LANGUAGE_POLICY.md']
REQUIRED_SKILLS = {
    'repo-recon','design-recon','prototype-ui-kit','screen-redesign','module-design','state-matrix',
    'design-system-manifest','design-system-compliance','design-handoff-qa','design-qa','visual-qa-loop',
    'ui-heuristic-audit','component-contract-scan','ds-code-contract-enforcement','production-service-planning','production-readiness-review',
    'taste-calibration','taste-review','creative-tension-review','expectation-anticipation','example-taste-board',
    'anticipation-radar','proactive-proposal-review','subagent-run-contract','subagent-failure-recovery','ui-review-packet','current-page-ui-review',
    'reference-fidelity','design-source-authority','manifest-freeze-check','screenshot-reference-comparison','content-realism-review','debug-control-review',
    'context-prune','context-snapshot','task-ledger','ticket-router','memory-integrity-check','new-task-protocol','knowledge-freshness-review'
}
CRITICAL_ROLES = ['product_designer','design_engineer','service_designer','information_architect','data_visualization_designer','conversation_designer']


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def load_json(path: str | Path):
    try:
        return json.loads(read(path))
    except Exception as e:
        errors.append(f'Invalid JSON {path}: {e}')
        return {}


def run(cmd, **kwargs):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kwargs)


# Presence / forbidden files
for file in REQUIRED_FILES:
    if not (ROOT / file).exists():
        errors.append(f'Missing required file: {file}')
for d in REQUIRED_DIRS:
    if not (ROOT / d).exists():
        errors.append(f'Missing memory directory: {d}')
for p in ROOT.rglob('*'):
    if p.suffix in ['.bak', '.tmp']:
        errors.append(f'Forbidden temp file: {rel(p)}')

# Script shebang/executable sanity
for script in ['scripts/validate_kit.py','scripts/test-routing.py','scripts/check-memory-integrity.mjs','scripts/export-codex-diagnostics-wsl.sh']:
    p = ROOT / script
    if p.exists():
        txt = p.read_text(encoding='utf-8', errors='ignore')
        if not txt.startswith('#!'):
            errors.append(f'Executable script missing first-line shebang: {script}')
        mode = p.stat().st_mode
        if not (mode & stat.S_IXUSR):
            errors.append(f'Expected executable bit missing: {script}')
if (ROOT/'scripts/validate_kit.py').exists() and read('scripts/validate_kit.py').startswith('\\'):
    errors.append('validate_kit.py starts with stray backslash before shebang')

# Indexes
role_index = load_json('docs/ROLE_INDEX.json')
roles = role_index.get('roles', [])
role_ids = [r.get('id') for r in roles]
skill_index = load_json('docs/SKILL_INDEX.json')
skills = {s.get('id') for s in skill_index.get('skills', [])}
scenarios = load_json('docs/SCENARIO_TESTS.json').get('scenarios', [])

if len(role_ids) != len(set(role_ids)):
    errors.append('Duplicate role IDs')
if len(skills) != len([s for s in skill_index.get('skills', [])]):
    errors.append('Duplicate skill IDs')
for rid in CRITICAL_ROLES:
    if rid not in role_ids:
        errors.append(f'Missing critical role: {rid}')
for sk in REQUIRED_SKILLS:
    if sk not in skills:
        errors.append(f'Missing required skill in index: {sk}')
    if not (ROOT / '.agents/skills' / sk / 'SKILL.md').exists():
        errors.append(f'Missing required skill file: {sk}')

# Skill front matter
fm_re = re.compile(r'^---\n(?P<body>.*?)\n---\n', re.S)
for skill_file in (ROOT/'.agents/skills').glob('*/SKILL.md'):
    sid = skill_file.parent.name
    text = skill_file.read_text(encoding='utf-8')
    m = fm_re.match(text)
    if not m:
        errors.append(f'Skill missing YAML front matter: {sid}')
        continue
    body = m.group('body')
    name_m = re.search(r'^name:\s*(.+)$', body, re.M)
    desc_m = re.search(r'^description:\s*(.+)$', body, re.M)
    if not name_m:
        errors.append(f'Skill front matter missing name: {sid}')
    elif name_m.group(1).strip() != sid:
        errors.append(f'Skill front matter name mismatch for {sid}: {name_m.group(1).strip()}')
    if not desc_m or len(desc_m.group(1).strip()) < 20:
        errors.append(f'Skill front matter description too short/missing: {sid}')
for sid in skills:
    if not (ROOT/'.agents/skills'/sid/'SKILL.md').exists():
        errors.append(f'Missing SKILL.md for indexed skill: {sid}')

# Role assets and references
for r in roles:
    rid = r.get('id')
    if not rid:
        errors.append('Role missing id')
        continue
    if not list((ROOT/'.agents/playbooks').glob(f'*-{rid}.md')):
        errors.append(f'Missing playbook for {rid}')
    if not (ROOT/'.agents/role_cards'/f'{rid}.md').exists():
        errors.append(f'Missing role card for {rid}')
    toml_path = ROOT/'.codex/agents'/f'{rid}.toml'
    if not toml_path.exists():
        errors.append(f'Missing toml agent for {rid}')
    else:
        try:
            data = tomllib.loads(toml_path.read_text(encoding='utf-8'))
            if data.get('name') != rid:
                errors.append(f'TOML name mismatch for {rid}: {data.get("name")}')
            instr = data.get('developer_instructions', '')
            for good_ref in ['docs/EVIDENCE_POLICY.md','docs/QUALITY_GATES.md','docs/SUBAGENT_ORCHESTRATION.md']:
                if good_ref not in instr:
                    errors.append(f'TOML missing qualified critical doc path {good_ref}: {toml_path.name}')
            for phrase in ['INSUFFICIENT EVIDENCE','Do not use aliases','Do not use TASK.md as working memory']:
                if phrase not in instr:
                    errors.append(f'TOML missing required runtime phrase {phrase}: {toml_path.name}')
        except Exception as e:
            errors.append(f'Invalid TOML for {rid}: {e}')
    for sid in r.get('default', []) + r.get('optional', []):
        if sid not in skills:
            errors.append(f'Role {rid} references unknown skill: {sid}')

# Scenario references and behavior
role_set = set(role_ids)
known_behavior_fields = {
    'max_questions','expected_complexity','expected_mode','expected_ds_mode','expected_orchestration','expected_first_step',
    'max_roles','max_active_roles','max_spawned_agents_default','requires_approval_before_spawn','requires_approval_if',
    'must_not_spawn_without_approval','must_not_implement','must_not_implement_without_approval',
    'must_not_implement_before_reference_spec','must_use_phased_orchestration','must_not_duplicate_running_role',
    'must_block_self_validating_manifest','must_not_pass_without_classification','must_not_load','forbidden_files_to_update_as_working_memory',
    'forbidden_terms','forbidden_spawn','forbidden_implementation','required_artifacts','notes'
}
base_fields = {'id','description','request','prompt','required_roles','optional_roles','required_skills','forbidden_skills'}
for s in scenarios:
    sid = s.get('id', '<missing-id>')
    if not s.get('id'):
        errors.append('Scenario missing id')
    for rid in s.get('required_roles') or []:
        if rid not in role_set:
            errors.append(f'{sid}: unknown required role {rid}')
    for rid in s.get('optional_roles') or []:
        if rid not in role_set:
            errors.append(f'{sid}: unknown optional role {rid}')
    for sk in s.get('required_skills') or []:
        if sk not in skills:
            errors.append(f'{sid}: unknown required skill {sk}')
    for sk in s.get('forbidden_skills') or []:
        if sk not in skills:
            errors.append(f'{sid}: unknown forbidden skill {sk}')
    for k in s.keys():
        if k not in base_fields and k not in known_behavior_fields:
            errors.append(f'{sid}: unknown scenario behavior field {k}')
    if s.get('must_not_spawn_without_approval') is True and not s.get('requires_approval_before_spawn'):
        errors.append(f'{sid}: must_not_spawn_without_approval requires requires_approval_before_spawn=true')
    if s.get('must_not_implement_before_reference_spec') is True and 'reference-fidelity' not in (s.get('required_skills') or []):
        errors.append(f'{sid}: reference implementation block requires reference-fidelity')
    if s.get('must_block_self_validating_manifest') is True:
        req = set(s.get('required_skills') or [])
        for sk in ['design-source-authority','manifest-freeze-check']:
            if sk not in req:
                errors.append(f'{sid}: self-validation block requires {sk}')
    if s.get('must_use_phased_orchestration') is True and 'production-service-planning' not in (s.get('required_skills') or []):
        errors.append(f'{sid}: phased orchestration requires production-service-planning')
    if 'TASK.md' in (s.get('forbidden_files_to_update_as_working_memory') or []):
        req = set(s.get('required_skills') or [])
        if not req.intersection({'ticket-router','task-ledger','memory-integrity-check'}):
            errors.append(f'{sid}: TASK.md working-memory ban requires ticketed-memory skill')
    if s.get('id') == 'tiny_copy_change':
        forbidden_loads = set(s.get('must_not_load') or [])
        for item in ['docs/ROLE_TINY_INDEX.json','docs/SKILL_TINY_INDEX.json']:
            if item not in forbidden_loads:
                errors.append('tiny_copy_change must forbid role/skill tiny indexes by default')
    if s.get('id') == 'production_web_service_code_ds':
        req = set(s.get('required_skills') or [])
        for sk in ['visual-qa-loop','component-contract-scan']:
            if sk not in req:
                errors.append(f'production_web_service_code_ds missing production UI skill: {sk}')

scenario_ids = {s.get('id') for s in scenarios}
md_ids = {p.stem for p in (ROOT/'docs/scenario_tests').glob('*.md')}
if scenario_ids != md_ids:
    missing = sorted(scenario_ids - md_ids)
    extra = sorted(md_ids - scenario_ids)
    if missing:
        errors.append(f'Scenario markdown mismatch: missing {missing}')
    if extra:
        errors.append(f'Scenario markdown mismatch: extra {extra}')

# Memory integrity
try:
    run(['node', str(ROOT/'scripts/check-memory-integrity.mjs')], check=True)
except Exception as e:
    errors.append(f'Memory integrity check failed: {e}')

task = read('TASK.md') if (ROOT/'TASK.md').exists() else ''
if 'Deprecated Compatibility Pointer' not in task:
    errors.append('TASK.md is not deprecated compatibility pointer')
if len(task) > 1600:
    errors.append(f'TASK.md shim too large: {len(task)} chars')
for legacy in ['## Scope','## Acceptance criteria','## Role-skill plan','## Verification plan','## Decisions']:
    if legacy in task:
        errors.append(f'TASK.md contains legacy working section: {legacy}')

# Startup / loading policy
fp = read('FIRST_PROMPT.md') if (ROOT/'FIRST_PROMPT.md').exists() else ''
if 'Load only these Tier 0 files first' not in fp:
    errors.append('FIRST_PROMPT.md missing canonical Tier 0 heading')
for item in CANONICAL_TIER0:
    if f'- {item}' not in fp:
        errors.append(f'FIRST_PROMPT.md Tier 0 missing {item}')
first_load_block = fp.split('Do not load all tickets', 1)[0]
if 'docs/QUESTION_TREE.md' in first_load_block:
    errors.append('FIRST_PROMPT.md loads QUESTION_TREE.md in Tier 0 instead of conditionally')
for doc in ['AGENTS.md','docs/BOOTSTRAP_INDEX.md','docs/CONTEXT_BUDGET_POLICY.md','docs/RUNTIME_LOAD_POLICY.md']:
    text = read(doc)
    for item in CANONICAL_TIER0:
        if item not in text:
            errors.append(f'{doc} missing canonical Tier 0 item: {item}')
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/BOOTSTRAP_INDEX.md','docs/CONTEXT_BUDGET_POLICY.md','docs/RUNTIME_LOAD_POLICY.md','docs/FAST_LANE.md','docs/COMPLEXITY_MODEL.md']:
    text = read(doc)
    if 'Tiny/Micro' not in text:
        errors.append(f'{doc} missing Tiny/Micro loading policy')
    if 'do not load role/skill indexes by default' not in text.lower() and 'no role/skill indexes by default' not in text.lower():
        errors.append(f'{doc} missing no-index default for Tiny/Micro')
bootstrap = read('docs/BOOTSTRAP_INDEX.md')
if any(x in bootstrap for x in ['2' + '.0 beta','beta 1',', ,','CURRENT.md / active ticket']):
    errors.append('BOOTSTRAP_INDEX.md contains stale labels or ambiguous refs')
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/BOOTSTRAP_INDEX.md','docs/RUNTIME_LOAD_POLICY.md']:
    if 'SKILL_ROUTER_INDEX.json' not in read(doc):
        errors.append(f'{doc} missing SKILL_ROUTER_INDEX optional routing reference')
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/BOOTSTRAP_INDEX.md','docs/RUNTIME_LOAD_POLICY.md']:
    if 'SKILL_DISCOVERY_POLICY.md' not in read(doc):
        errors.append(f'{doc} missing SKILL_DISCOVERY_POLICY reference')

# Tiny index sanity: do not over-optimize, but require actual savings.
try:
    if (ROOT/'docs/SKILL_TINY_INDEX.json').stat().st_size >= (ROOT/'docs/SKILL_INDEX.json').stat().st_size * 0.9:
        errors.append('SKILL_TINY_INDEX.json is too close to SKILL_INDEX.json size')
    if (ROOT/'docs/ROLE_TINY_INDEX.json').stat().st_size >= (ROOT/'docs/ROLE_MINI_INDEX.json').stat().st_size * 0.8:
        errors.append('ROLE_TINY_INDEX.json is too close to ROLE_MINI_INDEX.json size')
except Exception as e:
    errors.append(f'Tiny index size check failed: {e}')

# Critical phrases
for doc in ['AGENTS.md','FIRST_PROMPT.md']:
    text = read(doc)
    for phrase in ['CURRENT.md','TASK_INDEX.md','active ticket','TASK.md is only a deprecated compatibility pointer']:
        if phrase not in text:
            errors.append(f'{doc} missing ticketed memory phrase: {phrase}')
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/SUBAGENT_ORCHESTRATION.md','docs/UI_QUALITY_GATES.md']:
    text = read(doc)
    for phrase in ['UI Review Packet','SUBAGENT_FAILURE_POLICY','Subagent Completion Status']:
        if phrase not in text:
            errors.append(f'{doc} missing runtime adequacy phrase: {phrase}')
for doc in ['AGENTS.md','FIRST_PROMPT.md','docs/UI_QUALITY_GATES.md']:
    text = read(doc)
    for phrase in ['Reference Fidelity','Generated artifacts cannot validate themselves','Looks similar']:
        if phrase not in text:
            errors.append(f'{doc} missing reference/authority phrase: {phrase}')

# Syntax and semantic scanner checks
for js in ['scripts/find-raw-ui-values.mjs','scripts/check-component-imports.mjs','scripts/check-design-source-authority.mjs','scripts/check-memory-integrity.mjs']:
    try:
        run(['node','--check',str(ROOT/js)], check=True)
    except Exception as e:
        errors.append(f'Node syntax check failed for {js}: {e}')

# Strict DS scanner behavior: native primitive should fail outside DS source in strict mode.
try:
    with tempfile.TemporaryDirectory() as tmp:
        td = Path(tmp)
        (td/'src').mkdir()
        (td/'src/App.tsx').write_text('export function App(){ return <><button>Bad</button><input /></>; }', encoding='utf-8')
        (td/'src/components/ui').mkdir(parents=True)
        (td/'src/components/ui/button.tsx').write_text('export function Button(){ return <button />; }', encoding='utf-8')
        manifest = {
            'ds_mode':'governed_ds',
            'source_of_truth':['src/components/ui'],
            'component_imports':{'Button':'@/components/ui/button','Input':'@/components/ui/input'},
            'tokens':{}, 'forbidden':{}, 'patterns':{}, 'approved_deviations':[], 'ds_roots':['src/components/ui']
        }
        (td/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        res = subprocess.run(['node', str(ROOT/'scripts/check-component-imports.mjs'), str(td/'src'), '--manifest', str(td/'manifest.json'), '--strict-ds', '--fail-on-violation'], cwd=ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            errors.append('check-component-imports strict DS did not fail on native primitives outside DS source')
except Exception as e:
    errors.append(f'Strict DS scanner behavior test failed: {e}')

try:
    run([sys.executable, str(ROOT/'scripts/test-routing.py')], check=True)
except Exception as e:
    errors.append(f'Routing test failed: {e}')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)
print(f'VALIDATION PASSED: {len(role_ids)} roles, {len(skills)} skills, {len(scenarios)} scenarios.')
