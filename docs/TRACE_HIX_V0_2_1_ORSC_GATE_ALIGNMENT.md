# TRACE-HIX v0.2.1 ORSC Gate Alignment

TRACE-HIX v0.2.1 is a limited patch over v0.2. It does not add a larger rationale model.
It aligns TRACE-HIX with ORSC v6 evidence-gated action admissibility.

## Main change

The following outputs are treated as actions that require an admissibility gate:

```text
explanation output
training sample acceptance
follow-up answer
counterfactual explanation
lane successor transition
```

## Added gates

```text
ExplanationAdmissibilityGate
TrainingSampleAdmissibilityGate
FollowUpAdmissibilityGate
CounterfactualAdmissibilityGate
LaneSuccessorAdmissibilityGate
```

## Gate semantics

```text
READY      → next action may proceed
BLOCKED    → missing evidence/admissibility residuals must be listed
CLOSEOUT   → current route should be closed, not fragmented further
FAILCLOSED → illegal authority, reference, support, or successor condition
```

## Engineering boundary

The explanation model may produce structured explanation artifacts, claim atoms, uncertainty notes,
residual questions, and explanation-only counterfactuals. It must not produce runtime authority,
provider dispatch, new decisions, route decisions, fetch decisions, worker triggers, or writeback execution.

## v0.2.1 deliverables

```text
schemas/trace_hix_admissibility_gate_v0.schema.json
schemas/trace_hix_gate_aware_receipt_v0.schema.json
schemas/trace_hix_successor_resolution_v0.schema.json
registries/gate_result_taxonomy_v0.json
registries/admissibility_gate_registry_v0.json
src/zant_llm/gates/*.py
scripts/VERIFY_TRACE_HIX_V0_2_1_LOCAL.ps1
scripts/RUN_TRACE_HIX_V0_2_1_GATES.ps1
reports/v0_2_1/
release_manifests/trace_hix_v0_2_1_release_manifest.json
```
