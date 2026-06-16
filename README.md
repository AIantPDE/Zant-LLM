# Zant-LLM v0.4 Evidence-Gated Explanation Admissibility

Branch: `v0.4-evidence-gated-explanation-admissibility`.

This branch upgrades v0.3 Gemma4 LoRA baseline into gate-aware explanation training. It includes gate-aware SFT data, READY / BLOCKED / CLOSEOUT / FAILCLOSED targets, TRACE-HIX admissibility gates, contract evaluation, and Windows PowerShell training scripts.

## Boundary

- `RUNTIME_AUTHORITY_GRANTED=False`
- `PROVIDER_DISPATCH_ENABLED=False`
- no route decision
- no fetch decision
- no worker trigger
- no writeback execution

## Local run

```powershell
cd C:\Users\Administrator\Desktop\Zant-LLM-v0.4-work
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_4_ALL_LOCAL.ps1
```

## Real Gemma4 LoRA fallback training

```powershell
$env:PYTHONPATH = "$PWD\src"
$env:CUDA_VISIBLE_DEVICES = "0"
$env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:128"

python -X faulthandler .\scripts\train_v0_4_gemma4_lora.py `
  --base-model "D:\gemma-4-E2B-it" `
  --max-seq-len 64 `
  --epochs 1 `
  --batch-size 1 `
  --grad-accum 64 `
  --learning-rate 1e-4 `
  --no-4bit
```
