from typing import Mapping, Any, Dict
PROPOSED_SUCCESSOR = "v1.7-trace-hix-v0.2.1-training-gate-foundation"
FALLBACK_SUCCESSOR = "v1.6R-evidence-readback-or-route-closeout"

def resolve_v1_6r_successor(inputs: Mapping[str, bool]) -> Dict[str, Any]:
    if not inputs:
        return {"adopted": False, "actual_successor": FALLBACK_SUCCESSOR, "reason": "missing_inputs"}
    if any(v not in (True, False) for v in inputs.values()):
        return {"adopted": False, "actual_successor": FALLBACK_SUCCESSOR, "reason": "non_boolean_input"}
    adopted = all(inputs.values())
    return {"adopted": adopted, "proposed_successor": PROPOSED_SUCCESSOR, "actual_successor": PROPOSED_SUCCESSOR if adopted else FALLBACK_SUCCESSOR, "reason": "all_inputs_true" if adopted else "one_or_more_inputs_false"}
