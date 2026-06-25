# Security

v1.6 does not grant runtime authority and does not enable provider dispatch.

Security posture:

- Fail closed on missing required reports.
- Treat blocking issues as release blockers.
- Keep dashboard read-only.
- Keep hotfix readiness separate from production execution.
- Do not add crawler/scraper/spider code in this release.
