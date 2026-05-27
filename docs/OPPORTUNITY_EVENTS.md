# OPPORTUNITY_EVENTS.md

New signals/ideas during work are classified:
- OE-0: no decision impact, log/ignore.
- OE-1: small improvement, include if no scope/risk change or backlog.
- OE-2: changes acceptance criteria, user approval required.
- OE-3: changes risk/team/architecture, re-route and consistency audit.
- OE-4: blocker, stop implementation.

Use opportunity-event-triage before changing approved scope.


## Relation to Anticipation Branch

Opportunity events are incoming signals. Anticipation Branch is the proactive mechanism for identifying likely future expectations before they become explicit events.

Use:
- `opportunity-event-triage` for received signals;
- `anticipation-radar` for proactive expectation scanning;
- `proactive-proposal-review` before adding a proactive idea to the approved plan.

Do not change approved scope from either path without user approval.


## Relationship to anticipation

Opportunity events are reactive: a new signal arrives.
Expectation anticipation is proactive: the team proposes likely improvements before the user asks.

Both follow the same approval discipline: proposals that change scope, acceptance criteria, risk, architecture, or team composition require explicit user approval.
