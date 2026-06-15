# Governance Boundary

Zant-LLM v0.2 implements TRACE-HIX contracts and validators only. It does not connect to aiant-zant runtime and does not grant execution authority.

Allowed:

- Build and validate explanation bundles.
- Validate human explanation previews.
- Generate schema/reference/claim/authority reports.
- Produce gold and negative training assets for later v0.3 model training.

Forbidden:

- provider dispatch
- provider registry update
- route decision
- fetch decision
- worker trigger
- writeback execution
- runtime authority
- new decision creation

Important distinction:

- Input bundle governance metadata may declare authority boundaries, including fields such as `forbidden_output_fields`.
- Explanation output payloads must not carry forbidden control-plane or execution-plane fields at any value.
