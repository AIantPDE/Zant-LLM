$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\eval_v0_5_failclosed_hard_cases.py
if ($LASTEXITCODE -ne 0) { throw "eval failed" }
Write-Host "ZANT_LLM_V0_5_EVAL_POWERSHELL_OK=True"
