# ORSC v6 Calibration Successor Mapping

v0.6R follows a readback -> residual bucket -> bounded successor rule:

1. Read v0.6 eval distribution.
2. Detect residuals: over-failclosed, under-blocked, closeout misuse, source conflict instability, authority leakage.
3. Produce gate-aware receipt.
4. Recommend one successor only.

Possible successors:

- READY_TO_V0_7_CALIBRATION_SFT
- BLOCKED_BY_EVAL_RESIDUALS
- CLOSEOUT_CURRENT_LANE
- FAILCLOSED_DUE_TO_GOVERNANCE_LEAKAGE
