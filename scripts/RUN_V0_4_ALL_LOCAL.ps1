$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
function Run-Step([string]$Name, [scriptblock]$Block) {
  Write-Host "========== $Name =========="
  & $Block
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v0.4 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_4_LOCAL.ps1 }
Run-Step "build-sft" { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_4_GATE_AWARE_SFT_DATASET.ps1 }
Run-Step "eval-contract" { powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_4_GATE_AWARE_EXPLANATION.ps1 }
Run-Step "train-dry-run" { python .\scripts\train_v0_4_gemma4_lora.py --base-model "E:\gemma-4-E2B-it" --dry-run }
Run-Step "release-manifest" { powershell -ExecutionPolicy Bypass -File .\scripts\MAKE_V0_4_RELEASE_MANIFEST.ps1 }
Write-Host "ZANT_LLM_V0_4_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"

