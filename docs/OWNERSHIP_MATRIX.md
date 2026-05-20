# OWNERSHIP_MATRIX.md

## Primary ownership rules

| Area | Primary owner | Consulted roles | Final artifact |
|---|---|---|---|
| Task intake | Yuna | Cid, Aerith | Updated TASK.md |
| Team composition | Cid | Squall, Ashe | Role lineup |
| Delivery sequencing | Ashe | Cid, Aerith | Execution plan |
| Project memory | Aerith | all roles | CHRONICLE.md |
| Product scope | Cloud | Ramza, Balthier, Tifa, Noctis | Scope and acceptance criteria |
| Market evidence | Balthier | Cloud, Ramza | Market brief |
| User research | Tifa | Rinoa, Garnet | Research plan/findings |
| Customer journey | Noctis | Cloud, Tifa, Ramza, Prompto | Journey/service map |
| Support signals | Prompto | Noctis, Cloud, Garnet | Support signal summary |
| Requirements | Ramza | Cloud, Fran, Rikku | Requirements spec |
| Domain rules | Fran | Ramza, Basch, Lulu | Domain invariants |
| Interaction design | Rinoa | Garnet, Vivi, Lightning | Flow/state matrix |
| UX writing | Garnet | Rinoa, Cloud, Mog, Faris | Copy/message matrix |
| Localization/i18n | Faris | Garnet, Zidane, Rikku | Localization readiness review |
| Design system | Lightning | Terra, Vivi, Zidane | Component/token plan |
| Visual direction | Terra | Lightning, Rinoa | Visual brief |
| Accessibility | Vivi | Rinoa, Lightning, Rikku | A11y checklist |
| System architecture | Auron | all architects | Architecture plan |
| Frontend | Zidane | Lightning, Vivi, Rikku | Frontend plan |
| Backend | Basch | Kimahri, Lulu, Vincent | Backend plan |
| Mobile | Yuffie | Rinoa, Sabin, Cidolfus | Mobile plan |
| API contract | Kimahri | Basch, Rikku, Mog | Contract review |
| Data architecture | Lulu | Basch, Penelo, Serah | Data model plan |
| Analytics | Penelo | Cloud, Tifa, Lulu, Setzer | Metrics/event plan |
| Experimentation | Setzer | Penelo, Cloud, Rikku | Experiment plan |
| AI architecture | Shantotto | Celes, Rydia, Vincent | AI plan |
| Model evaluation | Celes | Shantotto, Rikku | Eval plan |
| AI safety | Rydia | Shantotto, Vincent, Serah | AI safety review |
| Security | Vincent | Basch, Serah, Edge | Threat model |
| Privacy/compliance | Serah | Lulu, Vincent, Garnet | Privacy risk review |
| Performance | Sabin | relevant architect, Barret | Performance plan |
| Dependencies | Edge | Vincent, Sabin | Dependency memo |
| Migration | Freya | Lulu, Basch, Cidolfus | Migration plan |
| Release | Cidolfus | Ashe, Barret | Release plan |
| Observability | Barret | Cidolfus, Sabin | Observability plan |
| Incident | Cecil | Barret, Vincent, Ashe | Incident report |
| QA | Rikku | all implementers | Test plan |
| Code review | Agrias | Rikku, Squall | Review report |
| Refactoring | Locke | relevant architect, Rikku | Refactor plan |
| Documentation | Mog | Aerith, Garnet | Handoff docs |

## Conflict resolution

If two roles disagree:
1. Identify whether the conflict is product value, user experience, technical risk, evidence quality, or delivery sequencing.
2. The primary owner proposes the decision.
3. Squall / Consistency Auditor checks contradictions and missing evidence.
4. The user approves decisions that affect scope, risk, cost, or public behavior.

## Conflict-resolution rules

- If two roles disagree on product scope, Product Strategist owns the recommendation and Consistency Auditor checks evidence.
- If two roles disagree on technical approach, Solution Architect owns the recommendation and relevant architects provide constraints.
- If UX, copy, accessibility, and visual direction conflict, UX Interaction Reviewer owns flow behavior, UX Writer owns language, Accessibility Specialist owns inclusive access, Design System Guardian owns reusable UI rules, and Visual Design Director owns aesthetic direction within those constraints.
- If a risk role blocks implementation, Delivery Manager records the gate and the user/human owner must approve resolution.
- If no role clearly owns a decision, Team Architect assigns owner before planning continues.
