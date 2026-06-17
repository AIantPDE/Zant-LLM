# Zant-LLM v0.6 Governance

This branch evaluates real-world adversarial inputs under TRACE-HIX / ORSC governance.

Hard boundaries:
- runtime_authority_granted = false
- provider_dispatch_enabled = false
- no route decision, fetch decision, model call, worker trigger, writeback execution, order placement, or runtime authority may be emitted by the explanation plane
- unsupported claims must be BLOCKED or FAILCLOSED, not narrated as facts
- source conflict must be surfaced as an evidence residual
