# FIRST_PROMPT.md — ULTIMATE startup prompt

Read the project operating instructions using staged loading.

## Stage 1 only: core loading

Read these files first, and do not load all playbooks yet:

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `TEAM.md`
- `docs/QUESTION_TREE.md`
- `docs/WORK_MODES.md`
- `docs/ROLE_ROUTING_MATRIX.md`
- `docs/OWNERSHIP_MATRIX.md`
- `docs/QUALITY_GATES.md`
- `docs/RISK_POLICY.md`
- `docs/EVIDENCE_POLICY.md`
- `docs/LANGUAGE_POLICY.md`
- `docs/FAST_LANE.md`
- `docs/COMPLEXITY_MODEL.md`
- `docs/ROLE_OUTPUT_SCHEMAS.md`
- `docs/ROLE_METHOD_LIBRARY.md`
- `docs/EXTERNAL_EVIDENCE_PROTOCOL.md`
- `docs/FINAL_FANTASY_CODENAME_POLICY.md`
- `docs/SCENARIO_TESTS.json`

Start in **Intake A**.

Reply to the user in Russian by default. Keep durable project-control artifacts in compact English unless the user asks otherwise. Use the product UI language for user-facing product copy.

## Hard stops

Do not write product code yet.
Do not create implementation files yet.
Do not load all playbooks yet.
Do not spawn all agents.
Do not assume the product scope.
Do not exceed the complexity tier role budget without asking the user.

## Your first job

1. Confirm the core instruction sources loaded.
2. Classify likely work-mode candidates using `docs/WORK_MODES.md`.
3. Classify likely complexity tier using `docs/COMPLEXITY_MODEL.md`.
4. Ask 5 to 9 adaptive questions from `docs/QUESTION_TREE.md`, or 0 to 3 questions if the task qualifies for Tiny/Fast Lane.
5. Use `docs/FAST_LANE.md`, `docs/ROLE_ROUTING_MATRIX.md`, and `docs/SCENARIO_TESTS.json` to avoid over-routing.
6. Do not update product code.
7. Do not present a final implementation plan until I answer the intake questions.
8. After my answers, update `TASK.md`, update `CHRONICLE.md`, select the smallest sufficient team, load only selected playbooks/skills, produce a consolidated plan, run Consistency Auditor when required, and ask for approval before implementation.

## Output format for the first response

- Loaded core sources
- Initial understanding
- Likely work mode candidates
- Likely complexity tier
- Adaptive briefing questions
- Language policy confirmation
- What you will do after I answer
