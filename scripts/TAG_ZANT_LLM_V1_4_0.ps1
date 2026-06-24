$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
git tag -a v1.4.0 -m "Zant-LLM v1.4.0 final runtime governance release"
git push origin v1.4.0
