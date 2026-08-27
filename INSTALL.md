# Установка Product OS 4.1

Product OS устанавливается на двух независимых уровнях:

1. **Плагины Codex** дают агенту skills и рабочие методы.
2. **Runtime проекта** добавляет в конкретный репозиторий `AGENTS.md`, `.cpt/`, состояние задач, контрольные точки и Product Knowledge.

Можно начать только с плагинов. Полный runtime нужен для продолжительной работы над конкретным продуктом.

## Вариант A: установить Product Designer в Codex

Для Product Designer нужны `cpt-core` и `cpt-design-ui`:

```bash
codex plugin marketplace add Lofiette/product-os --ref v4.1.0
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Проверьте результат:

```bash
codex plugin list
```

Оба плагина должны иметь статус `installed, enabled` и версию `4.1.0`.

После установки полностью откройте **новую задачу Codex**. Уже открытая задача могла загрузить список skills до установки.

### Установка через helper из скачанного репозитория

Windows PowerShell:

```powershell
.\scripts\register-codex-marketplace.ps1
```

macOS или Linux:

```bash
./scripts/register-codex-marketplace.sh
```

Helpers по умолчанию используют `Lofiette/product-os@v4.1.0` и устанавливают два основных плагина.

Повторный запуск безопасен для уже существующего direct Git marketplace без явной смены source/ref. Если установка управляется Product OS Manager и её путь соответствует `sources/product-os/<commit>`, helper остановится: такую установку нужно обновлять транзакцией Manager, чтобы не потерять receipt и rollback.

Установка плагинов выполняется последовательно. Если второй плагин не установился, устраните причину и повторите ту же команду: уже выполненный первый шаг не требуется отменять.

## Вариант B: установить полный runtime в проект

### Требования

- Python 3.10 или новее;
- Git;
- зависимости `PyYAML` и `jsonschema` из `requirements.txt`.

Сначала получите неизменяемую версию исходников:

```bash
git clone https://github.com/Lofiette/product-os.git
cd product-os
git fetch --tags
git switch --detach v4.1.0
python -m pip install -r requirements.txt
```

На Windows вместо последней команды можно использовать:

```powershell
py -3 -m pip install -r requirements.txt
```

### Local mode — личная установка

```bash
python tools/cpt_dist.py install \
  --project /path/to/your-project \
  --mode local \
  --enforcement-mode audit
```

В local mode:

- `.cpt/` добавляется в локальный `.git/info/exclude` и не попадает в историю проекта;
- `cpt-core` подключается через личный plugin scope;
- отсутствующий `AGENTS.md` создаётся и игнорируется;
- существующий tracked `AGENTS.md` автоматически не изменяется.

Если tracked `AGENTS.md` уже существует, installer создаёт `.cpt/AGENTS_SNIPPET.md`. Изучите его и добавляйте kernel вручную только после проверки.

### Team mode — общая установка команды

```bash
python tools/cpt_dist.py install \
  --project /path/to/your-project \
  --mode team \
  --enforcement-mode audit \
  --rules-profile conservative
```

В team mode runtime-файлы предназначены для хранения в Git. Управляемый kernel добавляется в `AGENTS.md`, но installer никогда сам не выполняет `git add`, не создаёт ветку и не делает commit.

Перед включением project hooks, rules и режима `enforce` команда должна изучить их и явно доверить проекту. Для начала рекомендуется `off` или `audit`.

### Добавить Product Designer

```bash
python tools/cpt_dist.py pack-add \
  --name cpt-design-ui \
  --scope personal \
  --project /path/to/your-project
```

Посмотреть все доступные domain packs:

```bash
python tools/cpt_dist.py pack-catalog
```

### Один Windows helper для runtime и pack

```powershell
.\scripts\product-os.ps1 \
  -Action install \
  -Project "C:\path\to\project" \
  -Mode local \
  -PluginScope personal \
  -EnforcementMode audit \
  -Packs cpt-design-ui
```

Python CLI остаётся каноническим. PowerShell helper только собирает и проверяет те же команды.

## Если в проекте уже есть tracked AGENTS.md

Безопасное поведение по умолчанию — не менять файл. Для явного объединения управляемого блока:

```bash
python tools/cpt_dist.py install \
  --project /path/to/your-project \
  --mode local \
  --agents-policy merge \
  --allow-tracked-agents-change
```

Команда намеренно создаст tracked change. Просмотрите diff перед commit.

## Runtime без Codex-плагинов

Product OS может работать через файлы проекта с агентом, который не поддерживает Codex plugin marketplace:

```bash
python tools/cpt_dist.py install \
  --project /path/to/your-project \
  --mode local \
  --plugin-scope none
```

Такой режим сохраняет runtime, Product Knowledge и методологию, но discovery skills зависит от возможностей выбранного агента.

## Дополнительные worker archetypes

Worker pack устанавливается отдельно и никогда не появляется автоматически:

```bash
python tools/cpt_dist.py workers-install --scope personal
```

Для намеренно общей установки в репозиторий команды:

```bash
python tools/cpt_dist.py workers-install \
  --scope repo \
  --project /path/to/your-project
```

Перед использованием изучите `WORKER_PACK.md` и ограничения `[agents]`. Наличие worker archetype не является разрешением на делегирование.

## Проверка установки проекта

```bash
python tools/cpt_dist.py status --project /path/to/your-project
python tools/cpt_dist.py doctor --project /path/to/your-project
```

Внутри проекта runtime также можно проверить его собственным CLI:

```bash
python .cpt/bin/cpt_runtime.py status
python .cpt/bin/cpt_runtime.py validate
```

Используйте Python, установленный именно для этого проекта. Не переиспользуйте runtime другого репозитория.

## Обновление Codex-плагинов

Для marketplace, который Codex напрямую зарегистрировал из Git:

```bash
codex plugin marketplace upgrade product-os
codex plugin add cpt-core@product-os
codex plugin add cpt-design-ui@product-os
```

Upgrade обновляет уже настроенный ref, но не предназначен для скрытой смены источника. После обновления откройте новую задачу Codex.

Manager-owned marketplace обновляется только через новый подтверждённый план:

```text
plan-local-git -> prepare -> switch -> doctor
```

`prepare` создаёт и проверяет backup и новый неизменяемый источник, не выключая старый. Отдельно подтверждённый `switch` меняет активную версию. При проблеме остаются `rollback` и консервативный `recover`.

## Обновление runtime проекта

Запускайте команды **из checkout новой версии Product OS**:

```bash
python tools/cpt_dist.py status --project /path/to/your-project
python tools/cpt_dist.py update --project /path/to/your-project
python tools/cpt_dist.py doctor --project /path/to/your-project
```

Updater заменяет только управляемые файлы и сохраняет изменяемое состояние runtime и Product Knowledge. При конфликте он останавливается, если пользователь явно не выбрал backed-up forced update.

## Удаление и rollback

Uninstall удаляет только управляемые компоненты и блокируется, пока активны задачи, workers, orchestrations или dirty managed worktrees.

Rollback миграции — отдельная receipt-driven операция: она должна восстановить точное состояние до миграции, а не просто удалить Product OS 4.1.

Подробнее:

- [UPDATE_AND_ROLLBACK.md](UPDATE_AND_ROLLBACK.md);
- [docs/PRODUCT_OS_MANAGER.md](docs/PRODUCT_OS_MANAGER.md);
- [docs/MIGRATION_4.0_TO_4.1.md](docs/MIGRATION_4.0_TO_4.1.md);
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md);
- [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

## Что сделать после установки

Откройте новую задачу Codex в своём проекте и сформулируйте результат обычным языком. Например:

> Изучи проект и объясни, какой режим Product OS сейчас установлен. Ничего не меняй, пока не покажешь план.

Если runtime установлен корректно, агент прочитает компактное состояние `.cpt`, выберет подходящий масштаб работы и продолжит по правилам проекта.
