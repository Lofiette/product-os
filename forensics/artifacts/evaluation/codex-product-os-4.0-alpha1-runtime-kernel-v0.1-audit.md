# Codex Product Operating System 4.0 Alpha 1 — Runtime Kernel Audit

Дата проверки: 2026-07-10  
Версия: `4.0.0-alpha.1`

## Вердикт

**PASS для Phase 1 / Alpha 1 с явно зафиксированными ограничениями.**

Пакет реализует исполняемый Runtime Kernel и соответствует критериям Alpha 1, но ещё не является готовой полной средой 4.0.

## Реализовано

- tiny root `AGENTS.md`;
- machine-readable runtime state на YAML;
- штатное состояние `current_task: null`;
- опциональный, но не активный по умолчанию `TKT-000`;
- Standard Task lifecycle;
- Micro Change Protocol без обязательного полного тикета;
- escalation из Micro Change в Standard Task intake;
- scoped authorization lease;
- compact generated `runtime-summary.md`;
- file-only storage adapter;
- checkpoint с integrity digest;
- mismatch detection;
- explicit recovery с pre-recovery backup;
- JSON Schema validation;
- cross-file invariants;
- synthetic compaction-recovery test;
- negative tests для битых current pointers и tampered checkpoint.

## Метрики kernel

| Метрика | Значение |
|---|---:|
| `AGENTS.md` | 4 609 bytes / 105 строк |
| Runtime YAML files | 3 |
| JSON Schemas | 7 |
| Protocol docs | 10 |
| Runtime CLI | 1 |
| Behavioral unit tests | 8 |
| External network services | 0 |
| Active task at startup | none |

Целевой размер root loader соблюдён как guidance, не как hard cap.

## Проверки

### Static/runtime validation

```text
RUNTIME VALIDATION PASSED
KERNEL CHECK PASSED: AGENTS.md=4609 bytes; templates=5
```

### Behavioral tests

Пройдены:

1. no-active-task state;
2. Standard Task lifecycle;
3. Micro Change without full ticket;
4. Micro Change escalation;
5. checkpoint mismatch detection and recovery;
6. tampered checkpoint rejection;
7. invalid current task rejection;
8. optional TKT-000 semantics.

### Synthetic compaction recovery

```text
SYNTHETIC COMPACTION RECOVERY PASSED
```

Сценарий:

1. создан активный task;
2. создан scoped lease;
3. сохранён checkpoint;
4. current/task state намеренно повреждены;
5. mismatch обнаружен;
6. state восстановлен;
7. повторная verification показывает `CHECKPOINT MATCH`;
8. runtime validation проходит.

### Schema/template validation

Проверены:

- task template;
- authorization lease template;
- checkpoint template;
- micro change template;
- optional TKT-000 example.

### Универсальность

В package не обнаружены названия конкретных продуктов, организаций или дизайн-систем из приватных кейсов. Runtime использует только нейтральные абстракции.

## Alpha 1 acceptance criteria

| Критерий | Статус | Evidence |
|---|---|---|
| Root `AGENTS.md` является небольшим loader | PASS | 4 609 bytes; kernel check |
| Machine-readable runtime state | PASS | `.cpt/*.yaml` + schemas |
| `current_task: null` поддерживается | PASS | initial state + unit test |
| `TKT-000` опционален | PASS | example only + unit test |
| Micro Change Protocol работает | PASS | lifecycle + escalation tests |
| Authorization lease schema валидируется | PASS | schema, CLI, lifecycle test |
| Runtime checkpoint восстанавливается | PASS | synthetic recovery + negative test |
| Core не зависит от внешних сервисов | PASS | file-only local execution |

## Критические границы честности

- Lease является declarative runtime record, а не security boundary.
- Нативные Codex permissions, sandbox, rules и approval prompts остаются обязательными.
- Hooks ещё не установлены и не enforcement-ят checkpoint автоматически.
- Recovery test синтетический; реальный `PreCompact/PostCompact` trace относится к Phase 6.
- YAML state пока является exact registry; SQLite появится позднее.
- Runtime validation не доказывает продуктовую или инженерную корректность результата.

## Риски следующей фазы

1. Не раздувать root `AGENTS.md` при добавлении plugin distribution.
2. Не дублировать YAML и будущий SQLite без single write path.
3. Не превращать lease в ложное обещание технической изоляции до hooks/rules.
4. Сохранить Micro Change как реальный быстрый путь.
5. Проверить Linux/WSL, macOS и Windows behavior отдельно.

## Рекомендация

Зафиксировать этот package как **Alpha 1 Runtime Kernel baseline** и переходить к Phase 2: distribution split, plugin scaffold и installer/uninstaller, не добавляя Product Knowledge или экспертные packs в always-on runtime.
