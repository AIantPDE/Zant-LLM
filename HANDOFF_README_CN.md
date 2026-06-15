# Zant-LLM v0.2 分支交接说明

本包对应分支：

```text
v0.2-trace-hix-contracts-and-validators
```

作用：

把 TRACE-HIX Training Formalization v0.2 落成 Zant-LLM 可运行工程资产，包括 schema、registry、validator、gold seed、negative seed、validation report 和 release manifest。

## 一键运行

```powershell
cd C:/Users/Hilo/Desktop/zant_llm_v0_2_trace_hix_contracts_and_validators_branch
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_2_ALL_LOCAL.ps1
```

## 推荐推送方式

如果 GitHub 已经有 v0.1 分支，建议执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_2_BASED_ON_REMOTE_V0_1.ps1
```

它会：

1. clone 远程 v0.1 分支；
2. 新建 v0.2 分支；
3. 覆盖 v0.2 文件；
4. 删除已知 v0.1 残留冲突文件；
5. 本地验证；
6. commit；
7. push 到 GitHub。

## 当前仍然禁止

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
ROUTE_DECISION_CREATED=False
FETCH_DECISION_CREATED=False
WORKER_TRIGGER_ENABLED=False
WRITEBACK_EXECUTION_ENABLED=False
```
