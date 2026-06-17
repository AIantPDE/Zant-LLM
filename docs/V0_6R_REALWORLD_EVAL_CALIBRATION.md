# V0.6R Real-world Eval Calibration

v0.6R analyzes v0.6 real-world adversarial evaluation outputs rather than training a new model.

Expected v0.6 distribution:

```text
READY=45
BLOCKED=138
CLOSEOUT=9
FAILCLOSED=108
TOTAL=300
```

If pass rate is high and no runtime/provider leakage is found, successor should be v0.7 with calibration-informed SFT candidates.
