$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v1.5-post-release-monitoring-and-maintenance"
$NewBranch = "v1.5R-post-release-monitoring-audit-and-hotfix-readiness"
$SourceRoot = Split-Path -Parent $PSScriptRoot
$PushWork = "C:\Users\Administrator\Desktop\Zant-LLM-v1.5R-push-work"

if (Test-Path $PushWork) {
  Remove-Item -Recurse -Force $PushWork
}

git clone --branch $BaseBranch $RepoUrl $PushWork
Set-Location $PushWork
git checkout -b $NewBranch

robocopy $SourceRoot $PushWork /MIR /XD .git .venv __pycache__ .pytest_cache /XF *.pyc
if ($LASTEXITCODE -le 7) {
  $global:LASTEXITCODE = 0
} else {
  throw "ROBOCOPY failed with exit code $LASTEXITCODE"
}

powershell -ExecutionPolicy Bypass -File ".\scripts\RUN_V1_5R_ALL_LOCAL.ps1"

git add -A
git commit -m "Add Zant-LLM v1.5R post-release audit and hotfix readiness"
git push -u origin $NewBranch

Write-Host "ZANT_LLM_V1_5R_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
