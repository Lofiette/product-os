# QUESTION_TREE.md

Ask only questions whose answers can change scope, risk, role selection, skill selection, acceptance criteria, implementation sequence, or verification.

## Micro Intake: 0–2 questions
For typos, copy changes, local reversible changes.

## Fast Lane Intake: 1–3 questions
Ask location, desired outcome, and verification if unclear.

## Standard Intake: 3–7 questions
Ask:
1. What outcome are we trying to achieve?
2. Prototype, PoC, MVP, production change, review, research, bugfix, or refactor?
3. Existing repo or greenfield?
4. Platform/surface?
5. Users/audience?
6. Design-system status, if UI is involved?
7. What is done/acceptance criteria?

## Complex/High-risk Intake: 5–9 + targeted follow-up
Add questions about auth, data, privacy, security, AI tools, migrations, release, metrics, compliance, and rollback.

## UI branch
- Are we creating/redesigning a screen, flow, component, or design system?
- Is there a design system? none / emerging / component library / documented DS / governed DS?
- Is there a DS folder, component docs, Storybook, Figma, tokens, or component registry?
- Must implementation strictly use DS components?
- What states must be covered?
- What product UI language should copy use?

## Design-system branch
- Where is DS source of truth?
- Are component variants documented?
- Are tokens mandatory?
- Are custom UI deviations allowed?
- Are there existing anti-patterns to avoid?
