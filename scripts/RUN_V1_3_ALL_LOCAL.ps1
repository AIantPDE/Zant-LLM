$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) {
    Write-Host "========== $Name =========="
    & $Block
    if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "========== Zant-LLM v1.3 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V1_3_LOCAL.ps1 }
Run-Step "build-rc-package" { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V1_3_RELEASE_CANDIDATE_PACKAGE.ps1 }
Run-Step "successor-recommendation" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V1_3_SUCCESSOR_RECOMMENDATION.ps1 }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V1_3_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V1_3_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
