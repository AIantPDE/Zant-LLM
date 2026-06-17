# Zant-LLM v0.6R Real-world Eval Calibration

This branch is a calibration/reporting branch based on `v0.6-realworld-adversarial-eval`.
It does not train a model. It analyzes the v0.6 real-world adversarial evaluation results and produces:

- calibration bucket summary
- successor recommendation
- v0.7 training candidate extraction
- release manifest

Expected branch name:

```text
v0.6R-realworld-eval-calibration
```

Run locally:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_6R_CALIBRATION.ps1
```

Push based on remote v0.6:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_6R_BASED_ON_REMOTE_V0_6.ps1
```

Governance invariants:

```text
runtime_authority_granted=False
provider_dispatch_enabled=False
```
