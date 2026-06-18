# Zant-LLM v0.11 Runtime Regression Dashboard

Branch: `v0.11-runtime-regression-dashboard`

This branch builds a regression dashboard from the latest runtime harness results. It is not a training branch. It summarizes v0.9, v0.10, and v0.10R runtime contract outcomes and records whether the system is ready to move toward deployment readiness checks.

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_11_ALL_LOCAL.ps1
```

Expected markers:

```text
ZANT_LLM_V0_11_REPOSITORY_VALID=True
ZANT_LLM_V0_11_STDLIB_TESTS_PASSED=True
ZANT_LLM_V0_11_DASHBOARD_CREATED=True
ZANT_LLM_V0_11_RELEASE_MANIFEST_CREATED=True
ZANT_LLM_V0_11_ALL_LOCAL_OK=True
```

## Successor

`v0.12-runtime-deployment-readiness`
