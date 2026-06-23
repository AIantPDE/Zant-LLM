# Zant-LLM v1.3R Release Candidate Signoff and Smoke

Branch: `v1.3R-release-candidate-signoff-and-smoke`

This branch signs off the v1.3 release-candidate package with deterministic smoke checks, artifact inventory checks, governance checks, and final release-readiness signals. It does not train a model and does not enable runtime authority or provider dispatch.

## Status

- Base branch: `v1.3-release-candidate-packaging`
- Signoff checks: 24
- Smoke cases: 12
- Signoff score: 1.0
- Smoke pass rate: 1.0
- Blocking issues: 0
- Accepted: true
- Successor: `v1.4-final-release-manifest-and-tagging`

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_3R_ALL_LOCAL.ps1
```
