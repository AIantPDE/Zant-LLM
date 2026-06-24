$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.4R-push-work"
$Source = "C:\Users\Administrator\Desktop\zant_llm_v1_4R_final_release_smoke_and_archive_branch"
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b v1.4-final-release-manifest-and-tagging $RepoUrl $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b v1.4R-final-release-smoke-and-archive
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_4R_ALL_LOCAL.ps1
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v1.4R final release smoke and archive"
git push -u origin v1.4R-final-release-smoke-and-archive
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V1_4R_BRANCH_PUSHED=True"
Write-Host "BRANCH=v1.4R-final-release-smoke-and-archive"
