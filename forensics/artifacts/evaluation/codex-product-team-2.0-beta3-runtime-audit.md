# Codex Product Team 2.0 beta 3 — Runtime Adequacy Audit

## Verdict

PASS WITH TARGETED RUNTIME HARDENING.

This patch addresses the observed failure mode: during real subagent UI review, 2 of 3 role-specific agents stayed running while fallback/default reviewers returned. The issue is not primarily a missing role problem. It is a runtime orchestration problem: spawned agents were too broad, insufficiently bounded, and lacked explicit recovery/quorum behavior.

## Validation

```text
VALIDATION PASSED: 49 roles, 73 skills, 22 scenarios.
ROUTING TEST PASSED: 22 scenarios, 49 roles, 73 skills.
Node syntax checks: PASS
Zip integrity: OK
```

## Observed failure mode

From the screenshot:

- `design_system_guardian` completed and returned WARN.
- `product_designer` and `design_engineer` remained running.
- fallback/default agents returned PASS quickly.
- final status depended on partial results and manual waiting.

This indicates that role-specific custom agents can become too expensive or too broad for a small rendered-page review. The framework must not treat spawned subagents as automatically better than bounded main-thread review.

## Root causes

1. **Custom agent tasks were not bounded enough.**
   Agents could interpret “review this page” as broad repo/design exploration.

2. **No UI Review Packet was required before spawning.**
   Reviewers lacked a compact target packet: URL, screenshot, changed files, DS mode, console/build status, review focus, limits.

3. **No failure/quorum policy.**
   The process did not specify what to do when some agents hang.

4. **Critical TOML doc paths were wrong.**
   Custom agents referenced `EVIDENCE_POLICY.md`, `QUALITY_GATES.md`, and `SUBAGENT_ORCHESTRATION.md` without `docs/` prefix. This could prevent spawned agents from using core policies.

5. **Too many real subagents for a current-page UI review.**
   For rendered page review, three role-specific subagents may be more expensive and less reliable than a review packet + one or two bounded reviewers.

## Beta 3 changes

### New runtime docs

- `docs/SUBAGENT_RUN_CONTRACT.md`
- `docs/SUBAGENT_FAILURE_POLICY.md`
- `docs/UI_REVIEW_PACKET.md`
- `docs/UI_REVIEW_RUNBOOK.md`

### New skills

- `subagent-run-contract`
- `subagent-failure-recovery`
- `ui-review-packet`
- `current-page-ui-review`

### New templates

- `.agents/templates/ui-review-packet.md`
- `.agents/templates/subagent-completion-status.md`

### New indices

- `docs/ROLE_TINY_INDEX.json`
- `docs/SKILL_TINY_INDEX.json`

### New scenarios

- `current_page_ui_review_bounded`
- `subagent_hang_recovery`

## Updated workflow for current-page UI review

1. Build UI Review Packet first.
2. Run main-thread multi-lens review or request approval for spawned reviewers.
3. Spawn at most 1–2 reviewers by default for Standard UI review.
4. Give each spawned agent a bounded task, strict schema, read-only permission, and stop condition.
5. If a spawned agent stays running, fails, or duplicates a still-running role, apply Subagent Failure Policy.
6. Report Subagent Completion Status.
7. Never convert missing specialist output into PASS.

## Important runtime rules

- Selected role does not mean spawned subagent.
- Loaded playbook does not mean spawned subagent.
- A spawned agent must have a run contract.
- A rendered page review must have a UI Review Packet.
- A stuck agent is a workflow limitation, not evidence of quality.
- Duplicate spawning of the same role while the earlier agent is running is forbidden without user approval.

## Recommended use in Codex

For a page review, prompt Codex with:

```text
Use bounded current-page UI review.
First create a UI Review Packet.
Do not spawn more than two real subagents unless I approve.
If any spawned agent stays running or fails, apply subagent-failure-recovery and report Subagent Completion Status.
```

## Remaining real-world caveat

Codex subagent behavior is platform/runtime-dependent. The framework can require bounded prompts, explicit approvals, and recovery policies, but it cannot guarantee that every spawned custom agent will complete. Therefore the reliable quality mechanism is not “more agents”; it is:

- better input packets;
- stricter reviewer output schemas;
- fallback hierarchy;
- explicit missing-evidence reporting;
- blocking gates that do not silently pass when agents fail.
