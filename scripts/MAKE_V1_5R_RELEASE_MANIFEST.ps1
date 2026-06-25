$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
python "$PSScriptRoot\make_v1_5R_release_manifest.py" --root "$Root"
