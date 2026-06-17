$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) {
  Write-Host "========== $Name =========="
  & $Block
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
Write-Host "========== Zant-LLM v0.6 full local run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_6_LOCAL.ps1 }
Run-Step "eval-realworld" { python .\scripts\eval_v0_6_realworld_adversarial.py }
Run-Step "release-manifest" { python .\scripts\make_v0_6_release_manifest.py }
Write-Host "ZANT_LLM_V0_6_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
