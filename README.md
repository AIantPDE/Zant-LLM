# Zant-LLM v0.1 Explanation Preview Baseline

Branch: `v0.1-explanation-preview-baseline`

This is the initial PowerShell-trainable branch package for `AIantPDE/Zant-LLM`.

## Purpose

Zant-LLM v0.1 is a local, text-only, PowerShell-runnable baseline for explanation preview generation.
It is designed as the first editable training branch, not as a runtime integration package.

Allowed:
- Train a baseline explanation preview generator.
- Evaluate the baseline on local seed data.
- Produce model artifacts and release manifests.
- Push this branch to `https://github.com/AIantPDE/Zant-LLM`.

Forbidden in v0.1:
- No aiant-zant runtime integration.
- No provider dispatch.
- No provider registry changes.
- No route/fetch decisions.
- No worker activation.
- No runtime authority.

## Quick start in PowerShell

```powershell
cd C:\Users\Administrator\Desktop\zant_llm_v0_1_powershell_trainable_branch
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_1_ALL_LOCAL.ps1
```

## Push to GitHub branch

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1
```

Default repository: `https://github.com/AIantPDE/Zant-LLM.git`

Default branch: `v0.1-explanation-preview-baseline`

## Training outputs

```text
outputs/v0_1/model_artifact.json
outputs/v0_1/train_report.json
outputs/v0_1/eval_report.json
outputs/v0_1/predictions.jsonl
release_manifests/zant_llm_v0_1_release_manifest.json
```


## v0.1 PowerShell 修正版说明

本版本修复了 `validate_v0_1_repository.py` 因扫描自身禁用词而误报的问题，并修复了 `RUN_V0_1_ALL_LOCAL.ps1` 对子 PowerShell 失败没有立即中止的问题。

一键本地运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_1_ALL_LOCAL.ps1
```


## Fresh Windows/Python note

This v0.1 package does not require pytest. If pytest is missing, the local verify script automatically uses `scripts/run_v0_1_stdlib_tests.py`.
