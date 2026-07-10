# Claim Lifecycle

Each durable statement is a typed claim.

```text
planned -> confirmed -> validated
hypothesized -> inferred -> confirmed
confirmed/validated -> needs_review -> confirmed/validated
needs_review -> stale -> deprecated or reverified
```

Allowed lifecycle states:

- `planned`: approved intent or target not yet evidenced in implementation.
- `hypothesized`: plausible proposition awaiting evidence.
- `inferred`: supported indirectly but not observed directly.
- `confirmed`: directly supported by approved evidence.
- `validated`: supported by a test or runtime observation.
- `needs_review`: a trigger or dependency changed.
- `stale`: evidence no longer represents current state.
- `deprecated`: intentionally retired.

Rules:

- `validated` requires test or runtime-observation evidence.
- `confirmed` requires evidence.
- high confidence is invalid for a hypothesis and suspicious for an inference.
- lifecycle transitions must follow the transition graph enforced by the runtime CLI.
- a claim never becomes more certain merely because prose sounds convincing.
