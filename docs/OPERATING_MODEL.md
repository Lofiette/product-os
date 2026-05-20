# OPERATING_MODEL.md

## Collaboration topology

1. Main agent coordinates.
2. Task Intake Orchestrator clarifies task.
3. Team Architect selects roles.
4. Specialist agents investigate in parallel when useful.
5. Main agent consolidates.
6. Consistency Auditor checks contradictions.
7. User approves.
8. Worker/implementation proceeds.
9. QA and risk roles verify.
10. Code Reviewer reviews.
11. Chronicle Keeper records.

## Parallelism policy

Use parallel subagents for read-heavy analysis, research planning, review, test-gap analysis, codebase exploration, or risk scans.

Avoid parallel write-heavy work unless the files and responsibilities are clearly separated. Prefer one implementing agent plus reviewers.

## Token discipline

- Start with small teams.
- Ask concise question batches.
- Summarize subagent outputs; do not dump raw logs into the main thread.
- Keep AGENTS.md compact and move details into playbooks and skills.
- Update CHRONICLE.md with distilled memory, not transcripts.
