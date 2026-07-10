# Role Routing

## Decision-first routing

1. Classify the task and choose the nearest routing profile.
2. List the decisions, artifacts, risks, and gates before selecting roles.
3. Assign exactly one accountable role to every meaningful decision/artifact.
4. Add supporting lenses only if they change evidence, risk detection, gate ownership, or independent challenge.
5. Map selected roles to canonical skills and gates.
6. Load compact lenses first; load deep methods only for accountable owners or material specialists.
7. Keep roles in the main thread unless a bounded worker contribution is justified.

## Minimality test

Remove a selected role when all of the following are true:

- it owns no unique decision or artifact;
- it supplies no unique evidence;
- it owns no required gate;
- it does not provide material independent challenge;
- its handoff can be handled by an already selected role.

## Routing profiles

`ROLE_ROUTING_PROFILES.json` is the machine-readable starting point, not an automatic verdict. Product context and risk triggers may modify a profile.

## Transparency output

Before major work, report:

- task type/profile;
- accountable roles and owned decisions;
- supporting roles and why selected;
- skills and gates;
- roles skipped;
- main-thread versus worker execution;
- evidence gaps and stop conditions.
