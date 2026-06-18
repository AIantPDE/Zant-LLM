$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) {
    Write-Host "========== $Name =========="
    & $Block
    if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "========== Zant-LLM v0.11 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_11_LOCAL.ps1 }
Run-Step "build-dashboard" { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_11_RUNTIME_REGRESSION_DASHBOARD.ps1 }
Run-Step "successor-recommendation" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_11_SUCCESSOR_RECOMMENDATION.ps1 }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_11_RELEASE_MANIFEST.ps1 }

Write-Host "ZANT_LLM_V0_11_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
