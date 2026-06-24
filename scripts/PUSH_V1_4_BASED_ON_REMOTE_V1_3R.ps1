$ErrorActionPreference = "Stop"
$Repo = "https://github.com/AIantPDE/Zant-LLM.git"
$Work = "C:\Users\Administrator\Desktop\Zant-LLM-v1.4-push-work"
$Source = "C:\Users\Administrator\Desktop\zant_llm_v1_4_final_release_manifest_and_tagging_branch"
$Base = "v1.3R-release-candidate-signoff-and-smoke"
$Branch = "v1.4-final-release-manifest-and-tagging"
Remove-Item -LiteralPath $Work -Recurse -Force -ErrorAction SilentlyContinue
git clone --depth 1 --single-branch -b $Base $Repo $Work
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
Set-Location $Work
git checkout -b $Branch
robocopy $Source $Work /MIR /XD ".git" ".venv" "__pycache__" ".pytest_cache" /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_4_ALL_LOCAL.ps1
if ($LASTEXITCODE -ne 0) { throw "RUN_V1_4_ALL_LOCAL failed" }
git config user.name "haobo wei"
git config user.email "1225777566@qq.com"
git add -A
git commit -m "Add Zant-LLM v1.4 final release manifest and tagging"
git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw "git push failed" }
Write-Host "ZANT_LLM_V1_4_BRANCH_PUSHED=True"
Write-Host "BRANCH=$Branch"
