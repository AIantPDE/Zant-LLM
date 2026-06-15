$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "[TRACE-HIX v0.2] running validators..."
python .\scripts\run_trace_hix_v0_2_validators.py
if ($LASTEXITCODE -ne 0) { throw "run_trace_hix_v0_2_validators.py failed" }
Write-Host "TRACE_HIX_V0_2_VALIDATORS_POWERSHELL_OK=True"
