$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) { Write-Host "========== $Name =========="; & $Block; if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" } }
Write-Host "========== Zant-LLM v0.7 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_7_LOCAL.ps1 }
Run-Step "build-sft" { python .\scripts\build_v0_7_calibration_sft_dataset.py }
Run-Step "eval-contract" { python .\scripts\eval_v0_7_calibration_sft_contract.py }
Run-Step "train-dry-run" { python .\scripts\train_v0_7_gemma4_lora.py --base-model "E:\gemma-4-E2B-it" --dry-run }
Run-Step "release-manifest" { python .\scripts\make_v0_7_release_manifest.py }
Write-Host "ZANT_LLM_V0_7_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
