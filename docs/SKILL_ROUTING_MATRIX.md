# SKILL_ROUTING_MATRIX.md

## UI task
- design-recon
- screen-redesign
- state-matrix
- design-system-compliance
- visual-qa-loop
- ui-heuristic-audit

## Existing repo
- repo-recon
- relevant architecture/design skills

## Design system present
- design-recon
- design-system-manifest
- design-system-compliance
- component-contract-scan

## AI feature
- ai-ml-planning
- model-evaluation
- ai-safety-review
- threat-modeling
- privacy-impact-review

## Research
- ux-research-planning / market-research-planning / cx-journey-mapping
- research-ops if actual study execution is planned


## Operational UI routing

| Situation | Required skills |
|---|---|
| UI prototype, no DS | design-recon, prototype-ui-kit, screen-redesign, state-matrix, ui-heuristic-audit |
| Existing DS in code | repo-recon, design-recon, design-system-manifest, design-system-compliance, ds-code-contract-enforcement |
| Module design for developer rebuild | design-recon, module-design, design-handoff-qa, handoff-docs |
| Implemented UI | design-system-compliance, component-contract-scan, visual-qa-loop, ui-heuristic-audit, design-qa |
| Production web/service | production-service-planning, production-readiness-review, implementation-review |


## Taste, culture, and anticipation

| Situation | Recommended skills |
|---|---|
| New/redesigned UI with subjective quality/taste impact | taste-calibration, taste-review |
| Prototype with no DS and visual direction unknown | prototype-ui-kit, taste-calibration |
| UI feels technically correct but not good enough | taste-review, creative-tension-review |
| New idea/signal may improve the task | anticipation-radar, proactive-proposal-review |
| Opportunity event during planning | opportunity-event-triage, creative-improvement-loop or creative-tension-review |
| Design handoff with quality concern | design-handoff-qa, taste-review |


## Taste / culture / anticipation

| Situation | Required / recommended skills |
|---|---|
| New product/interface concept with unclear feel | taste-calibration, example-taste-board if examples exist |
| UI prototype or redesign where craft matters | taste-calibration, taste-review |
| User supplied good/bad references | example-taste-board, taste-calibration, taste-review |
| Adequate solution could be materially better | creative-tension-review |
| Team should propose likely improvements before implementation | expectation-anticipation |
| Approved UI artifact before final handoff | taste-review, design-qa |

Rules:
- Taste skills are not evidence substitutes.
- Anticipation proposals A2/A3/A4 require approval before implementation.
- Do not use these skills for Tiny/Fast Lane mechanical tasks unless requested.


## Runtime stability and current-page review skills

Use these skills to prevent stalled or over-broad subagent workflows:

- `subagent-run-contract`: before any real spawned workflow.
- `subagent-failure-recovery`: when spawned agents are running too long, fail, duplicate, or return unusable artifacts.
- `ui-review-packet`: before asking UI/design reviewers to inspect a rendered page.
- `current-page-ui-review`: for bounded page/prototype review with PASS/WARN/BLOCKED verdict.

For current-page UI review, prefer `ui-review-packet` + `current-page-ui-review` before spawning multiple role-specific agents.

## Reference / authority / visual acceptance routing

- User provides reference screenshot/mock/example → `reference-fidelity`, `screenshot-reference-comparison`.
- User provides good/bad examples → `example-taste-board`, `reference-fidelity`, `taste-review`.
- DS manifest/registry created, changed, or used → `design-source-authority`, `manifest-freeze-check`.
- Rendered UI exists → `screenshot-reference-comparison`, `visual-qa-loop`.
- Prototype/demo/sample content exists → `content-realism-review`.
- Debug/prototype controls visible → `debug-control-review`.
