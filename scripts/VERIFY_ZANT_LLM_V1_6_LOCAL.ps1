$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python .\scripts\validate_v1_6_repository.py
& $Python .\scripts\run_v1_6_stdlib_tests.py
