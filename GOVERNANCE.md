# Governance

ZANT-LLM v1.6R keeps all authority and provider-dispatch boundaries closed.

```text
runtime_authority_granted = false
provider_dispatch_enabled = false
external_delivery_enabled = false
training_mutation_authorized = false
```

Gate-aware observability is a read-side governance hardening layer. A READY gate can authorize only the next bounded engineering delta named by the resolver. It cannot grant runtime authority, provider dispatch, worker trigger, writeback execution, policy update, or order placement.
