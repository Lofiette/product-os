#!/usr/bin/env python3
"""CPT 3.x -> 4.0 migration assistant.

The assistant is conservative by design:
- inspect and plan are read-only;
- apply requires an explicit command;
- backups live outside the project by default;
- AGENTS.override.md is never read, modified, migrated, or validated;
- legacy claims are preserved as unverified imports, never silently promoted;
- rollback refuses concurrent modifications unless explicitly forced.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, platform, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from typing import Any

SCHEMA_PLAN = 'cpt-migration-plan-v1'
SCHEMA_RECEIPT = 'cpt-migration-receipt-v1'
TARGET_VERSION = '4.0.0-alpha.9'
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DIST_TOOL = PACKAGE_ROOT / 'tools' / 'cpt_dist.py'

LEGACY_FRAMEWORK_DIRS = [
    '.agents', '.codex-runtime',
]
LEGACY_AGENT_DIR = '.codex/agents'
LEGACY_ROOT_FILES = [
    'FIRST_PROMPT.md','TASK.md','CHRONICLE.md','TEAM.md','KIT_MANIFEST.md',
    'AGENTS.source.md','SELF_AUDIT_REPORT.md'
]
LEGACY_MARKERS = [
    'codex product team', 'role-skill architecture', 'subagent orchestration',
    'product knowledge onboarding', 'runtime decision tree'
]
PRODUCT_KNOWLEDGE_NAMES = {'PRODUCT_MAP.md','KNOWLEDGE_INDEX.md'}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    os.replace(tmp, path)

def load_json(path: Path, default=None):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception: return default

def hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def hash_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024), b''): h.update(c)
    return h.hexdigest()

def run(cmd, cwd=None, env=None, check=True):
    p=subprocess.run([str(x) for x in cmd], cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(map(str,cmd))}\n{p.stdout}")
    return p

def git(project: Path, *args, check=False):
    return run(['git','-C',str(project),*args], check=check)

def git_root(project: Path) -> Path|None:
    p=git(project,'rev-parse','--show-toplevel')
    return Path(p.stdout.strip()).resolve() if p.returncode==0 else None

def git_status(project: Path) -> list[str]:
    p=git(project,'status','--porcelain=v1','--untracked-files=all')
    return [x for x in p.stdout.splitlines() if x.strip()] if p.returncode==0 else []

def is_tracked(project: Path, rel: str) -> bool:
    return git(project,'ls-files','--error-unmatch','--',rel).returncode==0

def safe_text(path: Path, limit=200000) -> str:
    try:
        if path.stat().st_size > limit: return ''
        return path.read_text(encoding='utf-8', errors='replace')
    except Exception: return ''

def framework_owned_agents(path: Path) -> bool:
    text=safe_text(path).lower()
    hits=sum(1 for x in LEGACY_MARKERS if x in text)
    return hits>=2 or ('task.md' in text and 'chronicle.md' in text and 'codex' in text)

def find_registry(name: str) -> Path|None:
    matches=list(PACKAGE_ROOT.rglob(name))
    return sorted(matches, key=lambda p:len(p.parts))[0] if matches else None

def extract_mapping(path: Path|None) -> dict[str,str]:
    if not path: return {}
    data=load_json(path,{})
    out={}
    source_keys=('source_id','legacy_id','source','from','old_id','legacy_skill','legacy_role')
    target_keys=('target_id','canonical_id','target','to','new_id','canonical_skill','canonical_role')
    def walk(v):
        if isinstance(v,dict):
            src=next((v.get(k) for k in source_keys if isinstance(v.get(k),str)),None)
            tgt=next((v.get(k) for k in target_keys if isinstance(v.get(k),str)),None)
            if src and tgt: out[src]=tgt
            # direct map heuristic
            if all(isinstance(k,str) and isinstance(val,str) for k,val in v.items()) and len(v)<300:
                for k,val in v.items():
                    if re.match(r'^[a-z0-9][a-z0-9_-]+$',k) and re.match(r'^[a-z0-9][a-z0-9_-]+$',val): out.setdefault(k,val)
            for val in v.values(): walk(val)
        elif isinstance(v,list):
            for x in v: walk(x)
    walk(data)
    return out

def discover_ids(project: Path, kind: str) -> list[str]:
    ids=set()
    if kind=='skills':
        for base in [project/'.agents/skills', project/'.agents'/'skills']:
            if base.is_dir():
                for p in base.iterdir():
                    if p.is_dir() and ((p/'SKILL.md').exists() or any(p.iterdir())): ids.add(p.name)
        idx=project/'docs/SKILL_INDEX.json'
        data=load_json(idx,{})
        def walk(v):
            if isinstance(v,dict):
                for key in ('id','skill_id','name'):
                    val=v.get(key)
                    if isinstance(val,str) and re.match(r'^[a-z0-9][a-z0-9_-]+$',val): ids.add(val)
                for x in v.values(): walk(x)
            elif isinstance(v,list):
                for x in v: walk(x)
        walk(data)
    else:
        for base in [project/'.agents/role_cards', project/'.agents/playbooks']:
            if base.is_dir():
                for p in base.iterdir():
                    if p.is_file() and p.suffix=='.md': ids.add(p.stem)
        idx=project/'docs/ROLE_INDEX.json'; data=load_json(idx,{})
        def walk(v):
            if isinstance(v,dict):
                for key in ('id','role_id'):
                    val=v.get(key)
                    if isinstance(val,str) and re.match(r'^[a-z0-9][a-z0-9_-]+$',val): ids.add(val)
                for x in v.values(): walk(x)
            elif isinstance(v,list):
                for x in v: walk(x)
        walk(data)
    return sorted(ids)

def inventory(project: Path) -> dict[str,Any]:
    project=project.resolve()
    root=git_root(project)
    version_markers=[]
    for rel in ['README.md','AGENTS.md','KIT_MANIFEST.md','docs/RELEASE_NOTES_2.1_BETA4.md','docs/RELEASE_NOTES_3.0.md']:
        p=project/rel
        t=safe_text(p).lower()
        for m in ('3.0','2.1','2.0','codex product team'):
            if m in t: version_markers.append({'path':rel,'marker':m})
    skill_ids=discover_ids(project,'skills'); role_ids=discover_ids(project,'roles')
    pk=[]
    pkr=project/'.codex-runtime/product'
    if pkr.is_dir(): pk=[str(p.relative_to(project)) for p in pkr.rglob('*.md')]
    runtime=[]
    for rel in ['CURRENT.md','TASK_INDEX.md','TASK.md','CHRONICLE.md','.codex-runtime/CURRENT.md','.codex-runtime/TASK_INDEX.md','.codex-runtime/CHRONICLE.md']:
        if (project/rel).exists(): runtime.append(rel)
    legacy_dirs=[d for d in LEGACY_FRAMEWORK_DIRS if (project/d).exists()]
    if (project/LEGACY_AGENT_DIR).exists(): legacy_dirs.append(LEGACY_AGENT_DIR)
    root_files=[f for f in LEGACY_ROOT_FILES if (project/f).exists()]
    agents=project/'AGENTS.md'
    agents_owned=agents.exists() and framework_owned_agents(agents)
    current4=(project/'.cpt/runtime.yaml').exists()
    if current4: kind='current_4x'
    elif (project/'.codex-runtime').exists(): kind='local_overlay_3x'
    elif skill_ids or role_ids or version_markers: kind='embedded_3x'
    else: kind='clean_or_unknown'
    return {
      'project':str(project),'git_root':str(root) if root else None,'git_status':git_status(project),
      'source_kind':kind,'version_markers':version_markers,
      'legacy_skill_ids':skill_ids,'legacy_role_ids':role_ids,
      'legacy_framework_dirs':legacy_dirs,'legacy_root_files':root_files,
      'legacy_runtime_files':runtime,'product_knowledge_files':pk,
      'agents_md':{'exists':agents.exists(),'tracked':is_tracked(project,'AGENTS.md') if root else False,'framework_owned':agents_owned},
      'override':{'present':(project/'AGENTS.override.md').exists(),'policy':'unmanaged_preserve_exactly'},
      'current_4x':current4,
      'platform':{'system':platform.system(),'release':platform.release(),'python':platform.python_version(),'wsl':bool(os.environ.get('WSL_DISTRO_NAME'))},
    }

def plan_hash(plan: dict) -> str:
    c=dict(plan); c.pop('plan_hash',None)
    return hash_bytes(json.dumps(c,sort_keys=True,separators=(',',':')).encode())

def default_state_dir() -> Path:
    return Path(os.environ.get('CPT_HOME', Path.home()/'.cpt')).expanduser()

def make_plan(project: Path, mode: str, legacy_action: str, agents_policy: str, packs: str, with_workers: bool, allow_existing_4x: bool) -> dict:
    inv=inventory(project)
    smap=extract_mapping(find_registry('SKILL_MIGRATION.json'))
    rmap=extract_mapping(find_registry('ROLE_MIGRATION.json'))
    skills=inv['legacy_skill_ids']; roles=inv['legacy_role_ids']
    mapped_skills={x:smap.get(x) for x in skills if smap.get(x)}
    mapped_roles={x:rmap.get(x,x if x in rmap.values() else None) for x in roles}
    mapped_roles={k:v for k,v in mapped_roles.items() if v}
    unmapped_skills=sorted(set(skills)-set(mapped_skills)); unmapped_roles=sorted(set(roles)-set(mapped_roles))
    conflicts=[]; warnings=[]
    if inv['current_4x'] and not allow_existing_4x: conflicts.append({'code':'existing_4x','message':'A 4.x runtime already exists; use update instead or explicitly allow review migration.'})
    if not DIST_TOOL.exists(): conflicts.append({'code':'missing_dist_tool','message':'CPT distribution tool is missing.'})
    if inv['git_status']:
        warnings.append({'code':'dirty_worktree','message':'Project has uncommitted changes. Migration will not stage or commit them.'})
    if inv['agents_md']['exists'] and not inv['agents_md']['framework_owned'] and agents_policy=='replace-if-framework':
        warnings.append({'code':'agents_ambiguous','message':'Existing AGENTS.md is not confidently framework-owned and will be preserved.'})
    if inv['override']['present']:
        warnings.append({'code':'override_unmanaged','message':'AGENTS.override.md is preserved exactly and remains outside the migration contract.'})
    if unmapped_skills: warnings.append({'code':'custom_skills','message':f'{len(unmapped_skills)} legacy/custom skills are not in the canonical mapping and will be preserved for review.'})
    if unmapped_roles: warnings.append({'code':'custom_roles','message':f'{len(unmapped_roles)} legacy/custom roles are not in the canonical mapping and will be preserved for review.'})
    mid='MIG-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+hashlib.sha256(str(project.resolve()).encode()).hexdigest()[:8]
    backup=default_state_dir()/'backups'/hashlib.sha256(str(project.resolve()).encode()).hexdigest()[:16]/mid
    actions=[
      {'id':'backup','kind':'backup','description':'Create an external, hash-verified backup of every path CPT may modify or retire.'},
      {'id':'install','kind':'install_core','description':f'Install the 4.0 runtime in {mode} mode using cpt_dist.py.'},
      {'id':'runtime-import','kind':'import_legacy_runtime','description':'Preserve legacy task/runtime documents as unverified migration sources; do not activate them automatically.'},
      {'id':'knowledge-import','kind':'import_product_knowledge','description':'Preserve legacy Product Knowledge Markdown and index it as needs-review migration evidence.'},
      {'id':'mapping','kind':'record_mappings','description':'Record 3.x skill and role mappings to 4.0 canonical assets.'},
      {'id':'legacy','kind':legacy_action,'description':f'Legacy framework action: {legacy_action}.'},
      {'id':'validate','kind':'validate','description':'Run doctor, runtime validation, migration verification, and Git status reporting.'},
    ]
    status='blocked' if conflicts else ('review' if warnings else 'ready')
    plan={
      'schema_version':SCHEMA_PLAN,'migration_id':mid,'created_at':now(),'status':status,
      'project':str(project.resolve()),'mode':mode,'source':inv,
      'target':{'version':TARGET_VERSION,'distribution_root':str(PACKAGE_ROOT)},
      'options':{'legacy_action':legacy_action,'agents_policy':agents_policy,'domain_packs':packs,'with_workers':with_workers,'allow_existing_4x':allow_existing_4x},
      'mapping':{'skills':mapped_skills,'roles':mapped_roles,'unmapped_skills':unmapped_skills,'unmapped_roles':unmapped_roles,
                 'skill_registry':str(find_registry('SKILL_MIGRATION.json') or ''),'role_registry':str(find_registry('ROLE_MIGRATION.json') or '')},
      'actions':actions,'conflicts':conflicts,'warnings':warnings,'backup':{'path':str(backup)},
      'guarantees':{'override_unmanaged':True,'no_stage_or_commit':True,'external_services_required':False,'canonical_claims_auto_promoted':False}
    }
    plan['plan_hash']=plan_hash(plan)
    return plan

def file_manifest(path: Path) -> dict[str,Any]:
    if not path.exists(): return {'exists':False}
    if path.is_file(): return {'exists':True,'type':'file','sha256':hash_file(path),'size':path.stat().st_size}
    files=[]
    for p in sorted(path.rglob('*')):
        if p.is_file(): files.append({'path':str(p.relative_to(path)),'sha256':hash_file(p),'size':p.stat().st_size})
    return {'exists':True,'type':'directory','files':files}

def copy_path(src: Path, dst: Path):
    if src.is_dir(): shutil.copytree(src,dst,dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

def backup_paths(project: Path, plan: dict) -> dict:
    backup=Path(plan['backup']['path'])
    if backup.exists(): raise RuntimeError(f'Backup already exists: {backup}')
    backup.mkdir(parents=True)
    rels=set(['.cpt','AGENTS.md','.git/info/exclude','.codex/plugins','.codex/marketplace.json','.codex/agents'])
    rels.update(plan['source']['legacy_framework_dirs']); rels.update(plan['source']['legacy_root_files']); rels.update(plan['source']['legacy_runtime_files'])
    entries=[]
    for rel in sorted(rels):
        if rel=='AGENTS.override.md': continue
        src=project/rel
        rec={'path':rel,**file_manifest(src)}
        if src.exists(): copy_path(src,backup/'files'/rel)
        entries.append(rec)
    manifest={'schema_version':'cpt-migration-backup-v1','migration_id':plan['migration_id'],'created_at':now(),'project':str(project),'entries':entries,'plan_hash':plan['plan_hash']}
    dump_json(backup/'backup_manifest.json',manifest)
    dump_json(backup/'plan.json',plan)
    return manifest

def remove_path(p: Path):
    if p.is_dir() and not p.is_symlink(): shutil.rmtree(p)
    elif p.exists() or p.is_symlink(): p.unlink()

def known_framework_paths(project: Path, plan: dict) -> list[str]:
    out=[]
    for rel in plan['source']['legacy_framework_dirs']+plan['source']['legacy_root_files']:
        if rel=='AGENTS.override.md': continue
        out.append(rel)
    if plan['source']['agents_md']['framework_owned']: out.append('AGENTS.md')
    return sorted(set(out))

def import_sources(project: Path, backup: Path, plan: dict):
    base=project/'.cpt/migration/imports'; base.mkdir(parents=True,exist_ok=True)
    imported=[]
    for rel in plan['source']['legacy_runtime_files']:
        src=backup/'files'/rel
        if src.exists():
            dst=base/'runtime'/rel; copy_path(src,dst); imported.append({'source':rel,'target':str(dst.relative_to(project)),'status':'needs_review'})
    for rel in plan['source']['product_knowledge_files']:
        src=backup/'files'/rel
        if not src.exists(): src=project/rel
        if src.exists():
            dst=base/'product-knowledge'/Path(rel).name; copy_path(src,dst); imported.append({'source':rel,'target':str(dst.relative_to(project)),'status':'needs_review'})
    # Preserve custom/unmapped assets via external backup pointer rather than activating them.
    index={'schema_version':'cpt-legacy-import-index-v1','created_at':now(),'migration_id':plan['migration_id'],
           'policy':'preserved_unverified_not_active','items':imported,
           'notes':['Imported Markdown is evidence, not canonical 4.0 knowledge. Review before promotion.', 'AGENTS.override.md is intentionally outside this import.']}
    dump_json(base/'index.json',index)
    return index

def discover_domain_packs() -> dict[str,Path]:
    """Return installable CPT domain packs, excluding fixtures/templates/examples."""
    out={}
    excluded={'evaluation','tests','test-fixtures','fixtures','examples','templates','payload','workers','cpt-core'}
    for pack_manifest in PACKAGE_ROOT.rglob('cpt-pack.json'):
        pack_root=pack_manifest.parent
        if not (pack_root/'.codex-plugin/plugin.json').exists():
            continue
        rel_parts=set(pack_root.relative_to(PACKAGE_ROOT).parts)
        if rel_parts & excluded:
            continue
        pdata=load_json(pack_manifest,{}) or {}
        plugin=load_json(pack_root/'.codex-plugin/plugin.json',{}) or {}
        name=str(plugin.get('name') or pdata.get('name') or pack_root.name)
        if not name.startswith('cpt-') or name in {'cpt-core','cpt-workers'}:
            continue
        out[name]=pack_root
    return out

def pack_skill_ids(pack_root: Path) -> set[str]:
    data=load_json(pack_root/'cpt-pack.json',{}) or {}
    ids=data.get('skill_ids') or data.get('skills') or []
    if isinstance(ids,dict): ids=list(ids)
    return {str(x) for x in ids if isinstance(x,str)}

def install_pack(project: Path, path: Path, scope: str, env):
    cmd=[sys.executable,str(DIST_TOOL),'pack-add','--path',str(path),'--scope',scope]
    if scope=='repo': cmd += ['--project',str(project)]
    return run(cmd,env=env)

def apply_plan(plan: dict, accept_warnings=False, force=False, backup_dir: Path|None=None) -> dict:
    if plan_hash(plan)!=plan.get('plan_hash'): raise RuntimeError('Plan hash mismatch')
    if plan['status']=='blocked' and not force: raise RuntimeError('Plan is blocked; resolve conflicts or use explicit force only after review')
    if plan['warnings'] and not accept_warnings: raise RuntimeError('Plan has warnings; pass --accept-warnings after review')
    project=Path(plan['project']).resolve()
    if backup_dir: plan['backup']['path']=str(backup_dir.resolve()/plan['migration_id'])
    backup_manifest=backup_paths(project,plan); backup=Path(plan['backup']['path'])
    pre_override=hash_file(project/'AGENTS.override.md') if (project/'AGENTS.override.md').exists() else None
    removed=[]
    if plan['options']['legacy_action']=='archive':
        for rel in known_framework_paths(project,plan):
            p=project/rel
            if p.exists(): remove_path(p); removed.append(rel)
    env=os.environ.copy()
    cmd=[sys.executable,str(DIST_TOOL),'install','--project',str(project),'--mode',plan['mode']]
    run(cmd,env=env)
    import_index=import_sources(project,backup,plan)
    migdir=project/'.cpt/migration'; migdir.mkdir(parents=True,exist_ok=True)
    dump_json(migdir/'plan.json',plan)
    dump_json(migdir/'mappings.json',plan['mapping'])
    dump_json(migdir/'legacy-inventory.json',plan['source'])
    # Pack installation is optional and uses native distribution operations.
    installed_packs=[]
    packs=discover_domain_packs()
    if plan['options']['domain_packs'] in {'all','detected'}:
        if plan['options']['domain_packs']=='all':
            selected=sorted(packs)
        else:
            target_skills=set(plan.get('mapping',{}).get('skills',{}).values())
            selected=sorted(name for name,path in packs.items() if pack_skill_ids(path) & target_skills)
        for name in selected:
            install_pack(project,packs[name],'personal',env); installed_packs.append(name)
    workers=False
    if plan['options']['with_workers']:
        run([sys.executable,str(DIST_TOOL),'workers-install','--scope','personal'],env=env); workers=True
    # Verify override preservation.
    post_override=hash_file(project/'AGENTS.override.md') if (project/'AGENTS.override.md').exists() else None
    if pre_override!=post_override: raise RuntimeError('AGENTS.override.md changed; migration contract forbids this')
    # Doctor and runtime validate.
    doctor=run([sys.executable,str(DIST_TOOL),'doctor','--project',str(project)],env=env)
    runtime=project/'.cpt/bin/cpt_runtime.py'
    if runtime.exists(): run([sys.executable,str(runtime),'validate'],cwd=project,env=env)
    receipt={
      'schema_version':SCHEMA_RECEIPT,'migration_id':plan['migration_id'],'applied_at':now(),'status':'applied',
      'project':str(project),'plan_hash':plan['plan_hash'],'backup_path':str(backup),'mode':plan['mode'],
      'removed_legacy_paths':removed,'installed_domain_packs':installed_packs,'workers_installed':workers,
      'override_sha256_before':pre_override,'override_sha256_after':post_override,'import_index':import_index,
      'post_git_status':git_status(project),'doctor_tail':doctor.stdout[-2000:],
      'managed_state':{'cpt':file_manifest(project/'.cpt'),'agents':file_manifest(project/'AGENTS.md'),'.codex':file_manifest(project/'.codex')}
    }
    dump_json(migdir/'receipt.json',receipt); dump_json(backup/'receipt.json',receipt)
    return receipt

def compare_manifest(path: Path, expected: dict) -> bool:
    current=file_manifest(path)
    return current==expected

def rollback(project: Path, receipt_path: Path|None, force=False) -> dict:
    project=project.resolve()
    receipt_path=receipt_path or project/'.cpt/migration/receipt.json'
    receipt=load_json(receipt_path)
    if not receipt: raise RuntimeError('Migration receipt not found')
    backup=Path(receipt['backup_path']); bm=load_json(backup/'backup_manifest.json')
    if not bm: raise RuntimeError('Backup manifest not found')
    # Concurrent managed changes block exact rollback unless forced.
    changed=[]
    for key,rel in [('cpt','.cpt'),('agents','AGENTS.md'),('.codex','.codex')]:
        exp=receipt.get('managed_state',{}).get(key)
        if exp is not None and not compare_manifest(project/rel,exp): changed.append(rel)
    if changed and not force: raise RuntimeError('Managed paths changed after migration: '+', '.join(changed))
    if force:
        emergency=default_state_dir()/'rollback-safety'/receipt['migration_id']+'-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        emergency.mkdir(parents=True,exist_ok=True)
        for rel in ['.cpt','AGENTS.md','.codex']:
            p=project/rel
            if p.exists(): copy_path(p,emergency/rel)
    # Remove all paths covered by the pre-migration snapshot, then restore exact prior state.
    for rec in bm['entries']:
        rel=rec['path']
        if rel=='AGENTS.override.md': continue
        p=project/rel
        if p.exists(): remove_path(p)
        src=backup/'files'/rel
        if rec.get('exists') and src.exists(): copy_path(src,p)
    # Remove CPT paths that did not exist before.
    pre={x['path']:x for x in bm['entries']}
    for rel in ['.cpt']:
        if not pre.get(rel,{}).get('exists') and (project/rel).exists(): remove_path(project/rel)
    # Never touch override; verify against receipt.
    current=hash_file(project/'AGENTS.override.md') if (project/'AGENTS.override.md').exists() else None
    if current!=receipt.get('override_sha256_before'): raise RuntimeError('AGENTS.override.md changed independently; rollback left it untouched')
    out={'schema_version':'cpt-migration-rollback-v1','migration_id':receipt['migration_id'],'rolled_back_at':now(),'project':str(project),'status':'rolled_back','post_git_status':git_status(project)}
    dump_json(backup/'rollback.json',out)
    return out

def verify(project: Path) -> dict:
    project=project.resolve(); receipt=load_json(project/'.cpt/migration/receipt.json')
    problems=[]
    if not receipt: problems.append('migration receipt missing')
    if not (project/'.cpt/runtime.yaml').exists(): problems.append('4.0 runtime missing')
    if (project/'AGENTS.override.md').exists() and receipt:
        if hash_file(project/'AGENTS.override.md')!=receipt.get('override_sha256_after'): problems.append('AGENTS.override.md changed after migration (unmanaged warning)')
    return {'project':str(project),'status':'PASS' if not problems else 'FAIL','problems':problems,'git_status':git_status(project),'receipt':receipt}

def platform_check(project: Path) -> dict:
    project=project.resolve(); parent=project.parent
    checks={
      'python_supported':sys.version_info>=(3,10), 'git_available':shutil.which('git') is not None,
      'project_exists':project.exists(), 'project_writable':os.access(project,os.W_OK) if project.exists() else False,
      'home_writable':os.access(Path.home(),os.W_OK), 'path_length':len(str(project)),
      'wsl':bool(os.environ.get('WSL_DISTRO_NAME')), 'system':platform.system(), 'python':platform.python_version(),
    }
    checks['status']='PASS' if all(checks[k] for k in ['python_supported','git_available','project_exists','project_writable','home_writable']) else 'FAIL'
    checks['warnings']=[]
    if checks['path_length']>220: checks['warnings'].append('Long project path may be problematic on some Windows configurations.')
    if str(project).startswith('/mnt/') and checks['wsl']: checks['warnings'].append('WSL project is on a mounted Windows filesystem; Linux-home paths are often faster and more predictable.')
    return checks

def parse_args():
    p=argparse.ArgumentParser(description='CPT 3.x -> 4.0 migration assistant')
    sub=p.add_subparsers(dest='cmd',required=True)
    def project_arg(sp): sp.add_argument('--project',default='.')
    sp=sub.add_parser('inspect'); project_arg(sp); sp.add_argument('--output')
    sp=sub.add_parser('plan'); project_arg(sp); sp.add_argument('--mode',choices=['local','team'],default='local'); sp.add_argument('--legacy-action',choices=['preserve','archive'],default='archive'); sp.add_argument('--agents-policy',choices=['preserve','replace-if-framework'],default='replace-if-framework'); sp.add_argument('--domain-packs',choices=['none','detected','all'],default='detected'); sp.add_argument('--with-workers',action='store_true'); sp.add_argument('--allow-existing-4x',action='store_true'); sp.add_argument('--output')
    sp=sub.add_parser('apply'); sp.add_argument('--plan',required=True); sp.add_argument('--accept-warnings',action='store_true'); sp.add_argument('--force',action='store_true'); sp.add_argument('--backup-dir')
    sp=sub.add_parser('rollback'); project_arg(sp); sp.add_argument('--receipt'); sp.add_argument('--force',action='store_true')
    sp=sub.add_parser('status'); project_arg(sp)
    sp=sub.add_parser('verify'); project_arg(sp)
    sp=sub.add_parser('platform-check'); project_arg(sp)
    return p.parse_args()

def main():
    a=parse_args()
    if a.cmd=='inspect':
        data=inventory(Path(a.project)); print(json.dumps(data,ensure_ascii=False,indent=2));
        if a.output: dump_json(Path(a.output),data)
    elif a.cmd=='plan':
        data=make_plan(Path(a.project),a.mode,a.legacy_action,a.agents_policy,a.domain_packs,a.with_workers,a.allow_existing_4x)
        out=Path(a.output) if a.output else default_state_dir()/'plans'/(data['migration_id']+'.json'); dump_json(out,data)
        print(json.dumps({'plan':str(out),'status':data['status'],'warnings':len(data['warnings']),'conflicts':len(data['conflicts']),'plan_hash':data['plan_hash']},indent=2))
    elif a.cmd=='apply':
        plan=load_json(Path(a.plan));
        if not plan: raise RuntimeError('Invalid plan')
        r=apply_plan(plan,a.accept_warnings,a.force,Path(a.backup_dir) if a.backup_dir else None); print(json.dumps(r,ensure_ascii=False,indent=2))
    elif a.cmd=='rollback': print(json.dumps(rollback(Path(a.project),Path(a.receipt) if a.receipt else None,a.force),ensure_ascii=False,indent=2))
    elif a.cmd=='status':
        p=Path(a.project).resolve(); print(json.dumps({'inventory':inventory(p),'receipt':load_json(p/'.cpt/migration/receipt.json')},ensure_ascii=False,indent=2))
    elif a.cmd=='verify':
        r=verify(Path(a.project)); print(json.dumps(r,ensure_ascii=False,indent=2)); raise SystemExit(0 if r['status']=='PASS' else 1)
    elif a.cmd=='platform-check':
        r=platform_check(Path(a.project)); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['status']=='PASS' else 1)
if __name__=='__main__': main()
