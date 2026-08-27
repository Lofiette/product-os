#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POWERSHELL_HELPER = ROOT / "scripts" / "register-codex-marketplace.ps1"
BASH_HELPER = ROOT / "scripts" / "register-codex-marketplace.sh"


def require_ordered(source: str, snippets: list[str], label: str) -> None:
    cursor = -1
    for snippet in snippets:
        position = source.find(snippet, cursor + 1)
        if position < 0:
            raise AssertionError(f"{label}: missing required contract {snippet!r}")
        cursor = position


def run_syntax_check(command: list[str], label: str) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{label} syntax validation failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def validate_powershell() -> bool:
    source = POWERSHELL_HELPER.read_text(encoding="utf-8")
    require_ordered(
        source,
        [
            "[string]$Source = 'Lofiette/product-os'",
            "[string]$Ref = 'v4.1.0'",
            "$MarketplaceOutput = (& codex plugin marketplace list",
            "$ManagerRootPattern =",
            "if ($MarketplaceRoot -match $ManagerRootPattern)",
            "& codex plugin marketplace upgrade $MarketplaceName",
            "& codex plugin marketplace add $Source --ref $Ref",
            "& codex plugin add \"$Plugin@$MarketplaceName\"",
            "& codex plugin list",
        ],
        "PowerShell helper",
    )

    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        return False
    helper_path = str(POWERSHELL_HELPER).replace("'", "''")
    parser_command = (
        f"$path='{helper_path}'; "
        "$tokens=$null; $errors=$null; "
        "[System.Management.Automation.Language.Parser]::ParseFile("
        "$path, [ref]$tokens, [ref]$errors) > $null; "
        "if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }"
    )
    run_syntax_check(
        [executable, "-NoProfile", "-Command", parser_command],
        "PowerShell helper",
    )
    return True


def validate_bash() -> bool:
    source = BASH_HELPER.read_text(encoding="utf-8")
    require_ordered(
        source,
        [
            'source_repo="Lofiette/product-os"',
            'release_ref="v4.1.0"',
            'marketplace_output="$(codex plugin marketplace list)"',
            'if [[ "$normalized_line" == *"/.product-os/sources/product-os/"* ]]',
            'codex plugin marketplace upgrade "$marketplace_name"',
            'codex plugin marketplace add "$source_repo" --ref "$release_ref"',
            'codex plugin add "cpt-core@${marketplace_name}"',
            'codex plugin add "cpt-design-ui@${marketplace_name}"',
            "codex plugin list",
        ],
        "Bash helper",
    )

    executable = shutil.which("bash")
    if not executable:
        return False
    run_syntax_check([executable, "-n", str(BASH_HELPER)], "Bash helper")
    return True


def main() -> int:
    powershell = validate_powershell()
    bash = validate_bash()
    if not powershell and not bash:
        raise SystemExit("Neither PowerShell nor Bash is available for helper syntax validation")
    print(
        "MARKETPLACE HELPER VALIDATION PASSED; "
        f"powershell={'PASS' if powershell else 'SKIP'}, bash={'PASS' if bash else 'SKIP'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
