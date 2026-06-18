$ErrorActionPreference = "Stop"
$Remote = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v0.9-inference-contract-stabilization"
$NewBranch = "v0.10-runtime-api-batch-harness"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v0.10-push-work"
$Source = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $BaseBranch $Remote $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -B $NewBranch
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_10_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "v0.10 local run failed" }
git add -A
git commit -m "Add Zant-LLM v0.10 runtime API batch harness"
git push -u origin $NewBranch
Write-Host "ZANT_LLM_V0_10_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
