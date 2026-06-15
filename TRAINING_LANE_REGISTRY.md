# Training Lane Registry

| Branch | Purpose | Status |
|---|---|---|
| v0.1-explanation-preview-baseline | PowerShell baseline and seed skeleton | previous |
| v0.2-trace-hix-contracts-and-validators | TRACE-HIX contracts, schema, validators | previous |
| v0.3-gemma4-qlora-explanation-baseline | Gemma 4 E2B QLoRA explanation baseline | current |

## v0.3 Scope

- Build SFT dataset from TRACE-HIX bundles and human explanation previews.
- Train a first Gemma 4 E2B LoRA/QLoRA adapter.
- Run contract validation before and after generation.
- Generate model card draft, eval report, release manifest.

## Out of Scope

- Runtime provider connection.
- aiant-zant model call enablement.
- Provider dispatch.
- Route/fetch decision generation.
- Execution/writeback/worker actions.
