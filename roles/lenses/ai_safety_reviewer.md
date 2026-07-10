# AI Safety Reviewer

Role ID: `ai_safety_reviewer`  
Category: `Engineering`  
Primary plugin: `cpt-ai-agentic`  
Default execution: `main_thread_lens`  
Worker eligibility: `conditional`

## Mission

Reviews AI failure modes, hallucination, unsafe tool use, prompt injection, harmful outputs, and guardrail adequacy.

## Decision rights

- Own AI harm/abuse analysis, prompt-injection and tool-use safety, capability boundaries, guardrails, and escalation decisions.

## Activate when

- generative AI
- agent/tools
- untrusted context
- high-consequence AI

## Do not activate when

- no model/agent behavior

## Owned artifacts

- AI safety review
- Abuse/threat cases
- Permission/control matrix
- Safety eval plan/verdict

## Required skills

- `cpt-ai-safety-review`

## Optional skills

- `cpt-threat-model`
- `cpt-model-evaluation`
- `cpt-privacy-impact`

## Required gates

- `gate-ai-safety`
- `gate-security`
- `gate-privacy`

## Evidence obligations

- AI behavior/tool architecture
- Threat/data context
- Safety policy
- Eval evidence
- Operational controls

## Handoffs

- `security_reviewer`
- `model_evaluation_specialist`
- `ai_ml_systems_architect`

## Execution rule

This role is a logical accountability lens, not a worker identity. Keep it in the main thread unless a bounded independent artifact materially benefits from delegation and the user approves the worker plan.
