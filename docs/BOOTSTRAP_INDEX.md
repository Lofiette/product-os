# BOOTSTRAP_INDEX.md — Lean Runtime Index

Purpose: start every task with enough operating context to make good first routing decisions without loading the full team library.

## Runtime loading principle

Load the smallest context that can change the next decision. Do not read full playbooks, the full role catalog, scenario tests, or deep method libraries until the task shape requires them.

## Minimal startup files

Read only:
- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/QUESTION_TREE.md`
- `docs/LANGUAGE_POLICY.md`

## After the user answers Intake A

Load only what is needed for the likely tier:
- Work mode and ceremony: `docs/WORK_MODES.md`, `docs/COMPLEXITY_MODEL.md`, `docs/FAST_LANE.md`
- Routing and risk: `docs/ROLE_ROUTING_MATRIX.md`, `docs/RISK_POLICY.md`, `docs/QUALITY_GATES.md`, `.agents/role_cards/*`
- Evidence and external facts: `docs/EVIDENCE_POLICY.md`, `docs/EXTERNAL_EVIDENCE_PROTOCOL.md`
- Creative/opportunity events: `docs/OPPORTUNITY_EVENTS.md`, `docs/CREATIVE_METHODS.md`

## Specialist loading

After selecting the team, load only:
- selected role cards first;
- selected full playbooks only when the role produces a non-trivial artifact;
- selected skills only when a workflow needs them;
- relevant sections of `docs/ROLE_METHOD_LIBRARY.md`, not the whole file.

## Complexity budget

- Tiny: answer or change directly with 0–2 questions and 0–2 roles.
- Fast Lane: 1–3 questions and 1–3 roles.
- Standard: 3–7 questions and 4–7 roles.
- Complex: 5–9 questions and 8–12 roles.
- High-risk: 5–9 questions plus targeted follow-up and 10–15 roles.
- 16+ roles requires explicit user approval.

## Question rule

Ask a question only if the answer can change scope, risk, role lineup, acceptance criteria, verification, approval gates, product language, or implementation sequence.

## Creative improvement rule

Use creative methods only when they can improve the decision, not as ritual. Creative output is hypothesis generation, not evidence. Selection still requires evidence, constraints, and verification.
