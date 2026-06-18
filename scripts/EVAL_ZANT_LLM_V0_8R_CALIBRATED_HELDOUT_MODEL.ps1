param(
  [string]$BaseModelPath = "E:\gemma-4-E2B-it",
  [string]$AdapterPath = "C:\Users\Administrator\Desktop\Zant-LLM-v0.7-push-work\outputs\v0_7\gemma4_lora_adapter",
  [int]$MaxCases = 12,
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$ArgsList = @(".\scripts\eval_v0_8R_calibrated_heldout_model.py","--base-model",$BaseModelPath,"--adapter-path",$AdapterPath,"--max-cases","$MaxCases")
if ($DryRun) { $ArgsList += "--dry-run" }
python @ArgsList
if ($LASTEXITCODE -ne 0) { throw "live probe failed" }
