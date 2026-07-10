# Codex Product Operating System 4.0 — Alpha 4: роли, экспертиза и маршрутизация

Alpha 4 сохраняет Runtime Kernel, модель распространения и 45 канонических skills из Alpha 3, а затем переносит все 50 логических ролей в типизированный экспертный слой.

## Что реализовано

- компактный repo scaffold и обязательный `cpt-core`;
- пять независимо устанавливаемых domain plugins;
- 45 канонических skills и полное покрытие миграции 95 старых skills;
- все 50 ролей сохранены и глубоко переработаны;
- decision rights, evidence obligations, owned artifacts, skills, gates, handoffs и worker eligibility;
- 50 компактных role lenses;
- 50 глубоких role-specific method references;
- 25 evidence-based quality gates;
- 14 task routing profiles;
- role-to-skill и role-to-gate matrices;
- migration registry;
- детерминированные proxy-evals триггеров и routing.

## Главная модель

Роль — это логическая ответственность и профессиональная перспектива, а не subagent.  
Skill — это метод.  
Gate — проверяемый контракт качества.  
Worker archetypes появятся позже в Execution Plane.

## Быстрый старт

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /путь/к/репозиторию --mode local
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /путь/к/репозиторию
```

## Проверка

```bash
python tools/validate_distribution.py --root .
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/eval_skill_triggers.py --root . --write-report evaluation/trigger-eval-report.json
python tools/eval_role_routing.py --root . --write-report evaluation/role-routing-eval-report.json
python tests/run_all.py
```

Основные документы: `ROLES.md`, `roles/ROLE_CATALOG.md`, `roles/ROLE_ROUTING.md`, `roles/QUALITY_GATE_MODEL.md`, `migration/ROLE_MIGRATION.csv`, `ALPHA4_LIMITATIONS.md`.

В Alpha 4 ещё нет исполняемых worker archetypes, Product Knowledge schemas, hooks/rules enforcement, SQLite/MCP и live Codex behavioral certification.
