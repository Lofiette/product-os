# Product OS 4.1

Product OS 4.1 объединяет Runtime, Product Knowledge, профессиональные роли, skills, quality gates, enforcement, worker orchestration, Evaluation Plane, миграцию и release-контур. Среда остаётся независимой от конкретной модели и клиента. Codex-плагины являются одним из адаптеров доставки, а не каноническим источником состояния.

## Что вошло в 4.1

Product Designer получил Interaction Intelligence, выбор паттернов, проектирование форм и длинных процессов, экспертизу по профессиональным интерфейсам данных и независимый от поставщика Design Execution Plane. OpenAI Product Design используется только как необязательный адаптер, если его возможности действительно обнаружены в Codex.

Подробности: `docs/PRODUCT_DESIGNER_4.1.md`.

## Быстрый старт в Codex

Для нового Product Designer нужны два плагина: `cpt-core` и `cpt-design-ui`.
Marketplace фиксируется на неизменяемом release tag, после установки нужно
открыть новую задачу Codex:

```bash
codex plugin marketplace add Lofiette/product-os --ref v4.1.0
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Из скачанного release checkout те же действия выполняет один helper:

```powershell
.\scripts\register-codex-marketplace.ps1
```

```bash
./scripts/register-codex-marketplace.sh
```

Это подключает возможности Product Designer к Codex, но не создаёт проектный
runtime `.cpt`. Для полного процесса Product OS рабочий проект дополнительно
устанавливается отдельной командой ниже.

## Две разные сущности

1. **Репозиторий Product OS** содержит исходники, версии, тесты, release-артефакты и marketplace.
2. **Установка в рабочий проект** содержит маленький repo scaffold: `AGENTS.md`, `.cpt/` и выбранные plugin packs.

Плагин не владеет каноническим состоянием проекта. Это позволяет использовать Product OS вне Codex и безопасно обновлять runtime отдельно от skills.

## Установка в проект

```bash
python -m pip install -r requirements.txt
python tools/cpt_dist.py install \
  --project /path/to/project \
  --mode local \
  --enforcement-mode audit
python tools/cpt_dist.py pack-add \
  --name cpt-design-ui \
  --scope personal \
  --project /path/to/project
```

## Обновление установленного проекта

Команда запускается **из исходников новой версии**:

```bash
python tools/cpt_dist.py status --project /path/to/project
python tools/cpt_dist.py update --project /path/to/project
python tools/cpt_dist.py doctor --project /path/to/project
```

В 4.1 `update` сохраняет mutable runtime state и обновляет не только `cpt-core`, но и все bundled domain packs, записанные в `.cpt/install.json`.

## Codex marketplace из Git

Репозиторий содержит `.agents/plugins/marketplace.json` со всеми шестью плагинами. После публикации репозитория:

```bash
codex plugin marketplace add <GIT_URL_OR_OWNER/REPO> --ref v4.1.0
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Обновление remote marketplace:

```bash
codex plugin marketplace upgrade product-os
```

После обновления плагинов создайте новый thread. Если в проектах установлен `.cpt/` scaffold, отдельно запустите `cpt_dist.py update` для каждого проекта.

Если marketplace `product-os` управляется Product OS Manager и указывает в
`~/.product-os/sources/`, не заменяйте его вручную. Используйте подтверждённую
Manager-транзакцию `plan-local-git -> prepare -> switch`.

## Граница сертификации

Версия продукта: `4.1.0`. Детерминированный offline-контур проверен. Статус release plane по-прежнему честно отделяет offline evidence от живых прогонов моделей, нативных клиентов и внешних инструментов.

```bash
python tools/cpt_release.py readiness --scope offline
```

## Проверка

```bash
python tools/validate_distribution.py
python tools/validate_release.py
python tools/validate_evaluation.py
python scripts/validate_migration_assets.py
python tests/run_all.py
```

## Документы

- `INSTALL.md`
- `UPDATE_AND_ROLLBACK.md`
- `docs/MIGRATION_4.0_TO_4.1.md`
- `docs/VERSIONING_AND_GIT.md`
- `docs/PLUGIN_AND_MARKETPLACE.md`
- `docs/PRODUCT_DESIGNER_4.1.md`
- `EVALUATION.md`
- `ORCHESTRATION.md`
- `ENFORCEMENT.md`
- `KNOWN_LIMITATIONS.md`
