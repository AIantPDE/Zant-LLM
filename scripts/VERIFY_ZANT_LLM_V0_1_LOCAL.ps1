param(
    [string]$TargetRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $TargetRoot

python .\scripts\validate_v0_1_pack.py
python .\scripts\run_v0_1_baseline_demo.py

if (Test-Path -LiteralPath ".\tests") {
    python -m pytest -q
}

Write-Host "ZANT_LLM_V0_1_LOCAL_VERIFY_DONE=True"
Write-Host "TARGET_ROOT=$TargetRoot"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
