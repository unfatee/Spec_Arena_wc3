param(
    [string]$BaseMap = "C:\war\Maps\_codex_backup\SA2573S_crashy_2026-05-29.w3x",
    [string]$OutputMap = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SourceDir = Join-Path $RepoRoot "source"
$ToolPath = Join-Path $RepoRoot "tools\mpqcli.exe"

if ($OutputMap -eq "") {
    $OutputMap = Join-Path $RepoRoot "dist\SA2573S2.w3x"
}

if (!(Test-Path -LiteralPath $ToolPath)) {
    throw "mpqcli.exe not found. Put it at: $ToolPath"
}

if (!(Test-Path -LiteralPath $BaseMap)) {
    throw "Base map not found: $BaseMap"
}

Copy-Item -LiteralPath $BaseMap -Destination $OutputMap -Force

$files = @(
    "war3map.j",
    "war3map.w3a",
    "war3map.w3i",
    "war3map.w3t",
    "war3map.w3u",
    "war3map.wts"
)

foreach ($name in $files) {
    $sourceFile = Join-Path $SourceDir $name
    if (!(Test-Path -LiteralPath $sourceFile)) {
        throw "Source file not found: $sourceFile"
    }

    & $ToolPath add $sourceFile $OutputMap -p $name -w -g warcraft3-map
    if ($LASTEXITCODE -ne 0) {
        throw "mpqcli failed while adding $name"
    }
}

Write-Host "Built: $OutputMap"

