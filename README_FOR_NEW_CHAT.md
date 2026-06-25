# New chat handoff for Zant-LLM v1.6

Use this folder as the source package for the branch:

```text
v1.6-runtime-observability-and-operator-dashboard
```

The package focuses on runtime observability and operator dashboards only.
It intentionally avoids crawler/external-ingestion work.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_6_ALL_LOCAL.ps1
```

Push:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V1_6_BASED_ON_REMOTE_V1_5R.ps1
```
