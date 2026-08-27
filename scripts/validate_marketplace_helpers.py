#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
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


def exercise_helper(executable: str, helper: Path, *, powershell: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="product-os-marketplace-helper-") as raw_tmp:
        tmp = Path(raw_tmp)
        fake = tmp / "fake_codex.py"
        fake.write_text(
            """from __future__ import annotations
import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
with Path(os.environ["FAKE_CODEX_LOG"]).open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\\n")
if args[:3] == ["plugin", "marketplace", "list"]:
    line = os.environ.get("FAKE_CODEX_MARKETPLACE_LINE", "")
    if line:
        print(line)
failure = os.environ.get("FAKE_CODEX_FAIL_CONTAINS", "")
if failure and failure in " ".join(args):
    raise SystemExit(9)
""",
            encoding="utf-8",
        )
        (tmp / "codex.cmd").write_text(
            '@echo off\r\n"%FAKE_CODEX_PYTHON%" "%~dp0fake_codex.py" %*\r\nexit /b %ERRORLEVEL%\r\n',
            encoding="utf-8",
        )
        bash_wrapper = tmp / "codex"
        bash_wrapper.write_text(
            '#!/usr/bin/env bash\nexec "$FAKE_CODEX_PYTHON" "$(dirname "$0")/fake_codex.py" "$@"\n',
            encoding="utf-8",
        )
        bash_wrapper.chmod(0o755)

        log = tmp / "calls.jsonl"
        base_env = os.environ.copy()
        base_env.update(
            {
                "PATH": str(tmp) + os.pathsep + base_env.get("PATH", ""),
                "FAKE_CODEX_LOG": str(log),
                "FAKE_CODEX_PYTHON": sys.executable,
            }
        )

        def invoke(args: list[str], marketplace_line: str = "", fail: str = "") -> tuple[subprocess.CompletedProcess[str], list[list[str]]]:
            log.unlink(missing_ok=True)
            env = base_env.copy()
            env["FAKE_CODEX_MARKETPLACE_LINE"] = marketplace_line
            env["FAKE_CODEX_FAIL_CONTAINS"] = fail
            command = (
                [executable, "-NoProfile", "-File", str(helper), *args]
                if powershell
                else [executable, str(helper), *args]
            )
            result = subprocess.run(
                command,
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=60,
            )
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
            return result, calls

        fresh, calls = invoke([])
        assert fresh.returncode == 0, fresh.stderr or fresh.stdout
        assert ["plugin", "marketplace", "add", "Lofiette/product-os", "--ref", "v4.1.0"] in calls
        assert ["plugin", "add", "cpt-core@product-os"] in calls
        assert ["plugin", "add", "cpt-design-ui@product-os"] in calls

        repeated, calls = invoke([], "product-os /tmp/codex/plugins/marketplaces/product-os")
        assert repeated.returncode == 0, repeated.stderr or repeated.stdout
        assert not any(call[:3] == ["plugin", "marketplace", "add"] for call in calls)
        assert ["plugin", "add", "cpt-core@product-os"] in calls

        explicit_ref_args = ["-Ref", "v4.1.0"] if powershell else ["--ref", "v4.1.0"]
        explicit_ref, calls = invoke(
            explicit_ref_args,
            "product-os /tmp/codex/plugins/marketplaces/product-os",
        )
        assert explicit_ref.returncode != 0
        assert "does not expose enough provenance" in (explicit_ref.stderr + explicit_ref.stdout)
        assert not any(call[:2] == ["plugin", "add"] for call in calls)

        explicit_source_args = (
            ["-Source", "other-owner/product-os"]
            if powershell
            else ["--source", "other-owner/product-os"]
        )
        explicit_source, calls = invoke(
            explicit_source_args,
            "product-os /tmp/codex/plugins/marketplaces/product-os",
        )
        assert explicit_source.returncode != 0
        assert "does not expose enough provenance" in (explicit_source.stderr + explicit_source.stdout)
        assert not any(call[:2] == ["plugin", "add"] for call in calls)

        manager, calls = invoke(
            ["-Upgrade"] if powershell else ["--upgrade"],
            "product-os /srv/custom/sources/product-os/abcdef1234567890",
        )
        assert manager.returncode != 0
        assert not any(call[:3] == ["plugin", "marketplace", "upgrade"] for call in calls)

        retarget_args = ["-Upgrade", "-Ref", "v4.2.0"] if powershell else ["--upgrade", "--ref", "v4.2.0"]
        retarget, calls = invoke(retarget_args, "product-os /tmp/codex/plugins/marketplaces/product-os")
        assert retarget.returncode != 0
        assert not any(call[:3] == ["plugin", "marketplace", "upgrade"] for call in calls)

        partial, calls = invoke([], fail="plugin add cpt-design-ui@product-os")
        assert partial.returncode != 0
        assert ["plugin", "add", "cpt-core@product-os"] in calls
        assert ["plugin", "add", "cpt-design-ui@product-os"] in calls


def validate_powershell() -> bool:
    source = POWERSHELL_HELPER.read_text(encoding="utf-8")
    require_ordered(
        source,
        [
            "[string]$Source = 'Lofiette/product-os'",
            "[string]$Ref = 'v4.1.0'",
            "$MarketplaceOutput = (& codex plugin marketplace list",
            "$ManagerRootPattern =",
            "$SourceExplicit = $PSBoundParameters.ContainsKey('Source')",
            "$RefExplicit = $PSBoundParameters.ContainsKey('Ref')",
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
    exercise_helper(executable, POWERSHELL_HELPER, powershell=True)
    return True


def validate_bash() -> bool:
    source = BASH_HELPER.read_text(encoding="utf-8")
    require_ordered(
        source,
        [
            'source_repo="Lofiette/product-os"',
            'release_ref="v4.1.0"',
            'source_explicit=false',
            'marketplace_output="$(codex plugin marketplace list)"',
            'if [[ "$normalized_line" =~ /sources/product-os/',
            'if [[ "$ref_explicit" == true ]]',
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
    exercise_helper(executable, BASH_HELPER, powershell=False)
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
