$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\eval_v0_9_inference_contract.py
if ($LASTEXITCODE -ne 0) { throw "eval_v0_9_inference_contract.py failed" }
