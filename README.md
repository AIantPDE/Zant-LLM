# Zant-LLM v0.2 TRACE-HIX Contracts and Validators

Branch: `v0.2-trace-hix-contracts-and-validators`

This branch turns the TRACE-HIX Training Formalization v0.2 design into executable repository assets for Zant-LLM:

- TRACE-HIX bundle, explanation preview, and claim atom schemas.
- Forbidden output, predicate, and rejection taxonomy registries.
- Reference closure, claim support, authority leakage, forbidden output, trace immutability, and counterfactual-only validators.
- 30 gold seed cases and 30 negative attack cases.
- PowerShell local verification and validator report generation.

## Local run

```powershell
cd C:/Users/Hilo/Desktop/zant_llm_v0_2_trace_hix_contracts_and_validators_branch
powershell -ExecutionPolicy Bypass -File .\scripts\RUN_V0_2_ALL_LOCAL.ps1
```

Expected success markers:

```text
TRACE_HIX_V0_2_LOCAL_VERIFY_OK=True
TRACE_HIX_V0_2_VALIDATORS_RAN=True
ALL_EXPECTATIONS_MET=True
TRACE_HIX_V0_2_RELEASE_MANIFEST_CREATED=True
TRACE_HIX_V0_2_ALL_LOCAL_OK=True
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```

## Push directly as v0.2 branch

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_2_BRANCH_TO_GITHUB.ps1
```

Default repository:

```text
https://github.com/AIantPDE/Zant-LLM.git
```

Default branch:

```text
v0.2-trace-hix-contracts-and-validators
```

## Push while preserving v0.1 history

Recommended if `v0.1-explanation-preview-baseline` already exists remotely:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_2_BASED_ON_REMOTE_V0_1.ps1
```

This script clones the remote v0.1 branch, creates v0.2, overlays this package, removes known v0.1 stale files, verifies locally, commits, and pushes.

## Boundary

Zant-LLM v0.2 remains an external training/contracts branch only.

```text
runtime_authority_granted=False
provider_dispatch_enabled=False
route_decision_created=False
fetch_decision_created=False
worker_trigger_enabled=False
writeback_execution_enabled=False
```
