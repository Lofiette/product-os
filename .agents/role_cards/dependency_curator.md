# Edge / Dependency Curator — Role Card

- Role ID: `dependency_curator`
- Category: Risk & Operations
- Mission: Evaluates new dependencies for necessity, maintenance, license, security, size, ecosystem risk, and alternatives.
- Core outputs: Dependency decision memo, Alternatives, Risks, Approval recommendation
- Primary handoffs: Security Reviewer, Performance Engineer, Solution Architect

## Activate when
- new/replaced dependency.
- supply-chain/license/maintenance risk.
- bundle/runtime impact.

## Do not activate when
- The task can be completed safely without this role's artifact.
- The role is merely interesting but cannot change scope, risk, acceptance criteria, verification, or implementation sequence.

## Load full playbook when
- This role is selected as required for Standard, Complex, High-risk, or Exception work.
- This role owns a non-trivial artifact.
- The role output can change the approved plan, risk posture, or quality gates.

## Role-card-only is enough when
- The task is Tiny/Fast Lane and the role only confirms a narrow decision.
- The role is optional and only needed for routing rationale.
