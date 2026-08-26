# Codex Product Team ULTIMATE Pro v1.4 — Challenge Audit

Verdict: **PASS WITH IMPORTANT PROCESS FIXES**.

The archive is structurally healthy and the embedded validator passes, but several runtime rules can conflict during real Codex use. The highest-risk issues are not missing files. They are hidden process contradictions, budget ambiguity, and role-output overhead.

## Validation snapshot

Embedded validator result:

```text
VALIDATION PASSED: 42 roles, 13 skills, 10 scenarios.
```

Additional checks performed:

- Zip integrity and unpackability.
- Role identity consistency across `TEAM.md`, playbooks, role cards, and `.codex/agents/*.toml`.
- Scenario JSON / markdown sync.
- Stage 0 / routing / role-card / playbook size estimates.
- Self-handoff and self-escalation checks.
- Stale version-label search.
- Runtime contradiction review across `AGENTS.md`, `FAST_LANE.md`, `QUALITY_GATES.md`, `SCENARIO_TESTS.json`, and work-mode docs.

## What is strong

### 1. Identity integrity is now clean

No codename drift found between:

- `TEAM.md`
- `.agents/playbooks/*.md`
- `.agents/role_cards/*.md`
- `.codex/agents/*.toml`

This fixes the previous Sabin/Prompto/Freya/Locke-style drift.

### 2. Lean startup is much better

Stage 0 now loads:

- `AGENTS.md`
- `TASK.md`
- `CHRONICLE.md`
- `docs/BOOTSTRAP_INDEX.md`
- `docs/QUESTION_TREE.md`
- `docs/LANGUAGE_POLICY.md`

Measured Stage 0 size:

```text
18,081 characters ≈ 4,520 rough tokens
```

This is a major improvement over the earlier heavy startup.

### 3. Creative improvement loop is correctly framed

`CREATIVE_METHODS.md` and `OPPORTUNITY_EVENTS.md` correctly treat creative frameworks as hypothesis-generation tools, not evidence or scope approval.

### 4. Role cards are useful

There are 42 role cards. Total size is around 48,937 characters, with each card around 1,100–1,200 characters. This is much cheaper than full playbooks and supports staged routing.

## Blocking / high-priority issues

## P0. Hidden contradiction: Chronicle Keeper is required for any file change, but Fast Lane treats it as optional

Evidence:

- `AGENTS.md`: Aerith / Chronicle Keeper is required for long tasks, multi-step tasks, and **any task that changes files**.
- `FAST_LANE.md`: update `CHRONICLE.md` only if work changes files or decisions.
- `SCENARIO_TESTS.json`: in `tiny_copy_change`, `chronicle_keeper` is optional and `max_roles` is 3.

Why this can break:

A tiny file-changing copy task may route as:

- Yuna / Intake
- Garnet / UX Writer
- Zidane / Frontend Architect
- Aerith / Chronicle Keeper
- optional Agrias / Code Reviewer

That already exceeds the 1–3 Fast Lane budget if system roles count as roles.

Recommendation:

Add a distinction between **role activation** and **system service update**:

```text
Chronicle update is required for file-changing work, but Chronicle Keeper as a full role is required only for multi-step, decision-heavy, long-running, or context-risky work.

For Tiny/Fast Lane file changes, the implementing agent may perform a compact Chronicle update using `progress-chronicle` without counting Aerith as an active specialist role.
```

Also clarify whether role budgets count system roles.

## P0. Hidden contradiction: “Review completed when code changed” can force Code Reviewer into every tiny task

Evidence:

- `QUALITY_GATES.md`: before final answer, “Review completed when code changed.”
- `SCENARIO_TESTS.json`: `tiny_copy_change` has `code_reviewer` optional.

Why this can break:

For a one-line copy change, the framework may over-activate Agrias / Code Reviewer just to satisfy Gate 4. That contradicts Fast Lane.

Recommendation:

Define review levels:

```text
Review Level 0 — self-check: Tiny, low-risk, no production-sensitive behavior.
Review Level 1 — lightweight checklist: Fast Lane file change.
Review Level 2 — Code Reviewer role: Standard production change, bugfix, refactor, public behavior change.
Review Level 3 — Code Reviewer + risk roles: High-risk, API, data, auth, privacy, AI, release, migration.
```

Then change Gate 4 to:

```text
Review appropriate to complexity tier completed.
```

## P0. Approval gate can over-block explicit tiny implementation requests

Evidence:

- `AGENTS.md`: “Stop and ask before implementation after planning.”
- `COMPLEXITY_MODEL.md`: Tiny says “user intent may be enough.”

Why this can break:

If the user says “переименуй кнопку”, the agent may still ask for approval after a micro-plan, making Fast Lane annoyingly bureaucratic.

Recommendation:

Add:

```text
For Tiny/Fast Lane, if the user explicitly asked to implement, no risk gates are triggered, and the change is reversible, the user request counts as implementation approval. Still state a one-line plan before editing when useful.
```

## P1. Role budget is ambiguous

Current budgets say:

- Fast Lane: 1–3 roles
- Standard: 4–7 roles
- Complex: 8–12 roles
- High-risk: 10–15 roles

Unclear:

- Do Yuna, Aerith, Squall, Ashe count?
- Does “role-card-only” count?
- Does a compact Chronicle update count?
- Does a one-off review checklist count?

Recommendation:

Introduce three buckets:

```text
Active specialist role: counts toward role budget.
System service: does not count unless full role artifact is produced.
Consulted role card: does not count unless the role produces an artifact.
```

This keeps budgets meaningful.

## P1. Stage 0 is leaner, but still not tiny-task cheap

Stage 0 is around 18k characters. Good for serious tasks, still chunky for tiny tasks.

Breakage mode:

For a trivial task, the model still loads six files before asking/doing anything.

Recommendation:

Add an even smaller `MICRO_START.md` or compress `AGENTS.md` into:

- `AGENTS.md` as short runtime constitution;
- `docs/OPERATING_MANUAL.md` for details.

Target:

```text
Micro/Tiny startup: 6k–9k characters
Standard startup: current 18k characters is acceptable
```

## P1. Full playbooks remain expensive and repetitive

Measurements:

```text
All playbooks total: 296,196 characters
Average playbook: ~7,052 characters
All role cards total: 48,937 characters
Average role card: ~1,165 characters
```

Worst-case required-role loading if full playbooks are loaded for all required roles:

| Scenario | Required roles | Cards | Full playbooks | Total with base+routing |
|---|---:|---:|---:|---:|
| tiny_copy_change | 2 | 2,354 | 14,393 | 45,159 |
| greenfield_ux_mvp | 7 | 8,219 | 48,152 | 84,783 |
| ai_tool_agent_feature | 10 | 11,801 | 71,538 | 111,751 |

This is manageable for large tasks, but bad if the agent accidentally loads full playbooks for Tiny/Fast Lane.

Recommendation:

- Full playbooks are forbidden in Tiny unless explicitly required.
- Full playbooks are optional in Fast Lane.
- Standard loads only 2–4 full playbooks: lead roles and highest-risk roles.
- Other selected roles produce role-card-level artifacts.

## P1. `QUESTION_TREE.md` still says Intake A is 5–9 questions

Evidence:

- `QUESTION_TREE.md`: “Intake A: universal first batch, 5 to 9 questions.”
- `FIRST_PROMPT.md`: “0 to 3 questions if Tiny/Fast Lane.”
- `task-intake/SKILL.md`: “5–9 adaptive questions max, or 0–3 for Tiny/Fast Lane.”

Why this can break:

The agent may over-ask because `QUESTION_TREE.md` looks authoritative.

Recommendation:

Rename heading:

```text
Intake A: universal first batch, 5 to 9 questions unless Tiny/Fast Lane applies
```

And split:

```text
Micro Intake: 0–2 questions
Fast Lane Intake: 1–3 questions
Standard Intake: 3–7 questions
Complex/High-risk Intake: 5–9 + targeted follow-up
```

## P1. MVP / Delivery Manager routing is slightly inconsistent

Evidence:

- `WORK_MODES.md`: “MVP: Product Strategist and Delivery Manager protect scope.”
- `ROLE_ROUTING_MATRIX.md`: Ashe required only for multi-phase/cross-area MVP.
- `SCENARIO_TESTS.json`: `delivery_manager` optional for greenfield UX MVP.

Recommendation:

Make this explicit:

```text
Delivery discipline is required for MVP, but Delivery Manager as a full role is required only for multi-phase, cross-area, deadline-bound, dependency-heavy, or high-risk MVP work.

Small MVP: Product Strategist owns scope discipline, Delivery Manager may be skipped or consulted by role card.
```

## P1. Review/audit mode is read-only, but “audit of framework” can still tempt patching

The read-only rule is good. To harden it:

Add to `self-audit/SKILL.md`:

```text
Self-audit outputs recommendations only. It must not modify the kit unless the user explicitly requests a patch/build iteration.
```

## P2. Opportunity events need a churn-control policy

Current creative loop is good, but repeated opportunity events can derail delivery.

Recommendation:

Add event classes:

```text
OE-0: no decision impact → ignore/log only
OE-1: small improvement → backlog or include if no scope change
OE-2: changes acceptance criteria → user approval required
OE-3: changes risk/team/architecture → re-route + consistency audit
OE-4: blocker → stop implementation
```

Add a rule:

```text
At most one creative loop per planning cycle unless the user explicitly asks for an ideation sprint.
```

## P2. Platform routing is under-specified

The routing matrix is strong by work mode and risk, but weak by platform.

Breakage example:

“Build a mobile MVP” routes through MVP roles and may miss Yuffie / Mobile Architect unless the agent infers it.

Recommendation:

Add a `By platform/surface` section to `ROLE_ROUTING_MATRIX.md`:

| Platform/surface | Required / likely roles |
|---|---|
| Web UI | Rinoa, Garnet, Lightning, Zidane, Rikku |
| Mobile app | Yuffie, Rinoa, Vivi, Sabin, Rikku |
| API/service | Basch, Kimahri, Rikku, Vincent if sensitive |
| Data product | Lulu, Penelo, Serah, Rikku |
| AI feature | Shantotto, Celes, Rydia, Serah/Vincent, Rikku |
| Design-system component | Lightning, Vivi, Zidane, Rikku |

## P2. External research path is safe but operationally incomplete

`EXTERNAL_EVIDENCE_PROTOCOL.md` says to produce a research plan when external facts are unavailable. Good.

Missing detail:

- source quality tiers;
- citation/evidence table schema;
- when to ask the user for source files;
- when to explicitly say “cannot conclude”.

Recommendation:

Add a compact source quality table:

```text
Primary official source > peer-reviewed/standards > reputable market data > first-party user/support data > third-party article > anecdote.
```

## P2. Repository reconnaissance is missing as a first-class skill

For Codex, many tasks start in an existing repo. There is no dedicated `repo-recon` skill.

Why this matters:

Without repo recon, agents may jump to implementation patterns before understanding:

- package manager;
- test commands;
- framework;
- existing design system;
- repo conventions;
- CI/build scripts;
- generated files;
- ownership boundaries.

Recommendation:

Add `.agents/skills/repo-recon/SKILL.md`:

```text
1. Inspect file tree shallowly.
2. Identify package manager, scripts, test commands, framework, lint/typecheck/build.
3. Locate AGENTS/local instructions and generated files.
4. Locate existing components/patterns/tests.
5. Return a Repo Recon Brief.
6. Do not load large files until relevant.
```

This is one of the best quality/resource improvements possible.

## P2. Chronicle can grow into a token swamp

`CHRONICLE.md` is currently compact. But long projects will make Stage 0 heavier because CHRONICLE is always loaded.

Recommendation:

Add compaction rules:

```text
Keep top Context rescue summary under 300 words.
Keep Current command center under 10 bullets.
Archive old timeline entries to docs/history/YYYY-MM.md when CHRONICLE exceeds N lines.
Do not paste long role outputs into CHRONICLE; link/summarize them.
```

## P2. Full playbooks still contain lots of shared boilerplate

Repeated phrases found across all 42 playbooks:

- “senior/principal-level specialist…” appears 42 times.
- “applies this capability through…” appears 309 times.
- shared handoff/escalation/failure sections repeat across most roles.

This is not logically wrong, but it wastes context when full playbooks are loaded.

Recommendation:

Move shared material to:

```text
.agents/playbooks/_shared_role_contract.md
```

Then each role playbook can become:

- identity;
- triggers;
- role-specific expertise;
- role-specific method;
- outputs;
- unique handoffs/escalations;
- strict schema.

This can cut full playbook loading by 25–40%.

## P3. Stale version labels remain

Found many `v1.3` labels in skills and playbooks, for example:

- “v1.3 complexity guardrail”
- “v1.3 output schema rule”
- “Strict output schema v1.3”

Recommendation:

Rename to version-neutral labels:

```text
Complexity guardrail
Output schema rule
Strict output schema
```

This avoids version confusion in future releases.

## P3. Role title shorthand should be normalized

Found shorthand references such as:

- “Privacy Reviewer” instead of “Privacy & Compliance Reviewer”
- “AI/ML Architect” instead of “AI/ML Systems Architect”
- “DevOps” instead of “DevOps & Release Engineer”

Not dangerous, but ULTIMATE polish should normalize them.

## Simulated workflow stress tests

## 1. Tiny UI copy change

Task: “Rename `Send` button to `Submit feedback`.”

Expected optimal flow:

```text
Micro/Tiny
0–2 questions
Roles: UX Writer, maybe Frontend Architect
No full playbooks
No full Chronicle Keeper role
Review Level 0/1
Compact Chronicle update if file changed
```

Where current v1.4 can wobble:

- Chronicle Keeper may become mandatory because files changed.
- Code Reviewer may become mandatory because “Review completed when code changed.”
- `QUESTION_TREE.md` may nudge 5–9 questions.

Fixes: system service distinction, review levels, question budget split.

## 2. Small greenfield UX MVP

Task: local-first UX insights tool with projects/interviews/insights/tags.

Expected optimal flow:

```text
Standard
Roles: Product Strategist, UX Interaction Reviewer, UX Writer, Design System Guardian, Frontend Architect, QA, Chronicle service
Backend skipped if local-only
Delivery Manager optional unless multi-phase
```

Where current v1.4 can wobble:

- UX Writer optional in scenario, but UI-heavy MVP benefits from required content/state ownership.
- Delivery Manager language is inconsistent between work-mode doc and routing.
- Full playbooks for all roles may cost too much before repo recon.

Fixes: make UX Writer required for UI products with meaningful states, clarify Delivery Manager threshold, add repo recon skill.

## 3. Opportunity event during planning

Event: support says users misunderstand insight interpretation more than project creation.

Expected optimal flow:

```text
Opportunity event detected
Classify evidence/source/impact
Run one creative method only if it changes MVP decision
Likely roles: Product Strategist, UX Interaction Reviewer, UX Writer, Customer Support Analyst, optional Consistency Auditor
No scope change without approval
```

Where current v1.4 can wobble:

- repeated new ideas can cause planning churn;
- creative loop can expand team toward 8 roles too easily;
- no explicit “parking lot” / event class threshold.

Fixes: OE-0…OE-4 classes, one creative loop per planning cycle, `Opportunity backlog` section.

## 4. AI tool-using agent

Task: AI agent reads user data and can perform actions after confirmation.

Expected optimal flow:

```text
High-risk
Risk-first intake
Roles: AI/ML Systems Architect, Model Evaluation, AI Safety, Security, Privacy, Backend/API, QA, Consistency, Chronicle
Tool permission matrix required
Human approval for irreversible actions
```

Where current v1.4 is strong:

- AI scenarios are split properly.
- Tool permission matrix exists.
- Security/privacy/safety/evals are required.

Where it can improve:

- add “Risk-first intake” branch before generic product questions;
- make irreversible-action gate more prominent in `QUALITY_GATES.md`;
- add output-budget limits so high-risk roles produce compact tables, not essays.

## 5. Existing repo feature/fix

Task: modify an existing repo with unknown stack.

Expected optimal flow:

```text
Repo Recon first
Identify stack/scripts/tests/patterns/generated files
Then route roles and load playbooks
```

Current gap:

No dedicated repo-recon skill, so selected roles may reason before understanding the actual codebase.

This is a high-value improvement.

## Recommended v1.5 patch

Name:

```text
Codex Product Team ULTIMATE Pro v1.5 — Runtime Hardening & Repo Recon Patch
```

Must fix:

1. Distinguish active roles vs system services vs consulted role cards.
2. Add review levels and adjust `QUALITY_GATES.md`.
3. Add Tiny/Fast Lane implementation approval rule.
4. Split Intake A budgets clearly in `QUESTION_TREE.md`.
5. Clarify MVP / Delivery Manager threshold.
6. Add `repo-recon` skill.
7. Add Chronicle compaction rules.
8. Add opportunity event classes and churn-control rule.
9. Normalize stale v1.3 labels.
10. Normalize role-title shorthand.

Should fix:

11. Add `ROLE_INDEX.json` or `ROLE_INDEX.md` for even cheaper candidate routing.
12. Move shared playbook boilerplate to `_shared_role_contract.md`.
13. Add output-length budgets by complexity tier.
14. Add platform/surface routing table.
15. Strengthen external evidence source-quality protocol.

Nice to have:

16. Add `docs/RUNTIME_DECISION_TREE.md` with one-page flowchart.
17. Add a generated “lean mode” starter prompt for Tiny/Fast Lane.
18. Add validator checks for contradictory mandatory/optional role rules.
19. Add validator checks for stale version labels.
20. Add validator checks for self-handoff and role-title shorthand.

## Bottom line

v1.4 is already a strong operating system. The remaining problems are not architectural collapse, they are runtime friction points:

- too-easy escalation from tiny task to full ceremony;
- ambiguity about what counts as a role;
- missing repo reconnaissance;
- missing review-level granularity;
- opportunity events can create planning churn;
- full playbooks still carry repeated boilerplate.

The next best improvement is not “more roles.” It is a tighter runtime kernel: active-role accounting, review levels, repo recon, chronicle compaction, and event churn control.
