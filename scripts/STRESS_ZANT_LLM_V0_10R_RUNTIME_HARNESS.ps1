$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\stress_v0_10R_runtime_harness.py
if ($LASTEXITCODE -ne 0) { throw "stress_v0_10R_runtime_harness.py failed" }
