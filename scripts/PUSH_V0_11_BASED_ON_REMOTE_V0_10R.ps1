$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/AIantPDE/Zant-LLM.git"
$BaseBranch = "v0.10R-runtime-harness-stress-and-log-audit"
$NewBranch = "v0.11-runtime-regression-dashboard"
$Desktop = [Environment]::GetFolderPath("Desktop")
$Source = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Work = Join-Path $Desktop "Zant-LLM-v0.11-push-work"

if (Test-Path $Work) {
    Remove-Item -LiteralPath $Work -Recurse -Force
}

git clone -b $BaseBranch $RepoUrl $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }

Set-Location $Work
git checkout -B $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git checkout failed" }

robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }

powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_11_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "RUN_V0_11_ALL_LOCAL failed" }

git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v0.11 runtime regression dashboard"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }

git push -u origin $NewBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host "ZANT_LLM_V0_11_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
