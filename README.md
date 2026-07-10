# Codex Product Operating System 4.0 — Alpha 5: Product Knowledge Schema and Lifecycle

Alpha 5 preserves the Runtime Kernel, distribution model, 45 canonical skills, 50 logical roles, and 25 quality gates from Alpha 4. It adds a typed, file-backed Product Knowledge layer that supports existing products, greenfield creation, and redesign/migration work without turning knowledge into an always-loaded encyclopedia.

## Included

- minimal repo scaffold and native `cpt-core` plugin;
- five independently installable domain plugins;
- 45 canonical skills with complete 95-skill migration coverage;
- all 50 logical roles and 25 evidence-based quality gates;
- canonical YAML Product Knowledge and generated Markdown views;
- Product Map, Area Map, Flow Map, Decision Record, API/Data Contract, and Context Packet types;
- claim lifecycle, confidence, evidence depth, source revision, unknowns, review triggers, and dependencies;
- existing, greenfield, and redesign modes;
- targeted freshness scanning with dependency propagation;
- task-completion knowledge accounting;
- explicit classification, sanitization, and sharing policy;
- safe install, update, doctor, uninstall, and domain-pack management.

## Product Knowledge principles

- Product Map routes work; it is not an encyclopedia.
- Parent artifacts link to deeper artifacts instead of duplicating them.
- Claims become more certain only when stronger evidence is attached.
- Greenfield intent stays planned until implementation and verification evidence exists.
- Redesign knowledge keeps current, target, and delta separate.
- Freshness updates only affected artifacts.
- Size guidance is advisory and never truncates useful knowledge.
- Canonical knowledge must not store credentials or raw restricted values.

## Quick start

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /path/to/repo --mode local
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /path/to/repo

cd /path/to/repo
python .cpt/bin/cpt_runtime.py knowledge-init   --title "Product Knowledge"   --mode existing   --owner-role product_strategist   --source-kind git_commit   --source-value "$(git rev-parse HEAD)"
```

Product Knowledge initializes lazily. A project that does not need durable product knowledge keeps the smaller Alpha 4 installation footprint.

## Validate the distribution

```bash
python tools/validate_distribution.py
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/validate_knowledge_assets.py
python tools/eval_knowledge_lifecycle.py --root .   --write-report evaluation/knowledge-lifecycle-eval-report.json
python tests/run_all.py
```

## Key references

- `KNOWLEDGE.md`
- `knowledge/KNOWLEDGE_ARCHITECTURE.md`
- `knowledge/CLAIM_LIFECYCLE.md`
- `knowledge/EVIDENCE_AND_PROVENANCE.md`
- `knowledge/FRESHNESS_AND_DEPENDENCIES.md`
- `knowledge/SANITIZATION_AND_SHARING.md`
- `knowledge/SCHEMA_REFERENCE.md`
- `ROLES.md`
- `SKILLS.md`
- `ALPHA5_LIMITATIONS.md`

## Deliberate limitations

Alpha 5 does not yet install hooks, use SQLite, expose MCP adapters, build AST dependency graphs, execute worker archetypes, or certify live Codex behavior. Those belong to later phases.
