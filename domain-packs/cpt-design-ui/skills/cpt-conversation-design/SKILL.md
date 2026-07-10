---
name: cpt-conversation-design
description: Use for chat, assistant, voice, or multi-turn flows including clarification, repair, confirmations, fallback, and human handoff.
---

# CPT Conversation Design

## Use when

- The product interaction is conversational or agentic.

## Do not use when

- The task is ordinary static microcopy.

## Required inputs

- User intents/jobs, system capabilities/limits, data/tools, safety constraints, tone, context retention, and handoff policy.

## Method

1. Define user intents, entry conditions, success, and unsupported intents.
2. Model turn structure, context, clarification, disambiguation, confirmation, progress, and cancellation.
3. Design repair for misunderstanding, tool failure, partial completion, and contradictory user input.
4. Specify uncertainty language, citations/evidence, privacy boundaries, and irreversible-action confirmation.
5. Define fallback and human handoff with preserved context.
6. Test representative, adversarial, multilingual, and accessibility cases.
7. Create dialogue state and message patterns separate from model prompt internals.

## Output contract

Produce a compact artifact containing:

- `Intent and dialogue-state model.`
- `Turn/message patterns.`
- `Repair, fallback, confirmation, and handoff rules.`
- `Test cases and unresolved capability/safety questions.`

## Evidence standard

- Do not promise capability the system cannot execute or verify.

## Stop and escalate

- Tool permissions, safety, or human handoff are unresolved.

## Failure modes to avoid

- Writing a happy-path script only.
- Using personality to mask uncertainty.
