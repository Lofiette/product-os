#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED_ROLE_FIELDS = {
    "id","title","category","primary_plugin","mission","decision_rights","mental_models",
    "activation_signals","non_activation","owned_artifacts","required_skills","optional_skills",
    "required_gates","evidence_requirements","handoffs","task_types","default_execution",
    "execution_modes_allowed","worker_eligibility","preferred_worker_archetype","load_cost",
    "lens_path","method_path","legacy_sources","status"
}
REQUIRED_LENS_SECTIONS = [
    "## Mission","## Decision rights","## Activate when","## Do not activate when",
    "## Owned artifacts","## Required skills","## Optional skills","## Required gates",
    "## Evidence obligations","## Handoffs","## Execution rule"
]
REQUIRED_METHOD_SECTIONS = [
    "## Purpose","## Core mental models","## Method","## Evidence standard",
    "## Failure modes to avoid","## Output contract","## Stop and escalate"
]
REQUIRED_GATE_FIELDS={"id","title","owner_roles","when","pass","block","evidence","verdicts","path"}

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    errors=[]

    skills=json.loads((root/"skills/SKILL_REGISTRY.json").read_text())["skills"]
    skill_ids={x["id"] for x in skills}
    plugins={"cpt-core"} | {p.name for p in (root/"domain-packs").glob("cpt-*") if p.is_dir()}

    registry=json.loads((root/"roles/ROLE_REGISTRY.json").read_text())
    roles=registry.get("roles",[])
    role_ids={r.get("id") for r in roles}
    if registry.get("schema")!="cpt-role-registry-v1": errors.append("ROLE_REGISTRY schema mismatch")
    if registry.get("version")!="4.0.0-alpha.6": errors.append("ROLE_REGISTRY version mismatch")
    if registry.get("role_count")!=50 or len(roles)!=50 or len(role_ids)!=50:
        errors.append("ROLE_REGISTRY must contain 50 unique roles")

    for role in roles:
        rid=role.get("id")
        missing=REQUIRED_ROLE_FIELDS-set(role)
        if missing: errors.append(f"{rid}: missing fields {sorted(missing)}")
        if role.get("primary_plugin") not in plugins: errors.append(f"{rid}: unknown plugin")
        for sid in role.get("required_skills",[])+role.get("optional_skills",[]):
            if sid not in skill_ids: errors.append(f"{rid}: unknown skill {sid}")
        for hid in role.get("handoffs",[]):
            if hid not in role_ids: errors.append(f"{rid}: unknown handoff {hid}")
        if not role.get("decision_rights") or not role.get("evidence_requirements"):
            errors.append(f"{rid}: decision/evidence depth absent")
        if len(role.get("mental_models",[]))<2: errors.append(f"{rid}: too few mental models")
        if role.get("worker_eligibility") not in {"never","conditional","recommended"}:
            errors.append(f"{rid}: invalid worker_eligibility")
        lens=root/role["lens_path"]; method=root/role["method_path"]
        if not lens.exists(): errors.append(f"{rid}: missing lens")
        else:
            text=lens.read_text()
            for section in REQUIRED_LENS_SECTIONS:
                if section not in text: errors.append(f"{rid}: lens missing {section}")
        if not method.exists(): errors.append(f"{rid}: missing method")
        else:
            text=method.read_text()
            for section in REQUIRED_METHOD_SECTIONS:
                if section not in text: errors.append(f"{rid}: method missing {section}")
            if len(text.splitlines())<35: errors.append(f"{rid}: method too thin")

    gates=json.loads((root/"roles/GATE_REGISTRY.json").read_text())
    gate_items=gates.get("gates",[])
    gate_ids={g.get("id") for g in gate_items}
    if gates.get("gate_count")!=len(gate_items) or len(gate_ids)!=len(gate_items):
        errors.append("GATE_REGISTRY count/uniqueness mismatch")
    for gate in gate_items:
        gid=gate.get("id")
        missing=REQUIRED_GATE_FIELDS-set(gate)
        if missing: errors.append(f"{gid}: missing gate fields {sorted(missing)}")
        for rid in gate.get("owner_roles",[]):
            if rid not in role_ids: errors.append(f"{gid}: unknown owner {rid}")
        if set(gate.get("verdicts",[]))!={"PASS","PASS_WITH_WARNINGS","BLOCKED","INSUFFICIENT_EVIDENCE"}:
            errors.append(f"{gid}: verdict contract mismatch")
        path=root/gate.get("path","")
        if not path.exists(): errors.append(f"{gid}: missing gate doc")
    for role in roles:
        for gid in role.get("required_gates",[]):
            if gid not in gate_ids: errors.append(f"{role['id']}: unknown gate {gid}")

    profiles=json.loads((root/"roles/ROLE_ROUTING_PROFILES.json").read_text()).get("profiles",{})
    for pid,p in profiles.items():
        for rid in p.get("accountable_roles",[])+p.get("supporting_roles",[]):
            if rid not in role_ids: errors.append(f"{pid}: unknown role {rid}")
        for sid in p.get("skills",[]):
            if sid not in skill_ids: errors.append(f"{pid}: unknown skill {sid}")
        for gid in p.get("gates",[]):
            if gid not in gate_ids: errors.append(f"{pid}: unknown gate {gid}")
        if len(p.get("accountable_roles",[]))!=1:
            errors.append(f"{pid}: profile must have exactly one accountable role")

    migration=json.loads((root/"migration/ROLE_MIGRATION.json").read_text())
    mappings=migration.get("mappings",[])
    if migration.get("source_count")!=50 or migration.get("target_count")!=50 or len(mappings)!=50:
        errors.append("ROLE_MIGRATION must preserve 50 roles")
    if {m.get("source_role") for m in mappings}!=role_ids or {m.get("target_role") for m in mappings}!=role_ids:
        errors.append("ROLE_MIGRATION ids mismatch")
    if any(m.get("status")!="retained_rewritten" for m in mappings):
        errors.append("all roles must be retained_rewritten")

    # Pack role inventories.
    plugin_paths=[root/"payload/marketplace-root/plugins/cpt-core"]+sorted(p for p in (root/"domain-packs").glob("cpt-*") if p.is_dir())
    by_plugin={}
    for role in roles: by_plugin.setdefault(role["primary_plugin"],set()).add(role["id"])
    for plugin in plugin_paths:
        pack=json.loads((plugin/"cpt-pack.json").read_text())
        expected=by_plugin.get(plugin.name,set())
        if pack.get("role_count")!=len(expected) or set(pack.get("role_ids",[]))!=expected:
            errors.append(f"{plugin.name}: role inventory mismatch")
        if pack.get("role_model")!="logical_lenses_in_cpt_core_references":
            errors.append(f"{plugin.name}: role_model mismatch")

    trigger_cases=json.loads((root/"evaluation/role-trigger-cases.json").read_text()).get("cases",[])
    covered={c.get("role") for c in trigger_cases}
    if covered!=role_ids or len(trigger_cases)!=150:
        errors.append("role trigger coverage must be 150 cases over 50 roles")
    route_cases=json.loads((root/"evaluation/role-routing-cases.json").read_text()).get("cases",[])
    if {c.get("profile") for c in route_cases}!=set(profiles):
        errors.append("routing case coverage mismatch")



    # Compact core runtime bundle.
    ref=root/"payload/marketplace-root/plugins/cpt-core/skills/cpt-task-planning/references"
    expected_files={"EXPERTISE_BUNDLE.json"}
    if {p.name for p in ref.iterdir() if p.is_file()}!=expected_files:
        errors.append("core expertise reference must contain exactly one bundle file")
    else:
        bundle=json.loads((ref/"EXPERTISE_BUNDLE.json").read_text())
        if {x["id"] for x in bundle.get("roles",[])}!=role_ids:
            errors.append("EXPERTISE_BUNDLE role ids mismatch")
        if {x["id"] for x in bundle.get("methods",[])}!=role_ids:
            errors.append("EXPERTISE_BUNDLE method ids mismatch")
        if bundle.get("profiles")!=profiles:
            errors.append("EXPERTISE_BUNDLE profile drift")
        if bundle.get("gates")!=gate_items:
            errors.append("EXPERTISE_BUNDLE gate drift")
        canonical_by_id={x["id"]:x for x in roles}
        for item in bundle.get("methods",[]):
            c=canonical_by_id.get(item["id"],{})
            for field in ["decision_rights","mental_models","methodology","evidence_requirements","anti_patterns","output_contract","handoffs"]:
                if item.get(field)!=c.get(field):
                    errors.append(f"{item['id']}: expertise method bundle drift in {field}")

    if errors:
        print("ROLE VALIDATION FAILED")
        for error in errors: print("ERROR:",error)
        return 1
    print(f"ROLE VALIDATION PASSED: {len(roles)} logical roles, {len(gate_items)} gates, {len(profiles)} routing profiles")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
