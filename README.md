# Codex Product Team ULTIMATE — Final Fantasy Codenames

Это максимальная версия адаптивной продуктовой команды для Codex. Роли получили кодовые имена в честь персонажей Final Fantasy, чтобы ими было проще управлять. Имена являются только мнемоникой. Рабочее поведение задаётся ролью, playbook и skills.

## Как стартовать

1. Распакуй архив.
2. Открой папку в Codex.
3. Отправь содержимое `FIRST_PROMPT.md`.
4. Ответь на вопросы Intake A.
5. Проверь, как Team Architect выбрал роли.
6. Попроси план.
7. Дай approval только после того, как план и состав команды тебе подходят.

## Главная идея

Команда не должна всегда запускать все роли. Она должна адаптироваться под задачу:

- маленькая правка: fast lane, 1–3 роли;
- обычная фича: standard, 4–7 ролей;
- сложная продуктовая задача: complex, 8–12 ролей;
- security/privacy/release/AI-heavy: high-risk, 10–15 ролей;
- больше 15 ролей только по явному разрешению.

## Что нового в ULTIMATE

- Staged loading вместо чтения всего архива на старте.
- Глубокие playbooks с методологиями, зонами компетентности и handoff-правилами.
- `FAST_LANE.md` для маленьких задач.
- `OWNERSHIP_MATRIX.md` для устранения конфликтов ответственности.
- `EVIDENCE_POLICY.md` для research, UX, CX, market и AI-задач.
- AI/ML роли: AI/ML Systems Architect, Model Evaluation Specialist, AI Safety Reviewer.
- Delivery Manager для длинных задач.
- Усиленный Consistency Auditor.
- Scenario tests для проверки маршрутизации.
- Self-audit script для структурной проверки архива.


## Language policy

By default, the team answers the user in Russian, keeps durable control artifacts in compact English, and writes product UI copy in the product language defined in `TASK.md`. See `docs/LANGUAGE_POLICY.md`.


## ULTIMATE additions

- `docs/COMPLEXITY_MODEL.md` — minimum sufficient ceremony and role budgets.
- `docs/ROLE_OUTPUT_SCHEMAS.md` — strict schemas for role artifacts.
- `docs/EXTERNAL_EVIDENCE_PROTOCOL.md` — what to do when external facts are needed but unavailable.
- `docs/FINAL_FANTASY_CODENAME_POLICY.md` — codenames are labels only, not roleplay.
- `docs/SCENARIO_TESTS.json` — machine-readable routing scenarios.


## ULTIMATE release

See `docs/ULTIMATE_RELEASE_NOTES.md` for final hardening changes. Start with `FIRST_PROMPT.md`.


## v1.4 Pro patch

This package includes lean bootstrap loading, role cards, context-budget tracking, codename integrity checks, and an opportunity/creative-improvement overlay. Start with `FIRST_PROMPT.md`; the system should not load full role playbooks until after intake and routing.
