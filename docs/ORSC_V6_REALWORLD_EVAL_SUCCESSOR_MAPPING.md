# ORSC v6 Mapping for v0.6

ORSC v6 requires each lane to read back actual state, evaluate residuals or gates, and only then resolve the successor lane.

v0.6 successor rule:

- If real-world adversarial pass rate is 1.0 and no forbidden runtime/provider field appears, successor may be v0.7.
- If READY/BLOCKED/CLOSEOUT/FAILCLOSED confusion appears, successor must be v0.6R calibration.
- If runtime authority or provider dispatch leaks, successor must be fail-closed remediation.
