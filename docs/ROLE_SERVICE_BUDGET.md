# ROLE_SERVICE_BUDGET.md

## Contributor classes

- Active specialist role: owns an artifact; counts against role budget.
- System service: compact intake/routing/chronicle/review/consistency work; does not count unless producing full artifact.
- Consulted role card: used only for routing; does not count.
- Spawned subagent: real delegated thread; counts and requires approval.
- Simulated lens: main-thread application of role perspective; counts only when producing an artifact.

## Budget discipline

Do not select a role unless it owns a decision or artifact. Do not load a full playbook if a role card is sufficient.
