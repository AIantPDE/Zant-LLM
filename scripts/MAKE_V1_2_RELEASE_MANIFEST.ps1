$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\make_v1_2_release_manifest.py
if ($LASTEXITCODE -ne 0) { throw "release manifest failed" }
