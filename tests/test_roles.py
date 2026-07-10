from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run_script(relative,*args):
    return subprocess.run([sys.executable,str(ROOT/relative),*args],cwd=ROOT,text=True,capture_output=True)

class RoleTests(unittest.TestCase):
    def test_role_registry_and_gates(self):
        result=run_script("tools/validate_roles.py","--root",str(ROOT))
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn("50 logical roles",result.stdout)
        self.assertIn("25 gates",result.stdout)

    def test_role_routing_proxy(self):
        report=ROOT/"evaluation/role-routing-eval-report.json"
        result=run_script("tools/eval_role_routing.py","--root",str(ROOT),"--write-report",str(report))
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        data=json.loads(report.read_text())
        self.assertEqual(data["failed"],0)
        self.assertEqual(data["trigger_case_count"],150)
        self.assertEqual(data["routing_case_count"],14)

    def test_all_legacy_roles_preserved(self):
        data=json.loads((ROOT/"migration/ROLE_MIGRATION.json").read_text())
        self.assertEqual(data["source_count"],50)
        self.assertEqual(data["target_count"],50)
        self.assertEqual(len(data["mappings"]),50)
        self.assertTrue(all(x["status"]=="retained_rewritten" for x in data["mappings"]))

    def test_roles_are_not_custom_agents(self):
        # Alpha 6 deliberately carries role references, not one TOML worker per role.
        self.assertFalse((ROOT/".codex/agents").exists())
        registry=json.loads((ROOT/"roles/ROLE_REGISTRY.json").read_text())
        self.assertEqual(len(registry["roles"]),50)
        self.assertTrue(all(r["default_execution"]!="spawned_worker" for r in registry["roles"]))

if __name__=="__main__":
    unittest.main()
