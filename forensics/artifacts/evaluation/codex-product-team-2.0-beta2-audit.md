# Codex Product Team 2.0 beta 2 — Culture, Taste & Anticipation Audit

## Verdict

PASS.

The archive was generated from the user-provided beta 1 package and patched into beta 2. Structural validation, routing validation, JS syntax checks, and zip integrity checks passed.

```text
VALIDATION PASSED: 49 roles, 69 skills, 20 scenarios.
ROUTING TEST PASSED: 20 scenarios, 49 roles, 69 skills.
Zip integrity: OK.
```

## Main beta 2 changes

### 1. Team Culture Layer

Added `docs/TEAM_CULTURE.md`.

This is not roleplay. It defines operational values:

- user stewardship;
- craft pride;
- systemic taste;
- evidence humility;
- constructive dissent;
- scope respect;
- calm ambition.

The main motivation contract is:

```text
Treat avoidable UX confusion, design-system drift, unclear hierarchy, broken states, and visible craft defects as unacceptable until either fixed or explicitly accepted by the user.
```

### 2. Taste Profile with good/bad examples

Added `docs/TASTE_PROFILE.md`.

It includes:

- default product taste;
- default UI taste;
- default content taste;
- anti-taste;
- good/bad examples for primary actions, empty states, error states, DS fidelity, prototypes without DS, data display, and copy tone.

Added templates:

- `.agents/templates/taste-profile.md`
- `.agents/templates/taste-review-report.md`
- `.agents/templates/example-taste-board.md`

### 3. Taste Review Gate

Added `docs/TASTE_REVIEW.md` and skill `taste-review`.

Taste Review produces:

```text
PASS / PASS WITH WARNINGS / BLOCKED
```

BLOCKED when visible craft failures, DS drift, unclear hierarchy, contradictions with bad examples, or avoidable UX confusion remain unresolved.

### 4. Example-driven taste calibration

Added skill `example-taste-board`.

This turns user-provided good and bad examples into:

- transferable qualities;
- anti-patterns;
- operational taste rules;
- avoidance rules.

### 5. Taste calibration workflow

Added skill `taste-calibration`.

It calibrates:

- desired feel;
- product adjectives;
- good examples;
- bad examples;
- operational rules;
- anti-taste rules;
- quality bar.

### 6. Creative tension review

Added `docs/CREATIVE_TENSION.md` and skill `creative-tension-review`.

It introduces controlled perspectives:

- Clarity Advocate;
- Craft Critic;
- System Guardian;
- User Advocate;
- Business Pragmatist;
- Creative Challenger.

This is used for improving decisions, not for theatrical agent personas.

### 7. Expectation Anticipation Branch

Added `docs/EXPECTATION_ANTICIPATION.md` and skill `expectation-anticipation`.

Anticipation levels:

- A0: no meaningful proposal;
- A1: small polish within approved scope;
- A2: quality improvement affecting acceptance criteria;
- A3: directional change affecting scope/team/architecture;
- A4: critical hidden expectation or blocker.

A2/A3/A4 proposals require explicit human approval before implementation.

### 8. Agent naming hardening

Added `docs/AGENT_NAMING_POLICY.md` and updated `AGENTS.md`, `FIRST_PROMPT.md`, `SUBAGENT_ORCHESTRATION.md`.

Rule:

```text
Use exact role_id / .codex agent names only. Do not assign personal names, fictional names, philosopher names, codenames, nicknames, or persona labels.
```

If the Codex UI auto-generates thread labels, they must be treated as interface noise. Artifacts and summaries must use exact agent IDs only.

### 9. TASK / CHRONICLE updates

`TASK.md` now tracks:

- team culture profile;
- taste profile status;
- desired feel;
- product adjectives;
- good examples;
- bad examples;
- UI density;
- visual expressiveness;
- content tone;
- DS strictness;
- anticipation branch.

`CHRONICLE.md` now tracks taste and anticipation decisions.

### 10. Routing and scenario tests

Added 4 new scenario tests:

- `taste_calibrated_ui_prototype`
- `good_bad_examples_redesign`
- `anticipation_proposals_before_implementation`
- `agent_id_no_personal_names`

Total scenario count: 20.

## Practical expected behavior

For a UI/prototype/redesign task, Codex should now propose something like:

```text
Operation: UI concept / prototype
Skills: design-recon, taste-calibration, prototype-ui-kit, screen-redesign, taste-review
Roles: product_designer, design_engineer, optional ux_writer / visual_design_director / design_system_guardian
Approval: required before real subagent spawn or scope-changing anticipation proposals
```

For user-provided references:

```text
example-taste-board -> taste-calibration -> screen/module design -> taste-review
```

For proactive improvement:

```text
expectation-anticipation -> proposal pack -> user approval -> TASK.md decision update -> implementation/replan
```

## Remaining risks

1. Codex UI may still display auto-generated labels for agent threads. The package now instructs Codex to ignore those labels and report exact agent IDs only, but UI rendering itself may not be controllable from project files.
2. Taste review improves quality only if Codex actually runs the selected skills. The framework now asks Codex to state selected/spawned/simulated execution explicitly.
3. Good/bad examples work best when the user supplies concrete examples or the repo contains existing screens/DS docs.

## Final status

Beta 2 is ready for practical testing.
