[CmdletBinding()]
param(
    [ValidateSet('install', 'update', 'status', 'doctor')]
    [string]$Action = 'update',

    [Parameter(Mandatory = $true)]
    [string]$Project,

    [ValidateSet('local', 'team')]
    [string]$Mode = 'local',

    [ValidateSet('personal', 'repo', 'none')]
    [string]$PluginScope = 'personal',

    [ValidateSet('off', 'audit', 'enforce')]
    [string]$EnforcementMode = 'audit',

    [string[]]$Packs = @(),

    [switch]$SkipDependencies,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProductOsRoot = Split-Path -Parent $PSScriptRoot
$Tool = Join-Path $ProductOsRoot 'tools\cpt_dist.py'
$Requirements = Join-Path $ProductOsRoot 'requirements.txt'
$ResolvedProject = [System.IO.Path]::GetFullPath((Resolve-Path $Project).Path)

function Invoke-ProductOsPython {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 @Arguments
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python @Arguments
    }
    else {
        throw 'Python 3 was not found. Install Python or add py/python to PATH.'
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Product OS command failed with exit code $LASTEXITCODE."
    }
}

if (-not $SkipDependencies) {
    Invoke-ProductOsPython @('-m', 'pip', 'install', '-r', $Requirements)
}

$Receipt = Join-Path $ResolvedProject '.cpt\install.json'

switch ($Action) {
    'install' {
        if (Test-Path $Receipt) {
            throw "A Product OS receipt already exists at $Receipt. Use -Action update."
        }

        $Arguments = @(
            $Tool, 'install',
            '--project', $ResolvedProject,
            '--mode', $Mode,
            '--plugin-scope', $PluginScope,
            '--enforcement-mode', $EnforcementMode
        )
        Invoke-ProductOsPython $Arguments

        foreach ($Pack in $Packs) {
            $PackArguments = @($Tool, 'pack-add', '--name', $Pack, '--scope', $PluginScope, '--project', $ResolvedProject)
            if ($PluginScope -eq 'none') {
                throw 'Domain packs require personal or repo plugin scope.'
            }
            Invoke-ProductOsPython $PackArguments
        }
    }

    'update' {
        if (-not (Test-Path $Receipt)) {
            throw "No Product OS installation receipt found at $Receipt. This may be a source folder rather than an installed project."
        }

        $Arguments = @($Tool, 'update', '--project', $ResolvedProject)
        if ($Force) {
            $Arguments += '--force'
        }
        Invoke-ProductOsPython $Arguments
    }

    'status' {
        Invoke-ProductOsPython @($Tool, 'status', '--project', $ResolvedProject)
    }

    'doctor' {
        Invoke-ProductOsPython @($Tool, 'doctor', '--project', $ResolvedProject)
    }
}

if ($Action -in @('install', 'update')) {
    Invoke-ProductOsPython @($Tool, 'doctor', '--project', $ResolvedProject)
}
