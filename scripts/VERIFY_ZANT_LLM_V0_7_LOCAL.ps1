$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "[Zant-LLM v0.7] repository root: $Root"
python .\scripts\validate_v0_7_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v0_7_repository.py failed" }
python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }
Write-Host "pytest dependency is optional; running stdlib fallback tests..."
python .\scripts\run_v0_7_stdlib_tests.py
if ($LASTEXITCODE -ne 0) { throw "stdlib tests failed" }
Write-Host "ZANT_LLM_V0_7_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
