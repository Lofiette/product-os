# Recovery Runbook

## Suspected context loss

1. Stop implementation.
2. Run `python scripts/cpt_runtime.py status`.
3. Run `python scripts/cpt_runtime.py validate`.
4. Run `python scripts/cpt_runtime.py recover --checkpoint latest --verify-only`.
5. If no mismatch exists, continue from `next_operation`.
6. If mismatch exists, inspect the checkpoint and current files.
7. Restore only after confirming the checkpoint is the intended source.

## Missing checkpoint

- Do not invent a lease or unfinished verification.
- Use current files as the only available canonical state.
- Mark uncertain facts as blockers.
- Ask the user to reconfirm scope before project writes.

## Corrupt checkpoint

Never restore a checkpoint that fails digest verification.
