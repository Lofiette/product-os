# RISK_POLICY.md

Activate risk roles when triggered:
- Security Reviewer: auth, permissions, secrets, injections, uploads, public APIs, AI tools.
- Privacy & Compliance Reviewer: personal data, research data, tracking, retention, AI context/data use.
- AI Safety Reviewer: AI assistants, tool use, untrusted input, unsafe outputs, irreversible actions.
- Migration Planner: schema/data/config migration or backfill.
- DevOps & Release Engineer: deployment, infra, env/config, rollout.

Irreversible actions require explicit approval.
