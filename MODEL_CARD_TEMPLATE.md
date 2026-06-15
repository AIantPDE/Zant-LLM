# Zant-LLM v0.3 Model Card Template

## Model

- Base model: `D:\gemma-4-E2B-it`
- Adapter type: QLoRA / LoRA
- Training branch: `v0.3-gemma4-qlora-explanation-baseline`

## Intended Use

Generate TRACE-HIX compliant explanation previews from DRL decision preview, actual decision trace, and bounded evidence projections.

## Not Intended For

- Creating new DRL decisions.
- Routing, fetching, provider dispatch, writeback, worker trigger, execution authority.
- Direct runtime use inside aiant-zant without separate provider readiness and guarded integration.

## Required Validators

- Schema validation.
- Reference closure validation.
- Claim support validation.
- Forbidden output scan.
- Authority leakage scan.
- New decision leakage scan.
