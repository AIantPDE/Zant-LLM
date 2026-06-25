# README for New Chat · Zant-LLM v1.5R

把本文件和压缩包一起上传到新聊天即可继续。

需要告诉新聊天：

- 仓库：`https://github.com/AIantPDE/Zant-LLM`
- 当前目标分支：`v1.5R-post-release-monitoring-audit-and-hotfix-readiness`
- 基线分支：`v1.5-post-release-monitoring-and-maintenance`
- 本地验证入口：`scripts/RUN_V1_5R_ALL_LOCAL.ps1`
- push 入口：`scripts/PUSH_V1_5R_BASED_ON_REMOTE_V1_5.ps1`
- 安全硬开关必须保持：
  - `RUNTIME_AUTHORITY_GRANTED=False`
  - `PROVIDER_DISPATCH_ENABLED=False`

完成 v1.5R 后，进入：

`v1.6-runtime-observability-and-operator-dashboard`
