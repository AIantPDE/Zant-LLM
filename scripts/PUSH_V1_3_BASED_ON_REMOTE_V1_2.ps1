$ErrorActionPreference = "Stop"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v1.2-runtime-deployment-readiness"
$NewBranch = "v1.3-release-candidate-packaging"
$Src = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.3-push-work"
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone -b $BaseBranch $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -B $NewBranch
robocopy $Src $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_3_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "v1.3 local run failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v1.3 release candidate packaging"
git push -u origin $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V1_3_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
