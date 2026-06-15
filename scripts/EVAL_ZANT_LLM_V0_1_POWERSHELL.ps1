param([string]$Python = "python", [string]$Config = "configs/v0_1_train_config.json")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "[Zant-LLM v0.1] evaluating baseline..."
& $Python .\scripts\eval_v0_1_baseline.py --config $Config
if ($LASTEXITCODE -ne 0) { throw "eval_v0_1_baseline.py failed" }
Write-Host "ZANT_LLM_V0_1_EVAL_POWERSHELL_OK=True"
