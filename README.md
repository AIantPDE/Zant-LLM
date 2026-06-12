# Zant-LLM v0.1 Initial Branch

Zant-LLM is the independent model-training repository for ZANT explanation-generation capabilities inside the AIant PDE family.

This `v0.1` branch is the **initial baseline branch file set**. It is intentionally small, governed, and safe to modify in later work.

## Scope

This repository is allowed to contain:

- explanation-preview training code;
- synthetic seed data and data manifests;
- baseline validation and demo scripts;
- model-card, evaluation, and release-manifest templates;
- governance documents and CI checks.

This repository is **not** allowed to modify or enable:

- `aiant-zant` runtime;
- provider registry;
- provider dispatch;
- route decision;
- fetch decision;
- worker activation;
- runtime authority.

## v0.1 baseline objective

Input:

- `semantic_preview`
- `evidence_references`
- `reason_codes`
- `residual_hints`
- `uncertainty_hints`

Output:

- `explanation_summary`
- `explanation_residual_hint`
- `evidence_grounded_rationale`
- `uncertainty_aware_wording`
- `fail_closed_fallback`

Forbidden output fields:

- `route_decision`
- `fetch_decision`
- `agent_action`
- `provider_dispatch`
- `runtime_authority`
- `worker_trigger`
- `writeback_execution`

## Local validation

```powershell
python .\scripts\validate_v0_1_pack.py
python .\scripts\run_v0_1_baseline_demo.py
```

Or run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\VERIFY_ZANT_LLM_V0_1_LOCAL.ps1
```

## Push this branch to GitHub

From this folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\PUSH_V0_1_BRANCH_TO_GITHUB.ps1
```

Default target:

```text
https://github.com/AIantPDE/Zant-LLM.git
```

Default branch:

```text
v0.1
```

## Branch policy

`v0.1` is the initial baseline branch. Later work should branch from it or open PRs into it depending on the workflow chosen by the team.
