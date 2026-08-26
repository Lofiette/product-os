# Codex Product Operating System 4.0 Beta 1

## Финальный offline-аудит дистрибутива

**Версия:** `4.0.0-beta.1`  
**Статус:** `BETA_READY`  
**Область сертификации:** детерминированная offline-проверка  
**Дата финальной сборки:** 2026-07-12  

## Итоговый вердикт

Codex Product Operating System 4.0 Beta 1 прошёл полный offline-контракт релиза: проверку архитектурных слоёв, установку и удаление, миграцию с 2.x/3.x, сохранность runtime-state, Product Knowledge, enforcement, worker orchestration, исполняемые evals, baseline regression, mutation testing, integrity manifest и повторный полный тестовый цикл уже из распакованного ZIP.

Сборка пригодна для контролируемого Beta-тестирования. Она **не объявляется Release Candidate**, потому что RC требует живых испытаний с установленным Codex: реальных модельных ответов, native worker threads, compaction/reconnect в клиентах, token/latency/cost measurements и нативной платформенной матрицы.

## Финальный архив

```text
Файл:
  codex-product-os-4.0-beta1-offline-v1.0.zip

Размер:
  753 336 байт

SHA-256:
  373973cfd16d1614b7a1417a8756dc7c4f9f60c42d03f32659a99c02b5dd7697

Файлов в ZIP:
  529

Управляемых файлов по MANIFEST.json:
  528
```

Проверки архива:

```text
CRC:             PASS
Inventory:       PASS
SHA-256 payload: PASS
Manifest:        PASS
Cache/bytecode:  отсутствуют
```

## Что входит в Beta 1

### Runtime Plane

- компактный kernel;
- типизированное runtime-состояние;
- Micro Change и Standard Task lifecycle;
- scoped authorization leases;
- checkpoints и recovery;
- безопасное пустое состояние без обязательного активного тикета;
- local ignored и team-shared режимы.

### Distribution Plane

- installer, updater, doctor и uninstaller;
- plugin-oriented поставка core и domain packs;
- безопасное сохранение mutable runtime-state;
- защита существующего `AGENTS.md`;
- локальная установка без загрязнения Git;
- migration assistant и rollback.

### Expertise Plane

- 45 canonical skills;
- 95/95 legacy skill mappings;
- 50 logical roles;
- 25 quality gates;
- 14 task routing profiles;
- task-specific staged loading;
- роли отделены от исполняемых workers.

### Product Knowledge Plane

- Product Map;
- Area Map;
- Flow Map;
- Decision Record;
- API/Data Contract;
- Context Packet;
- claim lifecycle;
- evidence provenance;
- freshness dependencies;
- existing, greenfield и redesign/migration modes;
- task-driven knowledge update accounting;
- sanitization и sharing policy.

### Deterministic Enforcement Plane

- режимы `off`, `audit`, `enforce`;
- 9 lifecycle hooks;
- проверка lease scope;
- защита от destructive Git и опасных filesystem-команд;
- PreCompact/PostCompact checkpoint checks;
- Product Knowledge stale propagation;
- локальный redacted audit log;
- safe fallback без hooks.

### Execution Plane

- 10 worker archetypes;
- bounded worker contracts;
- required/optional workers;
- `all_required`, `all`, `n_of_m` quorum;
- timeout, cancellation record и reconciliation;
- structured worker results;
- worktree isolation для параллельной записи;
- review-only integration plan;
- compaction-safe persisted orchestration state.

### Evaluation Plane

- 21 executable offline-cases;
- 6 fixture repositories;
- 4 evaluation suites;
- deterministic reference backend;
- live `codex exec --json` runner contract;
- external grading path;
- trace, output, filesystem, runtime и budget graders;
- baseline comparison;
- mutation testing;
- Release Plane с 33 trial tracks и 9 gates.

## Доказательная база

### Поведенческий контракт

```text
Distribution:       18 / 18
Skills:              5 / 5
Roles:               4 / 4
Product Knowledge:  13 / 13
Enforcement:         21 / 21
Orchestration:       24 / 24
Evaluation Plane:   13 / 13
Release Plane:      10 / 10
Migration:           7 / 7
--------------------------------
Полный контракт:   115 behavioral cases
```

Финальная строка полного прогона:

```text
BETA 1 COMPLETE TEST SUITE PASSED: 115 behavioral cases
```

### Исполняемые offline-evals

```text
Cases:                       21 / 21 PASS
Средний deterministic score: 100
Baseline regressions:         0
Known-bad mutations:          4 / 4 detected
```

Mutation testing доказал обнаружение:

- неразрешённой записи;
- отсутствующего обязательного поля результата;
- destructive Git-команды;
- ресурсной регрессии.

### Экспертные proxy-evals

```text
Skill trigger proxy:       135 / 135
Role routing proxy:        164 / 164
Knowledge lifecycle:        11 / 11
Enforcement policy:          5 / 5
Orchestration policy:        34 / 34
Enforcement integration:    13 / 13
Orchestration integration:  16 / 16
```

### Статические validators

```text
Distribution assets:       PASS
Release assets:            PASS
Evaluation assets:         PASS
Skills and migration:      PASS
Roles/gates/routing:       PASS
Knowledge schemas/runtime: PASS
Enforcement assets:        PASS
Orchestration assets:      PASS
Migration assets:          PASS
Python syntax:             PASS
JavaScript syntax:         PASS
Universality scan:         PASS
Package hygiene:           PASS
```

## Проверка распакованного ZIP

Финальная сборка была распакована в чистую директорию. Уже из распакованной копии выполнены:

- все package validators;
- local-mode installation;
- `doctor`;
- runtime validation;
- проверка чистоты Git;
- полный `offline-core`, 21/21;
- baseline comparison с 0 regressions;
- mutation testing 4/4;
- полный `tests/run_all.py`, 115 behavioral cases.

SHA-256 полного extracted-suite log:

```text
f337434c3356035a49b1950fd97b0bd1f0ded5ba6a8c653228a05f65a2b437d0
```

## Release gates

Offline Beta gates:

```text
Package integrity:          PASS
Offline regression:         PASS
Migration safety:           PASS
Install/update/rollback:    PASS
Universality:               PASS
Documentation:              PASS
```

RC-only gates пока остаются `PENDING`:

```text
Native platform matrix
Live model trials
Independent RC mega-audit
```

## Важные архитектурные решения

- Core полностью самодостаточен и не требует внешних сервисов.
- Chroma, Postgres, Langfuse, OpenTelemetry и другие сервисы остаются опциональными adapters.
- Каноническое Product Knowledge не хранится только во внешнем vector store.
- `AGENTS.override.md` находится вне контракта поведения CPT и остаётся пользовательским механизмом полного переопределения.
- Универсальные assets не содержат названий конкретных продуктов, проектов или дизайн-систем.
- Размеры knowledge-артефактов являются мягкими ориентирами, а не правилами обрезания контента.
- 50 логических ролей не превращаются в 50 default workers.
- Реальные workers опциональны и требуют ограниченных контрактов.
- Enforcement не выдаётся за замену sandbox, permissions и native approval policy Codex.
- Offline reference backend не выдаётся за сертификацию качества живой модели.

## Честные ограничения Beta 1

Не сертифицированы в рамках текущей сборки:

1. Реальное качество решений живой модели Codex.
2. Native spawn, cancellation delivery и event ordering реальных worker threads.
3. Compaction и reconnect в разных клиентах Codex.
4. Фактические token, latency и monetary-cost budgets.
5. Screenshot-based visual-fidelity grading.
6. Нативные прогоны Linux, macOS, Windows и WSL в целевой CI/клиентской среде.
7. Поведение под organization-managed policies и различными plugin trust settings.
8. Независимый финальный mega-audit перед RC.

## Рекомендованный следующий этап

Beta 1 следует устанавливать сначала в отдельный тестовый проект или копию продукта и использовать в режиме:

```text
enforcement: off или audit
workers: optional
external services: disabled
```

Далее нужны живые RC Trials:

- Micro Change;
- systemic UI change;
- existing-product onboarding;
- greenfield product;
- redesign/migration;
- API-dependent UI;
- governed design-system work;
- security-sensitive task;
- реальные workers и worktrees;
- timeout/cancellation;
- compaction/reconnect;
- platform matrix;
- token/latency/tool/approval scorecards.

## Заключение

Beta 1 завершает offline-архитектурный цикл Codex Product Operating System 4.0. Все основные плоскости системы работают совместно и прошли повторный полный тест уже из готового ZIP. Текущий статус корректно обозначен как `BETA_READY`, а не как RC: внутренняя и дистрибутивная целостность доказана, но качество живого агентного поведения ещё должно быть подтверждено на реальных задачах и клиентах Codex.
