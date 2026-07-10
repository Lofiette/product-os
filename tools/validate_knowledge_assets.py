#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
errors=[]
art=json.loads((ROOT/'knowledge/schemas/knowledge-artifact.schema.json').read_text())
idx=json.loads((ROOT/'knowledge/schemas/knowledge-index.schema.json').read_text())
validator=Draft202012Validator(art,format_checker=FormatChecker())
paths=sorted((ROOT/'knowledge/templates').rglob('*.yaml'))+sorted((ROOT/'knowledge/examples').rglob('*.yaml'))
for path in paths:
    data=yaml.safe_load(path.read_text())
    for e in validator.iter_errors(data):
        errors.append(f"{path.relative_to(ROOT)}:{list(e.path)}:{e.message}")
    if data.get('data_classification') is None or data.get('sharing') is None:
        errors.append(f"{path.relative_to(ROOT)}: missing classification/sharing metadata")
def walk(value,path='$'):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in {'maxLength','maxItems'}:
                errors.append(f"hard content cap {k} found at {path}.{k}")
            walk(v,f"{path}.{k}")
    elif isinstance(value,list):
        for i,v in enumerate(value): walk(v,f"{path}[{i}]")
walk(art); walk(idx)
for required in ['knowledge/SANITIZATION_AND_SHARING.md','knowledge/SCHEMA_REFERENCE.md','knowledge/FAILURE_MODES.md','knowledge/KNOWLEDGE_ARCHITECTURE.md','knowledge/CLAIM_LIFECYCLE.md','knowledge/EVIDENCE_AND_PROVENANCE.md','knowledge/FRESHNESS_AND_DEPENDENCIES.md','knowledge/HUMAN_PROJECTIONS.md','knowledge/TASK_DRIVEN_UPDATES.md']:
    if not (ROOT/required).exists(): errors.append(f"missing {required}")
for forbidden in ['ai'+'-web','SOVA'+'_DESIGN_SYSTEM_KIT','Плат'+'форма ОКО']:
    for path in list((ROOT/'knowledge').rglob('*')):
        if path.is_file() and path.suffix.lower() in {'.md','.json','.yaml','.yml'}:
            try:
                if forbidden.lower() in path.read_text(encoding='utf-8').lower(): errors.append(f"project-specific term {forbidden!r} in {path.relative_to(ROOT)}")
            except UnicodeDecodeError: pass
if errors:
    print('KNOWLEDGE ASSET VALIDATION FAILED')
    for e in errors: print('ERROR:',e)
    raise SystemExit(1)
print(f'KNOWLEDGE ASSET VALIDATION PASSED: {len(paths)} templates/examples, soft-size schemas, sanitization policy')
