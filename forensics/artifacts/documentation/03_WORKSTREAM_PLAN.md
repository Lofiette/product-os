# 4.0 Workstream Plan

## Phase 0. Freeze and Benchmark

### Цель

Создать неизменяемый baseline и regression fixtures.

### Работы

- зафиксировать archive hash и inventory;
- обезличить representative live traces;
- определить golden tasks;
- снять baseline metrics;
- сформировать benchmark scorecard.

### Exit criteria

- baseline reproducible;
- fixture data не содержит проектных имён или чувствительных данных;
- минимум 8 benchmark cases;
- метрики 3.0 сохранены.

## Phase 1. Kernel Reduction and Runtime Schema

### Работы

- создать tiny root `AGENTS.md`;
- определить `.cpt/runtime.yaml`, `current.yaml`, task index и checkpoint schema;
- реализовать optional `TKT-000`;
- добавить Micro Change Protocol;
- добавить scoped authorization lease;
- переименовать custom Chronicle в `RUNTIME_SUMMARY.md`;
- определить compaction checkpoint contract;
- создать local file-only fallback.

### Exit criteria

- startup не требует полного framework;
- no-active-task state валиден;
- micro change проходит без full ticket;
- runtime schema валидируется;
- recovery после искусственного compact восстанавливает task state.

## Phase 2. Distribution Split

### Работы

- repo scaffold;
- core plugin;
- domain plugin layout;
- installer/uninstaller/update command;
- local ignored и team-shared modes;
- plugin metadata budget measurement.

### Exit criteria

- новый проект получает менее 20 repo-local framework files;
- core работает без domain packs;
- pack можно включить/отключить независимо;
- uninstall не повреждает проект.

## Phase 3. Skills Consolidation

### Работы

- инвентаризация 95 skills;
- классификация core/domain/explicit/alias/deprecate/rewrite;
- объединение aliases;
- переработка 44 generic skills;
- `openai.yaml` и invocation policy;
- per-skill trigger evals;
- scripts/references для детерминированных операций.

### Exit criteria

- core active skill metadata укладывается в безопасный discovery budget;
- ни один critical skill не является generic boilerplate;
- implicit routing имеет eval coverage;
- deprecated aliases имеют migration notes.

## Phase 4. Role Expertise Overhaul

### Работы

- сохранить 50 roles;
- ownership audit;
- typed registry;
- method references;
- evidence standards;
- role-specific anti-patterns;
- worker eligibility;
- handoff contracts;
- frontend engineer full integration.

### Exit criteria

- каждая роль имеет distinct decision rights;
- критические roles имеют глубокую methodology pack;
- role routing покрывает основные task types;
- logical roles не создают 50 default workers.

## Phase 5. Product Knowledge Schema and Freshness

### Работы

- schema/frontmatter;
- claim lifecycle;
- evidence depth;
- source revision;
- path-based review triggers;
- dependency graph;
- freshness linter;
- targeted update workflow;
- sanitization rules;
- existing/greenfield/redesign adapters.

### Exit criteria

- stale knowledge определяется автоматически для fixture changes;
- обновляется только affected artifact set;
- vector store не требуется;
- schema supports greenfield planned knowledge and existing confirmed knowledge.

## Phase 6. Deterministic Runtime Controls

### Работы

- hooks;
- rules;
- permission profiles;
- checkpoint hooks;
- tool output budget;
- command policies;
- authorization lease enforcement;
- subagent state hooks;
- compact/recovery hooks.

### Exit criteria

- критические ограничения подкреплены enforcement;
- пользователь не подтверждает каждую routine read;
- scope expansion требует нового lease;
- project remains usable without optional hooks trusted.

## Phase 7. Worker Orchestration

### Работы

- 8–12 archetypes;
- role lens injection;
- timeout/cancel/quorum;
- worktree adapter;
- disjoint write verification;
- disk checkpoint;
- worker cost budget.

### Exit criteria

- зависший worker не блокирует task;
- compaction не теряет worker registry;
- parallel writes имеют безопасный merge path;
- simple task не spawn workers по умолчанию.

## Phase 8. Executable Evals and CI

### Работы

- fixture runner;
- trace capture;
- deterministic graders;
- LLM graders;
- mutation tests;
- regression dashboard;
- token/tool/approval budgets;
- cross-platform CI.

### Exit criteria

- критические scenarios исполняются автоматически;
- known failure mutation ловится;
- release blocked on behavioral regressions;
- scorecard сравнивает 3.0 и 4.0.

## Phase 9. Optional Integrations

### Работы

- MCP adapter SDK;
- Chroma/pgvector semantic recall adapter;
- Langfuse/OTel observability adapter;
- Postgres team registry adapter;
- issue tracker adapters;
- design tool adapters;
- graceful fallback tests.

### Exit criteria

- core полностью работает без adapters;
- отключение внешнего сервиса не теряет canonical state;
- provenance фиксирует external source;
- secrets и PII не попадают в knowledge без policy.

## Phase 10. Installer, Migration and RC

### Работы

- 3.x migration assistant;
- init wizard;
- diagnostics;
- Russian/English onboarding;
- compatibility matrix;
- RC trials;
- package signing/checksums.

### Exit criteria

- чистая установка;
- миграция sample 3.x;
- rollback;
- diagnostics pack;
- RC benchmark pass.
