$ErrorActionPreference = 'Stop'
$Branch = "v1.6-runtime-observability-and-operator-dashboard"
$BaseBranch = "v1.5R-post-release-monitoring-audit-and-hotfix-readiness"
$RepoUrl = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.6-push-work"
$Source = Split-Path -Parent $PSScriptRoot

if (Test-Path $Work) { Remove-Item -Recurse -Force $Work }
git clone --branch $BaseBranch $RepoUrl $Work
Set-Location $Work
git checkout -b $Branch
robocopy $Source $Work /MIR /XD .git .venv __pycache__ .pytest_cache /XF *.pyc
if ($LASTEXITCODE -le 7) { $global:LASTEXITCODE = 0 } else { exit $LASTEXITCODE }

powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_6_ALL_LOCAL.ps1

git add -A
git commit -m "Add Zant-LLM v1.6 runtime observability and operator dashboard"
git push -u origin $Branch
Write-Host "ZANT_LLM_V1_6_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
