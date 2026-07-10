# Codex Product Operating System 4.0 — Alpha 3 Skills Consolidation

Alpha 3 preserves the Alpha 2 Runtime Kernel and distribution model while migrating the 3.x skill surface into independently installable, deeper domain packs.

## Included

- minimal repo scaffold with fewer than 20 framework files;
- required `cpt-core` plugin with three focused runtime/context skills;
- five optional domain plugins;
- complete 95-to-45 skill migration registry;
- domain-specific methods, output contracts, evidence rules, stop conditions, and failure modes;
- per-skill `agents/openai.yaml` invocation policy;
- trigger proxy evals and activation-profile metadata checks;
- local-ignored and team-shared modes;
- safe install, update, doctor, uninstall, and independent pack management.

## Quick start

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /path/to/repo --mode local
python tools/cpt_dist.py pack-catalog
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /path/to/repo
```

Only `cpt-core` is required. Enable domain packs according to the task or a documented activation profile rather than enabling every pack by default.

## Validate the package

```bash
python tools/validate_distribution.py --root .
python tools/validate_skills.py --root .
python tools/eval_skill_triggers.py --root . --write-report evaluation/trigger-eval-report.json
python tools/measure_all_skill_metadata.py
python tests/run_all.py
```

## Key references

- `SKILLS.md`
- `docs/SKILL_AUTHORING_STANDARD.md`
- `docs/SKILL_CONSOLIDATION.md`
- `docs/SKILL_INVOCATION_POLICY.md`
- `docs/METADATA_BUDGET.md`
- `migration/SKILL_MIGRATION.csv`
- `ALPHA3_LIMITATIONS.md`

Alpha 3 does not yet migrate the 50-role library, Product Knowledge schemas, hooks/rules, worker archetypes, or external-service adapters.
