param([string]$Python = "python")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "[Zant-LLM v0.1] repository root: $Root"

& $Python .\scripts\validate_v0_1_repository.py
if ($LASTEXITCODE -ne 0) { throw "validate_v0_1_repository.py failed" }

& $Python -m compileall .\src .\scripts
if ($LASTEXITCODE -ne 0) { throw "python compile failed" }

if (Test-Path .\tests) {
  & $Python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('pytest') else 1)"
  if ($LASTEXITCODE -eq 0) {
    Write-Host "pytest detected; running pytest..."
    $env:PYTHONPATH = "$Root\src;$env:PYTHONPATH"
    & $Python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
  } else {
    Write-Host "pytest not installed; running stdlib fallback tests..."
    & $Python .\scripts\run_v0_1_stdlib_tests.py
    if ($LASTEXITCODE -ne 0) { throw "stdlib fallback tests failed" }
  }
}

Write-Host "ZANT_LLM_V0_1_LOCAL_VERIFY_OK=True"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
