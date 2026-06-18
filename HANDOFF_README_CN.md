# Zant-LLM v0.8 交接说明

v0.8 是 heldout model eval 分支，用于验证 v0.7 calibration-informed SFT 后的稳定性。

本分支默认先跑 contract-level heldout eval，不依赖真实模型。可选脚本可以加载 v0.7 LoRA adapter 做模型探针。

运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_8_ALL_LOCAL.ps1
```

推送：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_8_BASED_ON_REMOTE_V0_7.ps1
```
