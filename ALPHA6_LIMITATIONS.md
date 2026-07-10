
# Alpha 6 limitations

- Hook interception is not a complete security boundary and does not cover every tool path.
- Plugin hooks require explicit user trust and can be disabled by Codex configuration or managed requirements.
- The package cannot inspect Codex's internal hook trust registry; `trust_state` is an operator assertion.
- Permission profiles are examples and are not installed automatically.
- Command classification is intentionally conservative and may require lease tuning.
- Worker lifecycle recording does not yet implement worker archetype orchestration, cancellation, quorum, or worktree isolation.
- Audit events are local JSONL records, not an external observability backend.
