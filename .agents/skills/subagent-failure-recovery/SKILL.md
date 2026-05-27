---
name: subagent-failure-recovery
description: Use when one or more real subagents are still running, failed, duplicated, or did not return a usable artifact.
---

Follow `docs/SUBAGENT_FAILURE_POLICY.md`.

Process:
1. List expected agents and their artifacts.
2. Mark each status: completed, running/not used, failed, skipped, simulated fallback, insufficient evidence.
3. Decide whether quorum is sufficient.
4. Use fallback hierarchy only when it preserves quality.
5. Never invent specialist findings.
6. Return PASS/WARN/BLOCKED based on available evidence and missing-risk severity.

Output must include the Subagent Completion Status table.
