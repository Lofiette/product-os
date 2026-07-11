# Codex Product Operating System 4.0 Alpha 7

Alpha 7 добавляет управляемую оркестрацию workers поверх Runtime Kernel, Product Knowledge, канонических skills, 50 логических ролей, quality gates, распределения по plugins и детерминированного enforcement.

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

## Главные принципы

- Runtime-состояние типизировано и восстанавливается по checkpoint.
- Product Knowledge хранится в каноническом YAML; Markdown является generated view.
- 50 ролей остаются профессиональными линзами, а не 50 субагентами.
- 45 skills подключаются через небольшие plugins.
- Реальный worker требует Standard Task, lease, утверждённый contract и ограниченный scope.
- Основной поток владеет интеграцией и финальным решением.
- Параллельная запись идёт только через managed Git worktrees; автоматического merge нет.
- Нативные sandbox, permissions, approvals, trust и организационные политики Codex остаются главным техническим контуром.

## Документы

- `INSTALL.md`
- `ORCHESTRATION.md`
- `WORKER_PACK.md`
- `ENFORCEMENT.md`
- `KNOWLEDGE.md`
- `ROLES.md`
- `SKILLS.md`
- `ALPHA7_LIMITATIONS.md`
