$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "========== TRACE-HIX v0.2.1 gate run =========="
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_TRACE_HIX_V0_2_1_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "v0.2.1 gate run failed" }
Write-Host "TRACE_HIX_V0_2_1_ALL_LOCAL_OK=True"
