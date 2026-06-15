param(
  [string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git",
  [string]$Branch = "v0.2-trace-hix-contracts-and-validators",
  [string]$CommitMessage = "Add Zant-LLM v0.2 TRACE-HIX contracts and validators"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_2_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "local v0.2 run failed" }

if (-not (Test-Path -LiteralPath ".git")) {
  git init
}

git checkout -B $Branch

git remote get-url origin *> $null
if ($LASTEXITCODE -eq 0) {
  git remote set-url origin $Repository
} else {
  git remote add origin $Repository
}

git add -A

git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
  Write-Host "TRACE_HIX_V0_2_NO_CHANGES_TO_COMMIT=True"
} else {
  git commit -m $CommitMessage
}

git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }

Write-Host "TRACE_HIX_V0_2_BRANCH_PUSHED=True"
Write-Host "REPOSITORY=$Repository"
Write-Host "BRANCH=$Branch"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
