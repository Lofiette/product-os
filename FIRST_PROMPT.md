Read all project instructions first: `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `TEAM.md`, `docs/QUESTION_TREE.md`, `docs/ROLE_ROUTING_MATRIX.md`, `docs/WORK_MODES.md`, `docs/QUALITY_GATES.md`, `docs/RISK_POLICY.md`, `.agents/playbooks/*`, `.agents/skills/*/SKILL.md`, `.codex/config.toml`, and `.codex/agents/*`.

Start in Intake Mode.

Do not write or modify product code yet.
Do not create implementation files yet.
Do not assume the product scope.
Do not spawn every available subagent. Select the smallest sufficient team.

Your first job:

1. Confirm which instruction sources, playbooks, skills, and custom agents you loaded.
2. Interview me using the adaptive question tree.
3. Ask broad questions first, then branch only into relevant details.
4. Keep the first batch to 5–9 questions unless the task is obviously high-risk or I ask for exhaustive briefing.
5. Determine the work mode: research, prototype, PoC, MVP, production change, bugfix, refactor, review, audit, data/analytics, incident, or documentation.
6. Update `TASK.md` with confirmed answers, assumptions, open questions, constraints, and recommended work mode.
7. Ask Chronicle Keeper to initialize or update `CHRONICLE.md`.
8. Ask Team Architect to recommend the optimal subagent lineup from the available role catalog.
9. Ask Consistency Auditor to check the proposed lineup and plan for contradictions, missing gates, and unclear ownership.
10. Explain which roles are selected, which roles are skipped, and why.
11. Produce a concise planning brief and ask for my approval before implementation.

Output format:

- Loaded instruction sources
- Initial understanding
- Adaptive briefing questions
- Proposed work mode
- Proposed subagent lineup
- Roles intentionally skipped
- What will be updated in `TASK.md` and `CHRONICLE.md`
- Risks or missing information
- Next step requiring my approval
