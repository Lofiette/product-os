# 3.0 Ultra beta 2 — Baseline Freeze

Дата freeze: 2026-07-10  
Archive SHA-256: `0e0d3a17e2141b236746204d341c47781ee1acf902eef8cfa60f537b6ec070a9`  
Archive size: 484484 bytes

## Назначение freeze

3.0 Ultra beta 2 сохраняется как неизменяемый regression baseline. Работы 4.0 выполняются в отдельном дереве. Изменения не вносятся непосредственно в frozen archive.

## Фактический состав

| Элемент | Количество |
|---|---:|
| Всего файлов | 477 |
| Директорий | 129 |
| Markdown-документов | 404 |
| Логических ролей | 50 |
| Role playbooks | 50 |
| Custom agent TOML | 50 |
| Skills | 95 |
| Scenario markdown | 34 |
| Simulation cases | 10 |

## Ключевые размеры

| Файл / поверхность | Состояние |
|---|---:|
| Root `AGENTS.md` | 308 строк / 14 982 байта |
| `SKILL_TINY_INDEX.json` | около 14 KB |
| `SKILL_INDEX.json` | около 17.5 KB |
| Медиана role card | около 27 строк |
| Медиана playbook | около 82 строк |

## Что сохраняется как доказанная ценность

- ticketed runtime memory;
- compact recovery summary;
- Product Knowledge hierarchy;
- existing / greenfield / redesign modes;
- bounded discovery;
- Impact Map;
- API/Data Shape contract-level prewarm;
- staged expert loading;
- distinction between role, skill, playbook, gate and subagent;
- frontend engineering responsibility in UI implementation;
- soft artifact-size policy;
- local ignored runtime mode.

## Главные baseline defects

1. Always-on kernel слишком тяжёлый.
2. Дистрибуция копированием сотен файлов.
3. 95 skills создают metadata pressure.
4. 44 skills являются generic boilerplate.
5. Role expertise неравномерна и часто поверхностна.
6. 50 logical roles представлены как 50 spawnable agents.
7. Enforcement преимущественно prose-based.
8. Simulations не являются исполняемыми evals.
9. Product Knowledge freshness ручная.
10. Approval flow может быть слишком дробным.
11. Micro tasks недостаточно отделены от standard workflow.
12. Subagent timeout/quorum/cancel semantics неполны.
13. Документы и registries имеют слишком много ручных зеркал.

## Baseline metrics для будущего сравнения

В Phase 0/8 необходимо зафиксировать для representative cases:
- input/output tokens;
- число tool calls;
- число approvals;
- число compactions;
- прочитанные файлы;
- выбранные roles/skills;
- spawned workers;
- время до первого полезного артефакта;
- число пользовательских вмешательств;
- качество итогового результата;
- false PASS / missed scope rate.

## Приватные benchmark traces

Живые проектные кейсы преобразуются в обезличенные fixture-наборы. В универсальную среду не переносятся названия продуктов, организаций, дизайн-систем, приватные пути, исходный код или чувствительные данные.
