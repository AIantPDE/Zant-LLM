$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
python .\scripts\analyze_v0_8R_model_output_calibration.py
if ($LASTEXITCODE -ne 0) { throw "analysis failed" }
