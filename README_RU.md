# Codex Product Operating System 4.0 — Alpha 2

Это второй исполняемый инкремент 4.0. Он превращает Runtime Kernel Alpha 1 в устанавливаемую систему.

## Что появилось

- минимальный scaffold проекта;
- отдельный Codex plugin `cpt-core`;
- local-ignored и team-shared режимы;
- безопасные install / update / doctor / uninstall;
- независимое подключение domain packs;
- измерение metadata budget skills;
- installation receipt и безопасный rollback;
- автоматические тесты установки и удаления.

## Быстрый старт

```bash
python tools/cpt_dist.py install --project /путь/к/репозиторию --mode local
python tools/cpt_dist.py doctor --project /путь/к/репозиторию
```

После установки перезапустите Codex и включите CPT Core в разделе Plugins.

Alpha 2 пока не переносит роли, domain skills, Product Knowledge и hooks. Core полностью работает без них и без внешних сервисов.
