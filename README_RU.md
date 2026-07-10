# Codex Product Operating System 4.0 — Alpha 5: схема и жизненный цикл Product Knowledge

Alpha 5 сохраняет Runtime Kernel, модель распространения, 45 канонических skills, 50 логических ролей и 25 quality gates из Alpha 4. Новый слой добавляет типизированную файловую Product Knowledge для существующего продукта, greenfield-разработки и редизайна/миграции, не превращая знания в постоянно загружаемую энциклопедию.

## Что входит

- минимальный repo scaffold и нативный `cpt-core` plugin;
- пять независимо устанавливаемых domain plugins;
- 45 канонических skills и полное покрытие миграции 95 legacy skills;
- 50 логических ролей и 25 evidence-based gates;
- канонические YAML-артефакты и генерируемые Markdown-проекции;
- Product Map, Area Map, Flow Map, Decision Record, API/Data Contract и Context Packet;
- lifecycle утверждений, confidence, evidence depth, source revision, unknowns, review triggers и зависимости;
- режимы existing, greenfield и redesign;
- targeted freshness scan с распространением по зависимостям;
- обязательный учёт обновления знаний перед закрытием Standard Task;
- классификация, sanitization и правила внешнего шаринга;
- безопасные install, update, doctor, uninstall и управление domain packs.

## Принципы Product Knowledge

- Product Map маршрутизирует будущую работу, а не пересказывает весь продукт.
- Родительский артефакт ссылается на более глубокий, а не копирует его целиком.
- Уверенность растёт только вместе с качеством evidence.
- Greenfield-намерение остаётся planned до появления реализации и проверки.
- В редизайне current, target и delta не смешиваются.
- Freshness обновляет только затронутые артефакты.
- Целевые размеры являются рекомендацией и никогда не обрезают полезное знание.
- В канонических знаниях нельзя хранить credentials и сырые restricted-значения.

## Быстрый старт

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install --project /путь/к/репозиторию --mode local
python tools/cpt_dist.py pack-add --name cpt-design-ui --scope personal
python tools/cpt_dist.py doctor --project /путь/к/репозиторию

cd /путь/к/репозиторию
python .cpt/bin/cpt_runtime.py knowledge-init   --title "Product Knowledge"   --mode existing   --owner-role product_strategist   --source-kind git_commit   --source-value "$(git rev-parse HEAD)"
```

Product Knowledge создаётся лениво. Если проекту не нужны durable product knowledge artifacts, файловый бюджет установки не увеличивается.

## Проверка дистрибутива

```bash
python tools/validate_distribution.py
python tools/validate_skills.py --root .
python tools/validate_roles.py --root .
python tools/validate_knowledge_assets.py
python tools/eval_knowledge_lifecycle.py --root .   --write-report evaluation/knowledge-lifecycle-eval-report.json
python tests/run_all.py
```

Ключевые документы: `KNOWLEDGE.md`, `knowledge/KNOWLEDGE_ARCHITECTURE.md`, `knowledge/CLAIM_LIFECYCLE.md`, `knowledge/EVIDENCE_AND_PROVENANCE.md`, `knowledge/FRESHNESS_AND_DEPENDENCIES.md`, `knowledge/SANITIZATION_AND_SHARING.md`, `knowledge/SCHEMA_REFERENCE.md`, `ROLES.md`, `SKILLS.md`, `ALPHA5_LIMITATIONS.md`.

В Alpha 5 ещё нет автоматических hooks, SQLite, MCP adapters, AST dependency graph, исполняемых worker archetypes и live Codex behavioral certification.
