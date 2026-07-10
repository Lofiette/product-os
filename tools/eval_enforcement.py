
#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'tools/cpt_dist.py'
cases=json.loads((ROOT/'evaluation/enforcement-cases.json').read_text())['cases']
tmp=Path(tempfile.mkdtemp(prefix='cpt-enforcement-eval-'))
try:
    env=os.environ.copy(); env['HOME']=str(tmp/'home'); env['CODEX_HOME']=str(tmp/'home/.codex'); (tmp/'home').mkdir()
    repo=tmp/'repo'; repo.mkdir(); subprocess.run(['git','init','-q',str(repo)],check=True)
    subprocess.run([sys.executable,str(DIST),'install','--project',str(repo),'--mode','local'],env=env,check=True,capture_output=True,text=True)
    tool=repo/'.cpt/bin/cpt_runtime.py'
    results=[]
    for case in cases:
        subprocess.run([sys.executable,str(tool),'enforcement-set','--mode',case['mode'],*(['--trust-state','trusted'] if case['mode']=='enforce' else [])],cwd=repo,check=True,capture_output=True,text=True)
        run=subprocess.run([sys.executable,str(tool),'policy-check','--tool-name',case['tool_name'],'--command',case['command']],cwd=repo,capture_output=True,text=True)
        payload=json.loads(run.stdout); actual=payload['decision']; passed=actual==case['expected']; results.append({**case,'actual':actual,'passed':passed})
    report={'total':len(results),'passed':sum(x['passed'] for x in results),'cases':results}
    (ROOT/'evaluation/enforcement-eval-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f"ENFORCEMENT POLICY EVAL: {report['passed']}/{report['total']}")
    if report['passed']!=report['total']: raise SystemExit(1)
finally:
    shutil.rmtree(tmp)
