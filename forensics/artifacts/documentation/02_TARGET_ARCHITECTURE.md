# Target Architecture 4.0

## Обзор

4.0 строится как пять слабо связанных плоскостей.

```text
Runtime Plane
    ↓ выбирает задачу, scope и разрешения
Knowledge Plane
    ↓ маршрутизирует по продукту и evidence
Expertise Plane
    ↓ подключает методологии и accountability
Execution Plane
    ↓ выполняет работу и делегирование
Evaluation Plane
    ↺ проверяет поведение и регрессии
```

## 1. Runtime Plane

### Ответственность

- startup;
- runtime state;
- task lifecycle;
- micro/standard/complex classification;
- authorization leases;
- checkpoint/recovery;
- compaction safety;
- deterministic rules;
- minimal Definition of Done.

### Компоненты

```text
repo-scaffold/
  AGENTS.md
  .cpt/
    runtime.yaml
    current.yaml
    task-index.yaml
    runtime-summary.md
    tasks/
    checkpoints/

cpt-core-plugin/
  skills/
  hooks/
  schemas/
  rules/
  scripts/
```

### Инварианты

- root loader маленький;
- no active task — валидное состояние;
- state можно восстановить с диска;
- scope/approval machine-readable;
- micro task не требует full workflow;
- destructive операции технически ограничены, а не только запрещены текстом.

## 2. Knowledge Plane

### Ответственность

- Product Map;
- Knowledge Index;
- Area/Flow Maps;
- Decision Records;
- API/Data contracts;
- provenance;
- freshness;
- claim lifecycle;
- task-specific context packets.

### Типизированный metadata contract

```yaml
artifact_type: area_map
schema_version: 4.0
scope: string
owner_role: string
freshness: current | needs-review | stale | deprecated
confidence: high | medium | low
evidence_depth:
  - user_decision
  - design_artifact
  - route
  - component
  - hook_store
  - api_type
  - test
  - runtime_observation
source_revision: git-ref-or-null
review_triggers:
  - path glob
unknowns: []
dependencies: []
```

### Claim lifecycle

```text
planned → hypothesized → inferred → confirmed → validated
                                  ↘ needs-review → stale → deprecated
```

### Хранилища

- Markdown/typed frontmatter — canonical human-readable knowledge;
- SQLite registry — exact artifact graph, status and dependencies;
- optional vector adapter — semantic recall of archive/history.

## 3. Expertise Plane

### Ответственность

- 50 logical roles;
- deep methodologies;
- skills;
- playbooks;
- quality gates;
- routing registry;
- domain packs.

### Distribution

```text
cpt-core
cpt-product-research
cpt-design-ui
cpt-frontend
cpt-backend-api-data
cpt-risk-operations
cpt-ai-agentic
```

Пакеты устанавливаются отдельно. Core не активирует все domain metadata одновременно.

### Role registry

Каждая роль получает typed metadata:

```yaml
id:
domain:
decision_rights:
mental_models:
method_references:
evidence_requirements:
anti_patterns:
quality_heuristics:
primary_task_types:
compatible_skills:
required_gates:
worker_eligibility:
load_cost:
```

### Skill contract

Каждый настоящий skill содержит:
- trigger и non-trigger;
- required inputs;
- exact method;
- output schema;
- evidence standard;
- stop conditions;
- failure modes;
- examples;
- references/scripts/assets;
- implicit/explicit invocation policy.

## 4. Execution Plane

### Main-thread model

Main thread является decision owner и integrator.

### Worker archetypes

Целевой набор: 8–12 worker types вместо 50 role-specific workers.

Worker contract включает:
- task objective;
- role lenses;
- bounded input packet;
- read/write scope;
- expected artifact;
- timeout;
- required/optional status;
- stop condition;
- verification expectation.

### Defaults

- depth: 1;
- max concurrent workers: 3–4;
- read-heavy delegation preferred;
- parallel writes только в disjoint scopes или worktrees;
- deadline + cancellation обязательны;
- partial quorum разрешён;
- live state пишется на диск.

## 5. Evaluation Plane

### Fixture case

```text
evals/cases/<case-id>/
  fixture-repo/
  prompt.md
  expected.json
  forbidden.json
  grader.py
  budget.json
```

### Проверяемые свойства

- выбран правильный task protocol;
- не прочитаны запрещённые файлы;
- roles/skills/gates выбраны корректно;
- approval boundary соблюдён;
- artifact schema валидна;
- knowledge update таргетирован;
- context/tool/token budgets не превышены без причины;
- compaction recovery сохраняет состояние;
- subagent timeout не блокирует session;
- результат соответствует task acceptance.

## Distribution model

### Repo scaffold

Минимальные проектные файлы и локальный state.

### Codex plugins

Стабильные reusable workflows, skills, hooks и optional MCP definitions распространяются plugins, а не копированием всей библиотеки в каждый repository.

### Optional adapters

- semantic memory;
- observability;
- external issue trackers;
- design tools;
- remote databases;
- team knowledge services.

Все adapters отключаемы и имеют graceful fallback.
