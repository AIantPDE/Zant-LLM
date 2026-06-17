$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\build_v0_5_hardcase_sft_dataset.py
if ($LASTEXITCODE -ne 0) { throw "build failed" }
