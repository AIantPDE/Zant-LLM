# Zant-LLM v1.5R · Post-release Monitoring Audit and Hotfix Readiness

## 目标

v1.5R 是 v1.5 的 R 修正版，重点是把 post-release monitoring 从“能跑通”提升到“能审计、能复跑、能分流 hotfix”。

## 新增能力

1. Post-release audit checks  
   用 24 条审计项检查 v1.5 的 release-health、smoke、manifest、registry、schema、report 是否完整。

2. Hotfix readiness checks  
   用 24 条 hotfix readiness 项检查是否可以把问题分成 hotfix candidate、regression replay required、maintenance backlog。

3. Regression replay  
   用 24 条 replay case 确认 v1.5 的成功条件没有在 v1.5R 被破坏。

4. Fail-closed invariant  
   任何 runtime authority 或 provider dispatch 相关请求必须被阻断。

## 成功标准

```text
RELEASE_HEALTH_SCORE=1.0
SMOKE_PASS_RATE=1.0
AUDIT_PASS_RATE=1.0
HOTFIX_READINESS_SCORE=1.0
REGRESSION_REPLAY_PASS_RATE=1.0
BLOCKING_ISSUES=0
POST_RELEASE_AUDIT_ACCEPTED=True
HOTFIX_READINESS_ACCEPTED=True
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```
