$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\build_v1_2_deployment_readiness.py
if ($LASTEXITCODE -ne 0) { throw "build readiness failed" }
