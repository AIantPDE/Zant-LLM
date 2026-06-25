$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python .\scripts\make_v1_6_release_manifest.py
