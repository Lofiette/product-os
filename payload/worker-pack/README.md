# CPT Optional Worker Pack

This optional pack exposes ten narrow custom Codex agents used by the CPT managed orchestration plane. It is not installed by default.

Logical roles remain accountability lenses. Worker archetypes are execution containers that receive bounded contracts from the main thread.

## Included workers

- `cpt_explorer`
- `cpt_researcher`
- `cpt_product_mapper`
- `cpt_design_reviewer`
- `cpt_implementer`
- `cpt_test_runner`
- `cpt_code_reviewer`
- `cpt_risk_reviewer`
- `cpt_knowledge_curator`
- `cpt_incident_investigator`

Install through `tools/cpt_dist.py workers-install`. Review the files before enabling them. Workers inherit the parent task's live permission and approval choices unless the host applies a stricter agent-specific setting.
