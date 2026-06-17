param([string]$BaseModelPath = "E:\gemma-4-E2B-it", [switch]$No4Bit = $true)
$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$PWD\src"
$argsList = @(".\scripts\train_v0_7_gemma4_lora.py", "--base-model", $BaseModelPath, "--max-seq-len", "64", "--epochs", "1", "--batch-size", "1", "--grad-accum", "64", "--learning-rate", "1e-4")
if ($No4Bit) { $argsList += "--no-4bit" }
python @argsList
if ($LASTEXITCODE -ne 0) { throw "train_v0_7_gemma4_lora.py failed" }
Write-Host "ZANT_LLM_V0_7_TRAIN_POWERSHELL_OK=True"
