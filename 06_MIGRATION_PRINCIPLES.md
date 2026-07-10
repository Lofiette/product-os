# Migration Principles: 3.x → 4.0

## Не делать in-place rewrite

3.0 archive остаётся frozen. Миграция создаёт новое 4.0 дерево, затем переносит данные по mapping rules.

## Что переносится

- 50 logical roles;
- role ownership и полезные methodologies;
- проверенные Product Knowledge patterns;
- UI/DS quality layer;
- ticketed runtime concepts;
- bounded discovery;
- Impact Map;
- API/Data Shape prewarm;
- existing/greenfield/redesign modes;
- audits и полезные validators.

## Что трансформируется

- большой `AGENTS.md` → tiny loader + core skills/hooks;
- 50 role-specific agents → worker archetypes + role lenses;
- 95 flat skills → core/domain packs + aliases/deprecations;
- Markdown scenarios → executable eval cases;
- prose approvals → typed leases + permission profiles;
- manual freshness → path-based freshness graph;
- copy-the-kit distribution → plugin + scaffold installer;
- custom `CHRONICLE.md` → `RUNTIME_SUMMARY.md` + checkpoints.

## Что не переносится автоматически

- generic boilerplate skill content;
- project-specific examples;
- duplicated mirror docs без canonical owner;
- stale release labels;
- 50 default spawnable workers;
- line-count hard caps;
- обязательный current `TKT-000`;
- raw private traces.

## Compatibility policy

- migrations имеют dry-run;
- создаётся backup;
- mapping report обязателен;
- unknown custom files не удаляются;
- rollback поддерживается;
- project-specific runtime data остаётся локальным;
- optional external integrations не включаются автоматически.

## Role migration audit

Для каждой роли:
- сохранить / merge / deprecate;
- distinct decision rights;
- methods;
- task types;
- gates;
- worker eligibility;
- compatible skills.

До завершения audit ни одна роль не удаляется.

## Skill migration audit

Для каждого skill:
- domain;
- invocation mode;
- active metadata cost;
- depth assessment;
- aliases;
- scripts/references;
- eval coverage;
- migration outcome.
