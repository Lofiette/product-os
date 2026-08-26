# Codex Product Team Maximum v1.2 — Control Audit

Date: 2026-05-20
Artifact audited: `codex-product-team-maximum-v1.2-ff.zip`

## Verdict

**Status: PASS WITH WARNINGS.**

The kit is structurally valid and meaningfully improved over v1.1. Staged loading, language policy, risk gates, and the Squall self-escalation fix are present. The main remaining problem is not file structure, but **operational depth**: many role playbooks still share templated language and do not yet behave like truly principal-level specialists.

## What was checked

- Archive extraction and file layout
- `scripts/validate_kit.py`
- Role count and custom-agent count
- Skill count and front matter
- Core docs: `AGENTS.md`, `FIRST_PROMPT.md`, `LANGUAGE_POLICY.md`, `EVIDENCE_POLICY.md`, `RISK_POLICY.md`, `QUALITY_GATES.md`, `FAST_LANE.md`
- Role routing and ownership matrix
- Key role playbooks
- Scenario tests
- Repeated generic phrasing
- Self-escalation issue in Consistency Auditor

## Structural validation

Result:

```text
VALIDATION PASSED: 42 roles, 12 skills.
```

Observed counts:

```text
Playbooks: 42
Custom agents: 42
Skills: 12
```

No missing role/playbook/TOML links were found.

## Strong improvements confirmed

### 1. Staged loading is fixed

`AGENTS.md` and `FIRST_PROMPT.md` now instruct Codex to load only core docs first, then selected playbooks and skills after intake. This is a major improvement over v1.0/v1.1.

### 2. Language policy is solid

`LANGUAGE_POLICY.md` correctly separates:

- Russian user-facing conversation
- compact English durable control artifacts
- product UI language defined by task context
- code identifiers/comments following project convention

This avoids the earlier “think in English” trap and reduces bilingual chaos.

### 3. Squall self-escalation is fixed

Consistency Auditor now says unresolved conflicts should go to Team Architect or user instead of escalating to itself.

### 4. Risk gates are clear

`RISK_POLICY.md` and `QUALITY_GATES.md` define explicit triggers for security, privacy, AI/ML, migration, API, performance, release, and incident work.

### 5. Fast Lane exists and is useful

`FAST_LANE.md` properly prevents the full 42-role circus for tiny tasks.

## Major findings

## Finding 1 — Role playbooks still contain heavy templating

Severity: High

Evidence:

The phrase below appears 309 times across all 42 playbooks:

```text
knows core methods, when to use them, common traps, evidence requirements, and handoff implications.
```

This means many roles list expertise areas, but do not explain the actual craft depth behind those areas.

Example: Market Researcher lists category design, competitive teardown, TAM/SAM/SOM, positioning maps, pricing research, trend scanning, switching costs, and adoption barriers. But each is followed by the same generic phrase.

Impact:

- Roles may produce plausible generic outputs instead of expert work.
- Codex may not know how to execute role-specific methods deeply.
- The team looks mature but may behave shallowly in complex tasks.

Recommendation:

Replace generic expertise bullets with role-specific method fragments. For example, Market Researcher should include:

- category definition protocol
- competitor set taxonomy
- direct/indirect/substitute alternatives map
- positioning axes
- pricing model scan
- market evidence confidence levels
- adoption barrier analysis
- switching cost model
- “external research required” rules

Apply this especially to:

- Product Strategist
- Market Researcher
- UX Researcher
- CX Researcher
- UX Writer
- UX Interaction Reviewer
- Design System Guardian
- Solution Architect
- Frontend Architect
- Backend Architect
- AI/ML Systems Architect
- Model Evaluation Specialist
- AI Safety Reviewer
- Security Reviewer
- QA Engineer
- Code Reviewer

## Finding 2 — Activation criteria are generic in every playbook

Severity: High

Evidence:

All 42 playbooks contain the same activation pattern:

```text
Activate this role only when TASK.md, docs/ROLE_ROUTING_MATRIX.md, docs/RISK_POLICY.md, or Team Architect identifies a clear need for this responsibility.
```

Impact:

This delegates the activation decision back to routing docs instead of teaching each role when it is actually needed. For example, UX Writer, Security Reviewer, Market Researcher, and Migration Planner should have very different activation triggers.

Recommendation:

Give every role a specific trigger set.

Examples:

UX Writer activation:

- user-facing copy is added or changed
- labels/CTAs/error/empty/success states are in scope
- onboarding, permission, destructive, or confirmation flows are involved
- terminology/taxonomy affects comprehension
- localization may affect content structure

Security Reviewer activation:

- auth/authz/session/permissions/secrets are touched
- untrusted input is processed
- file uploads, user-generated content, or external integrations are involved
- data exposure or tenant isolation risk exists
- new dependencies or tools affect attack surface

Market Researcher activation:

- category, competitors, positioning, pricing, adoption, or GTM assumptions affect decisions
- the task requires external market facts
- the user asks for market sizing, competitor comparison, or trend analysis

## Finding 3 — Skills are improved but still too thin for “Maximum”

Severity: Medium-High

Evidence:

Skills now have useful procedures, but most do not include concrete artifact schemas.

For example, `ai-ml-planning` correctly asks for behavior contract, context map, tool permissions, eval plan, guardrails, and cost/latency budget. But it does not provide a required table structure for:

- behavior contract
- context/data access map
- tool risk matrix
- eval matrix
- failure taxonomy
- fallback matrix
- human escalation rules

Impact:

Codex may produce inconsistent output shapes, making review and handoff harder.

Recommendation:

Add required output templates to each skill.

For example, `ai-ml-planning` should require:

```markdown
## AI behavior contract
| Behavior | Required | Prohibited | Uncertainty handling | Evidence |

## Context/data map
| Source | Data type | Sensitivity | Retention | Access rule | Risk |

## Tool permission matrix
| Tool/action | Read/write | Reversible | Approval required | Failure mode |

## Eval matrix
| Scenario | Expected behavior | Failure mode | Test data | Pass criteria |
```

## Finding 4 — Scenario tests are descriptive, not executable

Severity: Medium

Evidence:

Scenario tests exist under `docs/scenario_tests`, but they are markdown expectations only.

Impact:

They help human review, but the validator cannot catch routing regressions, missing expected roles, or over-selection.

Recommendation:

Add machine-readable scenario front matter, for example:

```yaml
expected_work_mode: Fast Lane
required_roles: [Garnet, Zidane]
optional_roles: [Agrias]
forbidden_roles: [Balthier, Tifa, Noctis, Vincent]
max_questions: 3
max_roles: 3
```

Then extend `validate_kit.py` to parse and check scenario files.

## Finding 5 — MVP routing has a minor inconsistency

Severity: Medium

Evidence:

`ROLE_ROUTING_MATRIX.md` says MVP lead roles are Cloud and Ashe, with Rinoa/Zidane/Basch/Rikku support.

`docs/scenario_tests/02-mvp-greenfield-product.md` says expected roles are Cloud, Rinoa, Garnet, Lightning, Zidane, Rikku, Agrias, Aerith, optionally Cid/Ashe.

Impact:

Team Architect may be unsure whether Ashe is core for MVP or optional. For small greenfield MVPs, Delivery Manager may be optional; for multi-phase MVPs, required.

Recommendation:

Refine MVP routing:

- MVP small/greenfield: Cloud lead; Ashe optional
- MVP multi-phase/production-bound: Cloud + Ashe
- UI-heavy MVP: add Rinoa, Garnet, Lightning, Vivi as needed
- backend/data MVP: add Basch, Lulu, Kimahri as needed

## Finding 6 — “Final Fantasy codenames” need one more guardrail

Severity: Low-Medium

Evidence:

`AGENTS.md` says codenames are for memorability only. Good.

Risk:

Codex might still occasionally style outputs as if the characters were personas, especially with names like Yuna, Cloud, Squall, etc.

Recommendation:

Add a stronger rule:

```text
Codenames are labels only. Do not imitate the character's voice, personality, lore, values, plot, quotes, or fictional behavior. Never let codename lore affect professional recommendations.
```

Also consider a public-distribution note: internal use is fine, but avoid presenting the kit externally as endorsed by or affiliated with Square Enix / Final Fantasy.

## Finding 7 — Evidence policy is strong, but external research path is under-specified

Severity: Medium

Evidence:

`EVIDENCE_POLICY.md` correctly prohibits invented market facts and unsupported claims.

But it does not clearly specify what to do when Codex cannot browse or cannot access external evidence.

Impact:

Market/CX/UX roles may stall or accidentally drift into assumptions.

Recommendation:

Add a section:

```markdown
## When external evidence is unavailable
- Do not make factual external claims.
- Produce a research plan, source list, search queries, and decision impact map.
- Mark all market/customer claims as assumptions or hypotheses.
- Ask user to provide sources or permit/perform external research.
```

## Finding 8 — Language policy is good, but mixed artifact delivery needs one extra rule

Severity: Low-Medium

Evidence:

The policy says replies to user in Russian and durable artifacts in compact English.

Potential gap:

When Codex outputs a planning brief to the chat, it may be unclear whether that brief is a user-facing reply or a control artifact.

Recommendation:

Add:

```text
When presenting an English control artifact inside a Russian chat reply, introduce and summarize it in Russian, then provide the artifact in compact English. Do not duplicate the entire artifact in Russian unless asked.
```

## Finding 9 — Review flow should separate “reviewer” from “fixer” more strongly

Severity: Medium

Evidence:

Code Reviewer says “Do not rewrite code unless asked.” Good.

But `implementation-review` skill says “Do not implement unless the approved work mode and approval gate allow implementation,” which may leave a small loophole if the reviewer believes approval exists.

Recommendation:

Make it sharper:

```text
Review mode is read-only. A reviewer may propose patches, but must not apply them unless the user explicitly switches from review to implementation.
```

## Finding 10 — `validate_kit.py` should fail on remaining generic depth phrases

Severity: Medium

Evidence:

Validator passed despite 309 generic expertise phrases.

Recommendation:

Make validator emit at least warning/failure when repeated generic lines exceed a threshold.

Possible threshold:

- 0 allowed in key roles
- <= 10 allowed across whole kit during migration period

## Recommended v1.3 patch plan

### P0 — No immediate blocker

No structural blocker found. The kit can be used experimentally.

### P1 — Must fix before calling it “ultra-team ready”

1. Replace generic expertise bullets in key roles with real role-specific methods.
2. Replace generic activation criteria with role-specific activation triggers.
3. Add output schemas to all skills.
4. Strengthen `validate_kit.py` to catch generic role depth.
5. Clarify MVP routing and Delivery Manager optional/required logic.

### P2 — Should fix for polish and safety

6. Strengthen codename anti-roleplay rule.
7. Add external-evidence-unavailable protocol.
8. Add mixed-language artifact presentation rule.
9. Strengthen read-only review mode.
10. Add machine-readable scenario tests.

## Overall assessment

| Area | Score |
|---|---:|
| Structural integrity | 9.5/10 |
| Staged loading / token discipline | 9/10 |
| Language policy | 9/10 |
| Routing architecture | 8/10 |
| Risk gates | 8/10 |
| Evidence policy | 8/10 |
| Role depth | 6/10 |
| Skill depth | 7/10 |
| Scenario testing | 5.5/10 |
| Readiness for real projects | 7.5/10 |

## Final verdict

**v1.2 is usable and much stronger than v1.1, but it is not yet the final dragon.**

The architecture is right. The remaining work is craftsmanship: replace templated role depth with real professional protocols, add role-specific activation triggers, formalize output schemas, and make scenario tests partially machine-checkable.

Recommended next release: **Maximum v1.3 — Role Depth & Routing Hardening Patch**.
