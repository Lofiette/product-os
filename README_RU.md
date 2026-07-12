# Codex Product Operating System 4.0 Beta 1

Beta 1 объединяет Runtime, Product Knowledge, экспертизу, enforcement, worker orchestration, Evaluation Plane, миграцию и release-контур. Базовая среда полностью самодостаточна и не требует внешних сервисов.

## Граница сертификации

Beta 1 подтверждена для детерминированного offline-контура. Это не RC и не заявление о качестве живой модели Codex.

```bash
python tools/cpt_release.py readiness --scope offline
```

Для RC нужны нативные платформенные прогоны, живые задачи Codex, реальные worker threads, reconnect/compaction и финальная мегаревизия.

## Установка

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --enforcement-mode audit
```

## Миграция

```bash
python tools/cpt_migrate.py inspect --project /path/to/repo
python tools/cpt_migrate.py plan --project /path/to/repo --output /safe/path/plan.json
```

Сначала проверяется план. Миграция создаёт внешний backup, поддерживает rollback и не интерпретирует `AGENTS.override.md`.

## Проверка

```bash
python tools/validate_distribution.py
python tools/validate_release.py
python tools/validate_evaluation.py
python scripts/validate_migration_assets.py
python tests/run_all.py
```

Подробности: `BETA1_LIMITATIONS.md`, `EVALUATION_LIMITATIONS.md`, `docs/BETA1_RELEASE_INTEGRATION.md`, `docs/RC_TRIALS_AND_RELEASE_GATES.md`, `EVALUATION.md`, `docs/MIGRATION_3X_TO_4X.md`.
