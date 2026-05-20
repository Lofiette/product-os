# Codex Product Team Kit: Minimal Edition

Готовый минимальный комплект для запуска управляемой продуктовой команды внутри Codex.

Внутри есть:

- `AGENTS.md` — главный файл правил, который Codex должен читать перед работой.
- `TASK.md` — живой бриф задачи. Обновляется по мере появления новых вводных.
- `CHRONICLE.md` — летопись прогресса, решений и изменений, чтобы переживать сжатия контекста.
- `.codex/agents/*.toml` — проектные custom agents для ролей команды.
- `.agents/playbooks/*.md` — подробные компетенции, границы ответственности и выходные артефакты ролей.
- `.agents/skills/*/SKILL.md` — повторяемые workflows: брифинг, планирование, хроника, ревью.
- `.agents/templates/*` — шаблоны для брифа, плана, ревью и PR.
- `docs/QUESTION_TREE.md` — дерево вопросов для старта задачи.
- `FIRST_PROMPT.md` — первый промпт, который надо отправить в Codex после открытия папки.

## Быстрый старт

1. Распакуй архив в отдельную папку или в корень существующего проекта.
2. Открой эту папку в Codex.
3. Отправь содержимое `FIRST_PROMPT.md` первым сообщением.
4. Ответь на вопросы Intake Orchestrator.
5. Подтверди состав субагентов и план.
6. Только после этого разрешай реализацию.

## Важная идея

Этот комплект сделан не для того, чтобы Codex сразу бросался писать код. Он заставляет Codex сначала:

1. пробрифовать тебя;
2. обновить `TASK.md`;
3. выбрать нужные роли;
4. составить план;
5. зафиксировать прогресс в `CHRONICLE.md`;
6. попросить подтверждение на реализацию.

Так Codex работает как управляемая продуктовая команда, а не как взволнованный автокомплит на энергетиках.

## Минимальный состав команды

Системные роли, которые должны участвовать почти всегда:

- Task Intake Orchestrator — проводит стартовый брифинг и выбирает команду.
- Chronicle Keeper — ведёт летопись прогресса, решений и открытых вопросов.

Семь основных продуктово-инженерных ролей:

1. Product Strategist
2. UX Interaction Reviewer
3. Design System Guardian
4. Frontend Architect
5. Backend Architect
6. QA Engineer
7. Code Reviewer

## Главный рабочий цикл

```text
Brief → TASK.md → Team selection → Plan → Approval → Implementation → Review → CHRONICLE.md
```

## Как использовать в существующем проекте

Можно положить файлы в корень репозитория. Если в проекте уже есть `AGENTS.md`, не затирай его вслепую. Лучше:

1. сохрани текущий файл как `AGENTS.project-original.md`;
2. объедини уникальные проектные правила с этим комплектом;
3. оставь ссылки на `TASK.md`, `CHRONICLE.md`, `docs/QUESTION_TREE.md` и playbooks.

## Что можно менять под себя

- Команды запуска, тестов и линтинга в `AGENTS.md`.
- Список high-risk changes.
- Дерево вопросов в `docs/QUESTION_TREE.md`.
- Ролевые инструкции в `.agents/playbooks/`.
- Custom agents в `.codex/agents/`.

## Рекомендуемая команда проверки после установки

Попроси Codex:

```text
Summarize the active project instructions, list the available custom agents and skills, and explain the required workflow before implementation.
```

Если Codex не упоминает `TASK.md`, `CHRONICLE.md`, role selection и approval gate, значит инструкции не подхватились или стартовая папка выбрана неправильно.
