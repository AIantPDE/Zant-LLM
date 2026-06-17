param([string]$BaseModelPath = "E:\gemma-4-E2B-it", [switch]$No4Bit = $true)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$env:PYTHONPATH = "$Root\src"
if ($No4Bit) { python -X faulthandler .\scripts\train_v0_5_gemma4_lora.py --base-model "$BaseModelPath" --max-seq-len 64 --epochs 1 --batch-size 1 --grad-accum 64 --learning-rate 1e-4 --no-4bit } else { python -X faulthandler .\scripts\train_v0_5_gemma4_lora.py --base-model "$BaseModelPath" --max-seq-len 64 --epochs 1 --batch-size 1 --grad-accum 64 --learning-rate 1e-4 }
if ($LASTEXITCODE -ne 0) { throw "train failed" }
Write-Host "ZANT_LLM_V0_5_TRAIN_POWERSHELL_OK=True"
