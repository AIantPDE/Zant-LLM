# Governance Boundary

Zant-LLM v0.4 is an external training branch only.

Required invariants:

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
MODEL_CALL_ENABLED_IN_AIANT_ZANT=False
ROUTE_DECISION_CREATED=False
FETCH_DECISION_CREATED=False
WORKER_TRIGGER_CREATED=False
WRITEBACK_EXECUTION_AUTHORIZED=False
```

Input governance metadata may state boundary flags as false. Model-generated explanation payloads must not carry control-plane fields.
