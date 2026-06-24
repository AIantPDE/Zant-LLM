$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\build_v1_4R_final_smoke_and_archive.py
if ($LASTEXITCODE -ne 0) { throw "build_v1_4R_final_smoke_and_archive.py failed" }
