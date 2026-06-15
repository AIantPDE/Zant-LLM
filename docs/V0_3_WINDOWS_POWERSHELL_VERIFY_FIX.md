# v0.3 Windows PowerShell verify fix

This patch removes the hard dependency on pytest during local verification.

Reason: Windows PowerShell 5 may surface native stderr from `python -c "import pytest"` or `python -m pytest` as a terminating NativeCommandError when `$ErrorActionPreference = "Stop"` is enabled. The v0.3 package already includes `scripts/run_v0_3_stdlib_tests.py`, so the local verification path now always uses the stdlib test runner.

The CI workflow also uses the stdlib runner.

Boundary flags remain locked:

- RUNTIME_AUTHORITY_GRANTED=False
- PROVIDER_DISPATCH_ENABLED=False
