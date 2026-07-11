
# Sources

Alpha 7 enforcement and orchestration design follows the current Codex documentation for:

- lifecycle hooks and hook trust;
- `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, and `Stop` event behavior;
- project trust and project-scoped configuration;
- command rules and `codex execpolicy check`;
- permission profiles, sandboxing, and approval policies;
- plugin-bundled hooks and plugin trust.

CPT documentation intentionally distinguishes workflow guardrails from native Codex security boundaries.
