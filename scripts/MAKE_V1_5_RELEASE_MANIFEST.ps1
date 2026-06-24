$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\make_v1_5_release_manifest.py
if ($LASTEXITCODE -ne 0) { throw "make_v1_5_release_manifest.py failed" }
