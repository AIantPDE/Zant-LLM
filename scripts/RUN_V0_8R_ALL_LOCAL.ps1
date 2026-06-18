$ErrorActionPreference = "Stop"
function Run-Step($Name,[scriptblock]$Block){ Write-Host "========== $Name =========="; & $Block; if ($LASTEXITCODE -ne 0){ throw "$Name failed with exit code $LASTEXITCODE" } }
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "========== Zant-LLM v0.8R full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_8R_LOCAL.ps1 }
Run-Step "analyze-calibration" { powershell -ExecutionPolicy Bypass -File .\scripts\ANALYZE_V0_8R_MODEL_OUTPUT_CALIBRATION.ps1 }
Run-Step "model-probe-calibrated-dry-run" { powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_8R_CALIBRATED_HELDOUT_MODEL.ps1 -DryRun }
Run-Step "successor-recommendation" { python .\scripts\make_v0_8R_successor_recommendation.py }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_8R_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V0_8R_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
