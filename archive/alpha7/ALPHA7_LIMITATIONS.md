# Beta 1 limitations

1. Live Codex subagent sessions were not available in the build environment. Hook lifecycle events are simulated deterministically.
2. Worker cancellation is cooperative; CPT cannot itself terminate a native worker thread.
3. Native lifecycle events identify an archetype, not a CPT contract ID. Beta 1 therefore allows one contract per archetype in one run.
4. Worker TOML profiles and CPT leases do not replace native sandbox, approval, permission, trust, or organization policy.
5. Worktrees are isolated and validated, but CPT produces review plans only and never performs automatic merge or conflict resolution.
6. Shell and tool classification is incomplete for arbitrary programs.
7. Reconnect and event ordering across all Codex clients require live evaluation.
8. Local YAML/JSONL state is not tamper-evident remote storage.
9. The worker pack is optional; without it, orchestration may still use manual structured-result fallback but cannot claim native worker lifecycle evidence.
10. Beta 1 is not yet the Evaluation Plane. Model quality, token budgets, and real trace compliance remain Phase 8 work.
