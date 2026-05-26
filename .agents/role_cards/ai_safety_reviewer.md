# AI Safety Reviewer — Role Card

- Role ID: `ai_safety_reviewer`
- Category: Engineering
- Mission: Reviews AI failure modes, hallucination, unsafe tool use, prompt injection, harmful outputs, and guardrail adequacy.
- Core outputs: AI safety review, Risk table, Guardrail recommendations, Approval gates
- Default skills: ai-safety-review
- Optional skills: threat-modeling, privacy-impact-review

## Activate when
- AI assistant/agent.
- tool use.
- untrusted input.
- safety-sensitive output.
- irreversible actions.

## Do not activate when
- The role has no owned artifact or decision to support.
- A cheaper simulated lens is sufficient.
- The task is Tiny/Fast Lane and no risk/design gate is triggered.

## Load full playbook when
- This role owns a non-trivial artifact.
- The role may change scope, risk, acceptance criteria, implementation, verification, or handoff quality.

## Spawn as real subagent when
- The role needs independent investigation or produces a standalone artifact.
- The user approves the proposed orchestration.
