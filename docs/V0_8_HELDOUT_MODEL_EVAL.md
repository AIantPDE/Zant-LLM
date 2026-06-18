# v0.8 Heldout Model Eval

v0.8 tests the v0.7 calibration-informed adapter on heldout decision contracts and provides an optional adapter-backed model probe.

The default local run does not require the model; it runs repository validation, heldout contract eval, model-probe dry-run, and release manifest generation.

Expected heldout distribution:

- READY: 27
- BLOCKED: 81
- CLOSEOUT: 12
- FAILCLOSED: 60
