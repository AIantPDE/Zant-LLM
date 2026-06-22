$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\validate_v1_3_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v1_3_repository.py failed" }
python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "compileall failed" }
python .\scripts\run_v1_3_stdlib_tests.py
if ($LASTEXITCODE -ne 0) { throw "run_v1_3_stdlib_tests.py failed" }
Write-Host "ZANT_LLM_V1_3_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
