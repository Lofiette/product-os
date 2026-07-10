#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib.util, sys
from pathlib import Path


def load_runtime(path: Path):
    spec = importlib.util.spec_from_file_location("cpt_runtime", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main():
    p=argparse.ArgumentParser(); p.add_argument("--project",default="."); args=p.parse_args()
    root=Path(args.project).resolve(); runtime=load_runtime(root/".cpt/bin/cpt_runtime.py")
    errors,warnings=runtime.validate_knowledge(root,check_views=True)
    for warning in warnings: print(f"WARNING: {warning}")
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    print("KNOWLEDGE VALIDATION PASSED")
    return 0

if __name__=="__main__": raise SystemExit(main())
