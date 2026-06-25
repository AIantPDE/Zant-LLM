# Zant-LLM v1.6 中文交接说明

当前版本：`v1.6-runtime-observability-and-operator-dashboard`

## 阶段定位

v1.6 是 **运行时可观测性与操作员仪表盘阶段**。

它承接：

```text
v1.4R  final release smoke + archive
v1.5   post-release monitoring + maintenance
v1.5R  post-release audit + hotfix readiness
v1.6   runtime observability + operator dashboard
```

## 明确不包含

```text
crawler / scraper / spider / external ingestion / provider dispatch
```

也就是说，v1.6 不做爬虫、不接外部采集源、不开放运行时权限。

## 核心目标

1. 把 v1.5R 的 audit / hotfix readiness / regression replay 结果汇总为 dashboard。
2. 给操作员一个每日检查视图。
3. 给维护者一个 health score / regression trend / blocking issue 概览。
4. 保持 fail-closed 与治理边界不变。
5. 生成 v1.6R successor recommendation。

## 本地验证

```powershell
cd C:\Users\Administrator\Desktop\Zant-LLM-v1.6-runtime-observability-and-operator-dashboard
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_6_ALL_LOCAL.ps1
```

## 推送

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V1_6_BASED_ON_REMOTE_V1_5R.ps1
```
