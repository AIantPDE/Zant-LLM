$ErrorActionPreference = "Stop"
function Run-Step($Name, $ScriptBlock) {
    Write-Host "========== $Name =========="
    & $ScriptBlock
    if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v1.5 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V1_5_LOCAL.ps1 }
Run-Step "build-post-release-monitoring" { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V1_5_POST_RELEASE_MONITORING.ps1 }
Run-Step "successor-recommendation" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V1_5_SUCCESSOR_RECOMMENDATION.ps1 }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V1_5_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V1_5_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
