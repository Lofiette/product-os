# 4.0 Risk Register

| ID | Риск | Вероятность | Влияние | Контроль |
|---|---|---:|---:|---|
| R-01 | 4.0 станет ещё больше 3.0 | Высокая | Высокое | Plugin split, no-new-skill rule, size measured by active metadata |
| R-02 | Kernel снова распухнет | Высокая | Высокое | Loader contract, CI byte trend, task policy in skills/hooks |
| R-03 | Глубина roles останется номинальной | Высокая | Высокое | Methodology audit, evidence schemas, role-specific evals |
| R-04 | Skills будут переименованным boilerplate | Высокая | Высокое | 44-skill rewrite backlog, trigger/non-trigger tests |
| R-05 | Approval lease станет слишком широким | Средняя | Высокое | Expiration, forbidden list, scope diff, audit log |
| R-06 | Product Knowledge устареет | Высокая | Высокое | Source revision, path triggers, freshness linter |
| R-07 | SQLite и Markdown разойдутся | Средняя | Высокое | Single write API, reconciliation check, generated projections |
| R-08 | Vector recall выдаст ложное совпадение | Средняя | Среднее | Candidate-only retrieval, open canonical source |
| R-09 | External services станут скрытой dependency | Средняя | Высокое | Offline CI, adapter disable tests, local fallbacks |
| R-10 | Plugin metadata снова вытеснит skills | Средняя | Высокое | Domain activation, metadata budget eval |
| R-11 | Worker fan-out съест токены | Средняя | Высокое | depth=1, max workers, cost budget, read-heavy defaults |
| R-12 | Parallel writes конфликтуют | Средняя | Высокое | worktrees/disjoint scopes, merge owner, conflict test |
| R-13 | Compaction потеряет runtime state | Средняя | Высокое | Pre/PostCompact checkpoints, mismatch gate |
| R-14 | Micro protocol обойдёт важный gate | Средняя | Высокое | eligibility classifier, risk triggers, escalation rules |
| R-15 | Evals будут тестировать только happy path | Высокая | Высокое | mutation tests, forbidden actions, failure fixtures |
| R-16 | Универсальный core получит конкретные имена | Средняя | Среднее | terminology scanner, synthetic fixtures |
| R-17 | Override будет ошибочно считаться поддерживаемым режимом | Средняя | Среднее | Explicit out-of-contract documentation, no override tests |
| R-18 | Миграция повредит custom setup | Низкая/средняя | Высокое | dry-run, backup, unknown-file preservation, rollback |
