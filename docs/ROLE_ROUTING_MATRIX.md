# ROLE_ROUTING_MATRIX.md

Use this matrix after Intake A/B and before loading full playbooks. Start with role cards, then activate only roles that own an artifact.

## Contributor classes

- **Active specialist role**: counts against role budget and owns an artifact.
- **System service**: compact intake, routing, chronicle, consistency, or review work; does not count unless it produces a full artifact.
- **Consulted role card**: does not count unless the role becomes active.

## Always consider as services

- Yuna / Task Intake Orchestrator for new tasks.
- Aerith / Chronicle Keeper as compact service for file/decision changes; active role for long, high-risk, or multi-step work.
- Squall / Consistency Auditor as Consistency Lite for Standard work; active role for Complex/High-risk.
- Agrias / Code Reviewer only as active role for Review Level 2+.

## By work mode

| Work mode | Lead roles | Support roles | Notes |
|---|---|---|---|
| Research | Balthier, Tifa, Noctis depending on evidence type | Cloud, Ramza, Garnet, Prompto | Separate evidence from hypotheses. |
| Strategy | Cloud | Balthier, Ramza, Noctis, Setzer | No implementation by default. |
| Prototype | Rinoa, Terra, Garnet | Lightning, Zidane, Vivi | Optimize for learning and communication. |
| PoC | Auron | Zidane, Basch, Shantotto, Rikku | Prove feasibility, not product polish. |
| MVP | Cloud | Rinoa, Garnet, Lightning, Zidane, Basch, Rikku | Small MVP: Product Strategist owns scope discipline. Ashe required only for multi-phase/cross-area/deadline-heavy MVP. |
| Production change | relevant owner or Ashe if sequencing matters | relevant architect, Rikku, Agrias by review level | Respect risk gates. |
| Bugfix | Rikku | relevant architect, Agrias by review level | Reproduce, isolate, fix, verify. |
| Refactor | Locke | relevant architect, Rikku, Agrias | Preserve behavior. |
| Review/audit | Agrias or Squall | relevant specialists | Read-only until implementation is explicitly approved. |
| Incident | Cecil | Barret, Vincent, Ashe | Timeline and mitigation first. |
| AI/ML feature | Shantotto | Celes, Rydia, Vincent, Serah, Rikku | Evals and guardrails required. |
| Opportunity event / improvement loop | Cloud or relevant owner | Cid, Squall, Rinoa, Garnet, Setzer, Tifa/Noctis/Balthier when evidence is needed | Use one creative method only when it can improve a decision. |

## By platform / surface

| Surface | Typical active roles | Notes |
|---|---|---|
| Web UI | Rinoa, Garnet, Lightning, Zidane, Rikku | Add Vivi for accessibility-sensitive flows. |
| Mobile app | Yuffie, Rinoa, Garnet, Vivi, Sabin, Rikku | Include release constraints and device matrix. |
| API/service | Basch, Kimahri, Rikku | Add Vincent/Serah for sensitive data or auth. |
| Data product | Lulu, Penelo, Serah, Rikku | Add Balthier/Cloud if product metrics drive scope. |
| Design-system component | Lightning, Vivi, Zidane, Rikku | Add Garnet for content-heavy components. |
| AI summarization | Shantotto, Celes, Rydia, Serah, Garnet, Rikku | Add Vincent if data exposure or adversarial use exists. |
| AI tool-using agent | Shantotto, Celes, Rydia, Vincent, Serah, Basch, Rikku, Squall | Tool permission matrix required. |
| CLI / developer tooling | Auron, relevant architect, Rikku, Mog | Add Edge for dependencies. |
| Existing repository change | Repo Recon skill, then relevant roles | Run repo recon before deep planning or edits. |

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
| User-facing copy | Garnet, Rinoa; Faris when localization or multi-language is relevant |
| Design system/component | Lightning, Zidane, Vivi |
| Accessibility-sensitive UI | Vivi, Rinoa, Rikku |
| Experimentation/A-B testing | Setzer, Penelo, Cloud, Rikku |
| Support-ticket/customer complaint analysis | Prompto, Noctis, Cloud, Garnet |
| Localization/i18n | Faris, Garnet, Zidane, Rikku |
| Creative/opportunity signal | Cloud or relevant owner, Cid when routing changes, Squall when conflicts appear |

## Role budget by mode

- Tiny/Fast Lane: do not exceed 3 active roles without user approval.
- Standard feature/fix/review: target 4–7 active roles.
- Complex product/tech work: target 8–12 active roles.
- High-risk work: 10–15 active roles are allowed when risk triggers justify them.
- 16+ active roles requires explicit user approval and a Delivery Manager plan.

## Review mode guardrail

Review/audit mode is read-only by default. Reviewers may recommend changes, but must not edit files until the user explicitly approves implementation.
