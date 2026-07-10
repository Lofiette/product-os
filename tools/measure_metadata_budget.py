#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cpt_dist import metadata_budget_for_plugins

p = argparse.ArgumentParser()
p.add_argument('plugin', nargs='+')
p.add_argument('--max-chars', type=int, default=8000)
args = p.parse_args()
result = metadata_budget_for_plugins([Path(item).resolve() for item in args.plugin])
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['estimated_discovery_chars'] <= args.max_chars else 2)
