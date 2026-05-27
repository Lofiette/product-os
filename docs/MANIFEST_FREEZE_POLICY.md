# MANIFEST_FREEZE_POLICY.md

This policy prevents design-system manifests from becoming moving targets during implementation.

## Before implementation

If a DS manifest exists:
- snapshot its path and checksum if possible;
- treat it as the baseline.

If no manifest exists but DS sources exist:
- create a candidate manifest only from existing DS sources;
- mark it `candidate`;
- ask the user whether it can be used as compliance authority.

If no DS exists:
- do not create a DS manifest to validate UI;
- create a `Prototype UI Kit Contract` instead;
- mark any manifest-like artifact as `provisional`.

## During implementation

Do not materially change the baseline manifest and then use it as proof of compliance.

If manifest changes are needed:
1. stop;
2. explain why;
3. show diff;
4. ask approval;
5. check current implementation against the pre-change baseline and record approved deviations separately.

## Final report

Report:
- baseline manifest path;
- whether it existed before task;
- whether it changed;
- whether it was used as authority;
- approved deviations;
- remaining unproven compliance claims.
