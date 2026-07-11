# Codex Product Operating System 4.0 Alpha 9

Alpha 9 adds an **executable Evaluation Plane** to the Runtime Kernel, Product Knowledge, canonical skills, logical roles, quality gates, deterministic enforcement, and managed worker orchestration delivered in Alpha 1–7.

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

## Executable evaluations

Run the required self-contained suite:

```bash
python tools/cpt_eval.py run \
  --suite offline-core \
  --backend reference \
  --report-dir evaluation/executable/reports/offline-core
```

Compare it with the reviewed baseline:

```bash
python tools/cpt_eval.py compare-baseline \
  --current evaluation/executable/reports/offline-core/offline-core-reference-scorecard.json \
  --baseline evaluation/executable/baselines/offline-core-alpha8.json
```

Optional live cases use `codex exec --json` when the Codex CLI and credentials are available. See `EVALUATION.md`.

## Core principles

- Runtime state is typed and recoverable.
- Product Knowledge is canonical YAML with generated Markdown views.
- Fifty logical roles remain professional lenses, not fifty agents.
- Forty-five canonical skills load through focused plugins.
- Real workers require a Standard Task, authorization lease, approved contracts, and bounded scope.
- Main thread owns integration and final decisions.
- Parallel writes require managed Git worktrees; CPT never auto-merges.
- Evaluation results distinguish deterministic reference behavior from live-model evidence.
- Native Codex sandbox, permission, approval, trust, and organization policy remain authoritative.

## Start here

- `INSTALL.md`
- `EVALUATION.md`
- `ORCHESTRATION.md`
- `WORKER_PACK.md`
- `ENFORCEMENT.md`
- `KNOWLEDGE.md`
- `ROLES.md`
- `SKILLS.md`
- `ALPHA8_LIMITATIONS.md`

## Validate the package

```bash
python tools/validate_distribution.py
python tools/validate_evaluation.py
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/validate_knowledge_assets.py
python tools/validate_enforcement.py
python tools/validate_orchestration.py
python tests/run_all.py
```
