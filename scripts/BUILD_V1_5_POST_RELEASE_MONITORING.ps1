$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\build_v1_5_post_release_monitoring.py
if ($LASTEXITCODE -ne 0) { throw "build_v1_5_post_release_monitoring.py failed" }
