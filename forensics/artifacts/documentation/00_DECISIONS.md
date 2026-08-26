# 4.0 Architecture Decisions

## D-001. Продуктовое имя версии

Рабочее название: **Codex Product Operating System 4.0**.

Причина: система уже управляет runtime, знаниями, экспертизой, разрешениями, делегированием и проверками, а не только симулирует продуктовую команду.

## D-002. Override вне контракта

`AGENTS.override.md` является внешним пользовательским механизмом полного переопределения.

4.0:
- не запрещает override;
- не требует от него импортировать kernel;
- не проверяет сохранение framework behavior;
- не проектирует fallback при произвольном override;
- документирует, что при override штатные гарантии могут не действовать.

## D-003. Универсальный core без проектных имён

В core, templates, evals и документации запрещены названия конкретных продуктов, организаций и дизайн-систем. Примеры должны использовать нейтральные fixture-названия или синтетические данные.

## D-004. Self-contained by default

Полный базовый workflow работает локально без Chroma, Langfuse, Postgres, Linear, Jira, Figma, облачного хранилища или отдельного orchestrator.

Допустимые локальные зависимости:
- Git;
- стандартная файловая система;
- локальный structured registry;
- JSON Schema validator;
- локальный eval runner;
- локальные hooks/rules;
- Codex plugin runtime.

## D-005. Три плоскости состояния

1. **Human-readable canonical knowledge:** Markdown + typed frontmatter.
2. **Exact runtime registry:** локальная SQLite-база или эквивалентный встроенный adapter.
3. **Optional semantic recall:** Chroma/pgvector/другой vector adapter.

Vector store не является единственным источником истины.

## D-006. Tiny kernel

Root `AGENTS.md` остаётся только стабильным загрузчиком и набором инвариантов. Task-specific процессы живут в skills, plugin packs, config и schemas.

Целевой размер — ориентировочно 4–6 KB. Это рекомендация, не hard cap.

## D-007. Полная библиотека ролей сохраняется

Все 50 логических ролей 3.0 сохраняются до отдельного ownership-аудита. Новые роли не добавляются, пока ответственность не доказана как:
- долгоживущая;
- повторяемая;
- не покрытая существующими ролями;
- требующая отдельного decision owner.

Процедурные обязанности оформляются skills, protocols, gates или hooks, а не новыми ролями.

## D-008. Logical roles не равны workers

50 role lenses не превращаются в 50 executable agents.

Целевой worker pack: 8–12 архетипов, например:
- explorer;
- implementer;
- product mapper;
- design reviewer;
- code reviewer;
- QA/test worker;
- security/risk reviewer;
- researcher;
- knowledge curator;
- incident investigator.

Worker получает нужную role lens в bounded contract.

## D-009. Skills сначала консолидируются

95 skills проходят инвентаризацию:
- core;
- domain pack;
- explicit-only;
- alias/merge;
- deprecated;
- rewrite required.

До завершения инвентаризации новые skills не добавляются.

## D-010. Soft artifact budgets

Целевые размеры документов являются guidance ranges. Они не могут использоваться как причина удалить важное знание.

Если артефакт становится слишком большим:
1. сохраняется корректность;
2. выявляется смешение уровней абстракции;
3. детали переносятся в дочерний артефакт;
4. родитель получает ссылку и краткое резюме;
5. новый тип артефакта создаётся только при доказанной необходимости.

## D-011. `TKT-000` опционален

`TKT-000` можно хранить как system/intake record, но он не обязан быть `Current=yes`.

Пустое штатное состояние:

```yaml
runtime_status: ready
current_task: null
```

## D-012. Approval через scoped lease

Пользователь одобряет ограниченный пакет операций для конкретной задачи, а не каждую команду отдельно.

Lease включает:
- read scope;
- write scope;
- verification scope;
- delegation budget;
- forbidden operations;
- expiration conditions.

## D-013. Micro Change Protocol

Очевидные, локальные, обратимые и низкорисковые изменения могут выполняться без полного ticket/Impact Map ceremony.

## D-014. External integrations через adapters/MCP

Внешние сервисы подключаются через typed adapters или MCP. Любая интеграция обязана иметь локальный fallback и не владеть единственной canonical copy.

## D-015. Реальные evals обязательны

Markdown simulations больше не считаются доказательством поведения. 4.0 должен иметь fixture repos, prompts, expected traces, forbidden actions и автоматические graders.
