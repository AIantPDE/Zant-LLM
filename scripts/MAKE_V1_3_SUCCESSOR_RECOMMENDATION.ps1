$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\make_v1_3_successor_recommendation.py
if ($LASTEXITCODE -ne 0) { throw "make_v1_3_successor_recommendation.py failed" }
