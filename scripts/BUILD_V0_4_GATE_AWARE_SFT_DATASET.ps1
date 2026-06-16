$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = "$Root\src"
python .\scripts\build_v0_4_gate_aware_sft_dataset.py
if ($LASTEXITCODE -ne 0) { throw "build_v0_4_gate_aware_sft_dataset.py failed" }

