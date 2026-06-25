$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "========== Zant-LLM v1.5R full local run =========="
Write-Host "========== verify =========="
python "$PSScriptRoot\validate_v1_5R_repository.py" --root "$Root"

Write-Host "========== build-audit-and-hotfix-readiness =========="
python "$PSScriptRoot\build_v1_5R_audit_and_hotfix_readiness.py" --root "$Root"

Write-Host "========== stdlib-tests =========="
python "$PSScriptRoot\run_v1_5R_stdlib_tests.py" --root "$Root"

Write-Host "========== successor-recommendation =========="
python "$PSScriptRoot\make_v1_5R_successor_recommendation.py" --root "$Root"

Write-Host "========== release-manifest =========="
python "$PSScriptRoot\make_v1_5R_release_manifest.py" --root "$Root"

Write-Host "ZANT_LLM_V1_5R_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
