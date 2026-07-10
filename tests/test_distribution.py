from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools' / 'cpt_dist.py'
DOMAIN_TEMPLATE = ROOT / 'templates' / 'domain-plugin'


def run(*args: str, cwd: Path | None = None, env: dict | None = None, check: bool = True):
    result = subprocess.run([sys.executable, str(TOOL), *args], cwd=cwd, env=env, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(f"command failed {args}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='cpt-alpha5-test-'))
        self.home = self.tmp / 'home'
        self.home.mkdir()
        self.env = os.environ.copy()
        self.env['HOME'] = str(self.home)
        self.env['CODEX_HOME'] = str(self.home / '.codex')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def init_git(self, repo: Path):
        repo.mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)

    def test_local_install_is_git_clean_and_small(self):
        repo = self.tmp / 'local'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        status = subprocess.run(['git', '-C', str(repo), 'status', '--short', '--untracked-files=all'], text=True, capture_output=True, check=True)
        self.assertEqual(status.stdout.strip(), '')
        data = json.loads(run('status', '--project', str(repo), '--json', env=self.env).stdout)
        self.assertLess(data['framework_file_count'], 20)
        self.assertTrue(data['runtime_valid'])

    def test_team_repo_plugin_stays_below_twenty_files(self):
        repo = self.tmp / 'team'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        data = json.loads(run('status', '--project', str(repo), '--json', env=self.env).stdout)
        self.assertLess(data['framework_file_count'], 20)
        self.assertTrue((repo / 'plugins/cpt-core/.codex-plugin/plugin.json').exists())
        self.assertTrue((repo / '.agents/plugins/marketplace.json').exists())

    def test_local_existing_tracked_agents_is_not_modified(self):
        repo = self.tmp / 'tracked-agents'
        self.init_git(repo)
        agents = repo / 'AGENTS.md'
        agents.write_text('# Existing\n', encoding='utf-8')
        subprocess.run(['git', '-C', str(repo), 'add', 'AGENTS.md'], check=True)
        before = agents.read_text()
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        self.assertEqual(agents.read_text(), before)
        self.assertTrue((repo / '.cpt/AGENTS_SNIPPET.md').exists())

    def test_update_preserves_mutable_runtime_state(self):
        repo = self.tmp / 'update'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        current = repo / '.cpt/current.yaml'
        current.write_text(current.read_text().replace('state_revision: 0', 'state_revision: 7'), encoding='utf-8')
        run('update', '--project', str(repo), env=self.env)
        self.assertIn('state_revision: 7', current.read_text())

    def test_update_refuses_modified_managed_tool(self):
        repo = self.tmp / 'conflict'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        ops = repo / '.cpt/OPERATIONS.md'
        ops.write_text(ops.read_text() + '\nlocal edit\n', encoding='utf-8')
        result = run('update', '--project', str(repo), env=self.env, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn('managed files changed', result.stderr)

    def test_uninstall_does_not_touch_application_files(self):
        repo = self.tmp / 'uninstall'
        self.init_git(repo)
        source = repo / 'src/app.py'
        source.parent.mkdir(parents=True)
        source.write_text('print("keep")\n')
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        run('uninstall', '--project', str(repo), '--discard-state', env=self.env)
        self.assertEqual(source.read_text(), 'print("keep")\n')
        self.assertFalse((repo / '.cpt').exists())
        self.assertFalse((repo / 'AGENTS.md').exists())

    def test_personal_marketplace_preserves_other_plugins(self):
        market = self.home / '.agents/plugins/marketplace.json'
        market.parent.mkdir(parents=True)
        market.write_text(json.dumps({'name': 'existing', 'plugins': [{'name': 'other', 'source': {'source': 'local', 'path': './other'}}]}))
        repo = self.tmp / 'market'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        data = json.loads(market.read_text())
        self.assertEqual({p['name'] for p in data['plugins']}, {'other', 'cpt-core'})

    def test_domain_pack_is_independent(self):
        repo = self.tmp / 'packs'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        pack = self.tmp / 'cpt-domain-test'
        shutil.copytree(DOMAIN_TEMPLATE, pack)
        manifest = json.loads((pack / '.codex-plugin/plugin.json').read_text())
        manifest['name'] = 'cpt-domain-test'
        (pack / '.codex-plugin/plugin.json').write_text(json.dumps(manifest))
        meta = json.loads((pack / 'cpt-pack.json').read_text())
        meta['name'] = 'cpt-domain-test'
        (pack / 'cpt-pack.json').write_text(json.dumps(meta))
        run('pack-add', '--path', str(pack), '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertTrue((repo / 'plugins/cpt-domain-test').exists())
        run('pack-remove', '--name', 'cpt-domain-test', '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertFalse((repo / 'plugins/cpt-domain-test').exists())
        self.assertTrue((repo / 'plugins/cpt-core').exists())

    def test_team_merge_and_uninstall_preserves_existing_agents(self):
        repo = self.tmp / 'team-existing-agents'
        self.init_git(repo)
        agents = repo / 'AGENTS.md'
        agents.write_text('# Existing project guidance\n', encoding='utf-8')
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        self.assertIn('CPT-OS KERNEL BEGIN', agents.read_text())
        run('uninstall', '--project', str(repo), '--discard-state', env=self.env)
        self.assertEqual(agents.read_text(), '# Existing project guidance\n')

    def test_personal_plugin_survives_project_uninstall_by_default(self):
        repo = self.tmp / 'personal-survives'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        plugin = self.home / '.codex/plugins/cpt-core'
        self.assertTrue(plugin.exists())
        run('uninstall', '--project', str(repo), '--discard-state', env=self.env)
        self.assertTrue(plugin.exists())

    def test_metadata_budget_is_small(self):
        plugin = ROOT / 'payload/marketplace-root/plugins/cpt-core'
        result = run('metadata-budget', '--plugin', str(plugin), env=self.env)
        data = json.loads(result.stdout)
        self.assertEqual(data['skill_count'], 3)
        self.assertLess(data['estimated_discovery_chars'], 2000)

    def test_bundled_pack_can_be_added_by_name(self):
        repo = self.tmp / 'bundled-pack'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        run('pack-add', '--name', 'cpt-design-ui', '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertTrue((repo / 'plugins/cpt-design-ui/.codex-plugin/plugin.json').exists())
        receipt = json.loads((repo / '.cpt/install.json').read_text())
        self.assertTrue(any(p['name'] == 'cpt-design-ui' for p in receipt['packs']))
        run('pack-remove', '--name', 'cpt-design-ui', '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertFalse((repo / 'plugins/cpt-design-ui').exists())

    def test_doctor_passes(self):
        repo = self.tmp / 'doctor'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'local', env=self.env)
        result = run('doctor', '--project', str(repo), env=self.env)
        self.assertIn('runtime: PASS', result.stdout)

    def test_bundled_pack_catalog_and_install(self):
        catalog = run('pack-catalog', env=self.env).stdout
        self.assertIn('cpt-design-ui', catalog)
        self.assertIn('cpt-engineering', catalog)
        repo = self.tmp / 'bundled-pack'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        run('pack-add', '--name', 'cpt-design-ui', '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertTrue((repo / 'plugins/cpt-design-ui/skills/cpt-design-recon/SKILL.md').exists())
        run('pack-remove', '--name', 'cpt-design-ui', '--scope', 'repo', '--project', str(repo), env=self.env)
        self.assertFalse((repo / 'plugins/cpt-design-ui').exists())

    def test_skill_resolve_legacy_and_active(self):
        legacy = run('skill-resolve', '--name', 'bounded-discovery', '--json', env=self.env)
        legacy_data = json.loads(legacy.stdout)
        self.assertEqual(legacy_data['target_skill'], 'cpt-task-planning')
        active = run('skill-resolve', '--name', 'cpt-api-contract', '--json', env=self.env)
        active_data = json.loads(active.stdout)
        self.assertEqual(active_data['plugin'], 'cpt-engineering')

    def test_knowledge_directories_are_lazy_and_file_budget_stays_small(self):
        repo = self.tmp / 'knowledge-lazy'
        self.init_git(repo)
        run('install', '--project', str(repo), '--mode', 'team', env=self.env)
        data = json.loads(run('status', '--project', str(repo), '--json', env=self.env).stdout)
        self.assertLess(data['framework_file_count'], 20)
        self.assertTrue((repo / '.cpt/knowledge/artifacts').is_dir())
        self.assertFalse((repo / '.cpt/knowledge/index.yaml').exists())


if __name__ == '__main__':
    unittest.main()
