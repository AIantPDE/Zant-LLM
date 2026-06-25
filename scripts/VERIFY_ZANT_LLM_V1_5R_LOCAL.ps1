$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
python "$PSScriptRoot\validate_v1_5R_repository.py" --root "$Root"
python "$PSScriptRoot\build_v1_5R_audit_and_hotfix_readiness.py" --root "$Root"
python "$PSScriptRoot\run_v1_5R_stdlib_tests.py" --root "$Root"
Write-Host "ZANT_LLM_V1_5R_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
