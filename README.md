# Codex Product Operating System 4.0 — Alpha 4 Role Expertise and Routing

Alpha 4 preserves the Runtime Kernel, distribution model, and 45 canonical skills from Alpha 3, then migrates all 50 logical roles into a typed expertise layer.

## Included

- minimal repo scaffold and required `cpt-core` plugin;
- five independently installable domain plugins;
- 45 canonical skills with complete 95-skill migration coverage;
- all 50 logical roles retained and rewritten;
- explicit decision rights, evidence obligations, artifacts, skills, gates, handoffs, and worker eligibility;
- 50 compact role lenses and 50 deep role-specific method references;
- 25 evidence-based quality gates;
- 14 task routing profiles;
- role/skill/gate matrices and migration registry;
- deterministic role trigger/routing proxy evaluations;
- safe install, update, doctor, uninstall, and pack management.

## Core principle

Roles are logical accountability lenses, not subagents. Skills are methods. Gates are evidence-based acceptance contracts. Worker archetypes arrive in a later execution-plane phase.

## Quick start

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /path/to/repo --mode local
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /path/to/repo
```

## Validate

```bash
python tools/validate_distribution.py --root .
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/eval_skill_triggers.py --root . --write-report evaluation/trigger-eval-report.json
python tools/eval_role_routing.py --root . --write-report evaluation/role-routing-eval-report.json
python tests/run_all.py
```

## Key references

- `ROLES.md`
- `roles/ROLE_CATALOG.md`
- `roles/ROLE_ROUTING.md`
- `roles/ROLE_WORKER_POLICY.md`
- `roles/QUALITY_GATE_MODEL.md`
- `SKILLS.md`
- `docs/ROLE_SOURCES.md`
- `migration/ROLE_MIGRATION.csv`
- `ALPHA4_LIMITATIONS.md`

Alpha 4 does not yet implement executable worker archetypes, Product Knowledge schemas, hooks/rules enforcement, SQLite/MCP, or live Codex behavioral certification.
