$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
$Python = 'python'
Write-Host "========== Zant-LLM v1.6 full local run =========="
Write-Host "========== verify =========="
& $Python .\scripts\validate_v1_6_repository.py
& $Python .\scripts\run_v1_6_stdlib_tests.py
Write-Host "========== build-runtime-observability =========="
& $Python .\scripts\build_v1_6_runtime_observability.py
Write-Host "========== successor-recommendation =========="
& $Python .\scripts\make_v1_6_successor_recommendation.py
Write-Host "========== release-manifest =========="
& $Python .\scripts\make_v1_6_release_manifest.py
Write-Host "ZANT_LLM_V1_6_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
