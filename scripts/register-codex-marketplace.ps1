[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$MarketplaceName = 'product-os',

    [string[]]$Plugins = @('cpt-core', 'cpt-design-ui'),

    [switch]$Upgrade
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw 'Codex CLI was not found on PATH.'
}

if ($Upgrade) {
    & codex plugin marketplace upgrade $MarketplaceName
    if ($LASTEXITCODE -ne 0) {
        throw "Marketplace upgrade failed with exit code $LASTEXITCODE."
    }
}
else {
    & codex plugin marketplace add $Source
    if ($LASTEXITCODE -ne 0) {
        throw "Marketplace registration failed with exit code $LASTEXITCODE."
    }
}

foreach ($Plugin in $Plugins) {
    & codex plugin add "$Plugin@$MarketplaceName"
    if ($LASTEXITCODE -ne 0) {
        throw "Plugin installation failed for $Plugin."
    }
}

& codex plugin list
if ($LASTEXITCODE -ne 0) {
    throw "Plugin verification failed with exit code $LASTEXITCODE."
}

Write-Host 'Product OS marketplace operation completed. Start a new Codex thread before testing updated skills.'
