# Skill Trigger Evaluations

## Alpha 3 proxy evaluation

Every active skill has:

- two positive prompts;
- one nearby negative prompt;
- expected invocation behavior;
- ranking checks against every active skill description and positive-example vocabulary.

The proxy evaluator uses deterministic token-weighted similarity. It checks that the expected skill appears within the configured top-k for positive cases and does not dominate its negative case.

Run:

```bash
python tools/eval_skill_triggers.py \
  --root . \
  --write-report evaluation/trigger-eval-report.json
```

## What the proxy catches

- missing trigger coverage;
- descriptions that are too generic;
- obvious collisions between neighboring skills;
- stale registry entries;
- missing negative examples;
- regressions after consolidation or renaming.

## What it does not prove

- that Codex will invoke the skill in a live session;
- that full skill instructions produce the correct behavior;
- that enabled-plugin order has no effect;
- that a skill does not over-trigger on real project context;
- that outputs satisfy product or engineering quality.

## Phase 8 behavioral eval requirements

Executable evals must later include:

- a fixture repository or runtime state;
- the exact enabled plugin profile;
- user prompt;
- expected and forbidden skill selections;
- allowed and forbidden tool trace;
- expected artifact schema;
- context/tool/approval budget;
- deterministic graders plus calibrated LLM graders where necessary.

The Alpha 3 proxy is a preflight test, not behavioral certification.
