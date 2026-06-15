param([string]$BaseModelPath = "D:\gemma-4-E2B-it", [string]$OutputDir = "outputs\v0_3\gemma4_qlora_adapter", [switch]$DryRun, [switch]$No4Bit)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
if (-not (Test-Path -LiteralPath ".\data\trace_hix_v0_3\sft_train_60.jsonl")) { powershell -ExecutionPolicy Bypass -File .\scripts\BUILD_V0_3_SFT_DATASET.ps1 }
$argsList = @(".\scripts\train_v0_3_gemma4_qlora.py", "--base-model", $BaseModelPath, "--output-dir", $OutputDir)
if ($DryRun) { $argsList += "--dry-run" }
if ($No4Bit) { $argsList += "--no-4bit" }
python @argsList
if ($LASTEXITCODE -ne 0) { throw "train_v0_3_gemma4_qlora.py failed" }
Write-Host "ZANT_LLM_V0_3_TRAIN_POWERSHELL_OK=True"

