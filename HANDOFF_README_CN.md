# 新聊天交接说明 · Zant-LLM v1.5R

当前版本：`v1.5R-post-release-monitoring-audit-and-hotfix-readiness`

从上一阶段继承的状态：

- v1.4R 已完成 final release smoke and archive。
- v1.5 已完成 post-release monitoring and maintenance。
- v1.5 successor 推荐为 v1.5R。
- v1.5R 目标是审计 v1.5 的 post-release 机制，并建立 hotfix readiness 与 regression replay 闭环。

下一步：

1. 解压本包到桌面。
2. 进入目录运行 `scripts\RUN_V1_5R_ALL_LOCAL.ps1`。
3. 若通过，运行 `scripts\PUSH_V1_5R_BASED_ON_REMOTE_V1_5.ps1`。
4. push 成功后，进入 v1.6 observability / operator dashboard。
