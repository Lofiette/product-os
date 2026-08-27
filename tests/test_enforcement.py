
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'tools' / 'cpt_dist.py'


def run_dist(*args: str, env: dict, check: bool = True):
    result = subprocess.run([sys.executable, str(DIST), *args], text=True, capture_output=True, env=env)
    if check and result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result


class EnforcementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_tmp = Path(tempfile.mkdtemp(prefix='cpt-alpha8-enforcement-base-'))
        cls.base_home = cls.base_tmp / 'home'; cls.base_home.mkdir()
        cls.base_repo = cls.base_tmp / 'repo'; cls.base_repo.mkdir()
        subprocess.run(['git','init','-q',str(cls.base_repo)], check=True)
        cls.base_env = os.environ.copy()
        cls.base_env['HOME'] = str(cls.base_home)
        cls.base_env['CODEX_HOME'] = str(cls.base_home / '.codex')
        run_dist('install','--project',str(cls.base_repo),'--mode','local','--enforcement-mode','audit','--plugin-scope','none',env=cls.base_env)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.base_tmp)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='cpt-alpha8-enforcement-case-'))
        self.repo = self.tmp / 'repo'
        shutil.copytree(self.base_repo, self.repo)
        self.home = self.base_home
        self.env = self.base_env.copy()
        self.tool = self.repo / '.cpt/bin/cpt_runtime.py'

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_tool(self, *args: str, input_json: dict | None = None, check: bool = True):
        result = subprocess.run([sys.executable,str(self.tool),*args], cwd=self.repo, text=True, input=None if input_json is None else json.dumps(input_json), capture_output=True)
        if check and result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return result

    def set_mode(self, mode: str):
        self.run_tool('enforcement-set','--mode',mode,'--trust-state','trusted')

    def hook(self, event: str, **extra):
        payload={'session_id':'S1','turn_id':'T1','cwd':str(self.repo),'hook_event_name':event,'model':'gpt-test',**extra}
        return self.run_tool('hook-handle', input_json=payload, check=False)

    def create_task_lease(self, write: str='src/**', verify: str='pytest -q'):
        task=self.run_tool('create-task','--title','Task','--objective','Work','--activate').stdout.strip()
        self.run_tool('lease-create','--task',task,'--read','src/**','--write',write,'--verify',verify)
        return task

    def test_dependency_manifest_patch_requires_explicit_operation_allowance(self):
        self.set_mode('enforce')
        task=self.run_tool('create-task','--title','Manifest','--objective','Adjust manifest','--activate').stdout.strip()
        self.run_tool('lease-create','--task',task,'--read','package.json','--write','package.json')
        denied=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: package.json\n@@\n-{}\n+{"dependencies":{}}'})
        self.assertIn('lease forbids operation: dependency_change',denied.stdout)
        self.run_tool('lease-create','--task',task,'--read','package.json','--write','package.json','--allow-operation','dependency_change')
        allowed=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: package.json\n@@\n-{}\n+{"dependencies":{}}'})
        self.assertEqual(allowed.stdout.strip(),'')

    def test_broad_read_inside_approved_read_scope_is_allowed(self):
        self.set_mode('enforce')
        task=self.run_tool('create-task','--title','Explore','--objective','Inspect source paths','--activate').stdout.strip()
        self.run_tool('lease-create','--task',task,'--read','src/**')
        config_path=self.repo/'.cpt/enforcement.yaml'
        config=yaml.safe_load(config_path.read_text()); config['lease_policy']['read_scope_mode']='enforce'
        config_path.write_text(yaml.safe_dump(config,sort_keys=False))
        result=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'rg --files src'})
        self.assertEqual(result.stdout.strip(),'')


    def test_enforce_mode_requires_trusted_hook_review_record(self):
        result=self.run_tool('enforcement-set','--mode','enforce',check=False)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('requires an explicit trusted hook review record',result.stderr)

    def test_rotated_audit_files_are_included_in_validation(self):
        config_path=self.repo/'.cpt/enforcement.yaml'
        config=yaml.safe_load(config_path.read_text())
        config['audit']['rotate_bytes']=1024
        config['audit']['retain_files']=3
        config_path.write_text(yaml.safe_dump(config,sort_keys=False))
        for index in range(3):
            self.hook('PreToolUse',tool_name='Bash',tool_input={'command':f'curl https://example.com/{index}?token=secret-value-{index:02d}'})
        rotated=list((self.repo/'.cpt/audit').glob('events.jsonl.*'))
        self.assertTrue(rotated)
        result=self.run_tool('audit-validate')
        self.assertIn('across',result.stdout)


    def test_audit_mode_warns_but_does_not_deny_write_without_lease(self):
        r=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: src/a.py\n@@\n-x\n+y'})
        self.assertEqual(r.returncode,0); self.assertIn('additionalContext',r.stdout); self.assertNotIn('permissionDecision": "deny',r.stdout)

    def test_enforce_denies_write_without_lease(self):
        self.set_mode('enforce')
        r=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: src/a.py\n@@\n-x\n+y'})
        self.assertIn('permissionDecision',r.stdout); self.assertIn('deny',r.stdout)

    def test_write_inside_lease_is_allowed_and_outside_is_denied(self):
        self.set_mode('enforce'); self.create_task_lease('src/feature/**')
        allowed=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: src/feature/a.py\n@@\n-x\n+y'})
        self.assertEqual(allowed.stdout.strip(),'')
        denied=self.hook('PreToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: src/other.py\n@@\n-x\n+y'})
        self.assertIn('outside lease scope',denied.stdout)

    def test_verification_must_match_lease(self):
        self.set_mode('enforce'); self.create_task_lease(verify='pytest -q tests/feature')
        ok=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'pytest -q tests/feature'})
        self.assertEqual(ok.stdout.strip(),'')
        bad=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'pytest -q'})
        self.assertIn('not listed in the active lease',bad.stdout)

    def test_globally_destructive_git_is_denied_even_with_lease(self):
        self.set_mode('enforce'); self.create_task_lease('.')
        r=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'git reset --hard HEAD~1'})
        self.assertIn('globally forbidden operation',r.stdout)

    def test_pre_and_post_compact_checkpoint(self):
        self.set_mode('enforce'); self.create_task_lease()
        pre=self.hook('PreCompact',trigger='auto')
        self.assertIn('checkpoint',pre.stdout.lower())
        current=yaml.safe_load((self.repo/'.cpt/current.yaml').read_text()); self.assertTrue(current['latest_checkpoint'])
        post=self.hook('PostCompact',trigger='auto')
        self.assertIn('verified',post.stdout.lower())

    def test_postcompact_mismatch_blocks(self):
        self.set_mode('enforce'); task=self.create_task_lease(); self.hook('PreCompact',trigger='auto')
        path=self.repo/f'.cpt/tasks/{task}.yaml'; data=yaml.safe_load(path.read_text()); data['objective']='mutated'; path.write_text(yaml.safe_dump(data,sort_keys=False))
        post=self.hook('PostCompact',trigger='auto')
        self.assertIn('"continue": false',post.stdout)

    def test_posttool_marks_knowledge_stale(self):
        self.run_tool('knowledge-init','--title','Knowledge','--mode','existing','--owner-role','product_strategist')
        self.run_tool('knowledge-create','--id','area-a','--type','area_map','--title','Area','--owner-role','product_designer','--review-path','src/a/**')
        (self.repo/'src/a').mkdir(parents=True); (self.repo/'src/a/x.py').write_text('x=1\n')
        self.hook('PostToolUse',tool_name='apply_patch',tool_input={'command':'*** Update File: src/a/x.py'},tool_response={'ok':True})
        artifact=yaml.safe_load((self.repo/'.cpt/knowledge/artifacts/area-a.yaml').read_text()); self.assertEqual(artifact['freshness'],'needs_review')

    def test_worker_lifecycle_is_recorded(self):
        self.set_mode('audit')
        self.hook('SubagentStart',agent_id='agent-1',agent_type='explorer',permission_mode='default')
        self.hook('SubagentStop',agent_id='agent-1',agent_type='explorer',agent_transcript_path=None,stop_hook_active=False,last_assistant_message='done',permission_mode='default')
        worker=yaml.safe_load((self.repo/'.cpt/workers/agent-1.yaml').read_text()); self.assertEqual(worker['status'],'completed'); self.assertIsNotNone(worker['last_message_sha256'])

    def test_audit_redacts_secret_and_validates(self):
        self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'curl -H "Authorization: Bearer secret-token-value" https://example.com'})
        text=(self.repo/'.cpt/audit/events.jsonl').read_text(); self.assertNotIn('secret-token-value',text); self.assertIn('[REDACTED]',text)
        self.assertEqual(self.run_tool('audit-validate').returncode,0)

    def test_off_mode_hook_is_noop(self):
        self.set_mode('off')
        before=(self.repo/'.cpt/audit/events.jsonl').stat().st_size if (self.repo/'.cpt/audit/events.jsonl').exists() else 0
        r=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'git reset --hard'})
        after=(self.repo/'.cpt/audit/events.jsonl').stat().st_size if (self.repo/'.cpt/audit/events.jsonl').exists() else 0
        self.assertEqual(r.stdout.strip(),''); self.assertEqual(before,after)


    def test_permission_request_audit_warning_uses_supported_system_message(self):
        r=self.hook('PermissionRequest',tool_name='Bash',tool_input={'command':'curl https://example.com'})
        payload=json.loads(r.stdout)
        self.assertIn('systemMessage',payload)
        self.assertNotIn('hookSpecificOutput',payload)

    def test_read_only_posttool_does_not_mark_preexisting_changes_stale(self):
        self.run_tool('knowledge-init','--title','Knowledge','--mode','existing','--owner-role','product_strategist')
        self.run_tool('knowledge-create','--id','area-read','--type','area_map','--title','Area','--owner-role','product_designer','--review-path','src/a/**')
        (self.repo/'src/a').mkdir(parents=True); (self.repo/'src/a/x.py').write_text('x=1\n')
        self.hook('PostToolUse',tool_name='Bash',tool_input={'command':'git status --short'},tool_response={'ok':True})
        artifact=yaml.safe_load((self.repo/'.cpt/knowledge/artifacts/area-read.yaml').read_text())
        self.assertEqual(artifact['freshness'],'current')

    def test_plugin_bundles_hooks_and_rules_install_is_explicit(self):
        repo2=self.tmp/'plugin-rules'; repo2.mkdir(); subprocess.run(['git','init','-q',str(repo2)],check=True)
        home2=self.tmp/'plugin-home'; home2.mkdir()
        env2=os.environ.copy(); env2['HOME']=str(home2); env2['CODEX_HOME']=str(home2/'.codex')
        run_dist('install','--project',str(repo2),'--mode','local','--enforcement-mode','audit','--rules-profile','conservative',env=env2)
        plugin=home2/'.codex/plugins/cpt-core'
        self.assertTrue((plugin/'hooks/hooks.json').exists())
        self.assertTrue((plugin/'hooks/cpt_hook.py').exists())
        windows_launcher=plugin/'hooks/cpt_hook_windows.ps1'
        self.assertTrue(windows_launcher.exists())
        hooks=json.loads((plugin/'hooks/hooks.json').read_text(encoding='utf-8'))
        commands=[
            hook['commandWindows']
            for groups in hooks['hooks'].values()
            for group in groups
            for hook in group['hooks']
        ]
        self.assertTrue(commands)
        self.assertTrue(all('cpt_hook_windows.ps1' in command for command in commands))
        self.assertTrue(all(not command.startswith('py ') for command in commands))
        if os.name == 'nt':
            payload=json.dumps({'hook_event_name':'SessionStart','cwd':str(repo2),'source':'startup'})
            hook_env=env2.copy(); hook_env['PRODUCT_OS_PYTHON']=sys.executable
            launched=subprocess.run(
                ['powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(windows_launcher)],
                cwd=repo2,input=payload,text=True,capture_output=True,env=hook_env,
            )
            self.assertEqual(launched.returncode,0,launched.stdout+launched.stderr)
        self.assertTrue((repo2/'.codex/rules/cpt.rules').exists())

    def test_lazy_off_install_can_enable_enforcement_later(self):
        repo2=self.tmp/'lazy-enable'; repo2.mkdir(); subprocess.run(['git','init','-q',str(repo2)],check=True)
        run_dist('install','--project',str(repo2),'--mode','local',env=self.env)
        self.assertTrue((repo2/'.cpt/enforcement.yaml').exists())
        data=yaml.safe_load((repo2/'.cpt/enforcement.yaml').read_text())
        self.assertEqual(data['mode'], 'off')
        tool=repo2/'.cpt/bin/cpt_runtime.py'
        result=subprocess.run([sys.executable,str(tool),'enforcement-set','--mode','audit','--trust-state','trusted'],cwd=repo2,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        data=yaml.safe_load((repo2/'.cpt/enforcement.yaml').read_text())
        self.assertEqual(data['mode'],'audit'); self.assertEqual(data['hooks']['trust_state'],'trusted')

    def test_explicit_dependency_lease_can_allow_project_wide_change(self):
        self.set_mode('enforce')
        task=self.run_tool('create-task','--title','Deps','--objective','Update dependency','--activate').stdout.strip()
        self.run_tool('lease-create','--task',task,'--read','**','--write','.','--allow-operation','dependency_change')
        result=self.hook('PreToolUse',tool_name='Bash',tool_input={'command':'pnpm add zod'})
        self.assertEqual(result.stdout.strip(),'')

    def test_precompact_blocks_unmanaged_worker_in_enforce_mode(self):
        self.set_mode('enforce')
        task=self.run_tool('create-task','--title','Delegated','--objective','Review','--activate').stdout.strip()
        self.run_tool('lease-create','--task',task,'--read','src/**')
        start=self.hook('SubagentStart',agent_id='agent-live',agent_type='legacy_explorer',permission_mode='default')
        self.assertIn('"continue": false',start.stdout)
        result=self.hook('PreCompact',trigger='auto')
        self.assertIn('"continue": false',result.stdout)
        self.assertIn('unmanaged worker',result.stdout)


if __name__ == '__main__':
    unittest.main()
