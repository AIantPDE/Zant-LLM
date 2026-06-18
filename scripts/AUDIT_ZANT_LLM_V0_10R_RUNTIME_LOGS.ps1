$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\audit_v0_10R_runtime_logs.py
if ($LASTEXITCODE -ne 0) { throw "audit_v0_10R_runtime_logs.py failed" }
