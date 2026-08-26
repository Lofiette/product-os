# Codex Product Team 3.0 Ultra beta 2  
## Мегаревизия архитектуры и план версии 4.0

Дата ревизии: 2026-07-10  
Объект: `codex-product-team-3.0-ultra-beta2.zip`  
Режим работы: анализ без генерации новой сборки

---

## 1. Резюме для принятия решения

### Итоговый вердикт

**3.0 Ultra beta 2 — сильный исследовательский прототип и полезная рабочая среда, но ещё не производственная платформа для широкого распространения.**

Главное достижение 3.0 — правильная смена парадигмы:

- 2.x был преимущественно экспертным фреймворком;
- 3.0 добавил Runtime Kernel и Product Knowledge;
- среда научилась начинать задачу с карты продукта, ограниченного discovery и Impact Map;
- память была разделена на активное состояние, тикеты, compact summary и долгоживущие знания;
- дизайн, frontend, API/data и orchestration начали маршрутизироваться осознанно.

Однако текущая реализация остаётся неравномерной:

- **концептуальная архитектура глубже, чем её исполнимый runtime**;
- **структурные валидаторы сильнее, чем поведенческие проверки**;
- **количество ролей и skills намного больше фактической методологической глубины большинства документов**;
- **always-on kernel всё ещё слишком тяжёлый**;
- **распространение через копирование 477 файлов в проект — неоптимально**;
- **важные правила существуют в prose, но почти не подкреплены hooks, rules, config profiles и исполнимыми evals**.

### Общая оценка зрелости

| Направление | Оценка | Комментарий |
|---|---:|---|
| Концептуальная архитектура | 8.5/10 | Runtime Kernel + Product Knowledge + Expert Framework — сильная модель |
| Управление контекстом | 6.0/10 | Хорошая философия, но тяжёлый AGENTS, крупные индексы и 95 skill metadata |
| Product Knowledge | 8.0/10 | Лучший слой системы, но не хватает схем, freshness automation и claim-level provenance |
| Роли | 5.5/10 | Полный охват, но многие role cards и playbooks слишком шаблонны |
| Skills | 4.5/10 | 95 skills, из них 44 фактически являются одинаковыми заготовками |
| Оркестрация | 6.0/10 | Есть contracts/fallbacks, но слишком много spawnable agents и слабая runtime enforcement |
| Quality gates | 6.5/10 | UI/DS слой глубокий; остальные домены заметно слабее |
| Автоматизация и enforcement | 3.5/10 | Почти всё держится на инструкциях, а не hooks/rules/config |
| Симуляции и evals | 3.0/10 | Валидаторы структурные; simulations не являются реальными тестами |
| Установка и дистрибуция | 3.0/10 | «Скопировать kit в проект» — неустойчивый способ распространения |
| Поддерживаемость | 5.0/10 | Много зеркал, индексов, матриц и ручных связей |
| Совместимость с актуальным Codex | 5.5/10 | Используется базовая модель AGENTS/skills/subagents, но почти не используются plugins, hooks, permissions, goals, memories и современные config controls |

**Интегральная оценка: около 6.1/10.**  
Это не оценка качества идеи. Идея значительно сильнее. Это оценка текущей исполнимости, глубины документов и стоимости сопровождения.

---

## 2. Что было проверено

Архив распакован и проанализирован как связанная runtime-система.

### Фактический состав

- 477 файлов;
- 129 директорий;
- 50 role cards;
- 50 playbooks;
- 50 custom agent TOML;
- 95 skills;
- 34 scenario markdown;
- 404 Markdown-документа;
- 10 simulation cases;
- 2 audit checklists;
- scripts для routing, memory, DS и structural validation.

### Встроенные проверки

Все встроенные проверки проходят:

```text
VALIDATION PASSED: 50 roles, 95 skills, 34 scenarios.
3.0 VALIDATION PASSED: 50 roles, 95 skills, 34 scenarios.
ROUTING TEST PASSED: 34 scenarios, 50 roles, 95 skills.
MEMORY INTEGRITY PASSED.
```

Это доказывает **структурную целостность**, но не доказывает:

- что Codex реально выберет нужный skill;
- что после compaction сохранится активная цель;
- что approval flow не станет чрезмерно дорогим;
- что роли дадут экспертно глубокий результат;
- что subagents не зависнут;
- что Product Knowledge останется свежим;
- что сценарий будет выполнен поведенчески, а не только формально.

### Дополнительный артефакт

К отчёту приложен `document-depth-inventory.csv`, содержащий строку для каждого из 404 Markdown-файлов:

- путь;
- категория;
- объём;
- предварительная оценка глубины;
- флаги риска;
- рекомендуемое действие.

Это не заменяет ручной экспертный аудит, но даёт полный индекс ревизии.

---

## 3. Как среда работает сейчас: реконструкция полного цикла

### 3.1. Startup

Codex должен загрузить:

1. `AGENTS.md`;
2. `CURRENT.md`;
3. `TASK_INDEX.md`;
4. `CHRONICLE.md`;
5. `docs/BOOTSTRAP_INDEX.md`;
6. `docs/LANGUAGE_POLICY.md`.

Затем он должен:

- определить active ticket;
- выбрать complexity tier;
- найти Product Knowledge;
- загрузить role/skill indexes по необходимости;
- выбрать roles, skills, playbooks и gates;
- предложить bounded discovery;
- сформировать Impact Map;
- запросить approval;
- выполнить работу;
- обновить knowledge и runtime memory;
- сжать Chronicle.

### 3.2. Новый task

`New Task Protocol` требует:

- не начинать редактирование сразу;
- предложить/создать ticket;
- прочитать `PRODUCT_MAP` и `KNOWLEDGE_INDEX`;
- выбрать area maps;
- выбрать минимальный expert set;
- выполнить bounded discovery;
- подготовить Impact Map;
- получить approval;
- реализовать и проверить;
- обновить затронутое знание.

### 3.3. Product Knowledge

Среда использует иерархию:

- `PRODUCT_MAP`;
- `KNOWLEDGE_INDEX`;
- area maps;
- flow maps;
- decision records;
- context packets.

Есть три режима:

- existing product;
- greenfield;
- redesign/migration.

### 3.4. Expert Framework

Среда хранит:

- 50 roles;
- 95 skills;
- 50 playbooks;
- quality gates;
- 50 custom agents.

Role может быть:

- simulated;
- consulted;
- spawned as real subagent.

### 3.5. Completion

Definition of Done требует:

- выполнить requested behavior;
- уважить Impact Map/approval;
- пройти domain gates;
- выполнить verification;
- обновить affected Product Knowledge;
- обновить runtime memory;
- перечислить риски.

### Общий вывод по логике

Логика в целом правильная. Главная проблема не в последовательности, а в том, что она реализована **слишком большим количеством prose-документов и слабой автоматизацией**. В результате Codex должен сам интерпретировать десятки метаправил именно в тот момент, когда контекст и так дорог.

---

## 4. Критические архитектурные проблемы

## P0-1. `AGENTS.md` не является lightweight kernel

Факты:

- 308 строк;
- 14 982 байта;
- содержит не только стабильные правила, но и:
  - Product Knowledge modes;
  - New Task Protocol;
  - Bounded Discovery;
  - Framework Loading;
  - complexity tiers;
  - artifact-size policy;
  - role budget;
  - UI/DS policy;
  - subagent failure handling;
  - reference fidelity;
  - language policy;
  - Definition of Done.

Это полезные правила, но не все должны находиться в always-loaded instruction file.

### Почему это опасно

- Root instruction budget делится с global и nested AGENTS.
- Длинный kernel вытесняет task context.
- Любое изменение одного workflow требует редактировать критический startup document.
- Разные task types получают много нерелевантной политики.
- В случае override большая часть ядра может исчезнуть.

### Решение 4.0

Root `AGENTS.md` должен содержать только:

- идентичность runtime;
- canonical paths;
- стабильные safety invariants;
- task classification entrypoint;
- loader reference;
- minimal definition of done;
- правило «не грузить всё».

Целевой порядок размера — **ориентир 4–6 KB**, но не жёсткий cap.

Остальное:

- skills;
- protocol plugin;
- nested AGENTS;
- machine-readable routing registry;
- hooks/config.

---

## P0-2. `AGENTS.override.md` логически отключает root kernel

Текущий root `AGENTS.md` говорит: если есть local override, «следовать ему, сохраняя staged-loading policy».

Но Codex выбирает максимум один instruction file на directory level. Если в root есть `AGENTS.override.md`, root `AGENTS.md` не загружается. Следовательно, root kernel не может приказать override сохранять собственные правила.

Текущий template override — 17 строк и не воспроизводит:

- approval policy;
- Product Knowledge lifecycle;
- role/skill loading;
- UI/DS requirements;
- Definition of Done;
- failure recovery.

### Риск

Локальный override может незаметно превратить систему в урезанный safety shell без Expert Framework — именно это произошло в живом `ai-web` до ручного патчинга.

### Решение 4.0

Один из вариантов:

**Вариант A, рекомендуемый:**

- `AGENTS.md` остаётся маленьким canonical loader;
- local behavior хранится не в same-directory override, а в:
  - `.codex/runtime/config.yaml`;
  - project profile;
  - nested override ближе к конкретной области;
  - user-level plugin/config.

**Вариант B:**

- `AGENTS.override.md` содержит только ссылку на canonical `RUNTIME_KERNEL.md`;
- validator проверяет, что override импортирует kernel;
- runtime template генерируется installer-ом, а не копируется руками.

---

## P0-3. Неправильная единица распространения

README предлагает скопировать kit в проект.

Архив содержит 477 файлов. При таком подходе:

- framework загрязняет репозиторий;
- появляются сотни untracked/pending files;
- пользователь должен вручную управлять `.gitignore`/`.git/info/exclude`;
- Product Knowledge, runtime files и reusable expertise смешиваются;
- обновление версии превращается в сложный merge;
- skill metadata каждого проекта разрастается;
- универсальные файлы дублируются во всех репозиториях.

### Решение 4.0: split distribution

Разделить систему на:

1. **Repo Runtime Scaffold**
   - маленький `AGENTS.md`;
   - `.codex/runtime/`;
   - Product Knowledge;
   - project-specific config;
   - task memory.

2. **Core Plugin**
   - new-task;
   - bounded-discovery;
   - impact-map;
   - knowledge lifecycle;
   - core hooks.

3. **Domain Plugins**
   - product/research;
   - design/UI;
   - frontend;
   - backend/API/data;
   - risk/operations;
   - AI/agentic.

4. **Optional Worker Pack**
   - custom subagents.

5. **Installer / Migrator**
   - выбирает local ignored или team-shared mode;
   - пишет canonical paths;
   - проверяет Git;
   - ставит plugin packs;
   - создаёт config profile.

---

## P0-4. 95 skills превышают эффективный discovery surface

Суммарный размер name/description/path всех skills в архиве оценивается примерно в 23 KB. Tiny skill index — 14.1 KB, full skill index — 17.5 KB.

При этом 44 skills имеют почти одинаковую процедуру:

1. подтвердить необходимость;
2. загрузить relevant files;
3. разделить evidence/assumptions;
4. создать compact artifact;
5. сообщить blockers/handoffs.

### Риски

- skill metadata будет сокращаться или часть skills не попадёт в visible initial list;
- implicit matching станет непредсказуемым;
- похожие skills конкурируют;
- название skill обещает методологическую глубину, которой нет;
- индексы частично дублируют built-in skill discovery.

### Решение 4.0

- Разбить skills по installable domain packs.
- Оставить в Core 8–15 skills.
- Для дорогих/критичных skills:
  - explicit invocation preferred;
  - `agents/openai.yaml`;
  - implicit invocation disabled или ограничен;
  - dependencies declared.
- 44 boilerplate skills:
  - либо углубить;
  - либо заменить ссылкой на shared base protocol;
  - либо удалить alias.
- Использовать skill `references/`, `scripts/`, `assets/`.
- Ввести trigger evals.

---

## P0-5. Структурные тесты создают ложное чувство надёжности

Текущие simulations — 10 файлов по 14 строк с одинаковыми Expected bullets.

Они не:

- запускают Codex;
- не фиксируют tool trace;
- не проверяют forbidden reads;
- не проверяют edits-before-approval;
- не измеряют context cost;
- не проверяют skill selection;
- не воспроизводят compaction;
- не проверяют UI output;
- не оценивают subagent hang recovery.

Validators в основном проверяют:

- наличие файлов;
- наличие ID;
- наличие строк в routing matrix;
- совпадение scenario IDs.

### Найденный пример слабости валидатора

В `validate_3_0.py` regex для SOVA содержит literal backspace characters вместо корректного `\b`, поэтому project-specific term detector может фактически не работать.

### Решение 4.0

Нужен executable eval harness:

- fixture repositories;
- golden prompts;
- captured tool calls;
- policy assertions;
- artifact graders;
- token/output budget;
- pass/fail score;
- regression history.

---

## P0-6. Нет deterministic enforcement

Система имеет много правил, но почти не использует:

- hooks;
- command rules;
- permission profiles;
- config profiles;
- compact prompt;
- tool output limits;
- subagent max threads/depth/runtime;
- auto-review;
- memory controls.

`.codex/config.toml` содержит только project name.

### Следствие

Поведение зависит от того, насколько хорошо модель вспомнит prose-инструкции.

### Решение 4.0

Добавить opt-in profiles:

- `conservative`;
- `balanced`;
- `autonomous-worktree`.

Добавить hooks:

- `SessionStart`;
- `UserPromptSubmit`;
- `PreToolUse`;
- `PermissionRequest`;
- `PostToolUse`;
- `PreCompact`;
- `PostCompact`;
- `SubagentStart`;
- `SubagentStop`;
- `Stop`.

Добавить rules:

- forbid destructive Git;
- prompt on dependency install;
- allow known read-only commands;
- protect secrets;
- require justification for broad scans.

---

## 5. Противоречия и несогласованности

| Severity | Противоречие | Воздействие | Исправление |
|---|---|---|---|
| P0 | Override должен сохранить root policy, но root AGENTS не загружается | Framework может быть отключён | Canonical kernel loader / убрать same-level override |
| P0 | `true_subagent_workflow` говорит wait for all; failure policy говорит не ждать бесконечно | Зависание или неоднозначность | Timeout/quorum/cancel policy |
| P1 | Root runtime использует root paths, local overlay — `.codex-runtime`, kernel template — `product/...` | Path drift и потеря knowledge | Один canonical runtime root + modes |
| P1 | TKT-000 current placeholder, но Chronicle говорит no active user task | Формально корректно, но создаёт двусмысленность | Отдельное поле `active_user_task: none`; placeholder необязателен |
| P1 | Tiny/Micro освобождён от индексов, но New Task/Impact Map описаны как общий обязательный путь | Overhead на мелких задачах | Micro Change Protocol |
| P1 | 50 role lenses одновременно объявлены spawnable agent types | Слишком большой orchestration surface | Отделить role registry от worker archetypes |
| P1 | Product Designer handoff всё ещё часто ведёт к frontend_architect, не frontend_engineer | Implementation role интегрирован не полностью | Обновить role graph/ownership/handoffs |
| P1 | `OWNERSHIP_MATRIX` назначает frontend implementation architecture, но не implementation ownership | Неясен ответственный за код | Ввести Frontend Engineer ownership |
| P1 | `KNOWLEDGE_INDEX` проектируется как один файл | Рост и hot-spot | Partitioned evidence registry |
| P1 | `CHRONICLE` — кастомная память, но Codex теперь имеет отдельный продукт Chronicle | Терминологическая путаница | Переименовать в `RUNTIME_SUMMARY` |
| P2 | `FIRST_PROMPT` просит читать AGENTS, хотя он auto-loaded | Повторение и лишний prompt | Сделать Quick Start, не runtime dependency |
| P2 | `docs/RUNTIME_LOAD_POLICY.md` ссылается на отсутствующий `docs/SELF_AUDIT_REPORT.md` | Broken reference | Broken-reference validator |
| P2 | `SKILL_INDEX` / `SKILL_TINY_INDEX` имеют minor version drift | Maintenance noise | Единый generated registry |
| P2 | Product knowledge protocol copies — трёхстрочные stubs рядом с полными docs | Canonical source unclear | Удалить mirrors или генерировать их |

---

## 6. Runtime Kernel: подробная оценка документов

### `AGENTS.md`

**Оценка:** архитектурно сильный, operationally overloaded.

Что хорошо:

- ясная core model;
- правильное разделение role/skill/playbook/gate;
- хороший New Task Protocol;
- хороший Bounded Discovery;
- Product Knowledge modes;
- soft artifact size policy;
- прозрачность исполнения;
- сильный UI/reference/DS слой.

Что недостаточно:

- слишком много always-on правил;
- нет machine-readable loader;
- complexity/role budgets заданы эвристически;
- approval model не поддерживает scoped authorization;
- Definition of Done одинаково тяжёлый для разных task classes;
- нет current Codex features integration.

### `CURRENT.md`

**Оценка:** адекватный bootstrap template, но TKT-000 — лишняя сущность.

Нужно:

- typed state;
- active task vs placeholder отдельно;
- current goal/stopping condition;
- authorization lease;
- context budget state;
- last checkpoint;
- source commit/runtime version.

### `TASK_INDEX.md`

**Оценка:** полезный ledger, но Markdown-таблица плохо масштабируется.

4.0:

- `tasks/index.json` или YAML registry;
- human-readable generated Markdown view;
- task dependencies;
- stale/blocked state;
- goal link;
- current worktree/thread;
- checkpoint.

### `CHRONICLE.md`

**Оценка:** идея правильная, название и enforcement — слабые.

4.0:

- переименовать в `RUNTIME_SUMMARY.md`;
- чёткая схема:
  - objective;
  - completed;
  - decisions;
  - blockers;
  - next action;
  - artifact links;
- автоматический PreCompact snapshot;
- PostCompact recovery check.

### `TASK.md`

**Оценка:** compatibility shim допустим только на migration period.

4.0:

- убрать из новых installs;
- оставить migration symlink/pointer option;
- validator должен запрещать working state в TASK.md.

### `FIRST_PROMPT.md`

**Оценка:** полезен для onboarding человека, избыточен как runtime.

4.0:

- `QUICKSTART.md`;
- короткие launch prompts по modes;
- не дублировать startup list.

### `TEAM.md`

**Оценка:** полезный человеко-читаемый каталог, не runtime document.

4.0:

- генерировать из role registry;
- не грузить моделью целиком;
- сделать searchable docs / plugin UI.

---

## 7. Product Knowledge: подробная ревизия

### Сильные стороны

- иерархия вместо giant brief;
- existing/greenfield/redesign modes;
- confidence/freshness/evidence/unknowns/review_trigger;
- operational prewarm;
- contract-level API knowledge;
- task-driven deepening;
- Impact Map as bridge to implementation.

### Главные недоработки

#### 7.1. Templates являются skeleton, а не schema

Пример `PRODUCT_MAP.template.md` содержит только headings.

Не хватает:

- определения полей;
- allowed values;
- claim status;
- evidence depth;
- source revision;
- ownership;
- review lifecycle;
- examples good/bad;
- validation rules.

#### 7.2. Confidence слишком грубый

Один `confidence: medium` на весь artifact скрывает:

- route-level confirmed;
- component-level inferred;
- API-level unknown;
- user-approved decision.

4.0:

- artifact confidence;
- claim-level status:
  - planned;
  - hypothesized;
  - inferred;
  - confirmed;
  - validated;
  - stale;
  - deprecated.
- evidence depth:
  - user decision;
  - design artifact;
  - route;
  - component;
  - hook/store;
  - API/type;
  - test;
  - runtime observation.

#### 7.3. Freshness не автоматизирована

`review_trigger` — текст. Система не умеет:

- определить, какие maps затронуты diff-ом;
- выставить `needs-review`;
- проверить source revision;
- обновить evidence.

4.0:

- machine-readable path globs;
- source commit/hash;
- `knowledge-dependency-graph.json`;
- PostToolUse/Stop hook;
- freshness linter.

#### 7.4. `KNOWLEDGE_INDEX` станет bottleneck

При большом продукте один index:

- разрастается;
- часто меняется;
- сам требует много контекста;
- конфликтует в parallel work.

4.0:

- top-level compact index;
- `areas/<id>/index.yaml`;
- evidence registry partitioned by area;
- generated aggregate view.

#### 7.5. Нет privacy/secret policy

Product Knowledge не должен записывать:

- токены;
- секреты;
- реальные клиентские данные;
- sensitive payloads;
- raw user logs.

Нужен `KNOWLEDGE_SANITIZATION_POLICY`.

---

## 8. Роли: глубина и архитектурная состоятельность

### Что хорошо

- сохранён широкий capability coverage;
- роли имеют mission, outputs, triggers, skills, handoffs;
- role ≠ subagent формально закреплено;
- появился frontend_engineer.

### Что недостаточно

#### 8.1. Role cards тонкие

Медиана — 27 строк.

Для роли уровня «ультрапрофессионал» не хватает:

- decision rights;
- core mental models;
- methodology selection;
- evidence standards;
- anti-patterns;
- quality heuristics;
- edge cases;
- escalation;
- examples.

#### 8.2. Playbooks шаблонны

Медиана — 82 строки, но большая часть повторяется.

Метод роли обычно укладывается в один абзац.

Пример:

- Product Strategist упоминает JTBD, но не объясняет:
  - когда JTBD уместен;
  - как отличать outcome от solution;
  - как формировать metrics;
  - как работать с uncertainty.
- Security Reviewer не содержит:
  - STRIDE;
  - attack surface;
  - trust boundaries;
  - abuse cases;
  - OWASP mapping;
  - severity model.
- UX Researcher не содержит:
  - method selection matrix;
  - sampling;
  - bias controls;
  - validity;
  - synthesis methods.
- Frontend Engineer недостаточно раскрывает:
  - rendering boundaries;
  - state ownership;
  - async/error models;
  - accessibility;
  - performance;
  - server/client split;
  - testing pyramid.

#### 8.3. Методологическая библиотека почти пустая

`ROLE_METHOD_LIBRARY.md`:

- 21 строк;
- описывает 6 ролей;
- только линейные цепочки.

`ROLE_OUTPUT_SCHEMAS.md`:

- 17 строк;
- generic schema;
- несколько UI templates.

Это не соответствует обещанию 50 глубоких экспертиз.

#### 8.4. Metadata в index почти декоративна

- 46 из 50 roles имеют пустой `primary_task_types`;
- 44 имеют `load_cost=standard`;
- spawn policy почти одинаков;
- validator проверяет наличие ключа, не полезность значения.

### 4.0 model

Сохранить 50 role lenses, но добавить typed registry:

```yaml
id:
domain:
accountability:
decision_rights:
default_artifacts:
task_types:
activation_signals:
non_activation_signals:
evidence_requirements:
risk_triggers:
load_profile:
worker_eligibility:
preferred_worker_archetype:
compatible_skills:
required_gates:
```

---

## 9. Skills: глубина и достаточность

### Числа

- 95 skills;
- 44 generic placeholder skills;
- 0 `agents/openai.yaml`;
- initial metadata surface чрезмерно большой;
- tiny index почти столь же большой, как full.

### Сильные skills

Наиболее зрелые:

- `repo-recon`;
- `design-recon`;
- `screen-redesign`;
- `module-design`;
- `reference-fidelity`;
- `visual-qa-loop`;
- `bounded-discovery`;
- `product-knowledge-onboarding`;
- `current-page-ui-review`;
- `subagent-run-contract`.

У них есть конкретные steps, outputs и boundaries.

### Слабые skills

44 skills фактически имеют одну и ту же generic procedure.

Особенно опасно для:

- security;
- privacy;
- analytics;
- research;
- architecture;
- migration;
- AI safety;
- API review.

Название создаёт ожидание специализированного метода, но full instructions его не дают.

### Отдельные критичные недоработки

- `frontend-integration-review` — 17 строк и шесть bullets.
- `chronicle-compaction` — слишком короткий для recovery-critical workflow.
- `impact-map` хорош по структуре, но нет:
  - template reference;
  - examples;
  - task-size variants;
  - validation rules.
- alias skills (`security-review`) создают лишний metadata surface.

### 4.0 skill model

- Core skill pack: 8–15 skills.
- Domain packs.
- Каждый skill:
  - clear trigger;
  - non-trigger;
  - inputs;
  - steps;
  - output schema;
  - evidence;
  - stop conditions;
  - failure modes;
  - examples;
  - references;
  - scripts where deterministic.
- `agents/openai.yaml`.
- Skill trigger evals.
- Expensive skills explicit-only.

---

## 10. Playbooks и ownership

### Проблемы

- Handoff graph не полностью обновлён под `frontend_engineer`.
- `OWNERSHIP_MATRIX` говорит о frontend architecture, но не frontend implementation.
- Многие playbooks передают UI implementation в `frontend_architect`.
- Common output schema слишком общий.

### 4.0

Разделить:

- role card = accountability;
- method reference = expertise;
- playbook = task workflow;
- output schema = typed artifact;
- gate = acceptance;
- worker profile = execution.

Не повторять одинаковые sections в 50 playbooks вручную. Использовать inheritance/composition:

```yaml
extends:
  - common/evidence-review
  - common/approval-aware
method_pack:
  - product-strategy
```

Генерировать human-readable playbook из registry.

---

## 11. Subagents

### Что хорошо

- distinction role/agent/simulation;
- approval table;
- run contract;
- bounded packet;
- strict output;
- fallback hierarchy;
- UI review packet;
- duplicate-spawn ban.

### Что недостаточно

- `wait for all results` конфликтует с timeout/failure.
- нет явного cancel/close.
- нет configured:
  - max threads;
  - max depth;
  - runtime.
- 50 spawnable role agents — слишком большой выбор.
- нет worktree isolation для parallel writes.
- нет explicit policy: read-heavy delegation preferred, parallel writes exceptional.
- TOML не задают model/reasoning/sandbox/skills.

### 4.0

Разделить:

**Role lenses: 50.**

**Worker archetypes: 8–12:**

- explorer;
- implementer;
- product mapper;
- design reviewer;
- code reviewer;
- test/QA worker;
- security/risk reviewer;
- researcher;
- knowledge curator;
- incident investigator.

Role lens передаётся worker-у как task context.

Default:

- max depth 1;
- max threads 3–4;
- timeout;
- required/optional quorum;
- disjoint writes;
- worktree for parallel implementation;
- no wait-all without deadline.

---

## 12. Gates

### Сильная часть

UI/DS/reference fidelity слой действительно глубок:

- source authority;
- manifest freeze;
- screenshot comparison;
- content realism;
- debug controls;
- design-system modes;
- visual QA.

### Слабая часть

Другие domains представлены тонкими skills/policies:

- security;
- analytics;
- research;
- privacy;
- performance;
- architecture.

Также gates разбросаны:

- `QUALITY_GATES`;
- `UI_QUALITY_GATES`;
- `PRODUCTION_READINESS_GATES`;
- `SCREENSHOT_VISUAL_GATE`;
- `VISUAL_ACCEPTANCE_CRITERIA`;
- отдельные policies.

### 4.0 Gate Registry

Machine-readable:

```yaml
id:
trigger:
owner:
severity:
required_evidence:
check:
pass_condition:
warn_condition:
block_condition:
exception_policy:
applies_to:
```

Human docs генерируются из registry.

---

## 13. Approval model и пользовательская нагрузка

Текущая модель может привести к approval fatigue:

- read project files;
- edit;
- build/test/lint;
- broaden scope;
- subagent;
- external module.

Для живой работы нужен не approval на каждый шаг, а **scoped authorization lease**.

Пример:

```yaml
ticket: TKT-123
valid_until: implementation-complete
read_scope:
  - src/features/editor/**
write_scope:
  - src/features/editor/**
  - tests/editor/**
validation_scope:
  - npm test -- editor
  - npm run lint -- src/features/editor
delegation:
  max_workers: 1
  read_only: true
forbidden:
  - dependencies
  - migrations
  - external network
```

Lease можно расширить только с approval.

Это даёт safe autonomy без микроменеджмента.

---

## 14. Tiny/Micro workflow

Текущая система всё ещё может тратить слишком много ритуала на маленькую задачу.

4.0 нужен `Micro Change Protocol`.

Критерии:

- изменение очевидно;
- reversible;
- один bounded area;
- нет public API/data/security/DS risk;
- verification очевиден.

Flow:

1. краткий micro note;
2. targeted read;
3. edit;
4. smallest verification;
5. summary;
6. knowledge update только если durable structure изменилась.

Без:

- full ticket;
- full Impact Map;
- role matrix;
- Product Knowledge update по умолчанию.

---

## 15. Memory, compaction, goals, memories

### Текущая система

Хорошо:

- ticketed memory;
- snapshots;
- compact summary;
- knowledge maps.

Недостаточно:

- compaction recovery ручной;
- нет custom compact prompt;
- нет hooks;
- нет use of Goals;
- нет optional Memories policy;
- custom `CHRONICLE` конфликтует по имени с official Chronicle.

### 4.0

- `RUNTIME_SUMMARY.md`;
- `PreCompact` hook:
  - write checkpoint;
  - active ticket;
  - approvals;
  - subagent status;
  - unverified work.
- `PostCompact` hook:
  - load checkpoint;
  - compare active state;
  - block if mismatch.
- optional `/goal` integration for coherent long-running outcomes;
- local Memories only as non-authoritative recall;
- mandatory rules remain in repo/runtime;
- history/tool output limits in profiles.

---

## 16. Config, hooks, rules, permissions

### Current config

```toml
project = "codex-product-team-3.0-ultra-beta2"
```

Практически не используется.

### 4.0 profiles

#### Conservative

- read-only / workspace limited;
- user approvals;
- no proactive subagents;
- low thread count;
- hooks enforcement.

#### Balanced

- workspace write;
- scoped authorization;
- auto-safe reads;
- one reviewer worker;
- tests allowed by lease.

#### Autonomous Worktree

- isolated worktree;
- bounded goal;
- auto-review;
- parallel read workers;
- disjoint write workers;
- mandatory Stop verification.

### Controls

- `tool_output_token_limit`;
- `history.max_bytes`;
- `compact_prompt`;
- `agents.max_threads`;
- `agents.max_depth`;
- `agents.job_max_runtime_seconds`;
- permission profiles;
- rules;
- hooks.

---

## 17. Distribution strategy 4.0

### Package family

#### `cpt-runtime`

Repo-local scaffold:

```text
AGENTS.md
.codex/config.toml
.codex/runtime/
  CURRENT.yaml
  TASKS.yaml
  RUNTIME_SUMMARY.md
  product/
```

#### `cpt-core` plugin

- new task;
- bounded discovery;
- impact planning;
- knowledge lifecycle;
- hooks;
- shared schemas.

#### Domain plugins

- `cpt-product-research`;
- `cpt-design-ui`;
- `cpt-frontend`;
- `cpt-backend-data`;
- `cpt-risk-ops`;
- `cpt-ai-agentic`.

#### Optional `cpt-workers`

Custom worker archetypes.

#### `cpt-cli`

- install;
- init;
- migrate;
- validate;
- diagnostics;
- eval.

---

## 18. Cross-platform diagnostics

Текущий exporter — WSL-only.

4.0:

- Python core exporter;
- bash wrapper;
- PowerShell wrapper;
- automatic redaction;
- session extract, not full huge rollout;
- pack-size report;
- secret scan;
- component selection;
- support WSL/Linux/macOS/Windows;
- no auth.json/full SQLite by default.

---

## 19. Evals 4.0

### Eval fixture structure

```text
evals/
  existing-ui-button/
    repo/
    prompt.md
    expected.json
    forbidden.json
    grader.py
```

### Assertions

- loaded files;
- selected product area;
- selected roles/skills;
- forbidden reads;
- no write before approval;
- Impact Map fields;
- write scope;
- verification;
- knowledge update;
- output tokens;
- compaction survival;
- subagent status.

### Critical suites

1. Micro copy fix.
2. Systemic UI mode change.
3. API-dependent UI.
4. Existing product onboarding.
5. Greenfield MVP.
6. Redesign/migration.
7. Design-system governed implementation.
8. Reference fidelity.
9. Context stress and compaction.
10. Subagent timeout.
11. Parallel worktree.
12. Security-sensitive API.
13. Knowledge stale detection.
14. Framework skill truncation.
15. Override behavior.
16. Local ignored runtime.
17. Cross-platform diagnostics.

---

## 20. Документная глубина: результаты полного инвентаря

### Сводка по 404 Markdown-файлам

Предварительная классификация:

- 149 — adequate или требует обычного migration review;
- 50 — templated playbooks;
- 50 — thin role cards;
- 44 — generic placeholder skills;
- 34 — thin scenario files;
- 21 — skeletal templates;
- 14 — lightweight policies;
- 11 — placeholder simulations;
- 9 — thin policies;
- 6 — three-line protocol stubs;
- 3 — thin READMEs;
- 2 — thin audit checklists;
- 2 — critical-thin methodology/schema docs;
- отдельные critical findings:
  - overloaded AGENTS;
  - unsafe override template;
  - broken/underdeveloped runtime load policy;
  - conflicted subagent orchestration.

### Важное уточнение

Автоматическая оценка не означает, что каждый короткий файл плох. Короткий registry или pointer может быть идеальным. Риск появляется, когда документ обещает сложный метод, но содержит только название или generic checklist.

---

## 21. Целевая архитектура 4.0

### Runtime plane

- tiny canonical kernel;
- typed state;
- task/goal registry;
- authorization lease;
- checkpoints;
- hooks/rules/config.

### Knowledge plane

- schema-driven Product Knowledge;
- claim provenance;
- freshness graph;
- generated human views;
- area partitioning.

### Expertise plane

- complete role registry;
- domain plugin skill packs;
- method references;
- task-type routes;
- gate registry.

### Execution plane

- main thread;
- worker archetypes;
- worktrees;
- bounded delegation;
- quorum/timeouts.

### Evaluation plane

- executable scenarios;
- trace graders;
- regression reports;
- package CI.

---

## 22. План разработки 4.0

### Phase 0 — Freeze и baseline

- зафиксировать 3.0 beta 2;
- сохранить live ai-web traces;
- записать benchmark prompts;
- измерить token/tool-read baseline;
- не менять architecture до baseline.

### Phase 1 — Kernel reduction

- новый AGENTS;
- canonical paths;
- `RUNTIME_SUMMARY`;
- remove TKT-000 requirement;
- Micro Change Protocol;
- authorization leases;
- config profiles.

### Phase 2 — Distribution split

- repo scaffold;
- core plugin;
- domain plugins;
- installer/migrator;
- local/team modes.

### Phase 3 — Skills refactor

- inventory 95;
- remove/merge aliases;
- replace 44 boilerplates;
- add references/scripts/openai.yaml;
- build trigger evals;
- shrink active skill surface.

### Phase 4 — Role knowledge overhaul

- enrich 50 roles;
- update handoff graph;
- integrate frontend_engineer;
- machine-readable registry;
- worker eligibility;
- typed artifacts;
- methodology packs.

### Phase 5 — Product Knowledge schema

- YAML/JSON schemas;
- claim lifecycle;
- evidence depth;
- freshness graph;
- source revisions;
- privacy policy;
- generated index views.

### Phase 6 — Deterministic enforcement

- hooks;
- rules;
- permissions;
- output limits;
- compact prompt;
- subagent limits;
- Stop checks.

### Phase 7 — Worker orchestration

- 8–12 worker archetypes;
- role lens injection;
- timeout/cancel/quorum;
- worktree strategy;
- parallel write constraints.

### Phase 8 — Evals and CI

- fixtures;
- trace capture;
- graders;
- mutation tests;
- regression scorecard;
- cross-platform CI.

### Phase 9 — Migration and onboarding

- 3.x → 4.0 migrator;
- install wizard;
- docs;
- examples;
- troubleshooting;
- diagnostics.

### Phase 10 — RC live trials

- existing product;
- greenfield;
- redesign;
- micro task;
- high-risk API;
- UI/DS;
- subagent;
- compaction stress.

---

## 23. Приоритетный backlog

### P0

1. Уменьшить root AGENTS.
2. Исправить override architecture.
3. Разделить runtime и framework distribution.
4. Модульные skill packs.
5. Заменить placeholder simulations на executable evals.
6. Внедрить config/hooks/rules.
7. Canonical runtime paths.
8. Rename custom Chronicle.
9. Fix broken-reference validation.
10. Refactor 44 generic skills.

### P1

11. Typed Product Knowledge schemas.
12. Freshness automation.
13. Authorization leases.
14. Complete role metadata.
15. Integrate frontend_engineer throughout role graph.
16. Worker archetypes.
17. Cross-platform diagnostics.
18. Micro Change Protocol.
19. Gate registry.
20. Goals/Memories integration policy.

### P2

21. Plugin marketplace packaging.
22. Generated human docs.
23. UI for role/skill browsing.
24. Optional MCP integrations.
25. Automation/scheduled knowledge freshness audits.

---

## 24. Что нельзя делать в 4.0

- Не превращать AGENTS в ещё более длинный манифест.
- Не добавлять новые roles ради каждого procedural concern.
- Не увеличивать количество skills без metadata budget.
- Не делать жёсткие line limits.
- Не хранить всю историю в runtime summary.
- Не распространять universal framework через копирование сотен файлов.
- Не считать structural validator доказательством поведения.
- Не делать все 50 roles отдельными spawnable workers по умолчанию.
- Не строить Product Knowledge как энциклопедию.
- Не полагаться на memory/compaction без disk checkpoint.
- Не заставлять пользователя подтверждать каждый read.
- Не зашивать конкретную дизайн-систему или продукт в core.

---

## 25. Acceptance Criteria для 4.0

4.0 готов к RC, если:

1. Root AGENTS остаётся коротким и проходит instruction-budget test.
2. Local override не отключает kernel/framework.
3. Repo получает не более минимального scaffold.
4. Expert framework ставится как plugins/packs.
5. Skills initial metadata помещается в бюджет выбранного pack.
6. Все 50 roles сохранены как lenses.
7. Spawnable worker set ограничен и понятен.
8. New Task Protocol работает без ручного перечисления файлов.
9. Micro task не требует full ticket/Impact Map.
10. Authorization lease снижает approval fatigue.
11. Product Knowledge имеет schema и freshness automation.
12. Pre/PostCompact recovery проходит eval.
13. Subagent timeout/quorum/cancel проходит eval.
14. No-edit-before-approval проверяется trace grader.
15. UI/DS/API/security suites проходят.
16. Existing/greenfield/redesign modes проходят.
17. Cross-platform install/diagnostic работает.
18. Broken references отсутствуют.
19. No product-specific names in universal core.
20. Package CI и regression scorecard зелёные.

---

## 26. Финальный вывод

3.0 доказал главную гипотезу: Codex-команде нужен не только набор экспертиз, а операционная система контекста, памяти, discovery, approvals и знания продукта.

4.0 не должен быть «ещё большей папкой». Он должен стать:

- меньше в always-loaded слое;
- модульнее в expertise;
- строже в enforcement;
- глубже в методологиях;
- исполнимее в evals;
- проще в установке;
- устойчивее к compaction;
- дешевле по токенам;
- автономнее без потери контроля.

Ключевая формула 4.0:

> **Tiny kernel. Typed product knowledge. Installable expert packs. Scoped autonomy. Executable evaluation.**

