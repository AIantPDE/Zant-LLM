# ORSC v6 Lane Governance for Zant-LLM

This document records how Zant-LLM branches should use Ordered Residual-Driven Spiral Convergence
(ORSC) v6 for lane-level governance.

## Position

ORSC v6 is not model training data. It is the lane governance protocol for deciding whether a branch
may proceed, must be blocked, must close out, or must fail closed.

The v6 addition is evidence-gated action admissibility:

```text
Observe actual state
→ construct heterogeneous residual vector
→ select one bounded delta or one gate
→ evaluate readiness vector
→ generate receipt
→ resolve actual successor
→ use receipt as next factual predecessor
```

## Gate outcomes

```text
READY      = all required evidence and admissibility conditions are satisfied
BLOCKED    = missing evidence or admissibility residuals must be enumerated
CLOSEOUT   = no safe route remains; stop this lane instead of micro-fragmenting
FAILCLOSED = illegal transition, authority leak, unsupported action, or receipt failure
```

## Zant-LLM branch use

For Zant-LLM:

- v0.1 is a baseline repository and PowerShell verification branch.
- v0.2 defines TRACE-HIX contracts and validators.
- v0.2.1 adds ORSC v6 gate alignment.
- v0.3 performs Gemma4 LoRA / QLoRA baseline training.
- v0.4 should use gate-aware evidence admissibility before accepting explanations, follow-ups, counterfactuals, or lane successors.

## Prohibited inference

```text
ExplanationReady does not imply RuntimeAuthorityGranted.
ExplanationReady does not imply ProviderDispatchEnabled.
ExplanationReady does not imply NewDecisionCreated.
```

Required flags remain:

```text
RUNTIME_AUTHORITY_GRANTED=False
PROVIDER_DISPATCH_ENABLED=False
```
