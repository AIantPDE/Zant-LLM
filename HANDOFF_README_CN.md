# Zant-LLM v1.6R 交接说明

## 当前阶段

- 前置版本：v1.6-runtime-observability-and-operator-dashboard
- 当前版本：v1.6R-orsc-v6-gate-aware-observability-and-receipt-hardening
- 后继候选：v1.7-trace-hix-v0.2.1-training-gate-foundation

## 本版目标

把 ORSC v6 的 gate-aware 机制加入 ZANT-LLM 的工程治理层，确保后续 TRACE-HIX v0.2.1 训练准入前，工程侧已经具备：

1. gate result taxonomy；
2. action readiness vector；
3. successor input hydration；
4. actual successor resolution；
5. gate-aware receipt；
6. dashboard gate panel；
7. fail-closed negative smoke。

## 不做的事

- 不训练模型；
- 不接入爬虫；
- 不开启 provider dispatch；
- 不授予 runtime authority；
- 不新增外部副作用执行；
- 不直接进入 v1.7，必须由 v1.6R 的 resolver 采纳 actual successor。

## 运行命令

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V1_6R_ALL_LOCAL.ps1
```

## 关键判据

- READY / BLOCKED / CLOSEOUT / FAIL_CLOSED 全部有样例覆盖；
- BLOCKED 必须列出 blocking reasons；
- CLOSEOUT 后不得继续微拆同一路线；
- successor 输入不得使用 null / missing / unknown；
- actual successor 必须由 resolver 生成；
- receipt 必须可 canonicalize 并 SHA256 seal。
