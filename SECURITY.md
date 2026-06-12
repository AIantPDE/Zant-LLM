# Security Policy

## v0.1 runtime boundary

This repository is not a runtime authority source.

Do not add code that:

- changes `aiant-zant` runtime behavior;
- registers a provider;
- dispatches to a provider;
- creates route/fetch decisions;
- activates workers;
- writes back external state;
- grants runtime authority.

## Reporting issues

Open a private security issue in the repository or contact the AIantPDE maintainers.
