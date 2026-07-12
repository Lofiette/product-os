# Codex Product Operating System 4.0 Beta 1

Beta 1 is the first integrated, self-contained release of the 4.0 architecture. It combines the Runtime, Knowledge, Expertise, Enforcement, Worker Orchestration, Evaluation, Migration, and Release planes without requiring external services.

## Certification boundary

Beta 1 is certified for deterministic offline behavior. It is **not** an RC and does not claim live Codex or native cross-platform certification.

```bash
python tools/cpt_release.py readiness --scope offline
```

RC readiness remains blocked until native platform evidence, live Codex trials, real worker lifecycle evidence, and the final mega-audit exist.

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

## Migration from 2.x / 3.x

```bash
python tools/cpt_migrate.py inspect --project /path/to/repo
python tools/cpt_migrate.py plan --project /path/to/repo --output /safe/path/plan.json
```

Review the plan before `apply`. Migration is backup-backed, rollback-aware, and leaves `AGENTS.override.md` outside the CPT contract.

## Executable evaluations

```bash
python tools/cpt_eval.py run \
  --suite offline-core \
  --backend reference \
  --report-dir /tmp/cpt-offline-core
```

The required suite contains 21 isolated fixture-repository cases. Optional live cases use `codex exec --json` when the Codex CLI and credentials are available.

## Core principles

- Typed, recoverable runtime state.
- Product Knowledge uses canonical YAML and generated human views.
- Fifty logical roles are professional lenses, not fifty default agents.
- Forty-five canonical skills load through focused plugins.
- Real workers require a task, lease, approved contract, and bounded scope.
- Main thread owns integration and final decisions.
- Parallel writes require managed Git worktrees; CPT never auto-merges.
- External integrations are optional adapters, never core dependencies.
- Offline evidence and live evidence are never conflated.

## Start here

- `INSTALL.md`
- `docs/MIGRATION_3X_TO_4X.md`
- `EVALUATION.md`
- `ORCHESTRATION.md`
- `ENFORCEMENT.md`
- `KNOWLEDGE.md`
- `ROLES.md`
- `SKILLS.md`
- `BETA1_LIMITATIONS.md`
- `EVALUATION_LIMITATIONS.md`
- `docs/BETA1_RELEASE_INTEGRATION.md`
- `docs/RC_TRIALS_AND_RELEASE_GATES.md`

## Validate the package

```bash
python tools/validate_distribution.py
python tools/validate_release.py
python tools/validate_evaluation.py
python scripts/validate_migration_assets.py
python tests/run_all.py
```
