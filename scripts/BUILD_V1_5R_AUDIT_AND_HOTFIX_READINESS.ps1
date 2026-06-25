$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
python "$PSScriptRoot\build_v1_5R_audit_and_hotfix_readiness.py" --root "$Root"
