# Zant-LLM v0.1 PowerShell 可训练分支交接说明

目标仓库：`https://github.com/AIantPDE/Zant-LLM`

目标分支：`v0.1-explanation-preview-baseline`

## 一键本地训练

```powershell
cd C:\Users\Administrator\Desktop\zant_llm_v0_1_powershell_trainable_branch
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_1_ALL_LOCAL.ps1
```

## 单独训练

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_1_POWERSHELL.ps1
```

## 单独评估

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_1_POWERSHELL.ps1
```

## 推送分支

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1
```

这版是 v0.1 最初始可训练分支。训练方式是标准库实现的 token-overlap explanation baseline，用于建立训练/评估/manifest 流程，后续可以替换为 Gemma/QLoRA/Transformers 训练脚本。

当前仍然禁止接入 aiant-zant runtime。

## 2026-06-15 fixed2 note

本版本修复 fresh Windows/Python 环境中没有 pytest 时验证失败的问题。
`VERIFY_ZANT_LLM_V0_1_LOCAL.ps1` 会自动检测 pytest：

- 如果已安装 pytest，则运行 `python -m pytest -q`；
- 如果未安装 pytest，则运行标准库 fallback：`scripts/run_v0_1_stdlib_tests.py`。

因此不需要额外安装依赖，也可以直接执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_1_ALL_LOCAL.ps1
```
