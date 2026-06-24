$ErrorActionPreference = "Stop"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.5-push-work"
$Source = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b v1.4R-final-release-smoke-and-archive $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b v1.5-post-release-monitoring-and-maintenance
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_5_ALL_LOCAL.ps1
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v1.5 post-release monitoring and maintenance"
git push -u origin v1.5-post-release-monitoring-and-maintenance
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V1_5_BRANCH_PUSHED=True"
Write-Host "BRANCH=v1.5-post-release-monitoring-and-maintenance"
