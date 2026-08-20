$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python ".\scripts\make_v1_6R_successor_recommendation.py"
