# Zant-LLM v0.10R Runtime Harness Stress and Log Audit

Branch: `v0.10R-runtime-harness-stress-and-log-audit`

This branch stress-tests the v0.10 runtime API / batch harness and audits runtime logs.

Goals:
- Stress infer and batch-infer behavior with mixed READY / BLOCKED / CLOSEOUT / FAILCLOSED cases.
- Check malformed, empty, long, and authority-injection inputs.
- Verify runtime logs contain unique request_id values, timestamps, decisions, and safe runtime flags.
- Produce stress and log-audit reports.
- Keep `runtime_authority_granted=false` and `provider_dispatch_enabled=false`.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_10R_ALL_LOCAL.ps1
```
