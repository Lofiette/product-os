# ROLE_ROUTING_MATRIX.md

## Always consider
- Yuna / Task Intake Orchestrator for new tasks.
- Aerith / Chronicle Keeper for long tasks or file changes.
- Squall / Consistency Auditor for complex/high-risk planning.

## By work mode

| Work mode | Lead roles | Support roles | Notes |
|---|---|---|---|
| Research | Balthier, Tifa, Noctis | Cloud, Ramza, Garnet, Prompto | Separate evidence from hypotheses. |
| Strategy | Cloud | Balthier, Ramza, Noctis, Setzer | No implementation by default. |
| Prototype | Rinoa, Terra, Garnet | Lightning, Zidane, Vivi | Optimize for learning and communication. |
| PoC | Auron | Zidane, Basch, Shantotto, Rikku | Prove feasibility, not product polish. |
| MVP | Cloud, Ashe | Rinoa, Zidane, Basch, Rikku | Smallest end-to-end slice. |
| Production change | Ashe | relevant architect, Rikku, Agrias | Respect risk gates. |
| Bugfix | Rikku | relevant architect, Agrias | Reproduce, isolate, fix, verify. |
| Refactor | Locke | relevant architect, Rikku, Agrias | Preserve behavior. |
| Review/audit | Agrias or Squall | relevant specialists | Do not edit unless asked. |
| Incident | Cecil | Barret, Vincent, Ashe | Timeline and mitigation first. |
| AI/ML feature | Shantotto | Celes, Rydia, Vincent, Serah, Rikku | Evals and guardrails required. |

## Risk triggers

| Trigger | Required roles |
|---|---|
| Auth/permissions/secrets | Vincent, Basch, Rikku |
| PII/sensitive data/consent/retention | Serah, Vincent, Lulu |
| API contract/public integration | Kimahri, Basch, Rikku |
| Data model/migration | Lulu, Freya, Basch, Rikku |
| Performance-sensitive | Sabin, relevant architect, Barret |
| New dependency | Edge, Vincent, Sabin |
| Release/deployment | Cidolfus, Ashe, Barret |
| AI agent/tool use | Shantotto, Celes, Rydia, Vincent, Serah |
| User-facing copy | Garnet, Rinoa, Faris when localization or multi-language is relevant |
| Design system/component | Lightning, Zidane, Vivi |
| Accessibility-sensitive UI | Vivi, Rinoa, Rikku |
| Experimentation/A-B testing | Setzer, Penelo, Cloud, Rikku |
| Support-ticket/customer complaint analysis | Prompto, Noctis, Cloud, Garnet |
| Localization/i18n | Faris, Garnet, Zidane, Rikku |
