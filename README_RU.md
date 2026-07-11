# Codex Product Operating System 4.0 Alpha 8

Alpha 8 добавляет **исполняемый Evaluation Plane** поверх Runtime Kernel, Product Knowledge, канонических skills, 50 логических ролей, quality gates, детерминированного enforcement и управляемой оркестрации workers, созданных в Alpha 1–7.

## Установка ядра

```bash
python tools/cpt_dist.py install \
  --project /path/to/repo \
  --mode local \
  --enforcement-mode audit
```

Core plugin по умолчанию выставляется в personal scope. После установки перезапустите Codex, включите CPT Core и внимательно проверьте его hooks перед подтверждением доверия.

## Опциональный worker pack

```bash
python tools/cpt_dist.py workers-install --scope personal
```

Он содержит десять ограниченных custom-agent archetypes и никогда не устанавливается автоматически.

## Исполняемые оценки

Обязательный полностью локальный suite:

```bash
python tools/cpt_eval.py run \
  --suite offline-core \
  --backend reference \
  --report-dir evaluation/executable/reports/offline-core
```

Сравнение с проверенным baseline:

```bash
python tools/cpt_eval.py compare-baseline \
  --current evaluation/executable/reports/offline-core/offline-core-reference-scorecard.json \
  --baseline evaluation/executable/baselines/offline-core-alpha8.json
```

Опциональные live-cases используют `codex exec --json`, если доступны Codex CLI и credentials. Подробности в `EVALUATION.md`.

## Главные принципы

- Runtime-состояние типизировано и восстанавливается по checkpoint.
- Product Knowledge хранится в каноническом YAML; Markdown является generated view.
- 50 ролей остаются профессиональными линзами, а не 50 субагентами.
- 45 skills подключаются через небольшие plugins.
- Реальный worker требует Standard Task, lease, утверждённый contract и ограниченный scope.
- Основной поток владеет интеграцией и финальным решением.
- Параллельная запись идёт только через managed Git worktrees; автоматического merge нет.
- Evaluation Plane отделяет детерминированное эталонное поведение от evidence живой модели.
- Нативные sandbox, permissions, approvals, trust и организационные политики Codex остаются главным техническим контуром.

## Документы

- `INSTALL.md`
- `EVALUATION.md`
- `ORCHESTRATION.md`
- `WORKER_PACK.md`
- `ENFORCEMENT.md`
- `KNOWLEDGE.md`
- `ROLES.md`
- `SKILLS.md`
- `ALPHA8_LIMITATIONS.md`
