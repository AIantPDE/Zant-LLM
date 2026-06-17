$ErrorActionPreference = "Stop"
$SourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$WorkRoot = "C:\Users\Administrator\Desktop\Zant-LLM-v0.6R-push-work"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v0.6-realworld-adversarial-eval"
$NewBranch = "v0.6R-realworld-eval-calibration"
Remove-Item -LiteralPath $WorkRoot -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $BaseBranch $Repo $WorkRoot
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $WorkRoot
git checkout -b $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git checkout failed" }
robocopy $SourceRoot $WorkRoot /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_6R_CALIBRATION.ps1
if ($LASTEXITCODE -ne 0) { throw "v0.6R calibration run failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.6R real-world eval calibration"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push -u origin $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_6R_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
