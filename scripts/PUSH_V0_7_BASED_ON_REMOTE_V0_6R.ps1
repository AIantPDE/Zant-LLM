$ErrorActionPreference = "Stop"
$Src = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v0.7-push-work"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Base = "v0.6R-realworld-eval-calibration"
$Branch = "v0.7-calibration-informed-sft"
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $Base $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b $Branch
robocopy $Src $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_7_ALL_LOCAL.ps1
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.7 calibration-informed SFT"
git push -u origin $Branch
Write-Host "ZANT_LLM_V0_7_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
