param([string]$RepoUrl = "https://github.com/AIantPDE/Zant-LLM.git", [string]$BaseBranch = "v0.4-evidence-gated-explanation-admissibility", [string]$TargetBranch = "v0.5-adversarial-hard-cases-and-failclosed-eval")
$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$WorkRoot = Join-Path (Split-Path -Parent $SourceRoot) "Zant-LLM-v0.5-push-work"
if (Test-Path $WorkRoot) { Remove-Item -Recurse -Force $WorkRoot }
git clone -b $BaseBranch $RepoUrl $WorkRoot
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $WorkRoot
git checkout -b $TargetBranch
robocopy $SourceRoot $WorkRoot /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_5_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "local v0.5 run failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.5 adversarial hard cases and fail-closed eval"
git push -u origin $TargetBranch
Write-Host "ZANT_LLM_V0_5_BRANCH_PUSHED=True"
Write-Host "BRANCH=$TargetBranch"
