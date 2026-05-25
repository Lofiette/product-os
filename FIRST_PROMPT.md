# FIRST_PROMPT.md — ULTIMATE Pro v1.5 startup prompt

Read the project operating instructions using lean staged loading.

## Stage 0 only: bootstrap loading

Read these files first, and do not load all playbooks, full role catalog, scenario tests, or deep method libraries yet:

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/QUESTION_TREE.md`
- `docs/LANGUAGE_POLICY.md`

Start in **Intake A**.

Reply to the user in Russian by default. Keep durable project-control artifacts in compact English unless the user asks otherwise. Use the product UI language for user-facing product copy.

## Hard stops

Do not write product code yet unless the request is clearly Tiny/Fast Lane, explicitly asks for implementation, no risk gate is triggered, and the change is reversible.
Do not create implementation files yet for Standard/Complex/High-risk work.
Do not load all playbooks yet.
Do not spawn all agents.
Do not assume the product scope.
Do not count compact system services or consulted role cards as active specialist roles.
Do not exceed the complexity tier active-role budget without asking the user.
Do not run creative frameworks as ceremony; use them only when they can improve the next decision.

## Your first job

1. Confirm the bootstrap sources loaded.
2. Summarize the initial understanding in Russian.
3. Classify likely work-mode candidates lightly, without pretending certainty.
4. Classify likely complexity tier lightly, using `docs/BOOTSTRAP_INDEX.md` and `docs/RUNTIME_DECISION_TREE.md`.
5. Choose the right intake depth:
   - Micro Intake: 0–2 questions.
   - Fast Lane Intake: 1–3 questions.
   - Standard Intake: 3–7 questions.
   - Complex/High-risk Intake: 5–9 questions plus targeted follow-up.
6. Apply the decision-impact question rule: ask only questions that can change scope, risk, role lineup, acceptance criteria, verification, approval gates, product language, repo recon need, creative/opportunity handling, or implementation sequence.
7. Do not present a final implementation plan until I answer the intake questions, except for Tiny/Fast Lane where a short inline plan is enough.

## After I answer Intake A

Load only the additional documents needed for routing:

- `docs/RUNTIME_DECISION_TREE.md`
- `docs/WORK_MODES.md`
- `docs/COMPLEXITY_MODEL.md`
- `docs/FAST_LANE.md`
- `docs/ROLE_SERVICE_BUDGET.md`
- `docs/ROLE_ROUTING_MATRIX.md`
- `docs/RISK_POLICY.md`
- `docs/QUALITY_GATES.md`
- `docs/REVIEW_LEVELS.md`
- `docs/REPO_RECON.md` if the task touches an existing repository
- `.agents/role_cards/*` for candidate roles

Load evidence, external research, opportunity, creative, schema, full playbook, role method, and skill files only when the task requires them.

Then:

1. Run `repo-recon` if implementation/review may touch an existing repo.
2. Update `TASK.md` in compact English when useful.
3. Update `CHRONICLE.md` according to `docs/CHRONICLE_POLICY.md`.
4. Select the smallest sufficient active team.
5. Produce a selected-role contract.
6. Load only selected full playbooks/skills as needed.
7. Produce a consolidated plan or inline Fast Lane plan.
8. Run Consistency Auditor when required by complexity/risk.
9. Ask for approval before implementation unless Tiny/Fast implicit approval applies.

## Output format for the first response

- Loaded bootstrap sources
- Initial understanding
- Likely work mode candidates
- Likely complexity tier
- Intake depth chosen
- Adaptive briefing questions
- Language policy confirmation
- What will be loaded after I answer
- What you will not do yet
