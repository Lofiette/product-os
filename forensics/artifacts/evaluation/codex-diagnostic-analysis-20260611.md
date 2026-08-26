# Codex Diagnostic Analysis — 2026-06-11

## Verdict

**PASS: diagnostic pack is useful.** It explains why context compaction is happening so often and why the current working environment is not yet benefiting from the newer ticketed-memory architecture.

**Core diagnosis:** this VS Code Codex session is operating with a very large effective context floor. After each compaction, the next request still starts around **186k–220k input tokens**, and just before compaction it reaches **235k–251k input tokens** in a 258k context window. That is why compaction can happen repeatedly inside normal work.

## Key evidence

### Environment

- Project: `/home/lofiette/ai-web`
- WSL: `Ubuntu`
- Codex mode: VS Code extension, `codex` CLI not installed in WSL
- Config: `model = "gpt-5.5"`, `model_reasoning_effort = "medium"`
- Codex home: `/home/lofiette/.codex`

### Session size

The main session transcript is enormous:

- `rollout-2026-06-01T11-54-33-...jsonl`
- Size: **1,154 MB**
- Longest single JSONL lines: **~40 MB**
- The giant lines are likely encrypted reasoning / internal state payloads, so full transcript export is not practical.

### Context compaction events found in the extracted tail

The tail extract contains **16 `context_compacted` events** between `2026-06-11T09:23Z` and `2026-06-11T14:14Z`.

| Time UTC | Previous visible token event | Next request input |
|---|---:|---:|
| 09:23:18 | compaction event total 139,864 | 186,608 |
| 09:58:57 | compaction event total 145,029 | 195,207 |
| 10:04:15 | compaction event total 144,816 | 194,985 |
| 10:43:23 | compaction event total 146,724 | 197,973 |
| 10:53:53 | compaction event total 147,772 | 198,948 |
| 11:27:08 | compaction event total 146,504 | 197,635 |
| 11:34:33 | compaction event total 148,028 | 199,153 |
| 12:29:04 | compaction event total 153,655 | 208,009 |
| 12:38:23 | compaction event total 155,606 | 210,110 |
| 12:52:27 | compaction event total 152,978 | 207,487 |
| 13:08:51 | compaction event total 153,667 | 208,133 |
| 13:24:25 | compaction event total 152,863 | 207,339 |
| 13:46:27 | compaction event total 157,853 | 214,353 |
| 13:55:29 | compaction event total 156,289 | 212,869 |
| 14:08:46 | compaction event total 160,191 | 219,089 |
| 14:14:35 | compaction event total 161,090 | 220,002 |

Interpretation: compaction is not really making the next request small. It produces a huge compacted baseline, then normal file reads/tool outputs push the next turn back near the limit.

### Token usage at the end of the session

The last visible token event:

- `last_token_usage.input_tokens`: **244,185**
- `last_token_usage.cached_input_tokens`: **208,768**
- Context window: **258,400**

This is essentially operating at the edge of the context window each request.

### Tool usage pattern

In the tail extract:

- Function calls: **463**
- Function outputs: **363**
- Commands with high `max_output_tokens`:
  - `12000`: 118 commands
  - `20000`: 81 commands
  - `30000`: 58 commands
  - `40000`: 12 commands
  - `50000`: 4 commands

This is not the only cause of context pressure, but it is a clear amplifier.

Examples of high-ceiling commands:

- `npm run build` with `max_output_tokens: 50000`
- `git diff` with `max_output_tokens: 50000`
- multi-file `sed` reads with `max_output_tokens: 30000–40000`
- large `rg` scans with `max_output_tokens: 30000–40000`

### Current project memory is still old-style

The current root project still uses:

- `TASK.md` as source of truth
- `CHRONICLE.md` as current memory

`CHRONICLE.md` size in diagnostic pack:

- **71,149 bytes**

Root `AGENTS.md` explicitly says:

- “Current project task state: `TASK.md`.”
- “Current project memory: `CHRONICLE.md`.”
- “Keep durable project notes compact and update `TASK.md` and `CHRONICLE.md` when the working direction changes.”

This project is not yet using the 2.1 ticketed-memory architecture (`CURRENT.md`, `TASK_INDEX.md`, active tickets, compact `CHRONICLE.md`). That is a major reason context economy improvements are not showing up in this environment.

### Subagent evidence

In the extracted tail there are no clear structured runtime events like `SubagentStart` / `SubagentStop` / `agent_id` from actual spawned agents. “Subagent” appears mainly in docs/text.

Root `AGENTS.md` also says:

> Use the copied Codex Product Team methodology as a lightweight checklist, not as real autonomous subagents unless the user asks for that explicitly.

So, in this environment, the default is role-simulation/checklist behavior, not real subagent orchestration.

## Practical failure modes

### 1. Compaction baseline is too large

After compaction, the next turn still starts at roughly 186k–220k input tokens. This means the compacted summary plus always-carried context is far too large.

Likely contributors:

- long-lived single session with many days of work;
- large `CHRONICLE.md`;
- old `TASK.md` + `CHRONICLE.md` memory model;
- repeated project/source/design-system reads;
- high-output tool calls;
- possibly large internal compacted summaries preserving too much historical state.

### 2. `CHRONICLE.md` is acting as an archive, not a rescue summary

It contains a long multi-day history. This is useful as archive, but harmful as always-current context.

Expected 2.1 behavior:

- `CHRONICLE.md`: 300–600 words rescue summary.
- Full history: `chronicle/YYYY-MM-DD-session-log.md`.
- Active work details: `tasks/TKT-xxx.md`.

### 3. Tool output ceilings are too generous

The agent often asks for `max_output_tokens` far above what is needed. Even when outputs are not huge, this habit allows runaway context bursts.

### 4. Same files are re-read after compaction

After compaction events, the agent often re-loads skills/docs/source snippets. This is expected, but expensive because the baseline is already huge.

### 5. Real subagent orchestration is not visible in the extracted runtime

The project appears to be using role-simulation/checklist mode by default. That is okay for many UI tasks, but it means “roles” do not create independent review unless explicitly spawned.

### 6. Current diagnostic project state does not include `.agents/` / `.codex/`

Session logs reference `.agents/skills`, but the diagnostic project snapshot does not include `.agents` or `.codex`. This suggests the project state changed after the problematic run, or the local methodology lives elsewhere / was ignored / removed.

This limits exact reconstruction of skill behavior.

## Recommendations before next test

### P0 — immediate, high-value changes

1. **Move this project to ticketed memory**

   Replace current root memory with:

   - `CURRENT.md`
   - `TASK_INDEX.md`
   - `tasks/TKT-xxx.md`
   - short `CHRONICLE.md`
   - `TASK.md` as compatibility pointer only

2. **Compress `CHRONICLE.md` now**

   Target:

   - keep only current objective, blockers, decisions, and next action;
   - move long history to `chronicle/2026-06-01-to-2026-06-11-session-log.md`.

3. **Start a fresh Codex session after memory migration**

   The current session transcript is already huge. Continuing it will preserve a swollen compacted baseline.

4. **Add a tool output budget policy to project `AGENTS.md`**

   Suggested defaults:

   - normal `sed`: max 4k–8k output tokens;
   - multi-file reads: avoid unless necessary;
   - `git diff`: use `--stat` first, then targeted file diff;
   - build output: 8k–12k unless build fails;
   - no `max_output_tokens=50000` without explicit reason.

5. **Keep `CHRONICLE.md` under a hard threshold**

   Suggested warning threshold: 10 KB.
   Suggested target: 3–6 KB.

### P1 — workflow improvements

6. **Use bounded UI review packets**

   For UI work, subagents or simulated roles should receive a bounded `UI Review Packet`, not the entire project history.

7. **Make “resume after compaction” load only active ticket**

   After compaction, the assistant should not reload all memory docs. It should load `CURRENT.md`, active ticket, and the relevant operation packet only.

8. **Separate design-system kit archive from runtime**

   `SOVA_DESIGN_SYSTEM_KIT` is useful, but runtime should load only selected entrypoints, not broad file trees or generated sources by default.

9. **Prefer exact skill IDs for critical design workflows**

   Do not rely on implicit discovery for:

   - `reference-fidelity`
   - `design-system-compliance`
   - `design-source-authority`
   - `screenshot-reference-comparison`
   - `visual-qa-loop`

### P2 — diagnostics

10. **Use a session-extract based diagnostic exporter**

   Never export full session transcripts. The largest JSONL file here is 1.15 GB.

11. **If possible, enable lightweight logs/hooks for future runs**

   Capture compaction, subagent, skill, and file-load events as small external logs instead of full transcripts.

## Suggested next experiment

1. Apply ticketed memory to this project.
2. Start a new Codex thread.
3. Give one medium UI task.
4. Require:
   - exact active ticket;
   - exact skills loaded;
   - no broad file reads;
   - no tool output >12k unless error;
   - final token/compaction observation.
5. Compare compaction frequency to this diagnostic baseline.

## Bottom line

The frequent context compression is not mysterious. The session is living at the edge of the context window:

- before compaction: often 235k–251k input tokens;
- after compaction: still 186k–220k input tokens;
- current `CHRONICLE.md`: 71 KB;
- old `TASK.md` / `CHRONICLE.md` memory model still active;
- high-output commands are common;
- the session is long-lived and already huge.

The 2.1 ticketed-memory architecture is the right direction, but it is not yet applied to this project snapshot. The next useful step is not another generic role/skill patch. It is a migration of the working project to ticketed memory plus a stricter tool-output budget.
