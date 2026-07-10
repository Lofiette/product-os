# Alpha 1 Limitations

This package proves the Runtime Kernel contract. It is not a Release Candidate.

## Deliberate limitations

- File-only registry; SQLite is not implemented yet.
- Authorization leases are validated but not deterministically enforced by hooks/rules.
- Compaction recovery is explicit and synthetically tested; project hooks are not wired.
- No Product Knowledge schemas or freshness graph.
- No expertise/domain plugins.
- No worker archetypes or subagent registry.
- No external integrations.
- No 3.x migration assistant.
- Cross-platform CI is not yet established.

## Do not infer

A passing schema validation does not prove product quality, engineering correctness, or safe command execution. It proves runtime-state coherence only.
