# Zant-LLM v0.11 Runtime Regression Dashboard

Branch: `v0.11-runtime-regression-dashboard`

v0.11 converts the v0.10R runtime stress and log audit results into a small regression dashboard that can be checked repeatedly before runtime deployment.

## Source snapshots

| Branch | Total | Pass rate | READY | BLOCKED | CLOSEOUT | FAILCLOSED | Flags false |
|---|---:|---:|---:|---:|---:|---:|---|
| `v0.9-inference-contract-stabilization` | 160 | 1.000 | 32 | 64 | 16 | 48 | True |
| `v0.10-runtime-api-batch-harness` | 200 | 1.000 | 40 | 80 | 20 | 60 | True |
| `v0.10R-runtime-harness-stress-and-log-audit` | 380 | 1.000 | 60 | 175 | 40 | 105 | True |

## Latest v0.10R state

- STRESS_TOTAL: 380
- STRESS_PASS_RATE: 1.0
- REQUEST_ID_UNIQUE: True
- LOG_ROWS: 380
- ALL_FLAGS_FALSE: True
- runtime_authority_granted: False
- provider_dispatch_enabled: False

## Dashboard decision

Regression detected: **False**

Risk level: **LOW**

Successor recommendation: `v0.12-runtime-deployment-readiness`
