#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

def load_runtime(root: Path):
    path=root/'payload/repo-scaffold/.cpt/bin/cpt_runtime.py'
    spec=importlib.util.spec_from_file_location('cpt_runtime_knowledge_eval',path)
    module=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module); return module

def evidence_item(kind: str, revision: dict) -> dict:
    return {'type':kind,'source':'eval-source','locator':None,'summary':'eval','source_revision':revision,'observed_at':'2026-07-10T17:30:00Z'}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); p.add_argument('--write-report',type=Path)
    a=p.parse_args(); root=a.root.resolve(); rt=load_runtime(root)
    cases=json.loads((root/'evaluation/knowledge-lifecycle-cases.json').read_text())['cases']; results=[]
    rev={'kind':'git_commit','value':'eval','recorded_at':'2026-07-10T17:30:00Z'}
    for case in cases:
        if 'from' in case:
            actual=case['to'] in rt.CLAIM_TRANSITIONS.get(case['from'],set())
        else:
            artifact={'id':'eval-area','mode':case.get('mode','existing'),'dependencies':[],'claims':[],'unknowns':[],'data_classification':'internal','sharing':rt.default_sharing()}
            evidence=[evidence_item(kind,rev) for kind in case.get('evidence',[])]
            claim={'id':'CLM-001','statement':'Eval claim','lifecycle':case['lifecycle'],'confidence':case.get('confidence','medium'),'owner_role':'product_designer','evidence_depth':case['evidence'][0] if case.get('evidence') else 'none','evidence':evidence,'source_revision':rev,'last_verified':None,'review_triggers':[],'unknowns':[]}
            artifact['claims']=[claim]
            actual=not rt.semantic_knowledge_errors(artifact)[0]
        passed=actual==case.get('allowed',case.get('valid'))
        results.append({'id':case['id'],'passed':passed,'actual':actual})
    report={'case_count':len(results),'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),'results':results}
    if a.write_report:
        a.write_report.parent.mkdir(parents=True,exist_ok=True); a.write_report.write_text(json.dumps(report,indent=2)+'\n')
    print(f"KNOWLEDGE LIFECYCLE EVAL: {report['passed']}/{report['case_count']} passed")
    if report['failed']:
        for x in results:
            if not x['passed']: print('-',x)
        return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
