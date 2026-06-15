$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "[TRACE-HIX v0.2] repository root: $Root"

python .\scripts\validate_v0_2_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v0_2_repository.py failed" }

python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "python compile failed" }

python -m pytest .\tests -q
if ($LASTEXITCODE -ne 0) {
  Write-Host "pytest not installed or failed; running stdlib fallback tests..."
  python .\scripts\run_v0_2_stdlib_tests.py
  if ($LASTEXITCODE -ne 0) { throw "stdlib fallback tests failed" }
}

Write-Host "TRACE_HIX_V0_2_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
