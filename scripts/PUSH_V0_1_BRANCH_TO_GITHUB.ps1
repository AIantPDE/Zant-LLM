param(
    [string]$TargetRoot = (Get-Location).Path,
    [string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git",
    [string]$Branch = "v0.1",
    [string]$CommitMessage = "chore: bootstrap Zant-LLM v0.1 initial branch"
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $TargetRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "GIT_NOT_FOUND: please install Git for Windows first."
}

python .\scripts\validate_v0_1_pack.py

if (-not (Test-Path -LiteralPath ".git")) {
    git init
}

git checkout -B $Branch

git add --all

git diff --cached --check

$HasStagedChanges = $false
try {
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        $HasStagedChanges = $true
    }
} catch {
    $HasStagedChanges = $true
}

if ($HasStagedChanges) {
    git commit -m $CommitMessage
} else {
    Write-Host "NO_STAGED_CHANGES_TO_COMMIT=True"
}

$RemoteExists = $false
try {
    git remote get-url origin | Out-Null
    if ($LASTEXITCODE -eq 0) { $RemoteExists = $true }
} catch {
    $RemoteExists = $false
}

if ($RemoteExists) {
    git remote set-url origin $Repository
} else {
    git remote add origin $Repository
}

git push -u origin $Branch

Write-Host "ZANT_LLM_V0_1_BRANCH_PUSHED=True"
Write-Host "REPOSITORY=$Repository"
Write-Host "BRANCH=$Branch"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
