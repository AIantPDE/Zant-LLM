param([string]$InputPath = ".\data\trace_hix_v0_10\sample_batch_input.jsonl", [string]$OutputPath = ".\outputs\v0_10\batch_infer_output.jsonl")
python .\scripts\batch_infer_v0_10.py --input $InputPath --output $OutputPath
if ($LASTEXITCODE -ne 0) { throw "batch_infer_v0_10.py failed" }
