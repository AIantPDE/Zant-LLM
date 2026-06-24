# Zant-LLM v1.4R-final-release-smoke-and-archive

v1.4R validates the final release smoke and archive package after v1.4 final release manifest and tagging preparation.

## Local run

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_4R_ALL_LOCAL.ps1
```

Expected markers:

```text
ZANT_LLM_V1_4R_ALL_LOCAL_OK=True
ARCHIVE_SCORE=1.0
SMOKE_PASS_RATE=1.0
FINAL_ARCHIVE_ACCEPTED=True
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```

Recommended tag: `v1.4.0`.
