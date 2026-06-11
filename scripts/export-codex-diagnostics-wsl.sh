#!/usr/bin/env bash
set -euo pipefail

stamp="$(date +%Y%m%d-%H%M%S)"
out="codex-diagnostic-pack-${stamp}"
zip_path="${out}.zip"
mkdir -p "$out"/{codex,project,artifacts}

codex_home="${CODEX_HOME:-$HOME/.codex}"

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    cp -a "$src" "$dst"
  fi
}

# Codex state. Never copy auth.json.
copy_if_exists "$codex_home/config.toml" "$out/codex/config.toml"
copy_if_exists "$codex_home/history.jsonl" "$out/codex/history.jsonl"

if [ -d "$codex_home/sessions" ]; then
  mkdir -p "$out/codex/sessions-latest"
  find "$codex_home/sessions" -type f -printf '%T@ %p\n' 2>/dev/null \
    | sort -nr \
    | head -n 30 \
    | cut -d' ' -f2- \
    | while IFS= read -r f; do cp -a "$f" "$out/codex/sessions-latest/" || true; done
fi

if [ -d "$codex_home/archived_sessions" ]; then
  mkdir -p "$out/codex/archived-sessions-latest"
  find "$codex_home/archived_sessions" -type f -printf '%T@ %p\n' 2>/dev/null \
    | sort -nr \
    | head -n 10 \
    | cut -d' ' -f2- \
    | while IFS= read -r f; do cp -a "$f" "$out/codex/archived-sessions-latest/" || true; done
fi

# Optional TUI log if user started Codex with: codex -c log_dir=./.codex-log
if [ -d ".codex-log" ]; then
  cp -a .codex-log "$out/codex/project-codex-log"
fi

# Framework / project memory state.
for f in \
  AGENTS.md FIRST_PROMPT.md TASK.md CURRENT.md TASK_INDEX.md CHRONICLE.md README.md \
  docs/BOOTSTRAP_INDEX.md docs/LANGUAGE_POLICY.md docs/RUNTIME_LOAD_POLICY.md \
  docs/TICKETED_MEMORY.md docs/CONTEXT_BUDGET_POLICY.md docs/SKILL_DISCOVERY_POLICY.md \
  docs/UI_QUALITY_GATES.md docs/REFERENCE_FIDELITY.md docs/DESIGN_SOURCE_AUTHORITY.md \
  docs/MANIFEST_FREEZE_POLICY.md docs/SCREENSHOT_VISUAL_GATE.md docs/TASTE_PROFILE.md \
  docs/TASTE_REVIEW.md docs/SUBAGENT_ORCHESTRATION.md docs/SUBAGENT_RUN_CONTRACT.md \
  docs/SUBAGENT_FAILURE_POLICY.md docs/SCENARIO_TESTS.json; do
  copy_if_exists "$f" "$out/project/$f"
done

if [ -d tasks ]; then
  mkdir -p "$out/project/tasks"
  find tasks -maxdepth 1 -type f -name 'TKT-*.md' -print0 | xargs -0 -r cp -a -t "$out/project/tasks"
fi

if [ -d context/packets ]; then
  mkdir -p "$out/project/context/packets"
  find context/packets -maxdepth 1 -type f -print0 | xargs -0 -r cp -a -t "$out/project/context/packets"
fi

if [ -d context/snapshots ]; then
  mkdir -p "$out/project/context/snapshots"
  find context/snapshots -maxdepth 1 -type f -printf '%T@ %p\n' 2>/dev/null \
    | sort -nr | head -n 5 | cut -d' ' -f2- \
    | while IFS= read -r f; do cp -a "$f" "$out/project/context/snapshots/" || true; done
fi

# Common DS sources if present.
copy_if_exists docs/design-system "$out/project/docs/design-system"
copy_if_exists .codex/agents "$out/project/.codex/agents"

# Selected skills likely involved in UI/design/runtime failures.
for s in \
  reference-fidelity screenshot-reference-comparison design-source-authority manifest-freeze-check \
  design-system-compliance component-contract-scan visual-qa-loop current-page-ui-review \
  ui-review-packet content-realism-review debug-control-review taste-review design-recon \
  subagent-run-contract subagent-failure-recovery ticket-router task-ledger context-prune \
  context-snapshot memory-integrity-check; do
  if [ -d ".agents/skills/$s" ]; then
    mkdir -p "$out/project/.agents/skills/$s"
    cp -a ".agents/skills/$s"/* "$out/project/.agents/skills/$s/"
  fi
done

# Git status/diff.
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short > "$out/project/git-status.txt" || true
  git diff > "$out/project/diff.patch" || true
  git diff --name-only > "$out/project/changed-files.txt" || true
fi

# Useful environment breadcrumbs, no secrets.
{
  echo "date=$(date -Is)"
  echo "pwd=$(pwd)"
  echo "user=$(whoami)"
  echo "wsl_distro=${WSL_DISTRO_NAME:-}"
  echo "codex_home=$codex_home"
  command -v codex >/dev/null 2>&1 && echo "codex_path=$(command -v codex)"
  command -v node >/dev/null 2>&1 && echo "node=$(node --version)"
  command -v npm >/dev/null 2>&1 && echo "npm=$(npm --version)"
  command -v git >/dev/null 2>&1 && echo "git=$(git --version)"
} > "$out/project/environment.txt"

cat > "$out/README_REDACT_BEFORE_SHARING.md" <<'RED'
Before sharing this diagnostic pack:

- inspect codex/history.jsonl and sessions-latest;
- redact secrets, tokens, cookies, internal URLs, customer data;
- remove ~/.codex/auth.json if it was added manually;
- remove .env files, node_modules, dist/build/cache outputs.
RED

# Use python zipfile if zip is unavailable.
if command -v zip >/dev/null 2>&1; then
  zip -qr "$zip_path" "$out"
else
  python3 - <<PY
import shutil
shutil.make_archive("$out", "zip", "$out")
PY
fi

echo "Created diagnostic pack: $zip_path"
echo "Inspect and redact before sharing."
