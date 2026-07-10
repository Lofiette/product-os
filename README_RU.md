# Codex Product Operating System 4.0 — Alpha 3: консолидация skills

Alpha 3 сохраняет Runtime Kernel и модель распространения Alpha 2, но переносит skill-слой 3.x в глубокие и независимо устанавливаемые domain plugins.

## Что реализовано

- компактный `cpt-core` из трёх runtime/context skills;
- пять опциональных domain plugins;
- полное отображение 95 старых skills в 45 канонических;
- для каждого skill: trigger/non-trigger, входы, специализированный метод, output contract, evidence rules, stop conditions и failure modes;
- `agents/openai.yaml` с политикой implicit/explicit invocation;
- proxy-evals триггеров и контроль metadata budget по реальным профилям;
- установка domain pack по имени;
- сохранение local-ignored и team-shared режимов, безопасного update/uninstall.

## Быстрый старт

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /путь/к/репозиторию --mode local
python tools/cpt_dist.py pack-catalog
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /путь/к/репозиторию
```

Обязателен только `cpt-core`. Domain packs включаются по задаче или рабочему профилю, а не все одновременно.

## Проверка

```bash
python tools/validate_distribution.py --root .
python tools/validate_skills.py --root .
python tools/eval_skill_triggers.py --root . --write-report evaluation/trigger-eval-report.json
python tools/measure_all_skill_metadata.py
python tests/run_all.py
```

Полезные документы: `SKILLS.md`, `docs/SKILL_AUTHORING_STANDARD.md`, `docs/SKILL_CONSOLIDATION.md`, `migration/SKILL_MIGRATION.csv`, `ALPHA3_LIMITATIONS.md`.

Роли, Product Knowledge schemas, hooks/rules, worker archetypes и внешние adapters остаются следующими этапами.
