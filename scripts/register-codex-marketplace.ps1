[CmdletBinding()]
param(
    [string]$Source = 'Lofiette/product-os',

    [string]$Ref = 'v4.1.0',

    [string]$MarketplaceName = 'product-os',

    [string[]]$Plugins = @('cpt-core', 'cpt-design-ui'),

    [switch]$Upgrade
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw 'Codex CLI was not found on PATH.'
}

$MarketplaceOutput = (& codex plugin marketplace list 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0) {
    throw "Marketplace discovery failed with exit code $LASTEXITCODE."
}

$MarketplacePattern = '(?m)^\s*' + [regex]::Escape($MarketplaceName) + '\s+(.+?)\s*$'
$MarketplaceMatch = [regex]::Match($MarketplaceOutput, $MarketplacePattern)
$MarketplaceExists = $MarketplaceMatch.Success
$MarketplaceRoot = if ($MarketplaceExists) { $MarketplaceMatch.Groups[1].Value } else { '' }
$ManagerRootPattern = '[\\/]sources[\\/]product-os[\\/][0-9a-f]{7,64}(?:[\\/]|$)'
$SourceExplicit = $PSBoundParameters.ContainsKey('Source')
$RefExplicit = $PSBoundParameters.ContainsKey('Ref')

if ($Upgrade) {
    if (-not $MarketplaceExists) {
        throw "Marketplace '$MarketplaceName' is not registered. Run this script without -Upgrade first."
    }
    if ($MarketplaceRoot -match $ManagerRootPattern) {
        throw "Marketplace '$MarketplaceName' is managed by Product OS Manager. Use a confirmed Manager plan-local-git -> prepare -> switch transaction instead of marketplace upgrade."
    }
    if ($RefExplicit) {
        throw '-Ref cannot retarget an existing marketplace. The Codex upgrade command refreshes its configured ref; use Product OS Manager or register a separate marketplace to change refs.'
    }
    & codex plugin marketplace upgrade $MarketplaceName
    if ($LASTEXITCODE -ne 0) {
        throw "Marketplace upgrade failed with exit code $LASTEXITCODE."
    }
}
else {
    if ($MarketplaceExists) {
        if ($MarketplaceRoot -match $ManagerRootPattern) {
            throw "Marketplace '$MarketplaceName' is managed by Product OS Manager. Use a confirmed Manager plan-local-git -> prepare -> switch transaction instead of this direct helper."
        }
        if ($SourceExplicit -or $RefExplicit) {
            throw "Marketplace '$MarketplaceName' already exists, but Codex does not expose enough provenance to verify the explicitly requested source or ref. Re-run without -Source/-Ref to trust the existing marketplace, use -Upgrade to refresh its configured ref, or register a separate marketplace to retarget."
        }
        Write-Host "Marketplace '$MarketplaceName' is already registered at '$MarketplaceRoot'; keeping it and ensuring the requested plugins are installed."
    }
    else {
        & codex plugin marketplace add $Source --ref $Ref
        if ($LASTEXITCODE -ne 0) {
            throw "Marketplace registration failed with exit code $LASTEXITCODE."
        }
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
