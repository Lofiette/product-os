# Codex Product Operating System 4.0 Alpha 7

Alpha 7 adds optional managed worker orchestration to the self-contained Runtime Kernel, Product Knowledge, canonical skills, logical roles, quality gates, distribution split, and deterministic enforcement.

## Install the core runtime

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --enforcement-mode audit
```

The core plugin is exposed personally by default. Restart Codex, enable CPT Core, and review/trust its hooks before relying on lifecycle enforcement.

## Optional worker pack

```bash
python tools/cpt_dist.py workers-install --scope personal
```

The worker pack provides ten bounded custom-agent archetypes. It is never installed implicitly.

## Core principles

- Runtime state is typed and recoverable.
- Product Knowledge is canonical YAML with generated Markdown views.
- Fifty logical roles remain professional lenses, not fifty agents.
- Forty-five canonical skills load through focused plugins.
- Real workers require a Standard Task, authorization lease, approved contracts, and bounded scope.
- Main thread owns integration and final decisions.
- Parallel writes require managed Git worktrees; CPT never auto-merges.
- Native Codex sandbox, permission, approval, trust, and organization policy remain authoritative.

## Start here

- `INSTALL.md`
- `ORCHESTRATION.md`
- `WORKER_PACK.md`
- `ENFORCEMENT.md`
- `KNOWLEDGE.md`
- `ROLES.md`
- `SKILLS.md`
- `ALPHA7_LIMITATIONS.md`

## Validate the package

```bash
python tools/validate_distribution.py
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/validate_knowledge_assets.py
python tools/validate_enforcement.py
python tools/validate_orchestration.py
python tests/run_all.py
```
