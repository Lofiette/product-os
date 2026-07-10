# Role Authoring Standard

## Role model

A role is a durable accountability lens. It defines who owns a decision or artifact, which specialist judgment must be applied, what evidence is required, and which gates can block acceptance.

A role is not:

- a personality;
- a job-title costume;
- a skill;
- a playbook;
- a default subagent;
- a substitute for clear task ownership.

## Required registry fields

Every role must define:

- stable `id`, title, category, and primary plugin;
- mission and explicit decision rights;
- activation and non-activation signals;
- owned artifacts;
- required and optional canonical skills;
- required gates;
- evidence obligations;
- handoffs;
- task types;
- execution modes and worker eligibility;
- lens and deep-method references.

## Depth requirement

The lens stays compact. The method reference must contain role-specific mental models, a concrete method, evidence standard, output contract, stop/escalation rules, and professional anti-patterns.

Generic advice such as “read relevant files and report blockers” is insufficient.

## Ownership rules

- One accountable role per meaningful decision or artifact.
- Supporting roles may challenge, supply evidence, or own a gate.
- A supporting role must not silently take over the accountable decision.
- If ownership is ambiguous, resolve it before adding more roles.

## Change policy

Add a role only when a repeated, durable accountability cannot be cleanly owned by an existing role. Prefer a skill for a method, a gate for acceptance evidence, and a protocol for procedure.
