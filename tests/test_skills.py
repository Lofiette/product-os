from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relative: str, *args: str):
    return subprocess.run(
        [sys.executable, str(ROOT / relative), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class SkillTests(unittest.TestCase):
    def test_skill_structure_and_migration(self):
        result = run_script('tools/validate_skills.py', '--root', str(ROOT))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('95 unique legacy mappings', result.stdout)
        vnext = run_script('tools/validate_product_design_vnext2.py', '--root', str(ROOT))
        self.assertEqual(vnext.returncode, 0, vnext.stdout + vnext.stderr)

    def test_trigger_proxy_eval(self):
        result = run_script(
            'tools/eval_skill_triggers.py', '--root', str(ROOT),
            '--write-report', str(ROOT / 'evaluation/trigger-eval-report.json')
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads((ROOT / 'evaluation/trigger-eval-report.json').read_text())
        self.assertEqual(report['failed'], 0)
        self.assertEqual(report['case_count'], 147)

    def test_metadata_profiles(self):
        result = run_script('tools/measure_all_skill_metadata.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data['errors'])
        self.assertTrue(data['all_plugins_warning'])
        for profile in data['profiles']:
            self.assertLessEqual(profile['estimated_discovery_chars'], 8000)

    def test_code_audit_scripts_parse(self):
        scripts = ROOT / 'domain-packs/cpt-design-ui/skills/cpt-design-system-code-audit/scripts'
        if subprocess.run(['node', '--version'], capture_output=True).returncode != 0:
            self.skipTest('node is unavailable')
        for path in sorted(scripts.glob('*.mjs')):
            result = subprocess.run(['node', '--check', str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, f'{path}: {result.stdout}{result.stderr}')

    def test_skill_counts(self):
        registry = json.loads((ROOT / 'skills/SKILL_REGISTRY.json').read_text())
        self.assertEqual(len(registry['skills']), 49)
        migration = json.loads((ROOT / 'migration/SKILL_MIGRATION.json').read_text())
        self.assertEqual(len(migration['mappings']), 95)


if __name__ == '__main__':
    unittest.main()
