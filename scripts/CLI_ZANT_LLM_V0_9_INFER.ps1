param([string]$Text = "", [string]$ModelOutput = "")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
if ($ModelOutput -ne "") { python .\scripts\cli_infer_v0_9.py --text $Text --model-output $ModelOutput } else { python .\scripts\cli_infer_v0_9.py --text $Text }
