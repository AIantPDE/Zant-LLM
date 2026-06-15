$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "========== Zant-LLM / TRACE-HIX v0.2 full local run =========="
Write-Host "Root: $Root"

function Run-Step($StepName, $ScriptPath) {
    powershell -ExecutionPolicy Bypass -File $ScriptPath
    if ($LASTEXITCODE -ne 0) {
        throw "$StepName failed with exit code $LASTEXITCODE"
    }
}

Run-Step "verify" ".\scripts\VERIFY_TRACE_HIX_V0_2_LOCAL.ps1"
Run-Step "validators" ".\scripts\RUN_TRACE_HIX_V0_2_VALIDATORS.ps1"

python .\scripts\make_trace_hix_v0_2_release_manifest.py
if ($LASTEXITCODE -ne 0) { throw "make_trace_hix_v0_2_release_manifest.py failed" }

Write-Host "========== Zant-LLM / TRACE-HIX v0.2 full local run complete =========="
Write-Host "TRACE_HIX_V0_2_ALL_LOCAL_OK=True"
Write-Host "REPORT_DIR=reports\v0_2"
Write-Host "RELEASE_MANIFEST=release_manifests\trace_hix_v0_2_release_manifest.json"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
