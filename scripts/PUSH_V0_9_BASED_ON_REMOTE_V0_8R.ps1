$ErrorActionPreference = "Stop"
$Branch = "v0.9-inference-contract-stabilization"
$BaseBranch = "v0.8R-heldout-model-output-calibration"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Source = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v0.9-push-work"

git config --global http.version HTTP/1.1
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
git config --global core.compression 0

Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b $BaseBranch $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b $Branch
if ($LASTEXITCODE -ne 0) { throw "git checkout failed" }
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_9_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "RUN_V0_9_ALL_LOCAL.ps1 failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.9 inference contract stabilization"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_9_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
