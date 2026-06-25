$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python .\scripts\build_v1_6_runtime_observability.py
