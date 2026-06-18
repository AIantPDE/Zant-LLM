$ErrorActionPreference = "Stop"
$Branch = "v0.10R-runtime-harness-stress-and-log-audit"
$BaseBranch = "v0.10-runtime-api-batch-harness"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Desktop = [Environment]::GetFolderPath("Desktop")
$Source = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Work = Join-Path $Desktop "Zant-LLM-v0.10R-push-work"

Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b $BaseBranch $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }

Set-Location $Work
git checkout -b $Branch
if ($LASTEXITCODE -ne 0) { throw "git checkout failed" }

robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }

powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_10R_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "v0.10R local run failed" }

git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.10R runtime harness stress and log audit"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }

git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host "ZANT_LLM_V0_10R_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
