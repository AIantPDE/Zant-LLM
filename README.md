# Zant-LLM v1.5R · Post-release Monitoring Audit and Hotfix Readiness

本分支是 `v1.5-post-release-monitoring-and-maintenance` 的审计强化修正版，目标不是开启运行时能力，而是把 v1.5 的 post-release monitoring 流程补强为可审计、可复跑、可 hotfix 分流的维护闭环。

## 版本定位

- 分支名：`v1.5R-post-release-monitoring-audit-and-hotfix-readiness`
- 上游基线：`origin/v1.5-post-release-monitoring-and-maintenance`
- 推荐后继：`v1.6-runtime-observability-and-operator-dashboard`
- 版本性质：post-release audit / hotfix readiness / regression replay
- 运行时授权：关闭
- provider dispatch：关闭

## 安全不变量

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```

本分支不得提供真实执行权限、不得接通外部 provider、不得把治理输出解释为可执行授权。

## 本地一键运行

```powershell
cd C:\Users\Administrator\Desktop\zant_llm_v1_5R_post_release_monitoring_audit_and_hotfix_readiness_branch
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_5R_ALL_LOCAL.ps1
```

预期关键输出：

```text
ZANT_LLM_V1_5R_REPOSITORY_VALID=True
ZANT_LLM_V1_5R_STDLIB_TESTS_PASSED=True
ZANT_LLM_V1_5R_LOCAL_VERIFY_OK=True
ZANT_LLM_V1_5R_AUDIT_AND_HOTFIX_BUILT=True
ZANT_LLM_V1_5R_RELEASE_MANIFEST_CREATED=True
ZANT_LLM_V1_5R_ALL_LOCAL_OK=True
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```

## 推送分支

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V1_5R_BASED_ON_REMOTE_V1_5.ps1
```

该脚本会从远端 `v1.5-post-release-monitoring-and-maintenance` 创建 v1.5R 工作副本，复制当前交付内容，重新跑本地验证并 push 新分支。
