# Compaction Checkpoint Protocol

## Goal

Preserve exact runtime continuity when conversational context is compacted, interrupted, or suspected to be incomplete.

## Checkpoint contents

- current runtime state;
- task index;
- active task or micro change;
- active authorization lease;
- blockers;
- unfinished verification;
- next operation;
- reserved worker registry;
- integrity digests.

## Alpha 1 operations

```bash
python scripts/cpt_runtime.py checkpoint --source manual --reason "Before phase handoff"
python scripts/cpt_runtime.py recover --checkpoint latest --verify-only
python scripts/cpt_runtime.py recover --checkpoint latest
```

## Recovery rule

Do not reconstruct approvals, scope, blockers, or unfinished verification from conversational memory when a valid checkpoint exists.

If checkpoint verification fails, stop. Preserve current files, report the mismatch, and require manual resolution.

## Future hook mapping

A later enforcement phase may call checkpoint creation on `PreCompact` and verification on `PostCompact`. Alpha 1 deliberately does not install or trust project hooks automatically.
