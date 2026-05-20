# Scenario test: Russian user, compact English artifacts

## User request
“Мне удобнее общаться на русском. Сделай MVP формы обратной связи, но не жги токены.”

## Expected behavior
- Assistant replies to user in Russian.
- TASK.md and CHRONICLE.md are maintained in compact English.
- Product UI language is asked or set explicitly.
- UX Writer writes product copy in product UI language, not automatically in Russian.
- Team uses fast lane or standard routing depending on scope.

## Expected roles
- Yuna / Intake Orchestrator
- Aerith / Chronicle Keeper if files change
- Cid / Team Architect
- Garnet / UX Writer if UI copy matters
- Rinoa / UX Interaction Reviewer if flow/states matter
- Rikku / QA Engineer
