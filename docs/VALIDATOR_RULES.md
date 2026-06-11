# VALIDATOR_RULES.md

Validator checks:
- all role IDs have role card, playbook, TOML agent;
- all skills in SKILL_INDEX have SKILL.md;
- role skill maps reference existing skills;
- no codenames fields;
- no character codename policy;
- required v2.0 docs exist;
- scenario tests reference known roles/skills;
- no .bak/.tmp files;
- TOML valid;
- root zip integrity.


## Culture, taste, and anticipation validator additions

- Required culture/taste/anticipation docs exist.
- Required culture/taste/anticipation skills exist and are listed in SKILL_INDEX.
- FIRST_PROMPT includes agent naming policy and taste/anticipation handling.
- Scenario markdown matches SCENARIO_TESTS.json.
- TOML agent instructions include no-alias rule.


## Culture/taste/anticipation rules

Validator must check:
- TEAM_CULTURE.md exists;
- TASTE_PROFILE.md exists;
- TASTE_REVIEW.md exists;
- EXPECTATION_ANTICIPATION.md exists;
- required taste/anticipation skills are indexed and have SKILL.md;
- scenario markdown matches SCENARIO_TESTS.json;
- no personal agent display names or codenames appear in core orchestration docs;
- FIRST_PROMPT includes exact-agent-ID naming rule.
