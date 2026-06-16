param([string]$BaseModelPath = "E:\gemma-4-E2B-it", [switch]$No4Bit = $true)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = "$Root\src"
$env:CUDA_VISIBLE_DEVICES = "0"
$env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:128"
$ArgsList = @(".\scripts\train_v0_4_gemma4_lora.py", "--base-model", $BaseModelPath, "--max-seq-len", "64", "--epochs", "1", "--batch-size", "1", "--grad-accum", "64", "--learning-rate", "1e-4")
if ($No4Bit) { $ArgsList += "--no-4bit" }
python -X faulthandler @ArgsList
if ($LASTEXITCODE -ne 0) { throw "train_v0_4_gemma4_lora.py failed" }
Write-Host "ZANT_LLM_V0_4_TRAIN_POWERSHELL_OK=True"

