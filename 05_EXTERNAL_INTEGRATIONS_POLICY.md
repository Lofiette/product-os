# External Integrations Policy

## Основной принцип

Внешние сервисы расширяют 4.0, но не являются обязательным условием работы.

Каждая интеграция обязана выполнять пять требований:

1. Core работает без неё.
2. Есть typed adapter или MCP boundary.
3. Canonical state не хранится только во внешнем сервисе.
4. Есть graceful fallback.
5. Source provenance фиксируется в knowledge/runtime artifacts.

## Уровень 0 — Self-contained core

Должен работать без сетевых сервисов:
- Codex plugin;
- Git;
- локальная файловая система;
- SQLite runtime registry;
- JSON Schema/Pydantic/Zod validation;
- local hooks/rules;
- local eval runner;
- `rg` и optional local AST adapter.

## Уровень 1 — Recommended local integrations

### Git worktrees

Для изоляции альтернативных реализаций, параллельных write-workers и рискованных миграций.

Не используются для каждой задачи.

### Tree-sitter / AST index

Для symbol/import/dependency impact analysis. Дополняет targeted text search и уменьшает необходимость читать десятки файлов.

### Local SQLite registry

Default exact state store для:
- tasks;
- leases;
- checkpoints;
- artifact graph;
- freshness links;
- worker runs;
- eval results.

Markdown остаётся readable projection.

## Уровень 2 — Recommended development integrations

### OpenTelemetry

Vendor-neutral traces, metrics и logs. Core должен уметь писать локальный JSON trace даже без collector/backend.

### Langfuse

Опциональная визуализация и оценка LLM/agent traces, token usage, cost, latency и quality scores. Нужна разработчикам framework и командам, но не конечному single-user core.

## Уровень 3 — Optional semantic memory

### Chroma / pgvector / equivalent

Назначение:
- semantic recall по архиву задач;
- поиск похожих решений;
- исследования;
- historical decisions;
- postmortems;
- внешние стандарты.

Не хранит единственную копию:
- active task;
- approvals;
- обязательные правила;
- current Product Knowledge;
- worker state.

Результат semantic search является кандидатом. Codex обязан открыть canonical source перед принятием решения.

## Уровень 4 — Team and enterprise adapters

Опционально:
- Postgres shared registry;
- issue tracker;
- source hosting;
- documentation platform;
- design tool;
- artifact storage;
- remote knowledge service;
- external orchestrator.

## MCP strategy

MCP — предпочтительная интеграционная шина для внешних tools/context.

Пример capability groups:

```text
runtime.get_state
runtime.create_task
runtime.update_lease
knowledge.search
knowledge.get_artifact
knowledge.mark_stale
evals.run_case
observability.get_trace
design.lookup_component
issues.get_ticket
```

Tools должны иметь granular approval modes и allowlists.

## Failure behavior

- Semantic service down → exact local search.
- Observability backend down → local trace buffer.
- Remote DB down → local SQLite or read-only degraded mode.
- MCP unavailable → core tools remain functional.
- Design/issue integration unavailable → ask user for explicit input, не выдумывать данные.

## Privacy and security

- secrets никогда не индексируются;
- PII требует policy и redaction;
- external retrieval имеет source labels;
- user controls adapters independently;
- integrations disabled by default unless explicitly enabled;
- network access follows Codex approval/permission policy.
