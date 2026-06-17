from __future__ import annotations
from typing import Any
from .common import GateDecision, contains_forbidden_key, evaluate_readiness_vector, authority_metadata_ok
class LaneSuccessorAdmissibilityGate:
    name='LaneSuccessorAdmissibilityGate'; action_type='lane_successor'
    def evaluate(self, payload: dict[str, Any]) -> GateDecision:
        rv=dict(payload.get('readiness_vector', {}))
        rv.setdefault('authority_boundary_declared', payload.get('runtime_authority_granted') is False)
        rv.setdefault('provider_dispatch_disabled', payload.get('provider_dispatch_enabled') is False)
        if not authority_metadata_ok(payload):
            return GateDecision(self.name,self.action_type,'FAILCLOSED',rv,blocking_residuals=['authority_boundary'],reason='authority or dispatch not disabled')
        artifact=payload.get('artifact') or payload.get('output') or payload.get('explanation_output') or {}
        forbidden=contains_forbidden_key(artifact)
        if forbidden:
            return GateDecision(self.name,self.action_type,'FAILCLOSED',rv,blocking_residuals=forbidden,reason='forbidden output field detected')
        if payload.get('route_closeout') is True:
            return GateDecision(self.name,self.action_type,'CLOSEOUT',rv,reason='safe route closeout')
        decision,missing=evaluate_readiness_vector(rv)
        return GateDecision(self.name,self.action_type,decision,rv,missing_evidence=missing,blocking_residuals=missing,reason='ready' if decision=='READY' else 'missing evidence')
