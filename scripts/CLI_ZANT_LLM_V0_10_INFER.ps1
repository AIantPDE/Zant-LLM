param([string]$Text)
python .\scripts\cli_infer_v0_10.py --text $Text
if ($LASTEXITCODE -ne 0) { throw "cli_infer_v0_10.py failed" }
