param([ValidateSet("contract", "model")][string]$Mode = "contract", [string]$BaseModelPath = "D:\gemma-4-E2B-it", [string]$AdapterPath = "outputs\v0_3\gemma4_qlora_adapter")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\eval_v0_3_gemma4_qlora.py --mode $Mode --base-model $BaseModelPath --adapter-path $AdapterPath
if ($LASTEXITCODE -ne 0) { throw "eval_v0_3_gemma4_qlora.py failed" }
Write-Host "ZANT_LLM_V0_3_EVAL_POWERSHELL_OK=True"
