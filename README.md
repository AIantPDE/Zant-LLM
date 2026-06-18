# Zant-LLM v0.8 — Heldout Model Eval

This branch evaluates the v0.7 calibration-informed SFT lane on heldout adversarial and real-world style examples.

v0.8 is primarily an evaluation lane, not a new training lane. It contains a contract-level heldout eval and an optional adapter-backed model probe that can load the v0.7 LoRA adapter when available locally.

## Run locally

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_8_ALL_LOCAL.ps1
```

## Push

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_8_BASED_ON_REMOTE_V0_7.ps1
```

## Optional model-backed probe

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\EVAL_ZANT_LLM_V0_8_HELDOUT_MODEL.ps1 `
  -BaseModelPath "E:\gemma-4-E2B-it" `
  -AdapterPath "C:\Users\Administrator\Desktop\Zant-LLM-v0.7-push-work\outputs\v0_7\gemma4_lora_adapter"
```

Governance flags must remain false:

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```
