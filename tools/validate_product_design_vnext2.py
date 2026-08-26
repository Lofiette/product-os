#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import yaml

NEW_SKILLS = {
    'cpt-interaction-pattern-selection',
    'cpt-form-task-flow-design',
    'cpt-professional-data-interface-design',
    'cpt-design-execution-orchestration',
}
CAPABILITIES = {
    'context.confirm', 'research.synthesize', 'source.live.inspect',
    'source.screenshot.inspect', 'visual.direction.generate',
    'prototype.interactive.build', 'frontend.responsive.build',
    'source.image.to.code', 'qa.visual.diff', 'artifact.design.export',
    'artifact.annotate', 'preview.publish',
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def fail(errors: list[str]) -> int:
    print('PRODUCT DESIGN VNEXT2 VALIDATION FAILED')
    for error in errors:
        print('ERROR:', error)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    pack = root / 'domain-packs/cpt-design-ui'
    errors: list[str] = []

    for skill in NEW_SKILLS:
        base = pack / 'skills' / skill
        for rel in ('SKILL.md', 'agents/openai.yaml'):
            if not (base / rel).exists():
                errors.append(f'{skill}: missing {rel}')

    behavior = load_yaml(pack / 'skills/cpt-interaction-pattern-selection/references/BEHAVIOR_LENSES.yaml')
    if behavior.get('schema') != 'cpt-behavior-lenses-v1':
        errors.append('behavior lens schema mismatch')
    lenses = behavior.get('lenses', [])
    lens_ids = [item.get('id') for item in lenses]
    if len(lens_ids) != 12 or len(set(lens_ids)) != 12:
        errors.append('behavior lens library must contain 12 unique lenses')
    for item in lenses:
        for key in ('id','name','problem_signal','design_questions','supports','failure_signals'):
            if not item.get(key):
                errors.append(f"behavior lens {item.get('id')}: missing {key}")

    pattern_files = [
        'PAGE_NAVIGATION_PATTERNS.yaml',
        'WORKSPACE_COMMAND_PATTERNS.yaml',
        'DATA_EXPLORATION_PATTERNS.yaml',
    ]
    patterns = []
    for name in pattern_files:
        data = load_yaml(pack / 'skills/cpt-interaction-pattern-selection/references' / name)
        if data.get('schema') != 'cpt-interaction-pattern-catalog-v1':
            errors.append(f'{name}: schema mismatch')
        patterns.extend(data.get('patterns', []))
    pattern_ids = [item.get('id') for item in patterns]
    if len(pattern_ids) < 40 or len(pattern_ids) != len(set(pattern_ids)):
        errors.append('interaction pattern catalog must contain >=40 unique patterns')
    for item in patterns:
        for key in ('id','family','name','problem','use_when','avoid_when','forces','procedure','alternatives'):
            if not item.get(key):
                errors.append(f"interaction pattern {item.get('id')}: missing {key}")

    form_modes = load_yaml(pack / 'skills/cpt-form-task-flow-design/references/FORM_FLOW_MODE_MATRIX.yaml')
    if form_modes.get('schema') != 'cpt-form-flow-mode-matrix-v1':
        errors.append('form flow mode schema mismatch')
    modes = form_modes.get('modes', [])
    if len(modes) != 8 or len({item.get('id') for item in modes}) != 8:
        errors.append('form flow mode matrix must contain 8 unique modes')

    form_data = load_yaml(pack / 'skills/cpt-form-task-flow-design/references/FORM_PATTERN_CATALOG.yaml')
    if form_data.get('schema') != 'cpt-form-pattern-catalog-v1':
        errors.append('form pattern schema mismatch')
    form_patterns = form_data.get('patterns', [])
    form_ids = [item.get('id') for item in form_patterns]
    if len(form_ids) < 24 or len(form_ids) != len(set(form_ids)):
        errors.append('form pattern catalog must contain >=24 unique patterns')
    for item in form_patterns:
        for key in ('id','name','problem','use_when','procedure','avoid_when','tests'):
            if not item.get(key):
                errors.append(f"form pattern {item.get('id')}: missing {key}")

    professional = load_yaml(pack / 'skills/cpt-professional-data-interface-design/references/PROFESSIONAL_TASK_MATRIX.yaml')
    if professional.get('schema') != 'cpt-professional-task-matrix-v1':
        errors.append('professional task matrix schema mismatch')
    workflows = professional.get('workflows', [])
    if len(workflows) != 7 or len({item.get('id') for item in workflows}) != 7:
        errors.append('professional task matrix must contain 7 unique workflows')
    known_pattern_ids = set(pattern_ids) | set(form_ids)
    for item in workflows:
        for pattern in item.get('patterns', []):
            if pattern not in known_pattern_ids:
                errors.append(f"professional workflow {item.get('id')}: unknown pattern {pattern}")

    schema = json.loads((pack / 'skills/cpt-design-execution-orchestration/references/DESIGN_EXECUTION_ADAPTER_SCHEMA.json').read_text())
    if schema.get('properties', {}).get('schema', {}).get('const') != 'cpt-design-execution-adapter-v1':
        errors.append('execution adapter JSON schema mismatch')
    adapters_dir = pack / 'skills/cpt-design-execution-orchestration/references/adapters'
    adapters = []
    for path in sorted(adapters_dir.glob('*.yaml')):
        data = load_yaml(path)
        adapters.append(data)
        if data.get('schema') != 'cpt-design-execution-adapter-v1':
            errors.append(f'{path.name}: adapter schema mismatch')
        if not data.get('id') or not data.get('provider') or not data.get('detection'):
            errors.append(f'{path.name}: incomplete adapter identity/detection')
        for mapping in data.get('capability_map', []):
            if mapping.get('capability') not in CAPABILITIES:
                errors.append(f"{path.name}: unknown capability {mapping.get('capability')}")
            if mapping.get('use_only_if_observed') is not True:
                errors.append(f'{path.name}: every mapping must require observed availability')
    if {item.get('id') for item in adapters} != {'generic-agent-tools','openai-product-design'}:
        errors.append('execution plane must include generic and optional OpenAI adapters')
    openai = next((item for item in adapters if item.get('id') == 'openai-product-design'), {})
    if openai.get('status') != 'optional':
        errors.append('OpenAI Product Design adapter must remain optional')
    if not openai.get('detection', {}).get('do_not_assume'):
        errors.append('OpenAI adapter must document non-assumptions')

    role_registry = json.loads((root / 'roles/ROLE_REGISTRY.json').read_text())
    role = next((item for item in role_registry.get('roles', []) if item.get('id') == 'product_designer'), {})
    required = set(role.get('required_skills', []))
    optional = set(role.get('optional_skills', []))
    if 'cpt-interaction-pattern-selection' not in required:
        errors.append('Product Designer must require interaction pattern selection')
    if not {'cpt-form-task-flow-design','cpt-professional-data-interface-design','cpt-design-execution-orchestration'} <= optional:
        errors.append('Product Designer optional vNext2 skills are incomplete')

    migration = json.loads((root / 'migration/SKILL_MIGRATION.json').read_text())
    if set(migration.get('new_skills', [])) != NEW_SKILLS:
        errors.append('migration new_skills does not match vNext2 skills')

    screen = (pack / 'skills/cpt-screen-module-design/SKILL.md').read_text(encoding='utf-8')
    for skill in NEW_SKILLS:
        if skill not in screen:
            errors.append(f'screen-module-design does not route to {skill}')

    if errors:
        return fail(errors)
    print(
        'PRODUCT DESIGN VNEXT2 VALIDATION PASSED: '
        f'{len(lenses)} behavior lenses, {len(patterns)} interaction patterns, '
        f'{len(modes)} form modes, {len(form_patterns)} form patterns, '
        f'{len(workflows)} professional workflows, {len(adapters)} execution adapters'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
