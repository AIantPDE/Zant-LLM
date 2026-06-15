param(
  [string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git",
  [string]$Branch = "v0.1-explanation-preview-baseline",
  [string]$CommitMessage = "chore: add Zant-LLM v0.1 explanation preview baseline trainable branch"
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
if (-not (Test-Path .git)) { git init }
git checkout -B $Branch
git add --all
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }
$HasStaged = git diff --cached --name-only
if ($HasStaged) { git commit -m $CommitMessage } else { Write-Host "No staged changes to commit." }
$ExistingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) { git remote add origin $Repository } else { git remote set-url origin $Repository }
git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V0_1_BRANCH_PUSHED=True"
Write-Host "REPOSITORY=$Repository"
Write-Host "BRANCH=$Branch"
