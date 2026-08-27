$ErrorActionPreference = 'Stop'

$hookPath = Join-Path $PSScriptRoot 'cpt_hook.py'
$pythonPath = $null
$pythonArgs = @('-B')
$rawPayload = [Console]::In.ReadToEnd()
$searchPath = (Get-Location).Path

try {
    $hookPayload = $rawPayload | ConvertFrom-Json
    if ($hookPayload.cwd) {
        $candidateCwd = [System.IO.Path]::GetFullPath([string]$hookPayload.cwd)
        if (Test-Path -LiteralPath $candidateCwd -PathType Container) {
            $searchPath = $candidateCwd
        }
    }
} catch {
    # cpt_hook.py owns malformed-payload handling; discovery safely falls back.
}

if ($env:PRODUCT_OS_PYTHON) {
    $configured = [System.IO.Path]::GetFullPath($env:PRODUCT_OS_PYTHON)
    if (-not (Test-Path -LiteralPath $configured -PathType Leaf)) {
        [Console]::Error.WriteLine("PRODUCT_OS_PYTHON does not name an existing file: $configured")
        exit 127
    }
    $pythonPath = $configured
}

if (-not $pythonPath) {
    $current = [System.IO.DirectoryInfo]$searchPath
    while ($null -ne $current) {
        $candidate = Join-Path $current.FullName '.runtime\python\python.exe'
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $pythonPath = $candidate
            break
        }
        $current = $current.Parent
    }
}

if (-not $pythonPath) {
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        $pythonPath = $launcher.Source
        $pythonArgs = @('-3', '-B')
    }
}

if (-not $pythonPath) {
    foreach ($name in @('python.exe', 'python3.exe')) {
        $candidate = Get-Command $name -ErrorAction SilentlyContinue
        if ($candidate -and $candidate.Source -notlike '*\Microsoft\WindowsApps\*') {
            $pythonPath = $candidate.Source
            break
        }
    }
}

if (-not $pythonPath) {
    [Console]::Error.WriteLine(
        'Product OS hooks require Python 3. Set PRODUCT_OS_PYTHON or install the project-local .runtime\python\python.exe.'
    )
    exit 127
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$rawPayload | & $pythonPath @pythonArgs $hookPath
exit $LASTEXITCODE
