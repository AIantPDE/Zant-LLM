param(
  [string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git",
  [string]$BaseBranch = "v0.3-gemma4-qlora-explanation-baseline",
  [string]$TargetBranch = "v0.4-evidence-gated-explanation-admissibility",
  [string]$WorkRoot = "$env:USERPROFILE\Desktop\Zant-LLM-v0.4-push-work"
)
$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (Test-Path $WorkRoot) { Remove-Item $WorkRoot -Recurse -Force }
git clone -b $BaseBranch $Repository $WorkRoot
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $WorkRoot
git checkout -b $TargetBranch
robocopy $SourceRoot $WorkRoot /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_4_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "v0.4 local run failed" }
git add -A
git commit -m "Add Zant-LLM v0.4 evidence-gated explanation admissibility"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push -u origin $TargetBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_4_BRANCH_PUSHED=True"
Write-Host "BRANCH=$TargetBranch"

