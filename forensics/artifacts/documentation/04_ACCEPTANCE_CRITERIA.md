# 4.0 Acceptance Criteria

## Alpha 1 — Runtime Kernel

- Root `AGENTS.md` является небольшим loader, а не энциклопедией.
- Есть machine-readable runtime state.
- `current_task: null` поддерживается штатно.
- `TKT-000` опционален.
- Micro Change Protocol работает.
- Authorization lease schema валидируется.
- Runtime checkpoint восстанавливается после synthetic compaction.
- Core не зависит от внешних сервисов.

## Alpha 2 — Distribution and Expertise

- Core распространяется как plugin + repo scaffold.
- Domain packs включаются независимо.
- Все 50 roles сохранены и зарегистрированы.
- Worker archetypes отделены от roles.
- 95 skills проаудированы; aliases и boilerplates имеют решения.
- Critical skills углублены и имеют output schemas/evals.

## Beta 1 — Knowledge and Enforcement

- Product Knowledge schema типизирована.
- Claim provenance и evidence depth работают.
- Freshness triggers сопоставляются с file changes.
- Scoped approvals работают без постоянного микроменеджмента.
- Hooks/rules усиливают critical invariants.
- Existing, greenfield и redesign fixtures проходят.

## Beta 2 — Orchestration and Evals

- Worker timeout/cancel/quorum работают.
- Parallel worktree case проходит.
- Eval harness исполняет минимум 15 critical cases.
- Token/tool/approval budgets измеряются.
- Metadata truncation case не скрывает critical skills.
- Subagent compaction/reconnect case восстанавливает registry.

## Release Candidate

- Все P0/P1 work items закрыты.
- Нет project-specific names в universal core.
- Core работает offline/local без external services.
- Optional adapters имеют graceful fallback.
- 3.x migration и rollback протестированы.
- Cross-platform tests: Linux/WSL, macOS, Windows supported surfaces.
- Security review и privacy review завершены.
- Документация объясняет архитектуру, установку, operation и troubleshooting.
- Behavioral scorecard не хуже 3.0 по качеству и существенно лучше по context/approval/maintainability metrics.

## Quality guardrails

Нельзя считать критерий выполненным только потому, что файл существует. Для critical capabilities требуется:
- behavioral test;
- evidence trace;
- negative test;
- failure-mode test;
- documented fallback.
