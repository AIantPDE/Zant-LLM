$ErrorActionPreference = "Stop"
$Branch = "v0.8-heldout-model-eval"
$BaseBranch = "v0.7-calibration-informed-sft"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v0.8-push-work"
$Source = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $BaseBranch $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b $Branch
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_8_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "RUN_V0_8_ALL_LOCAL.ps1 failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.8 heldout model eval"
git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_8_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
