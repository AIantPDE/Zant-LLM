# Hotfix Readiness Checklist

A hotfix candidate is allowed only as a local governance branch proposal. It is not a production release authorization.

## Required evidence

- reproducible issue
- affected version
- affected fixture or report
- expected behavior
- actual behavior
- regression replay result
- fail-closed invariant result

## Required blocking rules

- runtime authority true blocks release
- provider dispatch true blocks release
- failed fail-closed test blocks release
- smoke pass rate below 1.0 blocks release
