# Zant-LLM v0.7 Calibration-Informed SFT

This branch turns the v0.6R real-world adversarial calibration into supervised fine-tuning data.

目标：把 v0.6 / v0.6R 的真实输入校准结果转成可训练的 gate-aware SFT 样本，使模型在真实噪声、缺证据、source conflict、prompt injection、runtime authority 诱导、provider dispatch 诱导等场景下稳定输出 READY / BLOCKED / CLOSEOUT / FAILCLOSED。

本分支仍保持：

- `runtime_authority_granted=false`
- `provider_dispatch_enabled=false`
- explanation plane 不升级为 decision plane / execution authority plane
- SFT 样本只能训练解释与拒绝格式，不能训练执行权限

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_7_ALL_LOCAL.ps1
```

## Push

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_7_BASED_ON_REMOTE_V0_6R.ps1
```

## Real training

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\TRAIN_ZANT_LLM_V0_7_GEMMA4_LORA.ps1 `
  -BaseModelPath "E:\gemma-4-E2B-it"
```
