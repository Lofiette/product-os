#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
errors=[]
version=(ROOT/'VERSION').read_text().strip()
required=['release/GATES.json','release/TRIALS.json','release/schemas/release-scorecard.schema.json','release/schemas/release-readiness.schema.json','tools/cpt_release.py','docs/RC_TRIALS_AND_RELEASE_GATES.md','KNOWN_LIMITATIONS.md']
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')
gates=json.loads((ROOT/'release/GATES.json').read_text())
trials=json.loads((ROOT/'release/TRIALS.json').read_text())
if gates.get('version')!=version: errors.append('release gates version mismatch')
if trials.get('version')!=version: errors.append('release trials version mismatch')
ids=[x['id'] for x in gates.get('gates',[])]
if len(ids)!=11 or len(set(ids))!=11: errors.append('release gate count/uniqueness mismatch')
tracks=[x['id'] for x in trials.get('tracks',[])]
if len(tracks)!=35 or len(set(tracks))!=35: errors.append('release track count/uniqueness mismatch')
for schema_name in ['release-scorecard.schema.json','release-readiness.schema.json']:
    try: Draft202012Validator.check_schema(json.loads((ROOT/'release/schemas'/schema_name).read_text()))
    except Exception as exc: errors.append(f'invalid {schema_name}: {exc}')
if errors:
    print('RELEASE ASSET VALIDATION FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('RELEASE ASSET VALIDATION PASSED; gates=11 tracks=35')
