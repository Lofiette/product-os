# Content Quality Gate

Gate ID: `gate-content-quality`

## Apply when

For user-facing copy, terminology, states, errors, onboarding, or conversational behavior.

## Owners

- `ux_writer`
- `conversation_designer`

## PASS criteria

- Terminology is consistent and audience-appropriate.
- Messages explain action, status, and recovery.
- Voice/tone and localization constraints are respected.

## BLOCK criteria

- Technical identifiers leak into user copy without intent.
- Errors do not support recovery.
- Critical actions are ambiguous or misleading.

## Required evidence

- Content matrix
- Terminology decisions
- State/message review

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
