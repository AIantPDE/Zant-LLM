$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "[TRACE-HIX v0.2.1] repository root: $Root"
python .\scripts\validate_v0_2_1_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v0_2_1_repository.py failed" }

python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }

python .\scripts\run_trace_hix_v0_2_1_gate_tests.py
if ($LASTEXITCODE -ne 0) { throw "gate tests failed" }

python .\scripts\make_trace_hix_v0_2_1_receipt.py
if ($LASTEXITCODE -ne 0) { throw "release manifest failed" }

Write-Host "TRACE_HIX_V0_2_1_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
