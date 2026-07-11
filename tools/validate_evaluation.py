#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation" / "executable"
PACKAGE_VERSION = "4.0.0-alpha.8"
errors: list[str] = []


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


required = [
    ROOT / "EVALUATION.md",
    ROOT / "ALPHA8_LIMITATIONS.md",
    EVAL / "README.md",
    EVAL / "SUITES.json",
    EVAL / "schemas" / "case.schema.json",
    EVAL / "schemas" / "task-result.schema.json",
    EVAL / "schemas" / "scorecard.schema.json",
    EVAL / "baselines" / "offline-core-alpha8.json",
    EVAL / "mutations" / "offline-core-alpha8-mutations.json",
    ROOT / "tools" / "cpt_eval.py",
    ROOT / "tests" / "test_evaluation.py",
    ROOT / ".github" / "workflows" / "offline-evals.yml",
    ROOT / ".github" / "workflows" / "live-smoke.yml",
]
for path in required:
    if not path.exists():
        errors.append(f"missing evaluation asset: {path.relative_to(ROOT)}")

for path in [ROOT / "tools" / "cpt_eval.py", ROOT / "tests" / "test_evaluation.py"]:
    if path.exists():
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Python syntax error {path.relative_to(ROOT)}: {exc}")

if (ROOT / "tests" / "test_evaluation.py").exists():
    tree = ast.parse((ROOT / "tests" / "test_evaluation.py").read_text(encoding="utf-8"))
    test_count = sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
    )
    if test_count != 13:
        errors.append(f"expected 13 evaluation unit tests, found {test_count}")

for workflow in [
    ROOT / ".github" / "workflows" / "offline-evals.yml",
    ROOT / ".github" / "workflows" / "live-smoke.yml",
]:
    if not workflow.exists():
        continue
    try:
        # BaseLoader prevents YAML 1.1 from converting the key `on` to True.
        document = yaml.load(workflow.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        if not isinstance(document, dict) or "jobs" not in document:
            errors.append(f"invalid workflow structure: {workflow.relative_to(ROOT)}")
            continue
        trigger = document.get("on", {})
        if isinstance(trigger, dict) and "pull_request_target" in trigger:
            errors.append(f"unsafe pull_request_target trigger: {workflow.relative_to(ROOT)}")
        permissions = document.get("permissions", {})
        if permissions not in ({"contents": "read"}, "read-all"):
            errors.append(f"workflow permissions are not least-privilege: {workflow.relative_to(ROOT)}")
    except Exception as exc:
        errors.append(f"workflow parse error {workflow.relative_to(ROOT)}: {exc}")

if all((EVAL / "schemas" / name).exists() for name in ["case.schema.json", "task-result.schema.json"]):
    case_schema = load(EVAL / "schemas" / "case.schema.json")
    case_schema["properties"]["reference_output"] = load(EVAL / "schemas" / "task-result.schema.json")
    case_validator = Draft202012Validator(case_schema)
else:
    case_validator = None

role_ids = (
    {item["id"] for item in load(ROOT / "roles" / "ROLE_REGISTRY.json")["roles"]}
    if (ROOT / "roles" / "ROLE_REGISTRY.json").exists()
    else set()
)
skill_ids = (
    {item["id"] for item in load(ROOT / "skills" / "SKILL_REGISTRY.json")["skills"]}
    if (ROOT / "skills" / "SKILL_REGISTRY.json").exists()
    else set()
)
worker_ids = (
    {item["id"] for item in load(ROOT / "orchestration" / "WORKER_ARCHETYPES.json")["archetypes"]}
    if (ROOT / "orchestration" / "WORKER_ARCHETYPES.json").exists()
    else set()
)
plugin_ids = {"cpt-core"} | {
    path.name for path in (ROOT / "domain-packs").glob("cpt-*") if path.is_dir()
}

cases: list[dict] = []
seen: set[str] = set()
for path in sorted((EVAL / "cases").glob("*.json")):
    case = load(path)
    cases.append(case)
    if case_validator:
        for error in case_validator.iter_errors(case):
            errors.append(f"{path.relative_to(ROOT)}:{list(error.path)}: {error.message}")
    case_id = case.get("id")
    if case_id != path.stem:
        errors.append(f"case id/path mismatch: {path.name}")
    if case_id in seen:
        errors.append(f"duplicate case id: {case_id}")
    seen.add(case_id)
    fixture = EVAL / "fixtures" / str(case.get("fixture")) / "repo"
    if not fixture.exists():
        errors.append(f"{case_id}: missing fixture {case.get('fixture')}")
    for plugin in case.get("activation", {}).get("plugins", []):
        if plugin not in plugin_ids:
            errors.append(f"{case_id}: unknown plugin {plugin}")
    output = case.get("reference_output", {})
    for role in output.get("selected_roles", []):
        if role not in role_ids:
            errors.append(f"{case_id}: unknown role {role}")
    for skill in output.get("selected_skills", []):
        if skill not in skill_ids:
            errors.append(f"{case_id}: unknown skill {skill}")
    for action in case.get("reference_actions", []):
        if action.get("type") == "runtime" and "worker-contract-add" in action.get("args", []):
            args = action.get("args", [])
            if "--archetype" in args:
                value = args[args.index("--archetype") + 1]
                if value not in worker_ids:
                    errors.append(f"{case_id}: unknown worker archetype {value}")
    budgets = case.get("budgets", {})
    if any(float(budgets.get(key, 0)) < 0 for key in budgets):
        errors.append(f"{case_id}: negative budget")

if len(cases) != 20:
    errors.append(f"expected 20 executable cases, found {len(cases)}")
fixture_dirs = [path for path in (EVAL / "fixtures").iterdir() if path.is_dir()]
if len(fixture_dirs) != 6:
    errors.append(f"expected 6 fixture repositories, found {len(fixture_dirs)}")

suite_doc = load(EVAL / "SUITES.json") if (EVAL / "SUITES.json").exists() else {}
if suite_doc.get("version") != PACKAGE_VERSION:
    errors.append("suite registry version mismatch")
suites = suite_doc.get("suites", {})
for required_suite in ["offline-core", "live-smoke", "live-readonly", "live-full"]:
    if required_suite not in suites:
        errors.append(f"missing suite: {required_suite}")
for case in cases:
    for suite in case.get("suites", []):
        if suite not in suites:
            errors.append(f"{case['id']}: references unknown suite {suite}")

baseline = EVAL / "baselines" / "offline-core-alpha8.json"
if baseline.exists():
    document = load(baseline)
    scorecard_schema = load(EVAL / "schemas" / "scorecard.schema.json")
    for error in Draft202012Validator(scorecard_schema).iter_errors(document):
        errors.append(f"offline baseline schema error {list(error.path)}: {error.message}")
    expected_case_ids = {case["id"] for case in cases if "offline-core" in case.get("suites", [])}
    if document.get("package_version") != PACKAGE_VERSION:
        errors.append("offline baseline package version mismatch")
    if document.get("suite") != "offline-core" or document.get("backend") != "reference":
        errors.append("offline baseline suite/backend mismatch")
    if document.get("status") != "PASS" or document.get("failed") != 0:
        errors.append("offline baseline is not green")
    if document.get("case_count") != len(expected_case_ids):
        errors.append("offline baseline case_count mismatch")
    if {item.get("id") for item in document.get("cases", [])} != expected_case_ids:
        errors.append("offline baseline case inventory mismatch")

mutation = EVAL / "mutations" / "offline-core-alpha8-mutations.json"
if mutation.exists():
    document = load(mutation)
    if document.get("package_version") != PACKAGE_VERSION:
        errors.append("mutation report package version mismatch")
    if document.get("status") != "PASS" or document.get("detected") != 4 or document.get("total") != 4:
        errors.append("mutation report must detect 4/4 known-bad behaviors")

# Generated run reports are runtime artifacts and must not be packaged.
for path in EVAL.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(EVAL)
    if rel.parts and rel.parts[0] == "reports" and path.name != ".gitkeep":
        errors.append(f"generated evaluation report packaged: {path.relative_to(ROOT)}")
    if path.name.endswith("-comparison.json"):
        errors.append(f"runtime comparison report packaged: {path.relative_to(ROOT)}")

if errors:
    print("EVALUATION ASSET VALIDATION FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print(f"EVALUATION ASSET VALIDATION PASSED: {len(cases)} cases, {len(fixture_dirs)} fixtures, {len(suites)} suites")
