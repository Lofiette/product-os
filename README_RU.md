# Codex Product Operating System 4.0 — Alpha 1 Runtime Kernel

Это первый исполняемый фрагмент 4.0. Он реализует только **Runtime Plane**:

- маленький root `AGENTS.md`;
- машинно-читаемое состояние под `.cpt/`;
- штатное состояние без активной задачи;
- опциональный `TKT-000`;
- Standard Task и Micro Change;
- scoped authorization lease;
- компактный recovery summary;
- checkpoint/recovery;
- JSON Schema и cross-file validation;
- синтетический тест восстановления после потери контекста.

## Проверка

```bash
python -m pip install -r requirements.txt
python scripts/cpt_runtime.py validate
python scripts/cpt_runtime.py status
python scripts/simulate_compaction_recovery.py
python -m unittest discover -s tests -v
```

## Что пока отсутствует

В этот alpha-пакет намеренно не входят роли, domain skills, Product Knowledge, workers, plugins, hooks, внешние сервисы и migration assistant. Они будут подключаться последующими фазами, не раздувая always-on kernel.

`Authorization lease` в Alpha 1 является проверяемой записью согласованного scope, но ещё не техническим security boundary. Нативные permissions и sandbox Codex остаются обязательными.
