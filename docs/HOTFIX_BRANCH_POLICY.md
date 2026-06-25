# Hotfix Branch Policy

Hotfix branches should use:

```text
hotfix/<short-description>
```

They must be based on:

```text
v1.5R-post-release-monitoring-audit-and-hotfix-readiness
```

Before merging or closing a hotfix branch, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_5R_ALL_LOCAL.ps1
```
