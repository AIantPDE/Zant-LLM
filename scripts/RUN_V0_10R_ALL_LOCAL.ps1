$ErrorActionPreference = "Stop"
function Run-Step($Name, $ScriptBlock) {
    Write-Host "========== $Name =========="
    & $ScriptBlock
    if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v0.10R full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_10R_LOCAL.ps1 }
Run-Step "stress-runtime-harness" { powershell -ExecutionPolicy Bypass -File .\scripts\STRESS_ZANT_LLM_V0_10R_RUNTIME_HARNESS.ps1 }
Run-Step "audit-runtime-logs" { powershell -ExecutionPolicy Bypass -File .\scripts\AUDIT_ZANT_LLM_V0_10R_RUNTIME_LOGS.ps1 }
Run-Step "successor-recommendation" { python .\scripts\make_v0_10R_successor_recommendation.py }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_10R_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V0_10R_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
