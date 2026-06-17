$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\eval_v0_6_realworld_adversarial.py
if ($LASTEXITCODE -ne 0) { throw "eval_v0_6_realworld_adversarial.py failed" }
Write-Host "ZANT_LLM_V0_6_EVAL_POWERSHELL_OK=True"
