$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = "$Root\src"
python .\scripts\eval_v0_4_gate_aware_explanation.py
if ($LASTEXITCODE -ne 0) { throw "eval_v0_4_gate_aware_explanation.py failed" }
Write-Host "ZANT_LLM_V0_4_EVAL_POWERSHELL_OK=True"

