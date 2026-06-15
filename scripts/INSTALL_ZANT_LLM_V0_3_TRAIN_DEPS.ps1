$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python -m pip install --upgrade pip
python -m pip install -r .\requirements-v0.3.txt
if ($LASTEXITCODE -ne 0) { throw "pip install requirements-v0.3.txt failed" }
Write-Host "ZANT_LLM_V0_3_TRAIN_DEPS_INSTALLED=True"
