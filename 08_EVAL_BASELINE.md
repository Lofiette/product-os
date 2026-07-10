# 4.0 Evaluation Baseline

## Цель

Сравнивать поведение 3.0 и 4.0 на одинаковых обезличенных задачах, а не оценивать только наличие файлов.

## Golden cases

1. Micro copy/icon change.
2. Systemic UI state change.
3. UI implementation with design-system constraints.
4. API-dependent form behavior.
5. Existing product onboarding.
6. Greenfield MVP bootstrap.
7. Redesign/migration with reference.
8. Product Knowledge freshness after code change.
9. Compaction during long task.
10. Required worker timeout.
11. Optional worker timeout with quorum.
12. Parallel write in worktrees.
13. Security-sensitive API change.
14. Skill discovery metadata pressure.
15. No-active-task startup.
16. Local-only self-contained run without integrations.
17. External semantic recall unavailable.
18. Observability backend unavailable.

## Case schema

```yaml
id:
mode:
fixture:
prompt:
expected_task_protocol:
expected_roles:
expected_skills:
expected_gates:
allowed_reads:
forbidden_reads:
allowed_writes:
forbidden_writes:
approval_expectation:
expected_artifacts:
verification:
budgets:
  input_tokens:
  output_tokens:
  tool_calls:
  approvals:
  workers:
  wall_time:
```

## Score dimensions

- Functional correctness.
- Product/UX quality.
- Engineering quality.
- Scope completeness.
- Role/skill routing accuracy.
- Context efficiency.
- Approval efficiency.
- Evidence quality.
- Knowledge freshness.
- Recovery reliability.
- Subagent efficiency.
- Safety violations.
- User intervention count.

## Private trace conversion

Live traces используются только после:
- удаления имён продуктов/организаций;
- удаления design-system names;
- удаления private paths, code and data;
- замены реальных сущностей синтетическими;
- выделения task, tool trace pattern, failure mode and expected behavior.

Raw transcripts не включаются в distribution.

## Release gate

4.0 RC должен:
- не ухудшить median quality score;
- снизить median always-on context;
- снизить approvals для standard tasks;
- снизить false broad reads;
- снизить compaction recovery failures;
- не увеличить user intervention для micro tasks;
- иметь zero critical safety violations.
