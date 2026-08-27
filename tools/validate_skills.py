#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
import yaml

REQUIRED_SECTIONS = [
    '## Use when', '## Do not use when', '## Required inputs', '## Method',
    '## Output contract', '## Evidence standard', '## Stop and escalate', '## Failure modes to avoid'
]
GENERIC = [
    'Confirm this skill is needed for the current operation.',
    'Load only relevant files/docs.',
    'Produce the required compact artifact.',
]


def plugin_paths(root: Path):
    yield root / 'payload/marketplace-root/plugins/cpt-core'
    yield from sorted(path for path in (root / 'domain-packs').glob('cpt-*') if path.is_dir())


def frontmatter(text: str):
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError('missing or unclosed frontmatter')
    end = text.find('\n---\n', 4)
    return yaml.safe_load(text[4:end]) or {}


def method_body(text: str) -> str:
    match = re.search(r'## Method\n\n(.*?)(?=\n## )', text, re.S)
    return match.group(1).strip() if match else ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = []
    skills = {}
    methods = collections.defaultdict(list)

    for plugin in plugin_paths(root):
        manifest_path = plugin / '.codex-plugin/plugin.json'
        pack_path = plugin / 'cpt-pack.json'
        if not manifest_path.exists() or not pack_path.exists():
            errors.append(f'{plugin}: missing plugin or pack manifest')
            continue
        manifest = json.loads(manifest_path.read_text())
        pack = json.loads(pack_path.read_text())
        found = []
        for path in sorted((plugin / 'skills').glob('*/SKILL.md')):
            text = path.read_text(encoding='utf-8')
            try:
                fm = frontmatter(text)
            except Exception as exc:
                errors.append(f'{path}: {exc}')
                continue
            name = fm.get('name')
            desc = fm.get('description', '')
            found.append(name)
            if name != path.parent.name:
                errors.append(f'{path}: name/path mismatch {name!r}')
            if name in skills:
                errors.append(f'duplicate skill name: {name}')
            skills[name] = {'plugin': plugin.name, 'description': desc, 'path': str(path)}
            if not desc or len(desc) > 220:
                errors.append(f'{path}: description absent or >220 chars')
            for section in REQUIRED_SECTIONS:
                if section not in text:
                    errors.append(f'{path}: missing {section}')
            for phrase in GENERIC:
                if phrase in text:
                    errors.append(f'{path}: legacy generic boilerplate')
            body = method_body(text)
            if len(body.splitlines()) < 3:
                errors.append(f'{path}: method is too thin')
            methods[body].append(name)
            openai_path = path.parent / 'agents/openai.yaml'
            if not openai_path.exists():
                errors.append(f'{path}: missing agents/openai.yaml')
            else:
                try:
                    oy = yaml.safe_load(openai_path.read_text()) or {}
                    short = oy.get('interface', {}).get('short_description', '')
                    implicit = oy.get('policy', {}).get('allow_implicit_invocation')
                    if not short or len(short) > 100:
                        errors.append(f'{openai_path}: short_description absent or >100 chars')
                    if not isinstance(implicit, bool):
                        errors.append(f'{openai_path}: allow_implicit_invocation must be boolean')
                except Exception as exc:
                    errors.append(f'{openai_path}: invalid YAML: {exc}')
        if pack.get('skill_count') != len(found):
            errors.append(f'{pack_path}: skill_count mismatch')
        if sorted(pack.get('skill_ids', [])) != sorted(found):
            errors.append(f'{pack_path}: skill_ids mismatch')
        if manifest.get('version') != pack.get('version'):
            errors.append(f'{plugin}: plugin/pack version mismatch')

    for body, names in methods.items():
        if body and len(names) > 1:
            errors.append(f'duplicate Method body: {names}')

    registry = json.loads((root / 'skills/SKILL_REGISTRY.json').read_text())
    registered = {item['id']: item for item in registry.get('skills', [])}
    if set(registered) != set(skills):
        errors.append('SKILL_REGISTRY ids do not match installed skills')
    for name, item in registered.items():
        if item.get('plugin') != skills.get(name, {}).get('plugin'):
            errors.append(f'{name}: registry plugin mismatch')
        if item.get('description') != skills.get(name, {}).get('description'):
            errors.append(f'{name}: registry description mismatch')

    cases = json.loads((root / 'evaluation/skill-trigger-cases.json').read_text()).get('cases', [])
    by_skill = collections.defaultdict(list)
    for case in cases:
        by_skill[case.get('skill')].append(case)
    if set(by_skill) != set(skills):
        errors.append('trigger case coverage does not match active skills')
    for name, items in by_skill.items():
        positives = [item for item in items if item.get('expected') == 'invoke']
        negatives = [item for item in items if item.get('expected') == 'do_not_invoke']
        if len(positives) < 2 or len(negatives) < 1:
            errors.append(f'{name}: requires >=2 positive and >=1 negative trigger cases')

    migration = json.loads((root / 'migration/SKILL_MIGRATION.json').read_text())
    mappings = migration.get('mappings', [])
    sources = [item.get('source_skill') for item in mappings]
    if migration.get('source_count') != 95 or len(mappings) != 95 or len(set(sources)) != 95:
        errors.append('legacy migration must contain 95 unique source skills')
    mapped_targets = {item.get('target_skill') for item in mappings}
    new_skills = set(migration.get('new_skills', []))
    if migration.get('target_count') != len(skills):
        errors.append('migration target_count does not match active skills')
    if mapped_targets & new_skills:
        errors.append('new_skills must not duplicate legacy mapping targets')
    if mapped_targets | new_skills != set(skills):
        errors.append('legacy targets plus new_skills do not match active skills')
    for item in mappings:
        target = item.get('target_skill')
        if item.get('target_plugin') != skills.get(target, {}).get('plugin'):
            errors.append(f"{item.get('source_skill')}: target plugin mismatch")

    if errors:
        print('SKILL VALIDATION FAILED')
        for error in errors:
            print('ERROR:', error)
        return 1
    print(f'SKILL VALIDATION PASSED: {len(skills)} active skills, 95 unique legacy mappings, {len(list(plugin_paths(root)))} plugins')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
