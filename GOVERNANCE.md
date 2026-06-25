# Governance

Zant-LLM v1.6 keeps governance fail-closed.

Required invariant values:

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```

The dashboard is observational only. It summarizes local reports and synthetic governance checks.
It does not call external providers, does not dispatch runtime authority, and does not fetch external content.
