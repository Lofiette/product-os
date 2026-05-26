# BOOTSTRAP_INDEX.md

Load this file during Stage 0.

## Runtime kernel

1. Classify request.
2. Choose intake depth.
3. Detect whether repo/design recon is needed.
4. Select roles by artifact ownership.
5. Select skills by method need.
6. Choose orchestration mode.
7. Ask for approval before real subagent spawn.
8. Execute, verify, review, and update Chronicle compactly.

## Load order

Stage 0 bootstrap:
- AGENTS.md
- TASK.md
- CHRONICLE.md
- docs/BOOTSTRAP_INDEX.md
- docs/QUESTION_TREE.md
- docs/LANGUAGE_POLICY.md

Stage 1 routing:
- docs/ROLE_INDEX.json
- docs/SKILL_INDEX.json
- .agents/role_cards/<relevant>.md
- docs/ROLE_ROUTING_MATRIX.md if routing is not obvious
- docs/SKILL_ROUTING_MATRIX.md if skill choice is not obvious

Stage 2 operation:
- selected role playbooks only
- selected skills only
- repo/design/risk docs only when triggered

## UI tasks

If UI changes are involved, determine design-system mode and run design-recon before implementation unless explicitly skipped.

## Subagent truth

A real subagent exists only if explicitly spawned. Otherwise roles are simulated in the main thread.
