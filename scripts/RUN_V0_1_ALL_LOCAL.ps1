param([string]$Python = "python")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

function Invoke-CheckedPowerShellStep {
  param(
    [string]$StepName,
    [string]$ScriptPath
  )
  powershell -ExecutionPolicy Bypass -File $ScriptPath -Python $Python
  if ($LASTEXITCODE -ne 0) {
    throw "$StepName failed with exit code $LASTEXITCODE"
  }
}

function Invoke-CheckedPythonStep {
  param(
    [string]$StepName,
    [string]$ScriptPath
  )
  & $Python $ScriptPath
  if ($LASTEXITCODE -ne 0) {
    throw "$StepName failed with exit code $LASTEXITCODE"
  }
}

Write-Host "========== Zant-LLM v0.1 full local run =========="
Write-Host "Root: $Root"

Invoke-CheckedPowerShellStep -StepName "verify" -ScriptPath ".\scripts\VERIFY_ZANT_LLM_V0_1_LOCAL.ps1"
Invoke-CheckedPowerShellStep -StepName "train" -ScriptPath ".\scripts\TRAIN_ZANT_LLM_V0_1_POWERSHELL.ps1"
Invoke-CheckedPowerShellStep -StepName "eval" -ScriptPath ".\scripts\EVAL_ZANT_LLM_V0_1_POWERSHELL.ps1"
Invoke-CheckedPythonStep -StepName "release manifest" -ScriptPath ".\scripts\make_v0_1_release_manifest.py"

Write-Host "========== Zant-LLM v0.1 full local run complete =========="
Write-Host "ZANT_LLM_V0_1_ALL_LOCAL_OK=True"
Write-Host "OUTPUT_DIR=outputs\v0_1"
Write-Host "RELEASE_MANIFEST=release_manifests\zant_llm_v0_1_release_manifest.json"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
