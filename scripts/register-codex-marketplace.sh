#!/usr/bin/env bash
set -euo pipefail

source_repo="Lofiette/product-os"
release_ref="v4.1.0"
marketplace_name="product-os"
upgrade=false

usage() {
  cat <<'EOF'
Usage: register-codex-marketplace.sh [options]

Options:
  --source OWNER/REPO_OR_URL  Marketplace source (default: Lofiette/product-os)
  --ref REF                   Immutable release tag or Git ref (default: v4.1.0)
  --marketplace NAME          Marketplace name (default: product-os)
  --upgrade                   Refresh an existing direct Git marketplace
  -h, --help                  Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_repo="${2:?--source requires a value}"
      shift 2
      ;;
    --ref)
      release_ref="${2:?--ref requires a value}"
      shift 2
      ;;
    --marketplace)
      marketplace_name="${2:?--marketplace requires a value}"
      shift 2
      ;;
    --upgrade)
      upgrade=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v codex >/dev/null 2>&1; then
  printf 'Codex CLI was not found on PATH.\n' >&2
  exit 1
fi

marketplace_output="$(codex plugin marketplace list)"
marketplace_line="$(printf '%s\n' "$marketplace_output" | awk -v name="$marketplace_name" '$1 == name { print; exit }')"

if [[ "$upgrade" == true ]]; then
  if [[ -z "$marketplace_line" ]]; then
    printf "Marketplace '%s' is not registered. Run this script without --upgrade first.\n" "$marketplace_name" >&2
    exit 1
  fi
  normalized_line="${marketplace_line//\\//}"
  if [[ "$normalized_line" == *"/.product-os/sources/product-os/"* ]]; then
    printf "Marketplace '%s' is managed by Product OS Manager. Use a confirmed Manager plan-local-git -> prepare -> switch transaction instead of marketplace upgrade.\n" "$marketplace_name" >&2
    exit 1
  fi
  codex plugin marketplace upgrade "$marketplace_name"
else
  if [[ -n "$marketplace_line" ]]; then
    printf "Marketplace '%s' is already registered. Use --upgrade only for a direct Git-backed marketplace; use Product OS Manager for a Manager-owned installation.\n" "$marketplace_name" >&2
    exit 1
  fi
  codex plugin marketplace add "$source_repo" --ref "$release_ref"
fi

codex plugin add "cpt-core@${marketplace_name}"
codex plugin add "cpt-design-ui@${marketplace_name}"
codex plugin list

printf 'Product OS marketplace operation completed. Start a new Codex thread before testing updated skills.\n'
