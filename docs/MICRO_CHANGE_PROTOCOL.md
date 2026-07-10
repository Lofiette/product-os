# Micro Change Protocol

## Purpose

Handle obvious, local, reversible, low-risk changes without a full ticket and Impact Map ceremony.

## Eligibility

All conditions must be true:

- scope is local and clear;
- change is easily reversible;
- no public API or contract change;
- no dependency or migration change;
- no security, privacy, auth, payment, destructive data, or compliance risk;
- no broad external-module discovery;
- no uncertain systemic effect;
- smallest verification is obvious;
- no real subagent is needed.

## Flow

1. State a one-line target and verification plan.
2. Create an `MC-*` runtime record.
3. Perform only targeted reads.
4. Edit only the declared target scope.
5. Run the smallest relevant verification.
6. Complete the micro record and return runtime to `ready`.

The user's direct imperative request is sufficient authorization for the declared eligible micro scope. A separate approval prompt is unnecessary.

## Mandatory escalation

Escalate to a Standard Task before editing when any eligibility condition fails, the target expands, a shared/systemic pattern is discovered, or verification reveals broader impact.
