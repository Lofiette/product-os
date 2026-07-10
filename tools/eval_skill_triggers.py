#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, re
from collections import Counter
from pathlib import Path

STOP={'the','a','an','and','or','to','for','of','in','on','with','this','that','is','are','be','before','after','use','review','plan','create','task'}
def tok(s): return [x for x in re.findall(r'[a-z0-9]+',s.lower()) if x not in STOP and len(x)>2]
def score(prompt, skill, idf):
    p=Counter(tok(prompt)); d=Counter(tok(skill['description']+' '+' '.join(skill['positive_examples'])))
    return sum(min(p[t],d[t])*idf.get(t,1.0) for t in p)/max(1,math.sqrt(sum(v*v for v in p.values())))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--top-k',type=int,default=3); ap.add_argument('--write-report')
    a=ap.parse_args(); root=Path(a.root); reg=json.loads((root/'skills/SKILL_REGISTRY.json').read_text())['skills']
    df=Counter();
    for s in reg:
        for t in set(tok(s['description']+' '+' '.join(s['positive_examples']))): df[t]+=1
    idf={t:math.log((1+len(reg))/(1+n))+1 for t,n in df.items()}
    failures=[]; cases=[]
    for s in reg:
        for p in s['positive_examples']:
            rank=sorted(((score(p,x,idf),x['id']) for x in reg),reverse=True)
            ids=[i for _,i in rank[:a.top_k]]; ok=s['id'] in ids
            cases.append({'prompt':p,'expected':s['id'],'top':ids,'pass':ok})
            if not ok: failures.append(cases[-1])
        n=s['negative_example']; own=score(n,s,idf); ranked=sorted(((score(n,x,idf),x['id']) for x in reg),reverse=True)
        ok=ranked[0][1]!=s['id'] or own==0
        cases.append({'prompt':n,'expected_not':s['id'],'top':[i for _,i in ranked[:a.top_k]],'pass':ok})
        if not ok: failures.append(cases[-1])
    report={'schema':'cpt-trigger-eval-report-v1','skill_count':len(reg),'case_count':len(cases),'passed':len(cases)-len(failures),'failed':len(failures),'cases':cases}
    if a.write_report: Path(a.write_report).write_text(json.dumps(report,indent=2)+'\n')
    print(f"TRIGGER PROXY EVAL: {report['passed']}/{report['case_count']} passed")
    for f in failures[:20]: print('FAIL',f)
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
