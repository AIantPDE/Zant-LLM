param(
    [string]$TargetRoot = (Get-Location).Path,
    [string]$Lane = "lane/zant-explanation-v0.1-baseline"
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $TargetRoot

git fetch origin
try {
    git checkout v0.1
} catch {
    git checkout -B v0.1 origin/v0.1
}

git checkout -B $Lane

Write-Host "ZANT_LLM_TRAINING_LANE_CREATED=True"
Write-Host "LANE=$Lane"
Write-Host "BASE=v0.1"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
