param(
  [string]$Repository = "https://github.com/AIantPDE/Zant-LLM.git",
  [string]$BaseBranch = "v0.1-explanation-preview-baseline",
  [string]$Branch = "v0.2-trace-hix-contracts-and-validators",
  [string]$WorkRoot = "$env:USERPROFILE\Desktop\Zant-LLM-v0.2-work",
  [string]$CommitMessage = "Add Zant-LLM v0.2 TRACE-HIX contracts and validators"
)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

if (Test-Path -LiteralPath $WorkRoot) {
  throw "WorkRoot already exists: $WorkRoot. Delete it or pass another -WorkRoot."
}

git clone -b $BaseBranch $Repository $WorkRoot
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $WorkRoot
git checkout -B $Branch
if ($LASTEXITCODE -ne 0) { throw "git checkout branch failed" }

robocopy $PackageRoot $WorkRoot /E /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }

# Remove known v0.1 stale files that can conflict with v0.2 validators.
$Stale = @(
  ".\tests\test_governance.py",
  ".\tests\test_schema.py",
  ".\scripts\run_v0_1_baseline_demo.py",
  ".\scripts\validate_v0_1_pack.py",
  ".\src\zant_llm\schema.py",
  ".\configs\zant_llm_v0_1_baseline_config.json",
  ".\data_manifests\zant_llm_v0_1_seed_manifest.json",
  ".\release_manifests\zant_llm_v0_1_initial_branch_manifest.json"
)
foreach ($Path in $Stale) {
  Remove-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
}

powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_2_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "local v0.2 run failed" }

git add -A
git commit -m $CommitMessage
git push -u origin $Branch

Write-Host "TRACE_HIX_V0_2_BRANCH_PUSHED_BASED_ON_REMOTE_V0_1=True"
Write-Host "WORK_ROOT=$WorkRoot"
Write-Host "REPOSITORY=$Repository"
Write-Host "BASE_BRANCH=$BaseBranch"
Write-Host "BRANCH=$Branch"
Write-Host "RUNTIME_AUTHORITY_GRANTED=False"
Write-Host "PROVIDER_DISPATCH_ENABLED=False"
