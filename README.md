# Zant-LLM v1.3 Release Candidate Packaging

Branch: `v1.3-release-candidate-packaging`

This branch packages the runtime-ready Zant-LLM lane into a release-candidate delivery shape. It does not train a model and does not enable runtime authority or provider dispatch.

## Status

- Base branch: `v1.2-runtime-deployment-readiness`
- RC checks: 20
- RC score: 1.0
- Blocking issues: 0
- Accepted: true
- Successor: `v1.3R-release-candidate-signoff-and-smoke`

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_3_ALL_LOCAL.ps1
```
