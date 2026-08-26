# Codex Product Team Maximum Edition — Mega Audit

## Executive verdict

The kit is structurally valid and conceptually strong, but not yet perfect. It has a good operating model, live task memory, role routing, quality gates, risk triggers, and custom-agent scaffolding. The main weaknesses are operational depth and internal efficiency: several role playbooks and skills are too generic, the first prompt loads too much context, and the system needs sharper routing budgets, richer role outputs, and stronger contradiction checks.

## Static validation

Passed:

- 35 roles found in `TEAM.md`.
- Each role has a playbook.
- Each role has a `.codex/agents/*.toml` custom agent file.
- `.codex/config.toml` references all roles.
- TOML files parse successfully.
- 12 skills include `SKILL.md` with front matter.
- Required live context files are present.

## Severity legend

- P0: must fix before treating as robust production operating kit.
- P1: important; likely to reduce quality or waste tokens.
- P2: useful improvement.
- P3: polish.

## Findings

### P0-1. FIRST_PROMPT asks Codex to load too much at startup

`FIRST_PROMPT.md` asks Codex to read all playbooks, all skills, all custom agents, and config before even knowing the task. This conflicts with the kit's own token discipline and smallest-sufficient-team philosophy.

Risk:

- Token waste.
- Worse routing because the model may drown in all role instructions.
- Slower first response.
- Higher chance of generic behavior.

Recommended fix:

- Startup should load only core coordination files first.
- Load full role playbooks only after Team Architect selects roles.
- Keep `TEAM.md` and `ROLE_ROUTING_MATRIX.md` as the role index.

Proposed behavior:

1. Load `AGENTS.md`, `TASK.md`, `CHRONICLE.md`, `TEAM.md`, `QUESTION_TREE.md`, `ROLE_ROUTING_MATRIX.md`, `WORK_MODES.md`, `QUALITY_GATES.md`, `RISK_POLICY.md`.
2. Ask first intake questions.
3. Select likely roles.
4. Load only selected role playbooks and relevant skills.

### P0-2. Several role playbooks are too generic

Many playbooks include only mission, generic boundaries, inputs, and generic output format. They lack role-specific method, checklist, outputs, and handoff expectations.

Affected examples:

- Product Strategist
- UX Interaction Reviewer
- Design System Guardian
- Solution Architect
- Frontend Architect
- Backend Architect
- API Contract Guardian
- Data Architect
- Analytics Engineer
- Performance Engineer
- Observability Engineer
- AI Workflow Auditor

Risk:

- Roles will produce similar bland summaries.
- Team outputs may overlap.
- Consistency Auditor has less concrete material to check.
- User may receive “committee fog” instead of expert work.

Recommended fix:

Each playbook needs:

- Mission
- When to activate
- Do not do
- Inputs
- Method/checklist
- Required output artifact
- Handoff to other roles
- Escalation triggers
- Common failure modes

### P0-3. Skills are mostly generic shells

The 12 skills have good names and descriptions, but most bodies repeat the same general instructions. They do not yet encode deep workflows.

Risk:

- Skills will not meaningfully improve behavior over `AGENTS.md`.
- The system relies too much on role descriptions.
- Repeatable workflows are not actually repeatable.

Recommended fix:

Make each skill procedural:

- `task-intake`: exact phase model and update rules.
- `team-routing`: routing budgets, mandatory/skippable roles, conflict handling.
- `research-planning`: market/UX/CX evidence maps and research protocol templates.
- `design-ux-planning`: flow/state/content/a11y/design-system matrices.
- `architecture-planning`: architecture decision tree and trade-off matrix.
- `risk-review`: triggered risk scan by domain.
- `implementation-review`: diff review checklist and merge recommendation rubric.
- `self-audit`: machine-check and semantic-check checklist.

### P1-1. No explicit team-size budget tiers

The docs say “smallest sufficient team”, but do not define what “small” means.

Risk:

- Codex may over-select roles for normal tasks.
- Maximum Edition becomes token-heavy.

Recommended fix:

Add team budgets:

- Fast lane: 1–3 roles.
- Standard: 4–7 roles.
- Complex: 8–12 roles.
- High-risk: 10–15 roles, only with explicit reason.
- Never select 16+ roles without explicit user approval.

### P1-2. Intake needs clearer two-phase behavior

`FIRST_PROMPT.md` asks Codex to interview the user and update `TASK.md` in the same first response. Realistically, after the first question batch, the user has not answered yet.

Risk:

- Codex may write guesses into `TASK.md` too early.
- Assumptions may solidify as pseudo-facts.

Recommended fix:

Define two intake phases:

- Intake A: load core instructions, ask first adaptive questions, do not update task except “intake started”.
- Intake B: after user answers, update `TASK.md`, update `CHRONICLE.md`, select roles, plan.

### P1-3. No RACI/ownership matrix

There are ownership boundaries in `TEAM.md`, but no explicit RACI across major artifact types.

Risk:

- Product Strategist, Business Analyst, Domain Expert, UX Researcher, and UX Interaction Reviewer may overlap.
- Design System Guardian and Visual Design Director may conflict on UI choices.
- QA Engineer and Code Reviewer may duplicate verification.

Recommended fix:

Add `docs/OWNERSHIP_MATRIX.md` with artifact ownership:

- Product goal: Product Strategist accountable.
- Requirements/business rules: Business Analyst accountable.
- Domain invariants: Domain Expert accountable.
- User evidence: UX Researcher accountable.
- Customer journey: CX Researcher accountable.
- Flow/state behavior: UX Interaction Reviewer accountable.
- UX copy: UX Writer accountable.
- Design tokens/components: Design System Guardian accountable.
- Visual direction: Visual Design Director accountable.
- Architecture decision: Solution Architect accountable.
- Verification strategy: QA Engineer accountable.
- Diff merge recommendation: Code Reviewer accountable.

### P1-4. Research roles need stronger evidence policy

Market Researcher says not to invent market facts, but the broader research skill does not enforce source freshness, evidence tiers, or separation between desk research and user-provided evidence.

Risk:

- Codex may hallucinate competitor facts or market claims.
- Research output may sound authoritative without evidence.

Recommended fix:

Add `docs/EVIDENCE_POLICY.md`:

- Evidence tiers: repository evidence, user-provided evidence, live external research, assumptions, hypotheses.
- Market facts require current sources or must be labeled assumptions.
- UX research findings require observed user evidence.
- CX claims require journey/service evidence.
- No invented statistics.

### P1-5. Missing AI/ML product risk role despite `TASK.md` having AI/ML components

`TASK.md` includes “AI/ML components”, but no dedicated AI/ML role exists.

Risk:

- AI product tasks are routed only through generic architecture/security/privacy roles.
- Missing model evaluation, prompt safety, latency/cost, hallucination, evals, data quality, guardrails.

Recommended fix:

Add roles in Maximum v1.1:

- AI Product Architect or AI/ML Systems Architect.
- Model Evaluation Specialist.
- Prompt & Agent Safety Reviewer, or extend AI Workflow Auditor beyond process.

### P1-6. Privacy role needs legal-boundary language

Privacy & Compliance Reviewer is useful, but it should not imply legal advice.

Risk:

- Overconfident compliance claims.

Recommended fix:

Add boundary:

“Identify product and engineering compliance risks. Do not provide legal advice or claim regulatory compliance. Escalate legal interpretation to qualified counsel.”

### P1-7. Accessibility role should be more operational

Accessibility Specialist currently says WCAG-oriented, but lacks a concrete test matrix.

Risk:

- A11y review becomes generic.

Recommended fix:

Add checklist:

- Semantic structure
- Keyboard path
- Focus order and restoration
- Accessible names/descriptions
- Form labels and errors
- Error announcements
- Contrast assumptions
- Reduced motion
- Screen reader smoke test
- Touch target size where relevant

### P1-8. Fast lane is implied but not operationalized

Quality gates mention bounded fast-lane change, but there is no clear fast-lane workflow.

Risk:

- Tiny tasks become bureaucratic.
- Codex may over-brief for small copy/code changes.

Recommended fix:

Add `docs/FAST_LANE.md`:

- Use for low-risk tasks under one or two files.
- Ask max 1–3 questions.
- Select max 1–3 roles.
- Still update `CHRONICLE.md` briefly if files changed.
- Skip full specialist planning if user explicitly approves bounded implementation.

### P1-9. Consistency Auditor is good but underpowered

The role exists and has a useful checklist, but it needs stricter pass/fail output.

Risk:

- It may produce soft suggestions instead of blocking inconsistencies.

Recommended fix:

Consistency Auditor output should be:

- PASS / PASS WITH WARNINGS / BLOCKED
- Blocking contradictions
- Missing roles
- Missing gates
- Scope conflicts
- Unsupported claims
- Required fixes before proceeding

### P2-1. `validate_kit.py` checks structure, not semantics

The validator catches missing files and TOML issues, but not weak playbooks, duplicate skill bodies, missing output artifacts, or route coverage.

Recommended fix:

Enhance validator to check:

- each playbook has `## Specific process` or `## Specific checklist`;
- each playbook has `## Output artifact`;
- each role appears in routing matrix at least once;
- each skill has unique procedural sections;
- `FIRST_PROMPT.md` does not require loading all playbooks before routing;
- docs reference mandatory gates.

### P2-2. Missing scenario tests

The kit lacks simulated scenarios to verify routing.

Recommended fix:

Add `tests/scenarios/*.md`:

- Tiny copy change
- UI MVP
- Backend API production change
- UX research plan
- Market research task
- Incident response
- Data analytics instrumentation
- Mobile feature
- AI feature

Each scenario should specify expected roles and skipped roles.

### P2-3. Missing task-type examples in `QUESTION_TREE.md`

The question tree is good, but it could include examples of first question batches by task type.

Recommended fix:

Add short “first batch examples” for:

- MVP
- Bugfix
- Research
- UI copy
- Incident
- Production API change

### P2-4. Technical Writer should not always be only end-stage

Technical Writer is in handoff, but for documentation-heavy tasks it may need to be selected earlier.

Recommended fix:

Routing matrix should include:

- Docs-first task: Technical Writer + Domain Expert / relevant architect.
- Public developer docs: Technical Writer + API Contract Guardian.
- User-facing help/onboarding content: UX Writer + Technical Writer.

### P2-5. Product analytics needs privacy trigger by default

Analytics/tracking currently lists Privacy Reviewer as optional.

Recommended fix:

If tracking includes user identifiers, personal data, behavioral events, consent, or production telemetry, Privacy Reviewer should be required.

### P2-6. Incident mode should include Communication/Handoff logic

Incident Investigator exists, but incident communications are not explicit.

Recommended fix:

Add incident handoff requirements:

- Current status
- Customer impact
- Mitigation
- Owner
- Timeline
- Follow-ups
- External/internal comms draft if requested

### P2-7. Design roles need artifact interfaces

Design System Guardian, Visual Design Director, UX Writer, Accessibility Specialist, and UX Interaction Reviewer need explicit handoff interfaces.

Recommended fix:

Add design artifact matrix:

- Flow/state matrix
- Copy deck/content matrix
- Component reuse map
- Visual direction notes
- Accessibility acceptance criteria

### P3-1. README should include “how to not overuse Maximum”

Maximum Edition’s biggest failure mode is over-orchestration. README should tell the user how to ask for fast lane and how to restrict roles.

### P3-2. Add naming convention for generated decisions

Decision records should use IDs like `DR-0001-short-title.md` if separate records are created.

## Recommended next version: Maximum v1.1

### Must-fix changes

1. Rewrite `FIRST_PROMPT.md` into staged loading.
2. Add team-size budget tiers.
3. Add `docs/OWNERSHIP_MATRIX.md`.
4. Add `docs/EVIDENCE_POLICY.md`.
5. Add `docs/FAST_LANE.md`.
6. Deepen all generic playbooks.
7. Deepen workflow skills.
8. Upgrade Consistency Auditor output to strict pass/block model.
9. Enhance `validate_kit.py` for semantic checks.
10. Add scenario tests.

### New roles to consider

- AI/ML Systems Architect
- Model Evaluation Specialist
- Delivery Manager / Project Coordinator
- Service Designer
- Content Strategist
- DesignOps Lead
- Legal Liaison, not legal advisor
- Customer Support Specialist
- Sales/Go-to-Market Strategist
- Localization Specialist

## Final assessment

The current Maximum Edition is a strong v1 scaffold. It is structurally coherent and strategically pointed in the right direction. However, to become the “ultra-team” the user wants, it needs more operational specificity, sharper role outputs, better routing controls, and semantic self-tests.

Recommended status: do not treat as final. Treat as Maximum v1.0 alpha and upgrade to v1.1 before real heavy use.
