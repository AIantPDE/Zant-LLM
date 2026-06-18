$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) {
  Write-Host "========== $Name =========="
  & $Block
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v0.8 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_8_LOCAL.ps1 }
Run-Step "eval-heldout-contract" { powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_8_HELDOUT_CONTRACT.ps1 }
Run-Step "eval-model-dry-run" { powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_8_HELDOUT_MODEL.ps1 -DryRun }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_8_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V0_8_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
