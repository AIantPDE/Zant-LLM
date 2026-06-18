# Zant-LLM v0.10 Runtime API Batch Harness

Branch: `v0.10-runtime-api-batch-harness`

v0.10 promotes the v0.9 inference contract into a reusable runtime harness:

- CLI single inference
- JSONL batch inference
- stdlib HTTP API server
- `/health`, `/infer`, `/batch_infer`, `/logs`
- request logging
- batch eval report
- runtime receipt
- fail-closed repair with `runtime_authority_granted=false` and `provider_dispatch_enabled=false`

Local run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_10_ALL_LOCAL.ps1
```
