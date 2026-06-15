param([string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git", [string]$BaseBranch = "v0.2-trace-hix-contracts-and-validators", [string]$TargetBranch = "v0.3-gemma4-qlora-explanation-baseline", [string]$WorkDir = "$env:USERPROFILE\Desktop\Zant-LLM-v0.3-push-work")
$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (Test-Path -LiteralPath $WorkDir) { Remove-Item -LiteralPath $WorkDir -Recurse -Force }
git clone -b $BaseBranch $Repository $WorkDir
if ($LASTEXITCODE -ne 0) { throw "git clone base branch failed" }
Set-Location $WorkDir
git checkout -B $TargetBranch
if ($LASTEXITCODE -ne 0) { throw "git checkout target branch failed" }
robocopy $PackageRoot $WorkDir /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_3_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "local v0.3 verification failed" }
git add -A
git commit -m "Add Zant-LLM v0.3 Gemma4 QLoRA explanation baseline"
if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
git push -u origin $TargetBranch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_3_BRANCH_PUSHED=True"
Write-Host "BRANCH=$TargetBranch"
Write-Host "REPOSITORY=$Repository"
