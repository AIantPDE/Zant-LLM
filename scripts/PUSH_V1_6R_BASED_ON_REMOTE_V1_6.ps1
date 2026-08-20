$ErrorActionPreference = 'Stop'
$SourceRoot = Split-Path -Parent $PSScriptRoot
$Desktop = [Environment]::GetFolderPath('Desktop')
$WorkRoot = Join-Path $Desktop 'Zant-LLM-v1.6R-push-work'
$RepoUrl = 'https://github.com/AIantPDE/Zant-LLM.git'
$BaseBranch = 'v1.6-runtime-observability-and-operator-dashboard'
$NewBranch = 'v1.6R-orsc-v6-gate-aware-observability-and-receipt-hardening'
if (Test-Path $WorkRoot) { Remove-Item -Recurse -Force $WorkRoot }
git clone --branch $BaseBranch $RepoUrl $WorkRoot
Set-Location $WorkRoot
git checkout -b $NewBranch
robocopy $SourceRoot $WorkRoot *.* /S /E /DCOPY:DA /COPY:DAT /PURGE /MIR /R:3 /W:2 /XD .git .venv __pycache__ .pytest_cache /XF *.pyc
if ($LASTEXITCODE -le 7) { $global:LASTEXITCODE = 0 } else { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File ".\scripts\RUN_V1_6R_ALL_LOCAL.ps1"
if (-not (git config user.name)) { git config user.name 'haobo wei' }
if (-not (git config user.email)) { git config user.email '1225777566@qq.com' }
git add -A
git commit -m 'Add Zant-LLM v1.6R ORSC v6 gate-aware observability and receipt hardening'
git push -u origin $NewBranch
Write-Host "ZANT_LLM_V1_6R_BRANCH_PUSHED=True"
Write-Host "BRANCH=$NewBranch"
