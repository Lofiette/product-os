# Codex Product Team Maximum v1.3 — Final Pre-Ultimate Audit

Date: 2026-05-20

## Verdict

**PASS WITH WARNINGS.**

v1.3 is structurally healthy and ready to become the base for the ULTIMATE release, but it should not be considered final without a small hardening patch.

The remaining issues are not architectural failures. They are polish and consistency defects that could create confusion during real Codex runs.

## Structural validation

Command run:

```bash
python scripts/validate_kit.py
```

Result:

```text
VALIDATION PASSED: 42 roles, 12 skills, 5 scenarios.
```

Checked:

- 42 role playbooks exist.
- 42 custom agent TOML files exist.
- 12 workflow skills exist.
- TOML files parse successfully.
- Required core docs exist.
- `AGENTS.md` references v1.3 governance docs.
- Old repeated v1.2 generic phrase is removed.
- Consistency Auditor no longer escalates to itself.
- Scenario JSON validates against known role IDs.

## What is strong

### 1. Complexity control is now real

`docs/COMPLEXITY_MODEL.md` provides a useful decision ladder:

- Tiny
- Fast Lane
- Standard
- Complex
- High-risk
- Exception

This directly answers the concern that the kit could become too heavy. The rule “more roles are not better; correct routing is better” is present in `AGENTS.md`.

### 2. Staged loading is correctly designed

The kit now prevents startup overloading:

- Stage 1: core docs only.
- Stage 2: selected role playbooks and selected skills only.
- Stage 3: relevant repo files only.

This is essential for token discipline.

### 3. Language policy is strong

`docs/LANGUAGE_POLICY.md` clearly says:

- User replies: Russian by default.
- Durable control artifacts: compact English.
- Product UI copy: product language from `TASK.md`.
- Do not use “think in English” as an instruction.

This is the right policy for Russian-speaking control with lower-token operational artifacts.

### 4. Evidence policy is strong

`docs/EVIDENCE_POLICY.md` correctly separates:

- repository evidence;
- user-provided evidence;
- external evidence;
- derived inference;
- assumptions;
- hypotheses.

The hard rules prevent fake market research, fake UX insights, fake metrics, and fake legal certainty.

### 5. Role depth is materially better than v1.2

Key roles now include useful advanced protocols, for example:

- Market Researcher: category framing, alternatives map, positioning axes, adoption barriers, evidence grading.
- UX Researcher: decision-first framing, method choice, participant logic, evidence handling, synthesis, confidence.
- UX Writer: message matrix, voice/tone, terminology, accessibility and localization notes.
- AI/ML Systems Architect: behavior contract, context/tool boundaries, eval boundary, fallback behavior, cost/latency, observability.
- QA Engineer: risk-based test matrix and test-level guidance.

## Remaining issues before ULTIMATE

## Issue 1 — `FIRST_PROMPT.md` has malformed doc-list formatting

In Stage 1 loading, several docs are grouped inside a single backtick block:

```text
`docs/FAST_LANE.md, docs/COMPLEXITY_MODEL.md, docs/ROLE_OUTPUT_SCHEMAS.md, docs/EXTERNAL_EVIDENCE_PROTOCOL.md, docs/FINAL_FANTASY_CODENAME_POLICY.md`
```

This should be five separate bullets/inline code spans.

### Risk

Low to medium. Codex can still infer intent, but malformed references reduce instruction clarity and could lead to missed loading.

### ULTIMATE fix

Rewrite Stage 1 list with one document per bullet:

```markdown
- `docs/FAST_LANE.md`
- `docs/COMPLEXITY_MODEL.md`
- `docs/ROLE_OUTPUT_SCHEMAS.md`
- `docs/EXTERNAL_EVIDENCE_PROTOCOL.md`
- `docs/FINAL_FANTASY_CODENAME_POLICY.md`
```

Also fix the later sentence that references all five docs inside one code span.

## Issue 2 — Scenario tests are inconsistent between JSON and Markdown

Files present:

- `docs/SCENARIO_TESTS.json` contains 5 scenarios.
- `docs/scenario_tests/` contains 6 markdown scenario files.

Mismatch:

- Markdown includes `06-language-policy-ru-user-en-artifacts.md`, but JSON does not.
- JSON includes `api_breaking_change_review`, but markdown has `04-production-auth-change.md` instead.
- Markdown scenario 2 expects Garnet and Agrias in the role set, while JSON makes `ux_writer` and `code_reviewer` optional.
- Markdown scenario 3 expects Tifa and Garnet for AI summarization, while JSON does not require them.

### Risk

Medium. Scenario tests are meant to harden routing. If the two sources disagree, Codex or a validator could learn inconsistent expectations.

### ULTIMATE fix

Make JSON the source of truth and generate markdown from it, or vice versa. Recommended: JSON as source of truth, Markdown as human-readable commentary.

Required JSON scenarios for ULTIMATE:

1. `tiny_copy_change`
2. `greenfield_ux_mvp`
3. `market_discovery`
4. `ai_agent_feature`
5. `production_auth_change`
6. `api_breaking_change_review`
7. `language_policy_ru_user_en_artifacts`

Update `validate_kit.py` to check that every JSON scenario has a matching markdown file and every markdown file maps to a JSON scenario.

## Issue 3 — Several roles still self-escalate

Detected self-escalations:

- `02-delivery_manager.md`: Ashe escalates to Ashe for sequencing/gates.
- `27-security_reviewer.md`: Vincent escalates to Vincent for auth/security/data exposure.
- `28-privacy_compliance_reviewer.md`: Serah escalates to Serah for privacy/compliance.
- `38-qa_engineer.md`: Rikku escalates to Rikku for test/verification needs.

### Risk

Low to medium. Humans will understand the intent, but agents may create circular handoffs.

### ULTIMATE fix

Replace self-escalation lines with role-specific wording.

Examples:

- Delivery Manager: “If sequencing/gates are unclear, produce an approval checkpoint and ask the user or Team Architect.”
- Security Reviewer: “If security risk appears, own the security review and escalate unresolved product/architecture decisions to Team Architect or user.”
- Privacy Reviewer: “If privacy risk appears, own the privacy review and escalate legal/compliance certainty to qualified human review.”
- QA Engineer: “If verification need appears, own the test plan and ask implementers for missing acceptance criteria.”

Add validator check for codename or role-title self-mentions inside `## Escalation triggers`.

## Issue 4 — Some handoff rules include self-references

Detected self-handoff references:

- UX Interaction Reviewer
- UX Writer
- Design System Guardian
- Accessibility Specialist
- Solution Architect

Cause: generic handoff block says “If this role changes user-facing behavior, UX Interaction Reviewer, UX Writer, Accessibility Specialist, and Design System Guardian may need review…” even inside those roles.

### Risk

Low. Mostly noise, but ULTIMATE should be clean.

### ULTIMATE fix

Replace generic handoff blocks with role-specific handoff blocks generated from `OWNERSHIP_MATRIX.md`, excluding the current role.

Add validator check for self-reference inside `## Handoff rules`.

## Issue 5 — `README.md.bak` should not ship

There is an extra file:

```text
README.md.bak
```

It differs from `README.md`.

### Risk

Low. It is clutter, but clutter in an instruction kit can confuse agents.

### ULTIMATE fix

Remove `README.md.bak` from the final archive.

## Issue 6 — Validator is good but not strict enough

Current validator catches structural issues, but misses:

- malformed comma-separated backtick doc refs in `FIRST_PROMPT.md`;
- JSON/markdown scenario mismatch;
- self-escalation in roles other than Consistency Auditor;
- self-handoff references;
- backup/stale files;
- mismatch between expected scenario markdown and JSON.

### ULTIMATE fix

Upgrade `validate_kit.py` with checks for:

1. no `.bak` files;
2. no backtick-enclosed doc list containing commas;
3. scenario JSON ↔ markdown parity;
4. no self-escalation;
5. no self-handoff;
6. each scenario has `complexity`, `max_roles`, `max_questions`, `required_roles`, `optional_roles`, `forbidden_roles`;
7. required roles do not exceed complexity budget unless scenario is Exception.

## Issue 7 — AI scenario routing should distinguish “AI summary” from “AI agent with tools”

Current JSON scenario `ai_agent_feature` says “Add AI agent with tools and user data access”. Markdown scenario says “Add AI summarization of customer interviews”. These are different risk profiles.

### Risk

Medium. AI summarization may not require the same tool-permission review as a write-capable agent, but it still requires privacy, evals, hallucination/fallback, UX copy, and possibly UX Researcher if interview content is involved.

### ULTIMATE fix

Split into two scenarios:

1. `ai_summarization_feature`
   - Required: AI/ML Systems Architect, Model Evaluation Specialist, AI Safety Reviewer, Privacy Reviewer, QA Engineer, UX Writer if user-facing summary labels/explanations matter.
   - Optional: UX Researcher if summary quality must reflect research methodology.

2. `ai_agent_tool_use_feature`
   - Required: AI/ML Systems Architect, Model Evaluation Specialist, AI Safety Reviewer, Security Reviewer, Privacy Reviewer, QA Engineer, relevant architect, Consistency Auditor.
   - Tool permission matrix required.

## Issue 8 — Role depth is good enough, but “principal-level” can be sharper in ULTIMATE

v1.3 is much better than v1.2, but some roles still contain a generic senior-specialist framing before the truly role-specific method.

### Risk

Low. The advanced protocols solve most of the earlier problem, but ULTIMATE can make the system feel less template-generated.

### ULTIMATE fix

For the most frequently used roles, rewrite `Ideal expertise and professional depth` manually:

- Task Intake Orchestrator
- Team Architect
- Product Strategist
- Market Researcher
- UX Researcher
- CX Researcher
- UX Interaction Reviewer
- UX Writer
- Design System Guardian
- Solution Architect
- Frontend Architect
- Backend Architect
- AI/ML Systems Architect
- Model Evaluation Specialist
- AI Safety Reviewer
- Security Reviewer
- Privacy Reviewer
- QA Engineer
- Code Reviewer

Do not rewrite all 42 unless necessary. The goal is optimal complexity, not ornamental perfection.

## Recommended ULTIMATE patch list

### Must fix

1. Fix `FIRST_PROMPT.md` malformed doc references.
2. Reconcile scenario JSON and markdown files.
3. Remove self-escalations.
4. Remove self-handoff references.
5. Remove `README.md.bak`.
6. Upgrade `validate_kit.py` to catch the above.

### Should fix

7. Split AI summarization and AI tool-agent scenarios.
8. Add scenario for “small backend bugfix”.
9. Add scenario for “research-only UX study”.
10. Add stricter skill-specific output schemas for AI, research, risk, and design/UX planning.

### Nice to have

11. Manually deepen the top 18–20 most-used roles.
12. Add `docs/ULTIMATE_RELEASE_NOTES.md` explaining what changed from v1.3.
13. Add `docs/VALIDATOR_RULES.md` describing what `validate_kit.py` checks.

## Final recommendation

Use v1.3 as the base for the ULTIMATE release, but apply the must-fix patch before calling it final.

The system is now architecturally correct. The remaining work is mostly cleanup and consistency hardening:

- fewer ambiguous instructions;
- no stale files;
- no circular handoffs;
- scenario tests as a reliable routing contract;
- stricter validator.

After these fixes, the kit will be ready for real project use as a robust Codex product-team operating system.
