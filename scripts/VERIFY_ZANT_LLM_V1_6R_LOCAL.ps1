$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
& $Python ".\scripts\validate_v1_6R_repository.py"
& $Python ".\scripts\run_v1_6R_stdlib_tests.py"
Write-Host "ZANT_LLM_V1_6R_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
