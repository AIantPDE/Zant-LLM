$ErrorActionPreference = "Stop"
function Run-Step($Name, [scriptblock]$Block) {
  Write-Host "========== $Name =========="
  & $Block
  if ($LASTEXITCODE -ne 0) { throw "$Name failed with exit code $LASTEXITCODE" }
}
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "========== Zant-LLM v0.6R calibration run =========="
Run-Step "verify" { powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_6R_LOCAL.ps1 }
Run-Step "analyze-calibration" { python .\scripts\analyze_v0_6_realworld_eval_calibration.py }
Run-Step "release-manifest" { python .\scripts\make_v0_6R_release_manifest.py }
Write-Host "ZANT_LLM_V0_6R_ALL_LOCAL_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
