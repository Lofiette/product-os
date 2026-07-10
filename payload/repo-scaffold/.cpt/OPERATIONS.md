# CPT Runtime Operations

Use the CLI at `.cpt/bin/cpt_runtime.py`.

## Validate and inspect

```bash
python .cpt/bin/cpt_runtime.py validate
python .cpt/bin/cpt_runtime.py status
```

## Standard Task

```bash
python .cpt/bin/cpt_runtime.py create-task \
  --title "Bounded task" \
  --objective "Describe the intended outcome" \
  --task-type implementation \
  --complexity standard \
  --activate

python .cpt/bin/cpt_runtime.py lease-create \
  --task TKT-001 \
  --read 'src/feature/**' \
  --write 'src/feature/**' \
  --verify 'python -m unittest tests.test_feature'
```

Before implementation, produce a compact Impact Map in the task record or an approved task artifact.

## Micro Change

```bash
python .cpt/bin/cpt_runtime.py micro-start \
  --title "Correct a local label" \
  --intent "Change one visible label without changing behavior" \
  --target 'src/ui/example.tsx' \
  --verify 'python -m unittest tests.test_ui' \
  --confirm-eligible
```

Escalate if scope or risk grows.

## Checkpoint and recovery

```bash
python .cpt/bin/cpt_runtime.py checkpoint --reason "Before handoff"
python .cpt/bin/cpt_runtime.py recover --checkpoint latest --verify-only
python .cpt/bin/cpt_runtime.py recover --checkpoint latest
```

## Completion

```bash
python .cpt/bin/cpt_runtime.py complete-task
python .cpt/bin/cpt_runtime.py micro-complete
```

## Product Knowledge

Initialize a knowledge base only when needed:

```bash
python .cpt/bin/cpt_runtime.py knowledge-init \
  --id product-knowledge \
  --title "Product Knowledge" \
  --mode existing \
  --owner-role product_strategist \
  --source-kind git_commit \
  --source-value "$(git rev-parse HEAD)"
```

Create and maintain artifacts:

```bash
python .cpt/bin/cpt_runtime.py knowledge-create --id product-map --type product_map --title "Product Map" --owner-role product_strategist
python .cpt/bin/cpt_runtime.py knowledge-claim-add --artifact product-map --statement "..." --lifecycle confirmed --confidence medium --owner-role product_strategist --evidence-type source_file --evidence-source src/example.ts
python .cpt/bin/cpt_runtime.py knowledge-stale-scan --changed src/example.ts
python .cpt/bin/cpt_runtime.py knowledge-render --all
python .cpt/bin/cpt_runtime.py knowledge-validate
python .cpt/bin/cpt_runtime.py knowledge-sanitize-check
python .cpt/bin/cpt_runtime.py knowledge-sanitize-check --external --artifact product-map
```

Account for knowledge before Standard Task completion:

```bash
python .cpt/bin/cpt_runtime.py knowledge-task-assess --task TKT-001 --status not_required --summary "No durable product knowledge changed."
```

Target sizes are guidance only. Validation never truncates knowledge.


## Deterministic enforcement

```bash
python .cpt/bin/cpt_runtime.py enforcement-status
python .cpt/bin/cpt_runtime.py enforcement-set --mode audit
python .cpt/bin/cpt_runtime.py enforcement-set --mode enforce --trust-state trusted
python .cpt/bin/cpt_runtime.py policy-check --tool-name Bash --command 'npm run test'
python .cpt/bin/cpt_runtime.py audit-tail --limit 20
python .cpt/bin/cpt_runtime.py audit-validate
python .cpt/bin/cpt_runtime.py worker-status
```

Recommended rollout:

1. Enable CPT Core plugin and review/trust its hooks.
2. Start in `audit` mode.
3. Inspect the audit log and tune leases/scopes.
4. Move to `enforce` mode only after the workflow is understood.

Hooks are optional. If they are disabled, keep using leases, checkpoints, runtime validation, and targeted knowledge freshness scans manually.
