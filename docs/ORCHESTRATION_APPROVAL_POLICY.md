# ORCHESTRATION_APPROVAL_POLICY.md

## Ask user approval before

- spawning real subagents;
- loading many full playbooks;
- high-risk roles or irreversible actions;
- changing approved scope;
- design-system deviations;
- custom UI when DS component exists.

## User approval options

Offer options:
- approve as proposed;
- modify lineup;
- use cheaper simulation mode;
- run only recon first;
- skip specialists and proceed main-thread only.

## Tiny/Fast Lane

If the user explicitly asks to implement a reversible, low-risk change, implementation approval is implied. Real subagent spawn is still not implied.
