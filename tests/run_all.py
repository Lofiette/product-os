#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = [
    'test_local_install_is_git_clean_and_small',
    'test_team_repo_plugin_stays_below_twenty_files',
    'test_local_existing_tracked_agents_is_not_modified',
    'test_update_preserves_mutable_runtime_state',
    'test_update_refuses_modified_managed_tool',
    'test_uninstall_does_not_touch_application_files',
    'test_personal_marketplace_preserves_other_plugins',
    'test_domain_pack_is_independent',
    'test_team_merge_and_uninstall_preserves_existing_agents',
    'test_personal_plugin_survives_project_uninstall_by_default',
    'test_metadata_budget_is_small',
    'test_doctor_passes',
]

for name in TESTS:
    print(f'=== {name} ===', flush=True)
    result = subprocess.run(
        [sys.executable, '-m', 'unittest', '-v', f'tests.test_distribution.DistributionTests.{name}'],
        cwd=ROOT,
    )
    if result.returncode:
        raise SystemExit(result.returncode)
print(f'DISTRIBUTION BEHAVIOR TESTS PASSED: {len(TESTS)}')
