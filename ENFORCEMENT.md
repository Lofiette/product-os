
# Deterministic Runtime Enforcement

Alpha 6 introduced the optional deterministic guardrail layer around the file-only runtime. Product OS 4.0 preserves it and adds executable policy-boundary evaluations.

## Modes

- `off`: hooks exit without changing behavior.
- `audit`: events, scope violations, compaction checkpoints, worker lifecycle, and output-size warnings are recorded without blocking supported operations.
- `enforce`: supported violations may deny a tool request, block compaction, or continue a turn until runtime state is repaired.

Begin with `audit`. Move to `enforce` only after reviewing the event stream and hook trust.

## What is enforced

- active lease and write-scope checks for supported `Bash` and `apply_patch` calls;
- exact approved verification commands;
- globally forbidden destructive operations;
- checkpoint creation before compaction and state verification afterward;
- runtime validity at session start, after tools, and before stop;
- targeted Product Knowledge freshness marking after detected project writes;
- managed subagent lifecycle records bound to orchestration contracts;
- audit events with redacted command previews rather than raw tool output.

## What is not guaranteed

CPT hooks are not a security boundary. Current hook interception is incomplete, and native Codex sandbox, permission profiles, approval policy, rules, project trust, and enterprise requirements remain authoritative. Hook trust cannot be established by the package itself.

## Safe fallback

When hooks are disabled or untrusted, the runtime remains functional. Use explicit `validate`, `policy-check`, `checkpoint`, `recover --verify-only`, `knowledge-stale-scan`, and `audit-validate` commands.
