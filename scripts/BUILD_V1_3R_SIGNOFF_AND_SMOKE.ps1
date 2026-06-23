$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\build_v1_3R_signoff_and_smoke.py
if ($LASTEXITCODE -ne 0) { throw "build_v1_3R_signoff_and_smoke.py failed" }
