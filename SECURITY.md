# Security Policy

v1.5R 是维护审计分支，不提供真实运行时能力。

## Reporting

任何发现都应先进入：

- `data/trace_hix_v1_5R/issue_audit_template.json`
- `data/trace_hix_v1_5R/hotfix_intake_template.json`

## Release blocking criteria

若出现以下情况，必须阻断：

- `runtime_authority_granted=True`
- `provider_dispatch_enabled=True`
- blocking issue > 0
- smoke pass rate < 1.0
- release health score < 1.0
- fail-closed invariant 不成立
