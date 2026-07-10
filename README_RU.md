
# Codex Product Operating System 4.0 Alpha 6

Alpha 6 добавляет опциональный детерминированный runtime-слой поверх Runtime Kernel, Skills, Roles и Product Knowledge.

## Быстрый старт

```bash
python tools/cpt_dist.py install --project /path/to/repo --mode local --enforcement-mode audit
```

Затем включите CPT Core plugin, перезапустите Codex, внимательно проверьте и подтвердите доверие к plugin hooks. После наблюдения за audit-режимом можно включить блокирующий режим:

```bash
python .cpt/bin/cpt_runtime.py enforcement-set --mode enforce --trust-state trusted
```

Нативные sandbox, permissions, approvals и rules Codex остаются главным техническим контуром безопасности. CPT lease и hooks не заменяют их.

## Что появилось

- lease-aware проверка поддерживаемых writes и verification-команд;
- автоматический checkpoint перед compaction;
- проверка state после compaction;
- targeted knowledge freshness после project writes;
- audit log с редактированными preview вместо сырых выводов;
- записи жизненного цикла subagents;
- optional command rules и permission-profile examples;
- fallback через CLI, если hooks отключены.

Полное описание: `ENFORCEMENT.md`.
