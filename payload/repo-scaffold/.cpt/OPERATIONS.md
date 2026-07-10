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
