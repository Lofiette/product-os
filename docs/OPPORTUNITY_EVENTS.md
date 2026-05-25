# OPPORTUNITY_EVENTS.md — Handling New Ideas and Changing Inputs

Product work is dynamic. New ideas can appear from stakeholders, support, sales, research, analytics, competitors, incidents, or technical discoveries. Treat these as opportunity events, not interruptions.

## Event types

- Stakeholder idea
- Cross-functional suggestion
- User research insight
- CX/support signal
- Market or competitor signal
- Analytics anomaly
- Technical discovery
- Incident learning
- Design critique
- Constraint change

## Event intake protocol

1. Capture the event in compact English.
2. Identify source, evidence level, urgency, and affected decisions.
3. Classify impact:
   - Ignore/defer: does not affect current decision.
   - Clarify: needs one or two questions.
   - Improve: run a creative improvement loop.
   - Re-route: adjust team or risk roles.
   - Re-plan: update scope, acceptance criteria, or implementation sequence.
   - Block: stop until user/human decision.
4. Add an Opportunity Event entry to `TASK.md` when it changes scope, risks, team, or acceptance criteria.
5. Add a Chronicle entry when it changes direction or creates a decision.
6. Never implement an event-driven change without approval when it changes approved scope.

## Event impact table

| Field | Value |
|---|---|
| Event ID | OE-YYYYMMDD-N |
| Source | user / stakeholder / research / support / analytics / repo / external |
| Evidence level | evidence / assumption / hypothesis |
| Affected area | product / UX / tech / risk / delivery / copy / research |
| Urgency | now / next iteration / backlog |
| Decision impact | none / clarify / improve / re-route / re-plan / block |
| Recommended method | none / creative loop / research / risk review / technical spike |
| Owner role | role ID |

## Opportunity gate

A new idea deserves attention when it can improve at least one of:
- user value;
- clarity and comprehension;
- accessibility or inclusivity;
- differentiation;
- implementation simplicity;
- risk reduction;
- learning speed;
- operational reliability.

A new idea does not deserve scope change merely because it is clever.

## Handoffs

- Product impact → Cloud / Product Strategist.
- Research evidence → Tifa / UX Researcher, Noctis / CX Researcher, or Balthier / Market Researcher.
- Flow/content impact → Rinoa / UX Interaction Reviewer and Garnet / UX Writer.
- Visual/component impact → Terra / Visual Design Director and Lightning / Design System Guardian.
- Technical impact → Auron / Solution Architect and relevant architect.
- Risk impact → relevant risk owner plus Squall / Consistency Auditor.
- Delivery impact → Ashe / Delivery Manager.
