$ErrorActionPreference = "Stop"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.3R-push-work"
$Source = "C:\Users\Administrator\Desktop\zant_llm_v1_3R_release_candidate_signoff_and_smoke_branch"
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b v1.3-release-candidate-packaging $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b v1.3R-release-candidate-signoff-and-smoke
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_3R_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "local run failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v1.3R release candidate signoff and smoke"
git push -u origin v1.3R-release-candidate-signoff-and-smoke
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V1_3R_BRANCH_PUSHED=True"
Write-Host "BRANCH=v1.3R-release-candidate-signoff-and-smoke"
