# Zant-LLM v1.5-post-release-monitoring-and-maintenance

This branch starts the post-release maintenance lane after the v1.4.0 final release line.

## Purpose

`v1.5-post-release-monitoring-and-maintenance` does not train models. It adds post-release monitoring, release-health checks, issue/regression intake templates, and hotfix readiness policy for the runtime governance release.

## Built-in status

- Base branch: `v1.4R-final-release-smoke-and-archive`
- Release tag under watch: `v1.4.0`
- Monitoring checks: 20
- Post-release smoke cases: 20
- Release health score: 1.0
- Blocking issues: 0
- Post-release monitoring accepted: true
- Runtime authority granted: false
- Provider dispatch enabled: false
- Successor: `v1.5R-post-release-monitoring-audit-and-hotfix-readiness`

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_5_ALL_LOCAL.ps1
```
