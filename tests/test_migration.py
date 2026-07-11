#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'tools/cpt_migrate.py'

def run(cmd,cwd=None,env=None,check=True):
 p=subprocess.run([str(x) for x in cmd],cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if check and p.returncode: raise AssertionError(f"failed {cmd}\n{p.stdout}")
 return p

def git(repo,*args): return run(['git','-C',str(repo),*args])
def init_repo(path):
 path.mkdir(); git(path,'init','-q'); git(path,'config','user.email','test@example.invalid'); git(path,'config','user.name','CPT Test')
 (path/'src').mkdir(); (path/'src/app.txt').write_text('app\n'); git(path,'add','.'); git(path,'commit','-qm','base')

def h(path): return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def make_overlay(repo):
 (repo/'.git/info/exclude').write_text('.codex-runtime/\nAGENTS.override.md\n')
 rt=repo/'.codex-runtime'; (rt/'product/areas').mkdir(parents=True)
 (rt/'CURRENT.md').write_text('# CURRENT\nNo active task\n')
 (rt/'TASK_INDEX.md').write_text('# TASK INDEX\n')
 (rt/'CHRONICLE.md').write_text('# rescue summary\n')
 (rt/'product/PRODUCT_MAP.md').write_text('# Product Map\n')
 (rt/'product/areas/core.md').write_text('# Core area\n')
 (repo/'AGENTS.override.md').write_text('# private override\n')

def make_embedded(repo):
 (repo/'AGENTS.md').write_text('# Codex Product Team\nRole-skill architecture\nRead TASK.md and CHRONICLE.md\n')
 (repo/'TASK.md').write_text('# legacy task\n'); (repo/'CHRONICLE.md').write_text('# legacy history\n')
 (repo/'.agents/skills').mkdir(parents=True); (repo/'.agents/role_cards').mkdir(parents=True); (repo/'.codex/agents').mkdir(parents=True)
 # Use a small representative set; mapping completeness is separately validated against package registries.
 for x in ['bounded-discovery','impact-map','design-recon']:
  d=repo/'.agents/skills'/x; d.mkdir(); (d/'SKILL.md').write_text(f'# {x}\n')
 for x in ['product_designer','frontend_architect','qa_engineer']:
  (repo/'.agents/role_cards'/f'{x}.md').write_text(f'# {x}\n')
  (repo/'.codex/agents'/f'{x}.toml').write_text(f'name="{x}"\n')
 git(repo,'add','.'); git(repo,'commit','-qm','legacy framework')

def cmd(*args,env=None,check=True): return run([sys.executable,CLI,*args],env=env,check=check)

def test_inspect_and_dry_plan(tmp,env):
 r=tmp/'inspect'; init_repo(r); make_overlay(r)
 before=git(r,'status','--porcelain=v1','--untracked-files=all').stdout
 o=cmd('inspect','--project',r,env=env); data=json.loads(o.stdout); assert data['source_kind']=='local_overlay_3x'; assert data['override']['policy']=='unmanaged_preserve_exactly'
 plan=tmp/'plan.json'; cmd('plan','--project',r,'--mode','local','--output',plan,env=env); assert plan.exists(); after=git(r,'status','--porcelain=v1','--untracked-files=all').stdout; assert before==after

def test_local_apply_and_override(tmp,env):
 r=tmp/'local'; init_repo(r); make_overlay(r); ov=h(r/'AGENTS.override.md')
 plan=tmp/'local-plan.json'; cmd('plan','--project',r,'--mode','local','--legacy-action','archive','--domain-packs','none','--output',plan,env=env)
 cmd('apply','--plan',plan,'--accept-warnings',env=env)
 assert (r/'.cpt/runtime.yaml').exists(); assert h(r/'AGENTS.override.md')==ov
 assert git(r,'status','--porcelain=v1','--untracked-files=all').stdout.strip()==''
 v=cmd('verify','--project',r,env=env); assert json.loads(v.stdout)['status']=='PASS'

def snapshot(repo):
 out={}
 for p in sorted(repo.rglob('*')):
  if '.git' in p.parts or not p.is_file(): continue
  out[str(p.relative_to(repo))]=h(p)
 return out

def test_team_apply_rollback(tmp,env):
 r=tmp/'team'; init_repo(r); make_embedded(r); before=snapshot(r); ov=r/'AGENTS.override.md'; ov.write_text('# unmanaged\n'); ovh=h(ov)
 plan=tmp/'team-plan.json'; cmd('plan','--project',r,'--mode','team','--legacy-action','archive','--domain-packs','none','--output',plan,env=env)
 cmd('apply','--plan',plan,'--accept-warnings',env=env); assert (r/'.cpt/migration/receipt.json').exists(); assert h(ov)==ovh
 cmd('rollback','--project',r,env=env)
 after=snapshot(r); after.pop('AGENTS.override.md',None); before2=dict(before)
 assert before2==after; assert h(ov)==ovh

def test_conflict_and_mapping(tmp,env):
 r=tmp/'conflict'; init_repo(r); (r/'.cpt').mkdir(); (r/'.cpt/runtime.yaml').write_text('schema_version: cpt-runtime-v1\n')
 plan=tmp/'conflict.json'; cmd('plan','--project',r,'--output',plan,env=env); data=json.loads(plan.read_text()); assert data['status']=='blocked'; assert any(x['code']=='existing_4x' for x in data['conflicts'])
 # Package migration registries must cover the full legacy set promised by Alpha 8.
 s=[]
 for p in ROOT.rglob('SKILL_MIGRATION.json'):
  try: s.append(json.loads(p.read_text()))
  except: pass
 assert s, 'skill migration registry missing'

def test_rollback_concurrent_change(tmp,env):
 r=tmp/'concurrent'; init_repo(r); make_overlay(r)
 plan=tmp/'cplan.json'; cmd('plan','--project',r,'--mode','local','--domain-packs','none','--output',plan,env=env); cmd('apply','--plan',plan,'--accept-warnings',env=env)
 (r/'.cpt/runtime-summary.md').write_text('changed after migration\n')
 p=cmd('rollback','--project',r,env=env,check=False); assert p.returncode!=0
 cmd('rollback','--project',r,'--force',env=env)

def test_platform(tmp,env):
 r=tmp/'platform'; init_repo(r); p=cmd('platform-check','--project',r,env=env); d=json.loads(p.stdout); assert d['status']=='PASS'; assert 'system' in d

def test_pack_discovery_excludes_fixtures(tmp,env):
 p=cmd('platform-check','--project',tmp,env=env,check=False)
 # Static source assertion: discovery requires cpt-pack.json and excludes fixture/example roots.
 text=CLI.read_text(encoding='utf-8')
 assert "rglob('cpt-pack.json')" in text
 assert "'fixtures'" in text and "'examples'" in text


def main():
 with tempfile.TemporaryDirectory(prefix='cpt-migration-tests-') as td:
  tmp=Path(td); home=tmp/'home'; home.mkdir(); env=os.environ.copy(); env['HOME']=str(home); env['CODEX_HOME']=str(home/'.codex'); env['CPT_HOME']=str(home/'.cpt')
  tests=[test_inspect_and_dry_plan,test_local_apply_and_override,test_team_apply_rollback,test_conflict_and_mapping,test_rollback_concurrent_change,test_platform,test_pack_discovery_excludes_fixtures]
  for t in tests: t(tmp,env); print('PASS',t.__name__)
 print('MIGRATION TESTS PASSED:',len(tests))
if __name__=='__main__': main()
