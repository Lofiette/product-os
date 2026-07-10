# AI Safety Gate

Gate ID: `gate-ai-safety`

## Apply when

For generative AI, tool use, untrusted context, sensitive decisions, irreversible actions, or abuse risk.

## Owners

- `ai_safety_reviewer`
- `security_reviewer`

## PASS criteria

- Harms, abuse cases, prompt injection, tool permissions, confirmation, escalation, and fallback are reviewed.
- High-risk actions have bounded authority and auditable controls.

## BLOCK criteria

- The model can perform irreversible actions without confirmation.
- Untrusted content can silently change system instructions.
- Safety-critical uncertainty has no escalation path.

## Required evidence

- Safety review
- Permission matrix
- Adversarial evals
- Fallback/escalation design

## Verdict contract

- `PASS`: required evidence supports the acceptance claim.
- `PASS_WITH_WARNINGS`: acceptance is supportable, with explicit non-blocking residual risk.
- `BLOCKED`: one or more blocking conditions are present.
- `INSUFFICIENT_EVIDENCE`: the gate cannot responsibly decide.

A warning must never hide a blocker. Missing evidence must never be converted into a clean pass.
