# Zant-LLM v0.9 Inference Contract Stabilization

Branch: `v0.9-inference-contract-stabilization`

v0.9 converts the v0.8R output calibration logic into a stable inference contract:

- fixed decision JSON schema
- new-token text handling for model outputs
- JSON parser with fallback classifier
- fail-closed repair for unsafe or malformed outputs
- local CLI and stdlib HTTP API entry points
- deterministic contract eval over 160 cases plus 40 smoke cases

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_9_ALL_LOCAL.ps1
```

Push:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_9_BASED_ON_REMOTE_V0_8R.ps1
```
