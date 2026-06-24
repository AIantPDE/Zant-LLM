$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\validate_v1_5_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v1_5_repository.py failed" }
python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }
Write-Host "pytest dependency is optional; running stdlib fallback tests..."
python .\scripts\run_v1_5_stdlib_tests.py
if ($LASTEXITCODE -ne 0) { throw "stdlib tests failed" }
Write-Host "ZANT_LLM_V1_5_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
