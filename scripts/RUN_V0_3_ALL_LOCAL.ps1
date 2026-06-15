param([switch]$Train, [string]$BaseModelPath = "D:\gemma-4-E2B-it")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
function Run-Step($Name, $ScriptBlock) {
  Write-Host "========== $Name =========="
  & $ScriptBlock
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v0.3 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_3_LOCAL.ps1 }
Run-Step "build-sft" { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_3_SFT_DATASET.ps1 }
Run-Step "eval-contract" { powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 -Mode contract }
if ($Train) { Run-Step "train-gemma4-qlora" { powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 -BaseModelPath $BaseModelPath } }
else { Run-Step "train-dry-run" { powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_3_GEMMA4_QLORA.ps1 -BaseModelPath $BaseModelPath -DryRun } }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_3_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V0_3_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
