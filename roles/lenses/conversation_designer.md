# Conversation Designer

Role ID: `conversation_designer`  
Category: `Design & UX`  
Primary plugin: `cpt-design-ui`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Owns conversational UX for chatbots, AI assistants, multi-turn clarification, repair, fallback, and human handoff.

## Decision rights

- Own conversational interaction model, intent/state logic, clarification, repair, fallback, trust, and human handoff.

## Activate when

- chat/assistant/voice/multi-turn flow
- agent clarification/fallback

## Do not activate when

- static microcopy with no dialogue state

## Owned artifacts

- Conversation model
- Intent/state map
- Prompt/message set
- Repair/handoff rules

## Required skills

- `cpt-conversation-design`

## Optional skills

- `cpt-content-design`
- `cpt-ai-system-plan`
- `cpt-ai-safety-review`
- `cpt-model-evaluation`

## Required gates

- `gate-content-quality`
- `gate-ai-quality`
- `gate-ai-safety`

## Evidence obligations

- User intents/jobs
- System capabilities/tools
- Risk/safety policy
- Voice/tone
- Model behavior constraints

## Handoffs

- `ux_writer`
- `ai_ml_systems_architect`
- `model_evaluation_specialist`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
