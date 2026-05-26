# PHASED_ORCHESTRATION.md

Use phased orchestration when a task spans multiple product/engineering/risk domains or when a production web/service is being planned.

## Why

A large team launched at once creates token waste, duplicated analysis, and conflicting recommendations. Phases keep the work sequenced and auditable.

## Default phases

### Phase 0: Intake and route
- Classify task, complexity, work mode, UI/DS state, repo state, risk state.
- Ask only questions that can change scope, risk, team, acceptance criteria, verification, or handoff.

### Phase 1: Recon
- Existing repo: `repo-recon`.
- UI/design: `design-recon`.
- Existing DS: `design-system-manifest` or load existing DS docs.
- Output: Recon briefs and blockers.

### Phase 2: Product/design/architecture planning
- Select only roles that own required artifacts.
- Produce planning artifacts before implementation.
- For modules: `Module Design Package`.
- For screens: `Screen Design Spec`.
- For production services: `Service Architecture Plan`.

### Phase 3: Risk and readiness gates
- Security/privacy/performance/release/migration/AI roles only when triggered.
- Use gate verdicts: PASS, PASS WITH WARNINGS, BLOCKED.

### Phase 4: Implementation or handoff
- Implementation mode: implement approved scope only.
- Design-only handoff mode: produce developer rebuild artifacts and do not modify product code unless requested.

### Phase 5: Verification and review
- Run relevant tests/scripts/checks.
- UI: visual/design QA and DS compliance.
- Production: readiness checklist and rollback notes.
- Final: summarize evidence, deviations, risks, and next actions.

## Anti-patterns

- Launching 10+ specialists before recon.
- Starting UI implementation before DS mode is known.
- Treating a module as a collection of unrelated screens.
- Treating design handoff as code implementation.
