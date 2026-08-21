#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, json, math, re
from pathlib import Path

STOP=set("""the a an and or to of for in on with from by as is are be this that when use need needs review plan define design create update current task role output evidence user product system should must before after if only into at no not own owns owning main thread work working""".split())

def toks(text):
    return [x for x in re.findall(r"[a-z0-9]+",text.lower().replace("_"," ")) if len(x)>2 and x not in STOP]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--write-report")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    reg=json.loads((root/"roles/ROLE_REGISTRY.json").read_text())
    roles=reg["roles"]
    docs={}
    for r in roles:
        method=(root/r["method_path"]).read_text()
        docs[r["id"]]=" ".join([
            r["title"],r["mission"]," ".join(r["activation_signals"])," ".join(r["task_types"]),
            " ".join(r["mental_models"]),method," ".join(r["owned_artifacts"])
        ])
    N=len(docs); df=collections.Counter()
    for d in docs.values(): df.update(set(toks(d)))
    idf={t:math.log((N+1)/(c+1))+1 for t,c in df.items()}
    vectors={rid:collections.Counter(toks(text)) for rid,text in docs.items()}
    def score(prompt,rid):
        q=collections.Counter(toks(prompt))
        return sum(min(q[t],vectors[rid][t])*idf.get(t,1) for t in q)
    def top(prompt):
        return max(docs,key=lambda rid:score(prompt,rid))

    cases=json.loads((root/"evaluation/role-trigger-cases.json").read_text())["cases"]
    results=[]; failed=0
    for c in cases:
        selected=top(c["prompt"])
        ok=(selected==c["role"]) if c["expected"]=="select" else (selected!=c["role"])
        failed+=not ok
        results.append({**c,"selected":selected,"passed":bool(ok)})
    route_cases=json.loads((root/"evaluation/role-routing-cases.json").read_text())["cases"]
    profiles=json.loads((root/"roles/ROLE_ROUTING_PROFILES.json").read_text())["profiles"]
    route_results=[]
    for c in route_cases:
        p=profiles.get(c["profile"],{})
        ok=(p.get("accountable_roles")==c["expected_accountable_roles"]
            and p.get("supporting_roles")==c["expected_supporting_roles"]
            and p.get("skills")==c["expected_skills"]
            and p.get("gates")==c["expected_gates"]
            and p.get("default_execution")==c["expected_default_execution"])
        failed+=not ok
        route_results.append({**c,"passed":bool(ok)})
    report={"schema":"cpt-role-routing-eval-report-v1","version":"4.0.0",
            "trigger_case_count":len(cases),"routing_case_count":len(route_cases),
            "passed":len(cases)+len(route_cases)-failed,"failed":failed,
            "note":"Deterministic metadata proxy and registry contract test; not a live Codex model trace.",
            "trigger_results":results,"routing_results":route_results}
    if args.write_report: Path(args.write_report).write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print(f"ROLE ROUTING PROXY EVAL: {report['passed']}/{len(cases)+len(route_cases)} passed")
    return 1 if failed else 0
if __name__=="__main__":
    raise SystemExit(main())
