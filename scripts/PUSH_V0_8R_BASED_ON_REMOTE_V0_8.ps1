$ErrorActionPreference = "Stop"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v0.8-heldout-model-eval"
$NewBranch = "v0.8R-heldout-model-output-calibration"
$Desktop = [Environment]::GetFolderPath("Desktop")
$Work = Join-Path $Desktop "Zant-LLM-v0.8R-push-work"
$Source = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $BaseBranch $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git checkout failed" }
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_8R_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "RUN_V0_8R_ALL_LOCAL.ps1 failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.8R heldout model output calibration"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push -u origin $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_8R_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
